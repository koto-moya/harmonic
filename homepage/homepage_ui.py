# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'homepage.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDateEdit, QGridLayout,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QStackedWidget, QTabWidget, QTableView, QTextEdit,
    QVBoxLayout, QWidget)
from homepage import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1140, 763)
        MainWindow.setStyleSheet(u"QMainWindow {\n"
"    background-color: #2d2b2b;\n"
"}\n"
"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_2 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.Icon_widget = QWidget(self.centralwidget)
        self.Icon_widget.setObjectName(u"Icon_widget")
        self.verticalLayout_2 = QVBoxLayout(self.Icon_widget)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(-1, 0, 12, 12)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 12, 0, 12)
        self.label = QLabel(self.Icon_widget)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(40, 40))
        self.label.setMaximumSize(QSize(40, 40))
        self.label.setPixmap(QPixmap(u":/icons/gestalt.png"))
        self.label.setScaledContents(True)

        self.horizontalLayout.addWidget(self.label)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.bt_home = QPushButton(self.Icon_widget)
        self.bt_home.setObjectName(u"bt_home")
        self.bt_home.setMinimumSize(QSize(40, 0))
        self.bt_home.setMaximumSize(QSize(100, 16777215))
        self.bt_home.setStyleSheet(u"QPushButton {\n"
"    background-color: #2d2b2b;       \n"
"    border: 1px solid #c9d1d9;          \n"
"    padding: 5px;                     \n"
"    border-radius: 5px;             \n"
"}\n"
"\n"
"QPushButton:checked{\n"
"	background-color: #981118;\n"
"}\n"
"\n"
"")
        icon = QIcon()
        icon.addFile(u":/icons/home.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.bt_home.setIcon(icon)
        self.bt_home.setCheckable(True)
        self.bt_home.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.bt_home)

        self.bt_brandperformance = QPushButton(self.Icon_widget)
        self.bt_brandperformance.setObjectName(u"bt_brandperformance")
        self.bt_brandperformance.setMinimumSize(QSize(40, 0))
        self.bt_brandperformance.setMaximumSize(QSize(100, 16777215))
        self.bt_brandperformance.setStyleSheet(u"QPushButton {\n"
"    background-color: #2d2b2b;       \n"
"    border: 1px solid #c9d1d9;              \n"
"    padding: 5px;                     \n"
"    border-radius: 5px;             \n"
"}\n"
"\n"
"QPushButton:checked{\n"
"	background-color: #981118;\n"
"}\n"
"")
        icon1 = QIcon()
        icon1.addFile(u":/icons/up-arrow.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.bt_brandperformance.setIcon(icon1)
        self.bt_brandperformance.setCheckable(True)
        self.bt_brandperformance.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.bt_brandperformance)

        self.bt_chat = QPushButton(self.Icon_widget)
        self.bt_chat.setObjectName(u"bt_chat")
        self.bt_chat.setMinimumSize(QSize(40, 0))
        self.bt_chat.setMaximumSize(QSize(100, 16777215))
        self.bt_chat.setStyleSheet(u"QPushButton {\n"
"    background-color: #2d2b2b;       \n"
"    border: 1px solid #c9d1d9;             \n"
"    padding: 5px;                     \n"
"    border-radius: 5px;             \n"
"}\n"
"\n"
"QPushButton:checked{\n"
"	background-color: #981118;\n"
"}\n"
"")
        icon2 = QIcon()
        icon2.addFile(u":/icons/chat.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.bt_chat.setIcon(icon2)
        self.bt_chat.setCheckable(True)
        self.bt_chat.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.bt_chat)

        self.bt_datainput = QPushButton(self.Icon_widget)
        self.bt_datainput.setObjectName(u"bt_datainput")
        self.bt_datainput.setMinimumSize(QSize(40, 0))
        self.bt_datainput.setMaximumSize(QSize(100, 16777215))
        self.bt_datainput.setStyleSheet(u"QPushButton {\n"
"    background-color: #2d2b2b;       \n"
"    border: 1px solid #c9d1d9;             \n"
"    padding: 5px;                     \n"
"    border-radius: 5px;             \n"
"}\n"
"\n"
"QPushButton:checked{\n"
"	background-color: #981118;\n"
"}\n"
"")
        icon3 = QIcon()
        icon3.addFile(u":/icons/upload.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.bt_datainput.setIcon(icon3)
        self.bt_datainput.setCheckable(True)
        self.bt_datainput.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.bt_datainput)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.verticalSpacer = QSpacerItem(20, 509, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.bt_logout = QPushButton(self.Icon_widget)
        self.bt_logout.setObjectName(u"bt_logout")
        self.bt_logout.setStyleSheet(u"QPushButton {\n"
"    background-color: #2d2b2b;       \n"
"    border: 1px solid #c9d1d9;             \n"
"    padding: 5px;                     \n"
"    border-radius: 5px;             \n"
"}\n"
"\n"
"QPushButton:checked{\n"
"	background-color: #981118;\n"
"}\n"
"")
        icon4 = QIcon()
        icon4.addFile(u":/icons/logout.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.bt_logout.setIcon(icon4)
        self.bt_logout.setCheckable(True)
        self.bt_logout.setAutoExclusive(True)

        self.verticalLayout_2.addWidget(self.bt_logout)


        self.horizontalLayout_2.addWidget(self.Icon_widget)

        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.label_2 = QLabel(self.page)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(350, 200, 251, 16))
        self.stackedWidget.addWidget(self.page)
        self.performance_page = QWidget()
        self.performance_page.setObjectName(u"performance_page")
        self.gridLayout_2 = QGridLayout(self.performance_page)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.cb_brandfilterperf = QComboBox(self.performance_page)
        self.cb_brandfilterperf.setObjectName(u"cb_brandfilterperf")

        self.verticalLayout_4.addWidget(self.cb_brandfilterperf)

        self.de_startdate = QDateEdit(self.performance_page)
        self.de_startdate.setObjectName(u"de_startdate")
        self.de_startdate.setCalendarPopup(True)

        self.verticalLayout_4.addWidget(self.de_startdate)

        self.de_enddate = QDateEdit(self.performance_page)
        self.de_enddate.setObjectName(u"de_enddate")
        self.de_enddate.setCalendarPopup(True)

        self.verticalLayout_4.addWidget(self.de_enddate)

        self.bt_seeperformance = QPushButton(self.performance_page)
        self.bt_seeperformance.setObjectName(u"bt_seeperformance")
        self.bt_seeperformance.setStyleSheet(u"QPushButton {\n"
"    background-color: #2d2b2b;       \n"
"    border: 1px solid #c9d1d9;              \n"
"    padding: 5px;                     \n"
"    border-radius: 5px;             \n"
"}\n"
"\n"
"\n"
"QPushButton:pressed{\n"
"	background-color: #981118;\n"
"}")
        icon5 = QIcon()
        icon5.addFile(u":/icons/send.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.bt_seeperformance.setIcon(icon5)

        self.verticalLayout_4.addWidget(self.bt_seeperformance)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)


        self.horizontalLayout_4.addLayout(self.verticalLayout_4)

        self.tbl_brandperformance = QTableView(self.performance_page)
        self.tbl_brandperformance.setObjectName(u"tbl_brandperformance")
        self.tbl_brandperformance.setStyleSheet(u"QTableView {\n"
"    background-color: #857c7c;\n"
"    border-radius: 10px;\n"
"    padding: 10px;\n"
"    font-family: 'Arial';\n"
"    font-size: 14px;\n"
"    gridline-color: #444;  /* Color of the grid lines */\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    background-color: #444;\n"
"    color: white;\n"
"    padding: 5px;\n"
"    font-family: 'Arial';\n"
"    font-size: 14px;\n"
"    border: none;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QTableView::item {\n"
"    background-color: #eaeaea;  /* Background for table cells */\n"
"    color: #000;                /* Text color in cells */\n"
"    padding: 5px;\n"
"    border: none;\n"
"}\n"
"\n"
"QTableView::item:selected {\n"
"    background-color: #981118;  /* Background when an item is selected */\n"
"    color: white;\n"
"}\n"
"")

        self.horizontalLayout_4.addWidget(self.tbl_brandperformance)


        self.gridLayout_2.addLayout(self.horizontalLayout_4, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.performance_page)
        self.chat_interface = QWidget()
        self.chat_interface.setObjectName(u"chat_interface")
        self.gridLayout = QGridLayout(self.chat_interface)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.te_chathistory = QTextEdit(self.chat_interface)
        self.te_chathistory.setObjectName(u"te_chathistory")
        self.te_chathistory.setStyleSheet(u"QTextEdit {\n"
"    background-color: #857c7c;\n"
"    border-radius: 10px;\n"
"    padding: 10px;\n"
"    font-family: 'Arial';\n"
"    font-size: 14px;\n"
"}")
        self.te_chathistory.setReadOnly(True)

        self.verticalLayout_3.addWidget(self.te_chathistory)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.te_chatinput = QTextEdit(self.chat_interface)
        self.te_chatinput.setObjectName(u"te_chatinput")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.te_chatinput.sizePolicy().hasHeightForWidth())
        self.te_chatinput.setSizePolicy(sizePolicy)
        self.te_chatinput.setMinimumSize(QSize(0, 60))
        self.te_chatinput.setMaximumSize(QSize(1000, 60))
        self.te_chatinput.setStyleSheet(u"QTextEdit {\n"
"    background-color: #2d2b2b;\n"
"    border-radius: 10px;\n"
"	border: 5px solid #857c7c;\n"
"    padding: 10px;\n"
"    font-family: 'Arial';\n"
"    font-size: 14px;\n"
"	caret-color: red;\n"
"}")

        self.horizontalLayout_3.addWidget(self.te_chatinput)

        self.bt_submitchat = QPushButton(self.chat_interface)
        self.bt_submitchat.setObjectName(u"bt_submitchat")
        self.bt_submitchat.setMinimumSize(QSize(50, 0))
        self.bt_submitchat.setMaximumSize(QSize(50, 16777215))
        self.bt_submitchat.setStyleSheet(u"QPushButton {\n"
"    background-color: #2d2b2b;       \n"
"    border: 1px solid #c9d1d9;          \n"
"    padding: 5px;                     \n"
"    border-radius: 5px;             \n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"	background-color: #981118;\n"
"}\n"
"")
        self.bt_submitchat.setIcon(icon5)
        self.bt_submitchat.setCheckable(True)

        self.horizontalLayout_3.addWidget(self.bt_submitchat)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)


        self.gridLayout.addLayout(self.verticalLayout_3, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.chat_interface)
        self.data_upload = QWidget()
        self.data_upload.setObjectName(u"data_upload")
        self.gridLayout_3 = QGridLayout(self.data_upload)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.tab_datainput = QTabWidget(self.data_upload)
        self.tab_datainput.setObjectName(u"tab_datainput")
        self.tab_datainput.setStyleSheet(u"QTabWidget::pane { \n"
"    border: 1px solid #444;            /* Border around the tab panel */\n"
"    border-radius: 10px;               /* Rounded corners for the tab panel */\n"
"    background-color: #857c7c;         /* Background color of the tab content area */\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QTabBar::tab {\n"
"    background-color: #2d2b2b;       \n"
"    border: 1px solid #c9d1d9;          \n"
"    padding: 5px;                     \n"
"    border-radius: 5px;                           /* Text color for tabs */\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"    background-color: #981118;         /* Background for the selected tab */\n"
"    color: white;                      /* Text color for the selected tab */\n"
"}\n"
"\n"
"\n"
"\n"
"")
        self.new_podcast = QWidget()
        self.new_podcast.setObjectName(u"new_podcast")
        self.layoutWidget = QWidget(self.new_podcast)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(30, 20, 264, 95))
        self.verticalLayout_5 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.label_12 = QLabel(self.layoutWidget)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_5.addWidget(self.label_12)

        self.cb_existingpodcasts = QComboBox(self.layoutWidget)
        self.cb_existingpodcasts.setObjectName(u"cb_existingpodcasts")

        self.verticalLayout_5.addWidget(self.cb_existingpodcasts)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.le_newpodcast = QLineEdit(self.layoutWidget)
        self.le_newpodcast.setObjectName(u"le_newpodcast")

        self.horizontalLayout_5.addWidget(self.le_newpodcast)

        self.bt_submitnewpodcast = QPushButton(self.layoutWidget)
        self.bt_submitnewpodcast.setObjectName(u"bt_submitnewpodcast")

        self.horizontalLayout_5.addWidget(self.bt_submitnewpodcast)


        self.verticalLayout_5.addLayout(self.horizontalLayout_5)

        self.tab_datainput.addTab(self.new_podcast, "")
        self.new_code = QWidget()
        self.new_code.setObjectName(u"new_code")
        self.widget = QWidget(self.new_code)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(90, 40, 244, 249))
        self.verticalLayout_14 = QVBoxLayout(self.widget)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.label_11 = QLabel(self.widget)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_16.addWidget(self.label_11)

        self.label_13 = QLabel(self.widget)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_16.addWidget(self.label_13)


        self.verticalLayout_7.addLayout(self.horizontalLayout_16)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.de_startdatenewcode = QDateEdit(self.widget)
        self.de_startdatenewcode.setObjectName(u"de_startdatenewcode")
        self.de_startdatenewcode.setCalendarPopup(True)

        self.horizontalLayout_6.addWidget(self.de_startdatenewcode)

        self.de_enddatenewcode = QDateEdit(self.widget)
        self.de_enddatenewcode.setObjectName(u"de_enddatenewcode")
        self.de_enddatenewcode.setCalendarPopup(True)

        self.horizontalLayout_6.addWidget(self.de_enddatenewcode)


        self.verticalLayout_6.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_12.addWidget(self.label_3)

        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_12.addWidget(self.label_4)


        self.verticalLayout_6.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.cb_brandfilternewcode = QComboBox(self.widget)
        self.cb_brandfilternewcode.setObjectName(u"cb_brandfilternewcode")

        self.horizontalLayout_7.addWidget(self.cb_brandfilternewcode)

        self.cb_podcastnewcode = QComboBox(self.widget)
        self.cb_podcastnewcode.setObjectName(u"cb_podcastnewcode")

        self.horizontalLayout_7.addWidget(self.cb_podcastnewcode)


        self.verticalLayout_6.addLayout(self.horizontalLayout_7)


        self.verticalLayout_7.addLayout(self.verticalLayout_6)

        self.le_newcode = QLineEdit(self.widget)
        self.le_newcode.setObjectName(u"le_newcode")

        self.verticalLayout_7.addWidget(self.le_newcode)

        self.cb_activeorinactivecode = QComboBox(self.widget)
        self.cb_activeorinactivecode.setObjectName(u"cb_activeorinactivecode")

        self.verticalLayout_7.addWidget(self.cb_activeorinactivecode)


        self.verticalLayout_14.addLayout(self.verticalLayout_7)

        self.bt_submitnewcode = QPushButton(self.widget)
        self.bt_submitnewcode.setObjectName(u"bt_submitnewcode")

        self.verticalLayout_14.addWidget(self.bt_submitnewcode)

        self.tab_datainput.addTab(self.new_code, "")
        self.suspend_code = QWidget()
        self.suspend_code.setObjectName(u"suspend_code")
        self.widget1 = QWidget(self.suspend_code)
        self.widget1.setObjectName(u"widget1")
        self.widget1.setGeometry(QRect(30, 30, 402, 145))
        self.verticalLayout_15 = QVBoxLayout(self.widget1)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_13 = QHBoxLayout()
#ifndef Q_OS_MAC
        self.horizontalLayout_13.setSpacing(-1)
#endif
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.label_5 = QLabel(self.widget1)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMaximumSize(QSize(16777215, 20))
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_13.addWidget(self.label_5)

        self.label_6 = QLabel(self.widget1)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMaximumSize(QSize(16777215, 20))
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_13.addWidget(self.label_6)

        self.label_14 = QLabel(self.widget1)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMaximumSize(QSize(16777215, 20))
        self.label_14.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_13.addWidget(self.label_14)

        self.label_15 = QLabel(self.widget1)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMaximumSize(QSize(16777215, 20))
        self.label_15.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_13.addWidget(self.label_15)


        self.verticalLayout_15.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.cb_existingcodes = QComboBox(self.widget1)
        self.cb_existingcodes.setObjectName(u"cb_existingcodes")

        self.horizontalLayout_11.addWidget(self.cb_existingcodes)

        self.cb_podcastsuspendcode = QComboBox(self.widget1)
        self.cb_podcastsuspendcode.setObjectName(u"cb_podcastsuspendcode")

        self.horizontalLayout_11.addWidget(self.cb_podcastsuspendcode)

        self.cb_brandsuspendcode = QComboBox(self.widget1)
        self.cb_brandsuspendcode.setObjectName(u"cb_brandsuspendcode")

        self.horizontalLayout_11.addWidget(self.cb_brandsuspendcode)

        self.de_suspenddate = QDateEdit(self.widget1)
        self.de_suspenddate.setObjectName(u"de_suspenddate")

        self.horizontalLayout_11.addWidget(self.de_suspenddate)


        self.verticalLayout_15.addLayout(self.horizontalLayout_11)

        self.bt_suspendcode = QPushButton(self.widget1)
        self.bt_suspendcode.setObjectName(u"bt_suspendcode")

        self.verticalLayout_15.addWidget(self.bt_suspendcode)

        self.tab_datainput.addTab(self.suspend_code, "")
        self.podcast_spend_goal = QWidget()
        self.podcast_spend_goal.setObjectName(u"podcast_spend_goal")
        self.layoutWidget1 = QWidget(self.podcast_spend_goal)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(40, 10, 316, 171))
        self.verticalLayout_11 = QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label_7 = QLabel(self.layoutWidget1)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_14.addWidget(self.label_7)

        self.label_8 = QLabel(self.layoutWidget1)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_14.addWidget(self.label_8)


        self.verticalLayout_11.addLayout(self.horizontalLayout_14)

        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.cb_brandfilterspdgl = QComboBox(self.layoutWidget1)
        self.cb_brandfilterspdgl.setObjectName(u"cb_brandfilterspdgl")

        self.horizontalLayout_8.addWidget(self.cb_brandfilterspdgl)

        self.cb_podcastspdgl = QComboBox(self.layoutWidget1)
        self.cb_podcastspdgl.setObjectName(u"cb_podcastspdgl")

        self.horizontalLayout_8.addWidget(self.cb_podcastspdgl)


        self.verticalLayout_9.addLayout(self.horizontalLayout_8)

        self.le_spendgoal = QLineEdit(self.layoutWidget1)
        self.le_spendgoal.setObjectName(u"le_spendgoal")

        self.verticalLayout_9.addWidget(self.le_spendgoal)


        self.verticalLayout_11.addLayout(self.verticalLayout_9)

        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.pushButton_6 = QPushButton(self.layoutWidget1)
        self.pushButton_6.setObjectName(u"pushButton_6")

        self.verticalLayout_10.addWidget(self.pushButton_6)

        self.pushButton_7 = QPushButton(self.layoutWidget1)
        self.pushButton_7.setObjectName(u"pushButton_7")

        self.verticalLayout_10.addWidget(self.pushButton_7)


        self.verticalLayout_11.addLayout(self.verticalLayout_10)

        self.tab_datainput.addTab(self.podcast_spend_goal, "")
        self.podcast_actual_spend = QWidget()
        self.podcast_actual_spend.setObjectName(u"podcast_actual_spend")
        self.layoutWidget2 = QWidget(self.podcast_actual_spend)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(60, 40, 321, 137))
        self.verticalLayout_13 = QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.label_9 = QLabel(self.layoutWidget2)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_15.addWidget(self.label_9)

        self.label_10 = QLabel(self.layoutWidget2)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_15.addWidget(self.label_10)


        self.verticalLayout_13.addLayout(self.horizontalLayout_15)

        self.verticalLayout_12 = QVBoxLayout()
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.cb_brandfilteractspd = QComboBox(self.layoutWidget2)
        self.cb_brandfilteractspd.setObjectName(u"cb_brandfilteractspd")

        self.horizontalLayout_9.addWidget(self.cb_brandfilteractspd)

        self.cb_podcastactspd = QComboBox(self.layoutWidget2)
        self.cb_podcastactspd.setObjectName(u"cb_podcastactspd")

        self.horizontalLayout_9.addWidget(self.cb_podcastactspd)


        self.verticalLayout_12.addLayout(self.horizontalLayout_9)

        self.le_actualspend = QLineEdit(self.layoutWidget2)
        self.le_actualspend.setObjectName(u"le_actualspend")

        self.verticalLayout_12.addWidget(self.le_actualspend)


        self.verticalLayout_13.addLayout(self.verticalLayout_12)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.pushButton_9 = QPushButton(self.layoutWidget2)
        self.pushButton_9.setObjectName(u"pushButton_9")

        self.horizontalLayout_10.addWidget(self.pushButton_9)

        self.pushButton_8 = QPushButton(self.layoutWidget2)
        self.pushButton_8.setObjectName(u"pushButton_8")

        self.horizontalLayout_10.addWidget(self.pushButton_8)


        self.verticalLayout_13.addLayout(self.horizontalLayout_10)

        self.tab_datainput.addTab(self.podcast_actual_spend, "")

        self.gridLayout_3.addWidget(self.tab_datainput, 0, 1, 1, 1)

        self.stackedWidget.addWidget(self.data_upload)

        self.horizontalLayout_2.addWidget(self.stackedWidget)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(3)
        self.tab_datainput.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText("")
        self.bt_home.setText("")
        self.bt_brandperformance.setText("")
        self.bt_chat.setText("")
        self.bt_datainput.setText("")
        self.bt_logout.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Homepage placeholder", None))
        self.bt_seeperformance.setText("")
        self.bt_submitchat.setText("")
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"podcast", None))
        self.le_newpodcast.setPlaceholderText(QCoreApplication.translate("MainWindow", u"new podcast", None))
        self.bt_submitnewpodcast.setText(QCoreApplication.translate("MainWindow", u"submit podcast", None))
        self.tab_datainput.setTabText(self.tab_datainput.indexOf(self.new_podcast), QCoreApplication.translate("MainWindow", u"new podcast", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"start date", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"end date", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"brand", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"podcast", None))
        self.le_newcode.setPlaceholderText(QCoreApplication.translate("MainWindow", u"new code", None))
        self.bt_submitnewcode.setText(QCoreApplication.translate("MainWindow", u"submit new code", None))
        self.tab_datainput.setTabText(self.tab_datainput.indexOf(self.new_code), QCoreApplication.translate("MainWindow", u"new code", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"code", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"podcast", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"brand", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"suspend date", None))
        self.bt_suspendcode.setText(QCoreApplication.translate("MainWindow", u"suspend code", None))
        self.tab_datainput.setTabText(self.tab_datainput.indexOf(self.suspend_code), QCoreApplication.translate("MainWindow", u"suspend code", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"brand", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"podcast", None))
        self.le_spendgoal.setPlaceholderText(QCoreApplication.translate("MainWindow", u"spend goal", None))
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"submit spend goal", None))
        self.pushButton_7.setText(QCoreApplication.translate("MainWindow", u"update spend goal", None))
        self.tab_datainput.setTabText(self.tab_datainput.indexOf(self.podcast_spend_goal), QCoreApplication.translate("MainWindow", u"podcast spend goal", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"brand", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"podcast", None))
        self.le_actualspend.setPlaceholderText(QCoreApplication.translate("MainWindow", u"actual spend", None))
        self.pushButton_9.setText(QCoreApplication.translate("MainWindow", u"update actual spend", None))
        self.pushButton_8.setText(QCoreApplication.translate("MainWindow", u"submit actual spend", None))
        self.tab_datainput.setTabText(self.tab_datainput.indexOf(self.podcast_actual_spend), QCoreApplication.translate("MainWindow", u"podcast actual spend", None))
    # retranslateUi

