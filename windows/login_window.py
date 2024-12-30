from PySide6 import QtWidgets
from PySide6.QtCore import Signal
from utils.app_requests import login, Token


class LoginWindow(QtWidgets.QWidget, Ui_login):
    login_successful = Signal(Token)
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.bt_login.clicked.connect(self.check_login)

    def check_login(self):
        username = self.le_username.text()
        password = self.le_password.text()
        token = login(username, password)
        if token:
            self.login_successful.emit(token)
        else:
            return None