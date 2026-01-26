from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton



class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.button_is_checked = True

        self.setWindowTitle("Flamingocon Library")

        self.button = QPushButton("That thing called my app")
        self.button.clicked.connect(self.the_button_was_clicked)

        self.setCentralWidget(self.button)

    def the_button_was_clicked(self):
        self.button.setText("Been there, done that")
        self.button.setEnabled(False)

        self.setWindowTitle("Done did it")

app = QApplication([])

window = MainView()
window.show()

app.exec()