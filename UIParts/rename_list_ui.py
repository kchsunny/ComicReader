# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file '重命名库-子界面.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(379, 144)
        Form.setMaximumSize(QSize(500, 300))
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(50, 0))
        self.label.setMaximumSize(QSize(50, 16777215))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.label)

        self.label_oldname = QLabel(self.widget)
        self.label_oldname.setObjectName(u"label_oldname")

        self.horizontalLayout.addWidget(self.label_oldname)


        self.verticalLayout.addWidget(self.widget)

        self.widget_2 = QWidget(Form)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.widget_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(50, 0))
        self.label_2.setMaximumSize(QSize(50, 16777215))
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label_2)

        self.lineEdit_newname = QLineEdit(self.widget_2)
        self.lineEdit_newname.setObjectName(u"lineEdit_newname")

        self.horizontalLayout_2.addWidget(self.lineEdit_newname)


        self.verticalLayout.addWidget(self.widget_2)

        self.widget_3 = QWidget(Form)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setMaximumSize(QSize(500, 300))
        self.horizontalLayout_3 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButton_rename = QPushButton(self.widget_3)
        self.pushButton_rename.setObjectName(u"pushButton_rename")
        self.pushButton_rename.setMinimumSize(QSize(50, 0))
        self.pushButton_rename.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_3.addWidget(self.pushButton_rename)

        self.pushButton_cancel = QPushButton(self.widget_3)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")
        self.pushButton_cancel.setMinimumSize(QSize(50, 0))
        self.pushButton_cancel.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_3.addWidget(self.pushButton_cancel)


        self.verticalLayout.addWidget(self.widget_3)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u539f\u540d\u79f0\uff1a", None))
        self.label_oldname.setText("")
        self.label_2.setText(QCoreApplication.translate("Form", u"\u65b0\u540d\u79f0\uff1a", None))
        self.pushButton_rename.setText(QCoreApplication.translate("Form", u"\u91cd\u547d\u540d", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Form", u"\u53d6\u6d88", None))
    # retranslateUi

