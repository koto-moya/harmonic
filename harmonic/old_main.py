from homepage.homepage_ui import Ui_MainWindow
from login.login_ui import Ui_login
from PySide6 import QtWidgets
from PySide6.QtCore import Qt, Signal, QDate, QThread
from PySide6.QtGui import QStandardItemModel, QStandardItem, QTextCursor, QFont
from modules.app_requests import gestalt_post, login, Token, gestalt_get
from modules.utils import * 
from modules.Nyx import Nyx
from harmonic.old_config import chat_interface_html_head
import requests
from harmonic.old_config import server_endpoint
import time
import re
import numpy as np
import datetime
from PySide6.QtGui import QFontDatabase
import os
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtCore import QRectF, Qt
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtCore import QRectF, Qt




class StreamWorker(QThread):
    new_token = Signal(str)
    sophon_trigger = Signal()

    def __init__(self, url, token, message):
        super().__init__()
        self.url = url
        self.token = token
        self.message = message
    
    def run(self):
         headers = {"Authorization":f"Bearer {self.token}",
               "Content-Type": "application/json"}
         payload = {"new_message": self.message}

         with requests.post(self.url, headers=headers, json=payload) as response:
             response.raise_for_status()
             for chunk in response.iter_content(chunk_size=1, decode_unicode=True):
                 chunk = chunk.replace("\\n", "<br>")
                 chunk = chunk.replace('"', "<b")
                 self.new_token.emit(chunk)
                 time.sleep(0.0125)
         self.sophon_trigger.emit()
        
                 
class LoginWindow(QtWidgets.QWidget, Ui_login):
    login_successful = Signal(Token)
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.bt_login.clicked.connect(self.check_login)

    def check_login(self) -> None:
        username = self.le_username.text()
        password = self.le_password.text()
        token = login(username, password)
        if token:
            self.login_successful.emit(token)
        else:
            return None
        
# The home window should only handle the mechanistic action of the UI not actually do any logic
class HomeWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.resize(950, 600)
        self.chat_history = []
        self.charts = []
        self.te_chathistory.setHtml(chat_interface_html_head+"<body></body>")

        self.lw_performancereport.addItems(["monthly performance", "YTD performance", "exec summary"])

        self.lw_performancereport.itemClicked.connect(self.report_selected)
        # sidebar select
        self.bt_home.clicked.connect(lambda: self.switch_view(0))
        self.bt_chat.clicked.connect(lambda: self.switch_view(2))
        self.bt_chat.clicked.connect(self.create_nyx)

        self.bt_brandperformance.clicked.connect(lambda: self.switch_view(1))
        self.bt_datainput.clicked.connect(lambda: self.switch_view(3))
        self.bt_dashboard.clicked.connect(lambda: self.switch_view(4))
        self.bt_dashboard.clicked.connect(self.client_performance)

        # Connect submit buttons to the combo box refresh
        self.bt_submitnewcode.clicked.connect(self.add_new_code)
        self.bt_submitnewpodcast.clicked.connect(self.add_new_podcast)
        self.bt_suspendcode.clicked.connect(self.sus_code)
        
        # brand performance page
        self.bt_seeperformance.clicked.connect(self.display_report)
        self.table_model = QStandardItemModel()
        self.tbl_brandperformance.setModel(self.table_model)
        self.de_startdate.setDate(QDate(2024,9,1))
        self.de_enddate.setDate(QDate(2024,10,1))

        # chat page
        self.bt_chat_submit = None
    def create_nyx(self,):
        if not self.bt_chat_submit:
            self.bt_chat_submit =  Nyx()
            self.horizontalLayout_3.addWidget(self.bt_chat_submit)
            self.bt_chat_submit.clicked.connect(self.handle_chat_submit_stream)

    
    def client_performance(self):
        clear_layout(self.gridLayout_5)
        dashboard_widget = QtWidgets.QWidget()
        dashboard_layout = QtWidgets.QGridLayout(dashboard_widget)
        report_config = {"config_name": "fn_get_performance_by_brand", "brand": "lume", "startdate": "2024-01-01", "enddate": "2024-11-30"}

        headers, data = gestalt_get(self.token, report_config)
        data = [[0 if item is None else item for item in row] for row in data]
        revenue_chart = HarmonicPlot(x_vals=[datetime.datetime.timestamp(datetime.datetime.strptime(row[0], "%Y-%m-%d")) for row in data],
                                    is_datetime=True, enable_mouseover=True)
        revenue_chart.addNewLines([float(row[1]) for row in data], data_label="Revenue", units="$")
        revenue_chart.addNewLines([float(row[2]) for row in data], data_label="Spend", units="$")
        revenue_chart.render_plot()

        # Embed chart in scene
        scene = QGraphicsScene(self)
        view = QGraphicsView(scene)
        proxy = DraggableResizablePlot(revenue_chart)
        scene.addItem(proxy)
        proxy.setGeometry(QRectF(100, 100, 400, 300))

        dashboard_layout.addWidget(view)
        self.gridLayout_5.addWidget(dashboard_widget, 2, 2)



    def display_report(self):
        report = self.lw_performancereport.selectedItems()[0]
        self.table_model.clear()
        self.table_model.setHorizontalHeaderLabels(data[0])
        for row in data[1:]:
            row_items = [QStandardItem(str(item)) for item in row]
            self.table_model.appendRow(row_items)

    
    def report_selected(self, item):
        
        report_config = {"YTD performance":["Month", "Podcast", "Podscribe Spend", "Podscribe Revenue"],
                    "monthly performance":["Month", "Podcast", "Podscribe Spend", "Podscribe Revenue"],
                    "Exec Summary":[]}
        self.lw_performancefields.addItems(report_config[item.text()])
        
    def recieve_token(self, token):
        self.token = token

    def show_harmonic_window(self):
        self.show()

    def intialize_combo_boxes(self):
        self.cb_activeorinactivecode.setPlaceholderText("active status")
        self.cb_activeorinactivecode.addItems(["active", "inactive"])
        self.completers = {}
        self.combo_boxes = {"fn_get_codes": [self.cb_existingcodes],
                            "fn_get_podcasts":[self.cb_existingpodcasts,self.cb_podcastnewcode, self.cb_podcastactspd,
                                        self.cb_podcastsuspendcode, self.cb_podcastspdgl],
                            "fn_get_brands":[self.cb_brandfilterperf, self.cb_brandfilterspdgl, self.cb_brandfilteractspd,
                                          self.cb_brandfilternewcode, self.cb_brandsuspendcode] 
                            }
        for config, cbx in self.combo_boxes.items():
            _, data = gestalt_get(self.token, payload={"config_name":config})
            data = list(sum([item for item in data], []))
            for cb in cbx:
                cb.setEditable(True)
                completer = QtWidgets.QCompleter(cb)
                completer.setCaseSensitivity(Qt.CaseSensitivity(False))
                cb.setCompleter(completer)
                self.completers[cb] = completer
                cb.setPlaceholderText(config)
                cb.addItems(data)
                completer.setModel(cb.model())
        
    def update_combo_boxes(self, config):
        data = gestalt_get(self.token, config)
        for cb in self.combo_boxes[config]:
            self.update_combo_box(cb, self.completers[cb], data, config)

    def update_combo_box(self, combo_box, completer, data, config):
        current_choice = combo_box.currentText()
        combo_box.clear()
        combo_box.setPlaceholderText(config)
        combo_box.addItems(data)
        completer.setModel(combo_box.model())
        if current_choice in data:
            index = combo_box.findText(current_choice)
            combo_box.setCurrentIndex(index)

    def switch_view(self, index):
        if self.charts:
            for x in self.charts:
                x.clear_tooltip()
        self.stackedWidget.setCurrentIndex(index)
        

    def handle_chat_submit(self):
        # find the equivalent method for line edits
        in_text = self.te_chatinput.toPlainText()
        self.chat_history += create_message("messageoutgoing", in_text)
        # update the outgoing message instantly
        chat = create_chat(self.chat_history)
        self.te_chathistory.setHtml(chat)
        self.te_chatinput.clear()
        self.te_chathistory.moveCursor(QTextCursor.End)
        self.te_chathistory.ensureCursorVisible()

        agent_message = gestalt_post(self.token, "/chat", {"new_message":in_text})
        agent_message = agent_message.replace("\\n","<br>")
        agent_message = agent_message.replace('"','')
        self.chat_history += create_message("messageincoming", agent_message)
        
        chat = create_chat(self.chat_history)
        self.te_chathistory.setHtml(chat)
        self.te_chathistory.moveCursor(QTextCursor.End)
        self.te_chathistory.ensureCursorVisible()
        

    def handle_chat_submit_stream(self):
        # find the equivalent method for line edits
        self.te_chathistory.moveCursor(QTextCursor.End)
        in_text = self.te_chatinput.toPlainText()

        out_going = create_message("messageoutgoing", in_text)
        self.chat_history.append(out_going)
        # update the outgoing message instantly
        chat = create_chat("".join(self.chat_history))
        self.te_chathistory.setHtml(chat)
        self.te_chatinput.clear()
        self.te_chathistory.moveCursor(QTextCursor.End)
        self.te_chathistory.ensureCursorVisible()
        
        self.stream_worker = StreamWorker(server_endpoint+"/chatstream", self.token, in_text)
        self.stream_worker.new_token.connect(self.update_chat)
        self.stream_start = True
        self.stream_worker.start()
        self.stream_worker.sophon_trigger.connect(self.bt_chat_submit.resetToSphere) 

    def update_chat(self, token_chunk):
        if self.stream_start == True:
            first_stream_chunk = create_first_stream_chunk(token_chunk)
            self.chat_history.append(first_stream_chunk)
        else:
            next_stream_chunk = create_next_stream_chunk(token_chunk)
            self.chat_history.append(next_stream_chunk)
        self.chat_history = [re.sub(r"<b(?!r)", "", x) for x in self.chat_history]
        self.chat_history = [x.replace("\n", "<br>") for x in self.chat_history]

        chat = create_chat("".join(self.chat_history))
        self.te_chathistory.setHtml(chat)
        self.te_chathistory.moveCursor(QTextCursor.End)
        self.te_chathistory.ensureCursorVisible()
        self.stream_start = False
    

    def add_new_code(self):
        new_code  = self.le_newcode.text()
        startdate = self.de_startdatenewcode.date().toString()
        enddate = self.de_enddatenewcode.date().toString()
        brand = self.cb_brandfilternewcode.currentText()
        podcast = self.cb_podcastnewcode.currentText()
        activestatus = self.cb_activeorinactivecode.currentText()
        if activestatus == "active":
            activestatus = True
        else:
            activestatus = False
        gestalt_post(self.token, "/newcodes", {"code":new_code, "brand":brand, "podcast":podcast, 
                                          "activestatus":activestatus, "startdate":startdate, "enddate":enddate})
        self.update_combo_boxes("/getcodes")

    def add_new_podcast(self):
        new_podcast = self.le_newpodcast.text()
        gestalt_post(self.token, "/newpodcasts", {"podcastname":new_podcast})
        self.update_combo_boxes("/getpodcasts")

    def sus_code(self):
        code = self.cb_existingcodes.currentText()
        podcast = self.cb_podcastsuspendcode.currentText()
        brand = self.cb_brandsuspendcode.currentText()
        suspenddate = self.de_suspenddate.date().toString()
        gestalt_post(self.token, "/suspendcodes", {"code":code, "suspenddate":suspenddate, "podcast":podcast, "brand":brand})
        self.update_combo_boxes("/getcodes")

if __name__ == "__main__":
    app = QtWidgets.QApplication()
    path = os.path.join("modules", "OxygenMono-Regular.ttf")
    abs_path = os.path.abspath(path)
    font_id = QFontDatabase.addApplicationFont(abs_path)
    
    if font_id!= -1:
       font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
       font = QFont(font_family, 10)
       app.setFont(font) 
    login_window = LoginWindow()

    harmonic_window = HomeWindow()

    login_window.login_successful.connect(harmonic_window.recieve_token)

    login_window.login_successful.connect(harmonic_window.intialize_combo_boxes)

    login_window.login_successful.connect(login_window.close)

    login_window.login_successful.connect(harmonic_window.show_harmonic_window)

    login_window.show()

    app.exec()