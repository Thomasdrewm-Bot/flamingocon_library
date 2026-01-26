from PyQt6.QtWidgets import QApplication

class LoginController:
    def __init__(self, user_repo, view, on_success):
        self.user_repo = user_repo
        self.view = view
        self.on_Success = on_success

        self.users = self.user_repo.get_login_users()
        view.set_user_list(self.users)

        # hook up events to ui
        self.view.on_login_clicked(self.attempt_login)
        self.view.on_cancel_clicked(self.exit_app)

        
    def attempt_login(self):
        user_id = self.view.get_user_id()
        password = self.view.get_password()

        if not user_id or not password:
            self.view.show_error("Select user and enter password")
            return
        
        # checks password, returns user if success
        user = self.user_repo.verify_pw(user_id = user_id, entered_password = password)

        if not user:
            self.view.show_error("Invalid credentials")
            self.view.clear_password()
            return
        
        self.on_success(user)


    def exit_app(self):
        QApplication.quit()