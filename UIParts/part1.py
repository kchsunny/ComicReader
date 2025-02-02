# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file '左上展示区域.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(309, 381)
        Form.setMinimumSize(QSize(201, 0))
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget_top_menu = QWidget(Form)
        self.widget_top_menu.setObjectName(u"widget_top_menu")
        self.widget_top_menu.setMinimumSize(QSize(0, 30))
        self.widget_top_menu.setMaximumSize(QSize(16777215, 30))
        self.horizontalLayout = QHBoxLayout(self.widget_top_menu)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(3, 0, 3, 0)
        self.label = QLabel(self.widget_top_menu)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(20, 25))
        self.label.setMaximumSize(QSize(20, 25))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButton_add = QPushButton(self.widget_top_menu)
        self.pushButton_add.setObjectName(u"pushButton_add")
        self.pushButton_add.setMinimumSize(QSize(25, 25))
        self.pushButton_add.setMaximumSize(QSize(25, 25))
        self.pushButton_add.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout.addWidget(self.pushButton_add)

        self.pushButton_import = QPushButton(self.widget_top_menu)
        self.pushButton_import.setObjectName(u"pushButton_import")
        self.pushButton_import.setMinimumSize(QSize(25, 25))
        self.pushButton_import.setMaximumSize(QSize(25, 25))
        self.pushButton_import.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout.addWidget(self.pushButton_import)


        self.verticalLayout.addWidget(self.widget_top_menu)

        self.scrollArea_top_list = QScrollArea(Form)
        self.scrollArea_top_list.setObjectName(u"scrollArea_top_list")
        self.scrollArea_top_list.setWidgetResizable(True)
        self.scrollAreaWidgetContents_LTop = QWidget()
        self.scrollAreaWidgetContents_LTop.setObjectName(u"scrollAreaWidgetContents_LTop")
        self.scrollAreaWidgetContents_LTop.setGeometry(QRect(0, 0, 307, 349))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents_LTop)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalSpacer = QSpacerItem(20, 328, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.scrollArea_top_list.setWidget(self.scrollAreaWidgetContents_LTop)

        self.verticalLayout.addWidget(self.scrollArea_top_list)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u5e93", None))
        self.pushButton_add.setText("")
        self.pushButton_import.setText("")
    # retranslateUi

