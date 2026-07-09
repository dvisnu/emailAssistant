from pynput import keyboard
from PyQt6.QtCore import QObject, pyqtSignal


class HotkeyService(QObject):
    hotkey_pressed = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.listener = keyboard.GlobalHotKeys({
            "<f8>": self._on_hotkey
        })

    def _on_hotkey(self):
        self.hotkey_pressed.emit()

    def start(self):
        self.listener.start()