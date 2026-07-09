import sys

from PyQt6.QtWidgets import QApplication
from controller.application_controller import ApplicationController

app = QApplication(sys.argv)

controller = ApplicationController(app)

controller.start()

sys.exit(app.exec())