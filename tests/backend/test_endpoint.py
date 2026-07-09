"""Tests for the FastAPI /generate endpoint and the backend LLM client."""

import backend.app as app_module
import backend.services.llm as llm_module


class TestGenerateEndpoint:
    """Tests that exercise FastAPI's /generate route via TestClient."""

    def test_home(self, client):
        """The root route returns a simple JSON message."""
        resp = client.get("/")
        assert resp.status_code == 200
        assert resp.json() == {"message": "backend is running successfully!!"}

    def test_generate_returns_suggestion_list(self, client, monkeypatch):
        """The endpoint returns the action, text, and suggestion list from the generator."""
        monkeypatch.setattr(
            app_module,
            "generate_suggestion",
            lambda action, text: [f"{action}:{text}"],
        )

        resp = client.post("/generate", json={"action": "grammar", "text": "hello world"})

        assert resp.status_code == 200
        assert resp.json() == {
            "action": "grammar",
            "text": "hello world",
            "suggestion": ["grammar:hello world"],
        }

    def test_generate_empty_text(self, client):
        """Empty text is rejected with a 400 response."""
        resp = client.post("/generate", json={"action": "grammar", "text": ""})
        assert resp.status_code == 400

    def test_generate_missing_action(self, client):
        """Missing action field returns a validation error."""
        resp = client.post("/generate", json={"text": "hello"})
        assert resp.status_code == 422

    def test_generate_unknown_action(self, client, monkeypatch):
        """Unknown actions are rejected with a 400 response."""

        def fail_generator(action, text):
            raise ValueError("Action not available ;(")

        monkeypatch.setattr(app_module, "generate_suggestion", fail_generator)
        resp = client.post("/generate", json={"action": "sparkles", "text": "hello"})
        assert resp.status_code == 400

    def test_generate_missing_text(self, client):
        """Missing text field returns a validation error."""
        resp = client.post("/generate", json={"action": "grammar"})
        assert resp.status_code == 422


class TestLlmClient:
    """Tests for the local and OpenAI-compatible LLM client paths."""

    def test_generate_uses_openai_payload_when_key_present(self, monkeypatch):
        """The OpenAI-compatible path should send a chat-completions payload."""

        class DummyResponse:
            def __init__(self, payload):
                self._payload = payload

            def raise_for_status(self):
                return None

            def json(self):
                return self._payload

        calls = {}

        def fake_post(url, headers=None, json=None):
            calls["url"] = url
            calls["headers"] = headers
            calls["json"] = json
            return DummyResponse({"choices": [{"message": {"content": "generated"}}]})

        monkeypatch.setattr(llm_module.requests, "post", fake_post)
        monkeypatch.setattr(llm_module, "LLM_KEY", "secret")
        monkeypatch.setattr(llm_module, "LLM_URL", "https://example.test/v1/chat/completions")
        monkeypatch.setattr(llm_module, "LLM_MODEL", "demo-model")
        monkeypatch.setattr(llm_module, "OLLAMA_URL", "http://localhost:11434/api/generate")
        monkeypatch.setattr(llm_module, "OLLAMA_MODEL", "demo")

        result = llm_module.generate("prompt")

        assert result == "generated"
        assert calls["url"] == "https://example.test/v1/chat/completions"
        assert calls["headers"]["Authorization"] == "Bearer secret"
        assert calls["json"]["messages"][0]["content"] == "prompt"

    def test_generate_falls_back_to_ollama_without_key(self, monkeypatch):
        """When no key is configured, the client should use the Ollama payload."""

        class DummyResponse:
            def __init__(self, payload):
                self._payload = payload

            def json(self):
                return self._payload

        calls = {}

        def fake_post(url, json=None):
            calls["url"] = url
            calls["json"] = json
            return DummyResponse({"response": "ollama reply"})

        monkeypatch.setattr(llm_module.requests, "post", fake_post)
        monkeypatch.setattr(llm_module, "LLM_KEY", None)
        monkeypatch.setattr(llm_module, "LLM_URL", "https://example.test/v1/chat/completions")
        monkeypatch.setattr(llm_module, "LLM_MODEL", "demo-model")
        monkeypatch.setattr(llm_module, "OLLAMA_URL", "http://localhost:11434/api/generate")
        monkeypatch.setattr(llm_module, "OLLAMA_MODEL", "demo")

        assert llm_module.generate("prompt") == "ollama reply"
        assert calls["url"] == "http://localhost:11434/api/generate"
        assert calls["json"]["prompt"] == "prompt"
