from homepage.homepage_ui import Ui_mw_home
from login.login_ui import Ui_login
from PySide6 import QtWidgets
from PySide6.QtCore import Qt, Signal, QDate
from PySide6.QtGui import QStandardItemModel, QStandardItem
from modules.app_requests import get, login, Token



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
        self.resize(800, 600)
        self.w_dock.setWindowTitle("podscale")
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
        self.bt_seeperformance.clicked.connect(self.display_performance)

        # Home page
        self.current_month_revenue.setText("revenue")
        self.current_spend_goal.setValue(100)

        # brand performance page
        
        self.table_model = QStandardItemModel()
        self.tbl_brandperformance.setModel(self.table_model)
        self.de_startdate.setDate(QDate(2024,9,1))
        self.de_enddate.setDate(QDate(2024,10,1))

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
                                        self.cb_podcastsuspendcode, self.cb_podcastspend],
                            "/getbrands":[self.cb_brandfilter, self.cb_brandspend] 
                            }
        for endpoint, cbx in self.combo_boxes.items():
            data = get(self.token, endpoint)
            for cb in cbx:
                cb.setEditable(True)
                completer = QtWidgets.QCompleter(cb)
                completer.setCaseSensitivity(Qt.CaseSensitivity(False))
                cb.setCompleter(completer)
                self.completers[cb] = completer
                cb.addItems(data)
                completer.setModel(cb.model())
        
    def update_combo_boxes(self, endpoint):
        for cb in self.combo_boxes[endpoint]:
            self.update_combo_box(cb, self.completers[cb], endpoint)

    def update_combo_box(self, combo_box, completer, endpoint):
        current_choice = combo_box.currentText()
        data = get(self.token, endpoint)
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

    def display_performance(self):
        # headers = ["podcasts", "copy start date", "spend", "code revenue", "code orders", "roas", 
        #            "attributed revenue", "attributed roas", "survey revenue", "survey revenue modeled", 
        #            "survey write-ins", "survey modeled write-ins", "survey roas", "podscribe revenue", "podscribe roas"]
        payload = {"startdate":self.de_startdate.date().toString(),
                   "enddate" : self.de_enddate.date().toString(),
                   "brand" : self.cb_brandfilter.currentText()}
        self.table_model.clear()
        data = get(self.token, "/getperformance", payload) # expect this to be a list of lists
        self.table_model.setHorizontalHeaderLabels(data[0])
        for row in data[1:]:
            row_items = [QStandardItem(str(item)) for item in row]
            self.table_model.appendRow(row_items)

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