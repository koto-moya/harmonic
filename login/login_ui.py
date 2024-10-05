# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login.ui'
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
from PySide6.QtWidgets import (QApplication, QLineEdit, QPushButton, QSizePolicy,
    QWidget)

class Ui_login(object):
    def setupUi(self, login):
        if not login.objectName():
            login.setObjectName(u"login")
        login.resize(352, 170)
        self.le_username = QLineEdit(login)
        self.le_username.setObjectName(u"le_username")
        self.le_username.setGeometry(QRect(80, 20, 181, 31))
        self.le_username.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.le_password = QLineEdit(login)
        self.le_password.setObjectName(u"le_password")
        self.le_password.setGeometry(QRect(80, 70, 181, 31))
        self.le_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.le_password.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.bt_login = QPushButton(login)
        self.bt_login.setObjectName(u"bt_login")
        self.bt_login.setGeometry(QRect(120, 120, 100, 32))

        self.retranslateUi(login)

        QMetaObject.connectSlotsByName(login)
    # setupUi

    def retranslateUi(self, login):
        login.setWindowTitle(QCoreApplication.translate("login", u"Form", None))
        self.le_username.setPlaceholderText(QCoreApplication.translate("login", u"username", None))
        self.le_password.setPlaceholderText(QCoreApplication.translate("login", u"password", None))
        self.bt_login.setText(QCoreApplication.translate("login", u"login", None))
    # retranslateUi

