from PyQt6.QtWidgets import QWidget, QMessageBox, QApplication
from ui.login_ui import Ui_Login

class LoginView(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Login()
        self.ui.setupUi(self)

        self.ui.setWindowTitle("Login")


    #---------------Event Triggers---------------
    def on_login_clicked(self, callback):
        self.ui.login_button.clicked.connect(callback)

    def on_cancel_clicked(self, callback):
        self.ui.cancel_button.clicked.connect(callback)

    def show_error(self, message: str):
        QMessageBox.warning(self, "Login Failed", message)

    # ---------------Clean up---------------
    def reset(self):
        self.ui.user_password_input.clear()

    # ---------------Initializing---------------
    def set_user_list(self, users):
        self.ui.user_choice.clear()
        self.ui.user_choice.addItem("Select User")

        for user in users:
            self.ui.user_choice.addItem(user.full_name, user.id)


    # ---------------Data Access---------------
    def get_password(self):
        return self.ui.user_password_input.text()
    
    def get_user_id(self):
        return self.ui.user_choice.currentData()