from pynput.keyboard import Controller,Key
from PyQt6.QtWidgets import QApplication
import time

class SelectionService:
    def __init__(self):
        self.keyboard = Controller()
    def get_selected_text(self):
        clipboard = QApplication.clipboard()

        original_text = clipboard.text()

        try:
            with self.keyboard.pressed(Key.ctrl):
                self.keyboard.press("c")
                self.keyboard.release("c")

            time.sleep(0.1)

            return clipboard.text()
        
        finally:
            clipboard.setText(original_text)

    def replace_selected_text(self,text):
        clipboard = QApplication.clipboard()

        original_text = clipboard.text()
        try:
            clipboard.setText(text)
            print(text)

            with self.keyboard.pressed(Key.ctrl):
                self.keyboard.press("v")
                self.keyboard.release("v")
            
            time.sleep(0.1)
        finally : 

            clipboard.setText(original_text)
