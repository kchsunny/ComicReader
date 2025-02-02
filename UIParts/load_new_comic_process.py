# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file '加载新漫画进度.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QProgressBar, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(545, 100)
        Form.setMinimumSize(QSize(0, 100))
        Form.setMaximumSize(QSize(16777215, 100))
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(16777215, 50))

        self.verticalLayout.addWidget(self.label)

        self.progressBar = QProgressBar(Form)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setStyleSheet(u"QProgressBar {\n"
"                border: 0px solid grey;\n"
"                background-color:transparent;\n"
"            }\n"
"            QProgressBar::chunk {\n"
"                background-color: #05B8CC;  /* \u8fdb\u5ea6\u6761\u5757\u7684\u989c\u8272 */\n"
"                width: 5px;  /* \u8fdb\u5ea6\u5757\u7684\u5bbd\u5ea6 */\n"
"                border-radius: 10px;\n"
"            }")
        self.progressBar.setValue(24)
        self.progressBar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.progressBar)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u9996\u6b21\u52a0\u8f7d\uff0c\u9700\u521d\u59cb\u5316\u9875\u9762\u4fe1\u606f\u2026\u2026", None))
        self.progressBar.setFormat(QCoreApplication.translate("Form", u"%v/%m", None))
    # retranslateUi

