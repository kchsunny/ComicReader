# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file '创建列表子界面.ui'
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
        Form.resize(599, 160)
        Form.setMaximumSize(QSize(16777215, 300))
        Form.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
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
        self.widget_5 = QWidget(self.widget_2)
        self.widget_5.setObjectName(u"widget_5")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_5)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_name = QLabel(self.widget_5)
        self.label_name.setObjectName(u"label_name")
        self.label_name.setMinimumSize(QSize(65, 0))
        self.label_name.setMaximumSize(QSize(65, 16777215))

        self.horizontalLayout_4.addWidget(self.label_name)

        self.lineEdit_name = QLineEdit(self.widget_5)
        self.lineEdit_name.setObjectName(u"lineEdit_name")

        self.horizontalLayout_4.addWidget(self.lineEdit_name)

        self.label_space = QLabel(self.widget_5)
        self.label_space.setObjectName(u"label_space")
        self.label_space.setMinimumSize(QSize(25, 0))
        self.label_space.setMaximumSize(QSize(25, 16777215))

        self.horizontalLayout_4.addWidget(self.label_space)


        self.verticalLayout_2.addWidget(self.widget_5)


        self.verticalLayout.addWidget(self.widget_2)

        self.widget_3 = QWidget(self.widget)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setMaximumSize(QSize(16777215, 60))
        self.horizontalLayout_2 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(9, 0, 0, 0)
        self.widget_4 = QWidget(self.widget_3)
        self.widget_4.setObjectName(u"widget_4")
        self.widget_4.setMinimumSize(QSize(150, 50))
        self.widget_4.setMaximumSize(QSize(150, 50))
        self.horizontalLayout_3 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pushButton_build = QPushButton(self.widget_4)
        self.pushButton_build.setObjectName(u"pushButton_build")
        self.pushButton_build.setMaximumSize(QSize(16777215, 16777215))
        self.pushButton_build.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout_3.addWidget(self.pushButton_build)

        self.pushButton_cancel = QPushButton(self.widget_4)
        self.pushButton_cancel.setObjectName(u"pushButton_cancel")
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
        self.label_name.setText(QCoreApplication.translate("Form", u"\u65b0\u5efa\u5217\u8868\u540d\uff1a", None))
        self.label_space.setText("")
        self.pushButton_build.setText(QCoreApplication.translate("Form", u"\u521b\u5efa", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Form", u"\u53d6\u6d88", None))
    # retranslateUi

