# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file '创建书库子界面.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QLineEdit, QProgressBar, QPushButton, QSizePolicy,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(699, 243)
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

        self.widget_6 = QWidget(self.widget_2)
        self.widget_6.setObjectName(u"widget_6")
        self.horizontalLayout_5 = QHBoxLayout(self.widget_6)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_parh = QLabel(self.widget_6)
        self.label_parh.setObjectName(u"label_parh")
        self.label_parh.setMinimumSize(QSize(65, 0))
        self.label_parh.setMaximumSize(QSize(65, 16777215))

        self.horizontalLayout_5.addWidget(self.label_parh)

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
        self.widget_7 = QWidget(self.widget_3)
        self.widget_7.setObjectName(u"widget_7")
        self.verticalLayout_3 = QVBoxLayout(self.widget_7)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.progressBar = QProgressBar(self.widget_7)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setStyleSheet(u"QProgressBar {\n"
"                border: 0px solid grey;\n"
"                background-color:gray;\n"
"            }\n"
"            QProgressBar::chunk {\n"
"                background-color: #05B8CC;  /* \u8fdb\u5ea6\u6761\u5757\u7684\u989c\u8272 */\n"
"                width: 5px;  /* \u8fdb\u5ea6\u5757\u7684\u5bbd\u5ea6 */\n"
"                border-radius: 10px;\n"
"            }")
        self.progressBar.setValue(24)
        self.progressBar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progressBar.setOrientation(Qt.Orientation.Horizontal)
        self.progressBar.setTextDirection(QProgressBar.Direction.BottomToTop)

        self.verticalLayout_3.addWidget(self.progressBar)

        self.label_text = QLabel(self.widget_7)
        self.label_text.setObjectName(u"label_text")
        self.label_text.setMinimumSize(QSize(0, 0))
        self.label_text.setMaximumSize(QSize(16777215, 50))

        self.verticalLayout_3.addWidget(self.label_text)


        self.horizontalLayout_2.addWidget(self.widget_7)

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

        self.widget_8 = QWidget(self.widget)
        self.widget_8.setObjectName(u"widget_8")
        self.verticalLayout_4 = QVBoxLayout(self.widget_8)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(6, 0, 6, 0)
        self.textEdit = QTextEdit(self.widget_8)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setFrameShape(QFrame.Shape.Box)
        self.textEdit.setFrameShadow(QFrame.Shadow.Sunken)
        self.textEdit.setReadOnly(True)

        self.verticalLayout_4.addWidget(self.textEdit)


        self.verticalLayout.addWidget(self.widget_8)


        self.horizontalLayout.addWidget(self.widget)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText("")
        self.label_name.setText(QCoreApplication.translate("Form", u"\u65b0\u5efa\u5e93\u540d\uff1a", None))
        self.label_space.setText("")
        self.label_parh.setText(QCoreApplication.translate("Form", u"\u6240\u5728\u76ee\u5f55\uff1a", None))
        self.open_folder.setText("")
        self.progressBar.setFormat(QCoreApplication.translate("Form", u"%v/%m", None))
        self.label_text.setText(QCoreApplication.translate("Form", u"\u521b\u5efa\u4e00\u4e2a\u65b0\u4e66\u5e93\u4f1a\u6d88\u8017\u4e00\u5b9a\u65f6\u95f4\uff0c\u8bf7\u8010\u5fc3\u7b49\u5f85\u2026\u2026", None))
        self.pushButton_build.setText(QCoreApplication.translate("Form", u"\u521b\u5efa", None))
        self.pushButton_cancel.setText(QCoreApplication.translate("Form", u"\u53d6\u6d88", None))
    # retranslateUi

