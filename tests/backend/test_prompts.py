"""Smoke tests for the prompt registry."""

from backend.prompts.registry import PROMPTS


class TestPromptRegistry:
    """Each registered action produces a prompt."""

    def test_registry_contains_expected_actions(self):
        """The current project exposes the expected actions."""
        assert set(PROMPTS) == {"grammar", "rewrite", "professional"}

    def test_each_registered_builder_is_callable(self):
        """Every entry in the registry should be a callable prompt builder."""
        for name, builder in PROMPTS.items():
            assert callable(builder), f"PROMPTS[{name!r}] is not callable"

    def test_each_builder_returns_text(self):
        """Every builder should return a non-empty prompt string."""
        sample = "the quick brown fox jumps"
        for name, builder in PROMPTS.items():
            prompt = builder(sample)
            assert isinstance(prompt, str), f"PROMPTS[{name!r}] should return a string"
            assert prompt.strip(), f"PROMPTS[{name!r}] returned an empty prompt"

    def test_prompt_contains_the_input_text(self):
        """Prompt builders should preserve the user's text in the generated prompt."""
        sample = "the quick brown fox jumps"
        assert sample in PROMPTS["grammar"](sample)
        assert sample in PROMPTS["rewrite"](sample)
        assert sample in PROMPTS["professional"](sample)
