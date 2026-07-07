from pynput import keyboard


class HotkeyService:
    def __init__(self, callback):
        self.callback = callback

        self.listener = keyboard.GlobalHotKeys({
            "<ctrl>+<shift>+<space>": self.callback
        })

    def start(self):
        self.listener.start()