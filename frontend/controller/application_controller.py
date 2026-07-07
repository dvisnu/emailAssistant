from ui.main_window import MainWindow
from services.selection_service import SelectionService
from services.hotkey_service import HotkeyService


class ApplicationController:
    def __init__(self, app):
        self.app = app

        self.selection_service = SelectionService()
        self.main_window = MainWindow()

        self.hotkey_service = HotkeyService(
            callback=self.on_hotkey_pressed
        )

    def start(self):
        self.hotkey_service.start()
        self.main_window.show()

    def on_hotkey_pressed(self):
        print("Hotkey pressed!")