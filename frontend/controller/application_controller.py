from ui.main_window import MainWindow
from services.selection_service import SelectionService
from services.hotkey_service import HotkeyService


class ApplicationController:
    def __init__(self, app):
        self.app = app

        self.selection_service = SelectionService()
        self.main_window = MainWindow()

        self.hotkey_service = HotkeyService()
        self.hotkey_service.hotkey_pressed.connect(self.on_hotkey_pressed)

    def start(self):
        self.main_window.hide()
        self.hotkey_service.start()

    def on_hotkey_pressed(self):
        text = self.selection_service.get_selected_text()

        self.main_window.set_input_text(text)

        self.main_window.show()
        self.main_window.raise_()
        self.main_window.activateWindow()