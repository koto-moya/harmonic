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
        self.code_combo_boxes = {"cb_existingcodes": self.cb_existingcodes,
                                    "cb_podcastsuspendcode": self.cb_podcastsuspendcode}
        self.brand_combo_boxes = {"cb_brandfilter": self.cb_brandfilter,
                       "cb_brandactualspend": self.cb_brandactualspend}
        self.podcast_combo_boxes = {"cb_podcast": self.cb_podcast,
                       "cb_podcastspendgoal": self.cb_podcastspendgoal,
                       "cb_podcastactualspend": self.cb_podcastactualspend}
        self.cbxs = [self.code_combo_boxes, self.brand_combo_boxes, self.podcast_combo_boxes]
        self.db_funcs = {"cb_existingcodes": get_codes(),
                       "cb_brandfilter": get_brands(),
                       "cb_podcast": get_podcasts(),
                       "cb_podcastsuspendcode": get_podcasts(),
                       "cb_podcastspendgoal": get_podcasts(),
                       "cb_podcastactualspend": get_podcasts(),
                       "cb_brandactualspend": get_brands()}
        
        for cbxs in self.cbxs:
            for k,v in cbxs.items():
                v.setEditable(True)
                completer = QtWidgets.QCompleter(v)
                completer.setCaseSensitivity(Qt.CaseSensitivity(False))
                v.setCompleter(completer)
                self.completers[k] = completer

                data = self.db_funcs[k]
                v.addItems(data)
                completer.setModel(v.model())

        #self.bt_.connect(lambda: self.update_combo_boxes(self.brand_combo_boxes))
        self.bt_submitnewcode.clicked.connect(self.add_new_code)
        self.bt_submitnewpodcast.clicked.connect(self.add_new_podcast)
        self.bt_suspendcode.clicked.connect(self.suspend_code)


        # Home page
        revenue = 2349.342
        spend_goal = 100_000
        current_spend = 75_678
        self.actionclose.triggered.connect(self.close)
        self.current_month_revenue.setText(f"${round(revenue)}")
        self.current_spend_goal.setValue((current_spend/spend_goal)*100)
        
        # chat page
        self.bt_submitchat.clicked.connect(self.handle_chat_submit)

    def update_combo_boxes(self, combo_boxes):
        for k,v in combo_boxes.items():
            self.update_combo_box(v, self.completers[k], self.db_funcs[k])

    def update_combo_box(self, combo_box, completer, db_func):
        current_choice = combo_box.currentText()
        data = db_func
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
        self.update_combo_boxes(self.code_combo_boxes)

    def add_new_podcast(self):
        self.update_combo_boxes(self.podcast_combo_boxes)

    def suspend_code(self):
        self.update_combo_boxes(self.code_combo_boxes)

    


if __name__ == "__main__":
    app = QtWidgets.QApplication()
    window = HomeWindow()
    window.show()
    app.exec()