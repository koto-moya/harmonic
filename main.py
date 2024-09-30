from homepage.homepage_ui import Ui_mw_home
from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QTimer
from modules.db import get_brands, get_podcasts, get_codes


class HomeWindow(QtWidgets.QMainWindow, Ui_mw_home):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.w_dock.setWindowTitle("podscale")
        self.w_dock.setFixedWidth(50)
        self.setStatusBar(None)

        # sidebar select
        self.bt_home.clicked.connect(lambda: self.switch_view(0))
        self.bt_chat.clicked.connect(lambda: self.switch_view(1))
        self.bt_brandperformance.clicked.connect(lambda: self.switch_view(2))
        self.bt_codepodcastinput.clicked.connect(lambda: self.switch_view(3))
        self.bt_spendinput.clicked.connect(lambda: self.switch_view(4))


        # setup combo boxes (filters)
        self.completers = {}
        self.combo_boxes = {"cb_existingcodes": self.cb_existingcodes,
                       "cb_brandfilter": self.cb_brandfilter,
                       "cb_podcast": self.cb_podcast,
                       "cb_podcastsuspendcode": self.cb_podcastsuspendcode,
                       "cb_spendgoalpodcast": self.cb_spendgoalpodcast,
                       "cb_actualspendpodcast": self.cb_actualspendpodcast,
                       "cb_actualspendbrand": self.cb_actualspendbrand}
        
        self.db_funcs = {"cb_existingcodes": get_codes(),
                       "cb_brandfilter": get_brands(),
                       "cb_podcast": get_podcasts(),
                       "cb_podcastsuspendcode": get_podcasts(),
                       "cb_spendgoalpodcast": get_podcasts(),
                       "cb_actualspendpodcast": get_podcasts(),
                       "cb_actualspendbrand": get_brands()}
        
        for k,v in self.combo_boxes.items():
            v.setEditable(True)
            completer = QtWidgets.QCompleter(v)
            completer.setCaseSensitivity(Qt.CaseSensitivity(False))
            v.setCompleter(completer)
            self.completers[k] = completer

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_combo_boxes)
        self.timer.start(5000)

        # Home page
        revenue = 2349.342
        spend_goal = 100_000
        current_spend = 75_678
        self.actionclose.triggered.connect(self.close)
        self.current_month_revenue.setText(f"${round(revenue)}")
        self.current_spend_goal.setValue((current_spend/spend_goal)*100)
        
        # chat page
        self.bt_submitchat.clicked.connect(self.handle_chat_submit)

    def update_combo_boxes(self):
        for k,v in self.combo_boxes.items():
            self.update_combo_box(v, self.completers[k], self.db_funcs[k])

    def update_combo_box(self, combo_box, completer, db_func):
        data = db_func
        combo_box.clear()
        combo_box.addItems(data)
        completer.setModel(combo_box.model())

    def switch_view(self, index):
        self.stackedWidget.setCurrentIndex(index)

    def handle_chat_submit(self):
        in_text = self.te_chatinput.toPlainText()
        self.te_chathistory.setHtml(f"<p>{in_text}</p>")
        self.te_chatinput.clear()


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    window = HomeWindow()
    window.show()
    app.exec()