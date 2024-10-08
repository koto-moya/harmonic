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
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDateEdit, QDockWidget,
    QGridLayout, QHBoxLayout, QHeaderView, QLabel,
    QLayout, QLineEdit, QMainWindow, QMenu,
    QMenuBar, QProgressBar, QPushButton, QSizePolicy,
    QSpacerItem, QStackedWidget, QStatusBar, QTableView,
    QTextBrowser, QTextEdit, QToolButton, QVBoxLayout,
    QWidget)

class Ui_mw_home(object):
    def setupUi(self, mw_home):
        if not mw_home.objectName():
            mw_home.setObjectName(u"mw_home")
        mw_home.setEnabled(True)
        mw_home.resize(1104, 933)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(mw_home.sizePolicy().hasHeightForWidth())
        mw_home.setSizePolicy(sizePolicy)
        self.actionclose = QAction(mw_home)
        self.actionclose.setObjectName(u"actionclose")
        self.centralwidget = QWidget(mw_home)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(10, 0, 1021, 871))
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy1)
        self.homepage = QWidget()
        self.homepage.setObjectName(u"homepage")
        self.gridLayoutWidget_2 = QWidget(self.homepage)
        self.gridLayoutWidget_2.setObjectName(u"gridLayoutWidget_2")
        self.gridLayoutWidget_2.setGeometry(QRect(120, 60, 321, 161))
        self.gridLayout_2 = QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.current_month_revenue = QLabel(self.gridLayoutWidget_2)
        self.current_month_revenue.setObjectName(u"current_month_revenue")

        self.gridLayout_2.addWidget(self.current_month_revenue, 1, 0, 1, 1)

        self.rev_title = QLabel(self.gridLayoutWidget_2)
        self.rev_title.setObjectName(u"rev_title")

        self.gridLayout_2.addWidget(self.rev_title, 0, 0, 1, 1)

        self.spend_label = QLabel(self.gridLayoutWidget_2)
        self.spend_label.setObjectName(u"spend_label")

        self.gridLayout_2.addWidget(self.spend_label, 0, 1, 1, 1)

        self.current_spend_goal = QProgressBar(self.gridLayoutWidget_2)
        self.current_spend_goal.setObjectName(u"current_spend_goal")
        self.current_spend_goal.setValue(24)

        self.gridLayout_2.addWidget(self.current_spend_goal, 1, 1, 1, 1)

        self.stackedWidget.addWidget(self.homepage)
        self.chatpage = QWidget()
        self.chatpage.setObjectName(u"chatpage")
        self.gridLayoutWidget = QWidget(self.chatpage)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 20, 961, 811))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.te_chathistory = QTextBrowser(self.gridLayoutWidget)
        self.te_chathistory.setObjectName(u"te_chathistory")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.te_chathistory.sizePolicy().hasHeightForWidth())
        self.te_chathistory.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.te_chathistory, 0, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, -1, -1, 0)
        self.te_chatinput = QTextEdit(self.gridLayoutWidget)
        self.te_chatinput.setObjectName(u"te_chatinput")
        sizePolicy1.setHeightForWidth(self.te_chatinput.sizePolicy().hasHeightForWidth())
        self.te_chatinput.setSizePolicy(sizePolicy1)

        self.horizontalLayout_3.addWidget(self.te_chatinput)

        self.bt_submitchat = QPushButton(self.gridLayoutWidget)
        self.bt_submitchat.setObjectName(u"bt_submitchat")
        sizePolicy1.setHeightForWidth(self.bt_submitchat.sizePolicy().hasHeightForWidth())
        self.bt_submitchat.setSizePolicy(sizePolicy1)
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoUp))
        self.bt_submitchat.setIcon(icon)

        self.horizontalLayout_3.addWidget(self.bt_submitchat)

        self.horizontalLayout_3.setStretch(0, 10)
        self.horizontalLayout_3.setStretch(1, 1)

        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)

        self.gridLayout.setRowStretch(0, 100)
        self.gridLayout.setRowStretch(1, 10)
        self.gridLayout.setColumnStretch(0, 100)
        self.stackedWidget.addWidget(self.chatpage)
        self.brandperformance = QWidget()
        self.brandperformance.setObjectName(u"brandperformance")
        sizePolicy.setHeightForWidth(self.brandperformance.sizePolicy().hasHeightForWidth())
        self.brandperformance.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.brandperformance)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lbl_brandfilter = QLabel(self.brandperformance)
        self.lbl_brandfilter.setObjectName(u"lbl_brandfilter")

        self.horizontalLayout_2.addWidget(self.lbl_brandfilter)

        self.horizontalSpacer_2 = QSpacerItem(98, 17, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.lbl_datefilter = QLabel(self.brandperformance)
        self.lbl_datefilter.setObjectName(u"lbl_datefilter")

        self.horizontalLayout_2.addWidget(self.lbl_datefilter)

        self.horizontalSpacer = QSpacerItem(1, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.cb_brandfilter = QComboBox(self.brandperformance)
        self.cb_brandfilter.setObjectName(u"cb_brandfilter")

        self.horizontalLayout.addWidget(self.cb_brandfilter)

        self.de_startdate = QDateEdit(self.brandperformance)
        self.de_startdate.setObjectName(u"de_startdate")
        self.de_startdate.setCalendarPopup(True)

        self.horizontalLayout.addWidget(self.de_startdate)

        self.de_enddate = QDateEdit(self.brandperformance)
        self.de_enddate.setObjectName(u"de_enddate")
        self.de_enddate.setCalendarPopup(True)

        self.horizontalLayout.addWidget(self.de_enddate)

        self.bt_seeperformance = QPushButton(self.brandperformance)
        self.bt_seeperformance.setObjectName(u"bt_seeperformance")

        self.horizontalLayout.addWidget(self.bt_seeperformance)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.tbl_brandperformance = QTableView(self.brandperformance)
        self.tbl_brandperformance.setObjectName(u"tbl_brandperformance")
        sizePolicy.setHeightForWidth(self.tbl_brandperformance.sizePolicy().hasHeightForWidth())
        self.tbl_brandperformance.setSizePolicy(sizePolicy)

        self.verticalLayout_2.addWidget(self.tbl_brandperformance)

        self.stackedWidget.addWidget(self.brandperformance)
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.gridLayoutWidget_3 = QWidget(self.page)
        self.gridLayoutWidget_3.setObjectName(u"gridLayoutWidget_3")
        self.gridLayoutWidget_3.setGeometry(QRect(40, 50, 881, 271))
        self.gridLayout_3 = QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.cb_existingcodes = QComboBox(self.gridLayoutWidget_3)
        self.cb_existingcodes.setObjectName(u"cb_existingcodes")

        self.gridLayout_3.addWidget(self.cb_existingcodes, 2, 4, 1, 1)

        self.bt_submitnewpodcast = QPushButton(self.gridLayoutWidget_3)
        self.bt_submitnewpodcast.setObjectName(u"bt_submitnewpodcast")

        self.gridLayout_3.addWidget(self.bt_submitnewpodcast, 3, 2, 1, 1)

        self.bt_submitnewcode = QPushButton(self.gridLayoutWidget_3)
        self.bt_submitnewcode.setObjectName(u"bt_submitnewcode")

        self.gridLayout_3.addWidget(self.bt_submitnewcode, 3, 0, 1, 1)

        self.bt_suspendcode = QPushButton(self.gridLayoutWidget_3)
        self.bt_suspendcode.setObjectName(u"bt_suspendcode")

        self.gridLayout_3.addWidget(self.bt_suspendcode, 3, 4, 1, 1)

        self.lbl_newcode_3 = QLabel(self.gridLayoutWidget_3)
        self.lbl_newcode_3.setObjectName(u"lbl_newcode_3")

        self.gridLayout_3.addWidget(self.lbl_newcode_3, 1, 2, 1, 1)

        self.le_newcode = QLineEdit(self.gridLayoutWidget_3)
        self.le_newcode.setObjectName(u"le_newcode")

        self.gridLayout_3.addWidget(self.le_newcode, 2, 0, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_3, 1, 1, 1, 1)

        self.lbl_newcode_2 = QLabel(self.gridLayoutWidget_3)
        self.lbl_newcode_2.setObjectName(u"lbl_newcode_2")

        self.gridLayout_3.addWidget(self.lbl_newcode_2, 1, 4, 1, 1)

        self.lbl_newcode = QLabel(self.gridLayoutWidget_3)
        self.lbl_newcode.setObjectName(u"lbl_newcode")

        self.gridLayout_3.addWidget(self.lbl_newcode, 1, 0, 1, 1)

        self.gridLayout_8 = QGridLayout()
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.cb_podcastsuspendcode = QComboBox(self.gridLayoutWidget_3)
        self.cb_podcastsuspendcode.setObjectName(u"cb_podcastsuspendcode")

        self.gridLayout_8.addWidget(self.cb_podcastsuspendcode, 2, 0, 1, 1)

        self.lbl_podcast_2 = QLabel(self.gridLayoutWidget_3)
        self.lbl_podcast_2.setObjectName(u"lbl_podcast_2")

        self.gridLayout_8.addWidget(self.lbl_podcast_2, 1, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_8.addItem(self.verticalSpacer_2, 0, 0, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_8, 0, 4, 1, 1)

        self.gridLayout_7 = QGridLayout()
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.de_codeenddate = QDateEdit(self.gridLayoutWidget_3)
        self.de_codeenddate.setObjectName(u"de_codeenddate")
        self.de_codeenddate.setCalendarPopup(True)

        self.gridLayout_6.addWidget(self.de_codeenddate, 1, 1, 1, 1)

        self.lbl_newcodestartdate = QLabel(self.gridLayoutWidget_3)
        self.lbl_newcodestartdate.setObjectName(u"lbl_newcodestartdate")

        self.gridLayout_6.addWidget(self.lbl_newcodestartdate, 0, 0, 1, 1)

        self.de_codestartdate = QDateEdit(self.gridLayoutWidget_3)
        self.de_codestartdate.setObjectName(u"de_codestartdate")
        self.de_codestartdate.setCalendarPopup(True)

        self.gridLayout_6.addWidget(self.de_codestartdate, 1, 0, 1, 1)

        self.lbl_newcodeenddate = QLabel(self.gridLayoutWidget_3)
        self.lbl_newcodeenddate.setObjectName(u"lbl_newcodeenddate")

        self.gridLayout_6.addWidget(self.lbl_newcodeenddate, 0, 1, 1, 1)


        self.gridLayout_7.addLayout(self.gridLayout_6, 0, 0, 1, 1)

        self.cb_podcast = QComboBox(self.gridLayoutWidget_3)
        self.cb_podcast.setObjectName(u"cb_podcast")

        self.gridLayout_7.addWidget(self.cb_podcast, 2, 0, 1, 1)

        self.lbl_podcast = QLabel(self.gridLayoutWidget_3)
        self.lbl_podcast.setObjectName(u"lbl_podcast")

        self.gridLayout_7.addWidget(self.lbl_podcast, 1, 0, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_7, 0, 0, 1, 1)

        self.le_newpodcast = QLineEdit(self.gridLayoutWidget_3)
        self.le_newpodcast.setObjectName(u"le_newpodcast")

        self.gridLayout_3.addWidget(self.le_newpodcast, 2, 2, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_4, 1, 3, 1, 1)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.verticalLayoutWidget = QWidget(self.page_2)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(70, 30, 481, 321))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.cb_brandspend = QComboBox(self.verticalLayoutWidget)
        self.cb_brandspend.setObjectName(u"cb_brandspend")

        self.gridLayout_4.addWidget(self.cb_brandspend, 2, 0, 1, 1)

        self.cb_podcastspend = QComboBox(self.verticalLayoutWidget)
        self.cb_podcastspend.setObjectName(u"cb_podcastspend")

        self.gridLayout_4.addWidget(self.cb_podcastspend, 4, 0, 1, 1)

        self.label_5 = QLabel(self.verticalLayoutWidget)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout_4.addWidget(self.label_5, 3, 0, 1, 1)

        self.lbl_actualspendbrand = QLabel(self.verticalLayoutWidget)
        self.lbl_actualspendbrand.setObjectName(u"lbl_actualspendbrand")

        self.gridLayout_4.addWidget(self.lbl_actualspendbrand, 1, 0, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_4)

        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.bt_spendgoal = QPushButton(self.verticalLayoutWidget)
        self.bt_spendgoal.setObjectName(u"bt_spendgoal")

        self.gridLayout_5.addWidget(self.bt_spendgoal, 2, 0, 1, 1)

        self.le_spendgoal = QLineEdit(self.verticalLayoutWidget)
        self.le_spendgoal.setObjectName(u"le_spendgoal")

        self.gridLayout_5.addWidget(self.le_spendgoal, 1, 0, 1, 1)

        self.lbl_actualspend = QLabel(self.verticalLayoutWidget)
        self.lbl_actualspend.setObjectName(u"lbl_actualspend")

        self.gridLayout_5.addWidget(self.lbl_actualspend, 0, 1, 1, 1)

        self.lbl_spendgoal = QLabel(self.verticalLayoutWidget)
        self.lbl_spendgoal.setObjectName(u"lbl_spendgoal")

        self.gridLayout_5.addWidget(self.lbl_spendgoal, 0, 0, 1, 1)

        self.le_actualspend = QLineEdit(self.verticalLayoutWidget)
        self.le_actualspend.setObjectName(u"le_actualspend")

        self.gridLayout_5.addWidget(self.le_actualspend, 1, 1, 1, 1)

        self.bt_updtspendgoal = QPushButton(self.verticalLayoutWidget)
        self.bt_updtspendgoal.setObjectName(u"bt_updtspendgoal")

        self.gridLayout_5.addWidget(self.bt_updtspendgoal, 3, 0, 1, 1)

        self.bt_submitactualspend = QPushButton(self.verticalLayoutWidget)
        self.bt_submitactualspend.setObjectName(u"bt_submitactualspend")

        self.gridLayout_5.addWidget(self.bt_submitactualspend, 2, 1, 1, 1)

        self.bt_updtactualspend = QPushButton(self.verticalLayoutWidget)
        self.bt_updtactualspend.setObjectName(u"bt_updtactualspend")

        self.gridLayout_5.addWidget(self.bt_updtactualspend, 3, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_5)

        self.stackedWidget.addWidget(self.page_2)
        mw_home.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(mw_home)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1104, 24))
        self.menubar.setDefaultUp(False)
        self.menubar.setNativeMenuBar(False)
        self.file = QMenu(self.menubar)
        self.file.setObjectName(u"file")
        self.file.setEnabled(True)
        mw_home.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(mw_home)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setEnabled(False)
        self.statusbar.setSizeGripEnabled(False)
        mw_home.setStatusBar(self.statusbar)
        self.w_dock = QDockWidget(mw_home)
        self.w_dock.setObjectName(u"w_dock")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.w_dock.sizePolicy().hasHeightForWidth())
        self.w_dock.setSizePolicy(sizePolicy3)
        self.w_dock.setMinimumSize(QSize(50, 288))
        font = QFont()
        font.setPointSize(9)
        self.w_dock.setFont(font)
        self.w_dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.verticalLayout_3 = QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.bt_home = QToolButton(self.dockWidgetContents)
        self.bt_home.setObjectName(u"bt_home")
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.GoHome))
        self.bt_home.setIcon(icon1)

        self.verticalLayout_3.addWidget(self.bt_home)

        self.bt_chat = QToolButton(self.dockWidgetContents)
        self.bt_chat.setObjectName(u"bt_chat")
        icon2 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.WeatherStorm))
        self.bt_chat.setIcon(icon2)

        self.verticalLayout_3.addWidget(self.bt_chat)

        self.bt_brandperformance = QToolButton(self.dockWidgetContents)
        self.bt_brandperformance.setObjectName(u"bt_brandperformance")
        icon3 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.MailMarkImportant))
        self.bt_brandperformance.setIcon(icon3)

        self.verticalLayout_3.addWidget(self.bt_brandperformance)

        self.bt_codepodcastinput = QToolButton(self.dockWidgetContents)
        self.bt_codepodcastinput.setObjectName(u"bt_codepodcastinput")
        icon4 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.MediaEject))
        self.bt_codepodcastinput.setIcon(icon4)

        self.verticalLayout_3.addWidget(self.bt_codepodcastinput)

        self.bt_spendinput = QToolButton(self.dockWidgetContents)
        self.bt_spendinput.setObjectName(u"bt_spendinput")
        icon5 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditPaste))
        self.bt_spendinput.setIcon(icon5)

        self.verticalLayout_3.addWidget(self.bt_spendinput)

        self.verticalSpacer = QSpacerItem(20, 285, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.bt_refresh = QToolButton(self.dockWidgetContents)
        self.bt_refresh.setObjectName(u"bt_refresh")
        icon6 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.MediaSeekForward))
        self.bt_refresh.setIcon(icon6)

        self.verticalLayout_3.addWidget(self.bt_refresh)

        self.bt_settings = QToolButton(self.dockWidgetContents)
        self.bt_settings.setObjectName(u"bt_settings")
        icon7 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.HelpAbout))
        self.bt_settings.setIcon(icon7)

        self.verticalLayout_3.addWidget(self.bt_settings)

        self.w_dock.setWidget(self.dockWidgetContents)
        mw_home.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.w_dock)

        self.menubar.addAction(self.file.menuAction())
        self.file.addAction(self.actionclose)

        self.retranslateUi(mw_home)

        self.stackedWidget.setCurrentIndex(3)


        QMetaObject.connectSlotsByName(mw_home)
    # setupUi

    def retranslateUi(self, mw_home):
        mw_home.setWindowTitle(QCoreApplication.translate("mw_home", u"MainWindow", None))
        self.actionclose.setText(QCoreApplication.translate("mw_home", u"close", None))
        self.current_month_revenue.setText(QCoreApplication.translate("mw_home", u"TextLabel", None))
        self.rev_title.setText(QCoreApplication.translate("mw_home", u"Curent Monthly Revenue", None))
        self.spend_label.setText(QCoreApplication.translate("mw_home", u"spend goal", None))
        self.bt_submitchat.setText("")
        self.lbl_brandfilter.setText(QCoreApplication.translate("mw_home", u"brand", None))
        self.lbl_datefilter.setText(QCoreApplication.translate("mw_home", u"date filter", None))
        self.bt_seeperformance.setText(QCoreApplication.translate("mw_home", u"see performance", None))
        self.bt_submitnewpodcast.setText(QCoreApplication.translate("mw_home", u"submit podcast", None))
        self.bt_submitnewcode.setText(QCoreApplication.translate("mw_home", u"submit code", None))
        self.bt_suspendcode.setText(QCoreApplication.translate("mw_home", u"suspend code", None))
        self.lbl_newcode_3.setText(QCoreApplication.translate("mw_home", u"new podcast", None))
        self.lbl_newcode_2.setText(QCoreApplication.translate("mw_home", u"Exisiting code", None))
        self.lbl_newcode.setText(QCoreApplication.translate("mw_home", u"new code", None))
        self.lbl_podcast_2.setText(QCoreApplication.translate("mw_home", u"podcast", None))
        self.lbl_newcodestartdate.setText(QCoreApplication.translate("mw_home", u"code start date", None))
        self.lbl_newcodeenddate.setText(QCoreApplication.translate("mw_home", u"code end date", None))
        self.lbl_podcast.setText(QCoreApplication.translate("mw_home", u"podcast", None))
        self.label_5.setText(QCoreApplication.translate("mw_home", u"podcast", None))
        self.lbl_actualspendbrand.setText(QCoreApplication.translate("mw_home", u"brand", None))
        self.bt_spendgoal.setText(QCoreApplication.translate("mw_home", u"submit spend goal", None))
        self.lbl_actualspend.setText(QCoreApplication.translate("mw_home", u"actual spend", None))
        self.lbl_spendgoal.setText(QCoreApplication.translate("mw_home", u"spend goal", None))
        self.bt_updtspendgoal.setText(QCoreApplication.translate("mw_home", u"update spend goal", None))
        self.bt_submitactualspend.setText(QCoreApplication.translate("mw_home", u"submit actual spend", None))
        self.bt_updtactualspend.setText(QCoreApplication.translate("mw_home", u"update actual spend", None))
        self.file.setTitle(QCoreApplication.translate("mw_home", u"file", None))
        self.w_dock.setWindowTitle(QCoreApplication.translate("mw_home", u"podscale", None))
        self.bt_home.setText(QCoreApplication.translate("mw_home", u"...", None))
        self.bt_chat.setText(QCoreApplication.translate("mw_home", u"...", None))
        self.bt_brandperformance.setText(QCoreApplication.translate("mw_home", u"...", None))
        self.bt_codepodcastinput.setText(QCoreApplication.translate("mw_home", u"...", None))
        self.bt_spendinput.setText(QCoreApplication.translate("mw_home", u"...", None))
        self.bt_refresh.setText(QCoreApplication.translate("mw_home", u"...", None))
        self.bt_settings.setText(QCoreApplication.translate("mw_home", u"...", None))
    # retranslateUi

