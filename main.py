import sys
from PyQt6.QtWidgets import QApplication

from repositories.UserRepository import UserRepos
from repositories.EventRepository import EventRepos
from repositories.GameRepository import GameRepos
from repositories.TransactionRepository import TransactionRepos
from view.LoginView import LoginView
from view.MainView import MainView
from infrastructure.db import Database
from controller.LoginController import LoginController
from controller.MainController import MainController


def main():
    app = QApplication(sys.argv)
    db = Database()
    user_repo = UserRepos(db)
    event_repo = EventRepos(db)
    game_repo = GameRepos(db)
    transaction_repo = TransactionRepos(db)
    login_view = LoginView()

    def on_login_success(user):
        login_view.close()


    LoginController(
        user_repo=user_repo,
        view=login_view,
        on_success=on_login_success
    )

    login_view.show()
    sys.exit(app.exec())



if __name__ == "__main__":
    main()