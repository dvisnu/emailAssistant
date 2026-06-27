from PyQt6.QtWidgets import QWidget , QVBoxLayout , QPushButton

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        def rewrite_clicked(self):
            print("rewrite clicked!!")
        def grammar_clicked(self):
            print("grammar clicked!!")
        def professional_clicked(self):
            print("professional clicked!!")
        

        self.setWindowTitle("AI Writing Assistant :)")
        self.resize(400,300)

        layout = QVBoxLayout()

        self.rewrite_button = QPushButton("Rewrite")
        self.grammar_button = QPushButton("Correct Grammar")
        self.professional_button = QPushButton("Make It Professional")

        layout.addWidget(self.rewrite_button)
        layout.addWidget(self.grammar_button)
        layout.addWidget(self.professional_button)

        self.rewrite_button.clicked.connect(rewrite_clicked)
        self.grammar_button.clicked.connect(grammar_clicked)
        self.professional_button.clicked.connect(professional_clicked)

        self.setLayout(layout)