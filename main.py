from homepage.homepage_ui import Ui_mw_home
from login.login_ui import Ui_login
from PySide6 import QtWidgets
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QStandardItemModel, QStandardItem
from modules.app_requests import get_combo_boxes, login, Token



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
        
# The home window should only handle the mechanistic action of the UI not actually do any logic
class HomeWindow(QtWidgets.QMainWindow, Ui_mw_home):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.w_dock.setWindowTitle("podscale")
        self.w_dock.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        self.w_dock.setFixedWidth(50)
        self.setStatusBar(None)
        self.actionclose.triggered.connect(self.close)

        # sidebar select
        self.bt_home.clicked.connect(lambda: self.switch_view(0))
        self.bt_chat.clicked.connect(lambda: self.switch_view(1))
        self.bt_brandperformance.clicked.connect(lambda: self.switch_view(2))
        self.bt_codepodcastinput.clicked.connect(lambda: self.switch_view(3))
        self.bt_spendinput.clicked.connect(lambda: self.switch_view(4))

        # Connect submit buttons to the combo box refresh
        self.bt_submitnewcode.clicked.connect(self.add_new_code)
        self.bt_submitnewpodcast.clicked.connect(self.add_new_podcast)
        self.bt_suspendcode.clicked.connect(self.suspend_code)

        # Home page
        self.current_month_revenue.setText("revenue")
        self.current_spend_goal.setValue(100)

        # brand performance page
        headers = ["podcasts", "copy start date", "spend", "code revenue", "code orders", "roas", 
                   "attributed revenue", "attributed roas", "survey revenue", "survey revenue modeled", 
                   "survey write-ins", "survey modeled write-ins", "survey roas", "podscribe revenue", "podscribe roas"]
        
        table_model = QStandardItemModel()
        table_model.setHorizontalHeaderLabels(headers)
        self.tbl_brandperformance.setModel(table_model)
        # chat page
        self.bt_submitchat.clicked.connect(self.handle_chat_submit)

    def recieve_token(self, token):
        self.token = token

    def show_harmonic_window(self):
        self.show()

    def intialize_combo_boxes(self):
        self.completers = {}
        self.combo_boxes = {"/getcodes": [self.cb_existingcodes],
                            "/getpodcasts":[self.cb_podcast,
                                        self.cb_podcastspendgoal,
                                        self.cb_podcastactualspend,
                                        self.cb_podcastsuspendcode],
                            "/getbrands":[self.cb_brandfilter,
                                    self.cb_brandspendgoal,
                                    self.cb_brandactualspend] 
                            }
        for endpoint, cbx in self.combo_boxes.items():
            for cb in cbx:
                cb.setEditable(True)
                completer = QtWidgets.QCompleter(cb)
                completer.setCaseSensitivity(Qt.CaseSensitivity(False))
                cb.setCompleter(completer)
                self.completers[cb] = completer
                data = get_combo_boxes(self.token, endpoint)
                cb.addItems(data)
                completer.setModel(cb.model())
        
    def update_combo_boxes(self, endpoint):
        for cb in self.combo_boxes[endpoint]:
            self.update_combo_box(cb, self.completers[cb], endpoint)

    def update_combo_box(self, combo_box, completer, endpoint):
        current_choice = combo_box.currentText()
        data = get_combo_boxes(self.token, endpoint)
        combo_box.clear()
        combo_box.addItems(data)
        completer.setModel(combo_box.model())
        if current_choice in data:
            index = combo_box.findText(current_choice)
            combo_box.setCurrentIndex(index)

    def switch_view(self, index):
        self.stackedWidget.setCurrentIndex(index)

    def handle_chat_submit(self):
        in_text = self.te_chatinput.toPlainText()
        self.te_chathistory.setHtml(f"<p>{in_text}</p>")
        self.te_chatinput.clear()

    def add_new_code(self):
        new_code  = self.le_newcode.toPlainText()

        self.update_combo_boxes("code")

    def add_new_podcast(self):
        self.update_combo_boxes("podcasts")

    def suspend_code(self):
        self.update_combo_boxes("code")

if __name__ == "__main__":
    app = QtWidgets.QApplication()

    login_window = LoginWindow()

    harmonic_window = HomeWindow()

    login_window.login_successful.connect(harmonic_window.recieve_token)

    login_window.login_successful.connect(harmonic_window.intialize_combo_boxes)

    login_window.login_successful.connect(login_window.close)

    login_window.login_successful.connect(harmonic_window.show_harmonic_window)

    login_window.show()

    app.exec()