# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file '导入已有书库子界面.ui'
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
        Form.resize(581, 160)
        Form.setMaximumSize(QSize(16777215, 300))
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(-1, 5, 0, 5)
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(150, 150))
        self.label.setMaximumSize(QSize(150, 150))
        self.label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout.addWidget(self.label)

        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setMaximumSize(QSize(16777215, 150))
        self.verticalLayout_2 = QVBoxLayout(self.widget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.widget_6 = QWidget(self.widget_2)
        self.widget_6.setObjectName(u"widget_6")
        self.horizontalLayout_5 = QHBoxLayout(self.widget_6)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.lineEdit_path = QLineEdit(self.widget_6)
        self.lineEdit_path.setObjectName(u"lineEdit_path")

        self.horizontalLayout_5.addWidget(self.lineEdit_path)

        self.open_folder = QPushButton(self.widget_6)
        self.open_folder.setObjectName(u"open_folder")
        self.open_folder.setMinimumSize(QSize(25, 25))
        self.open_folder.setMaximumSize(QSize(25, 25))
        self.open_folder.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout_5.addWidget(self.open_folder)


        self.verticalLayout_2.addWidget(self.widget_6)


        self.verticalLayout.addWidget(self.widget_2)

        self.widget_3 = QWidget(self.widget)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setMaximumSize(QSize(16777215, 60))
        self.horizontalLayout_2 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(9, 0, 0, 0)
        self.label_parh = QLabel(self.widget_3)
        self.label_parh.setObjectName(u"label_parh")
        self.label_parh.setMinimumSize(QSize(150, 0))
        self.label_parh.setMaximumSize(QSize(150, 16777215))

        self.horizontalLayout_2.addWidget(self.label_parh)

        self.widget_4 = QWidget(self.widget_3)
        self.widget_4.setObjectName(u"widget_4")
        self.widget_4.setMinimumSize(QSize(150, 50))
        self.widget_4.setMaximumSize(QSize(150, 50))
        self.horizontalLayout_3 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButton_build = QPushButton(self.widget_4)
        self.pushButton_build.setObjectName(u"pushButton_build")
        self.pushButton_build.setMinimumSize(QSize(0, 30))
        self.pushButton_build.setMaximumSize(QSize(16777215, 30))
        self.pushButton_build.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout_3.addWidget(self.pushButton_build)

        self.pushButton_cancel = QPushButton(self.widget_4)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")
        self.pushButton_cancel.setMinimumSize(QSize(0, 30))
        self.pushButton_cancel.setMaximumSize(QSize(16777215, 30))
        self.pushButton_cancel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout_3.addWidget(self.pushButton_cancel)


        self.horizontalLayout_2.addWidget(self.widget_4)


        self.verticalLayout.addWidget(self.widget_3)


        self.horizontalLayout.addWidget(self.widget)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText("")
        self.open_folder.setText("")
        self.label_parh.setText(QCoreApplication.translate("Form", u"\u8bf7\u9009\u62e9comics.comic\u6587\u4ef6", None))
        self.pushButton_build.setText(QCoreApplication.translate("Form", u"\u5bfc\u5165", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Form", u"\u53d6\u6d88", None))
    # retranslateUi

