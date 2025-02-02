# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'bookcontainer.ui'
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
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QFrame, QLabel,
    QProgressBar, QSizePolicy, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(381, 578)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(3, 3, 3, 3)
        self.book_cover = QLabel(Form)
        self.book_cover.setObjectName(u"book_cover")
        self.book_cover.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.book_cover)

        self.progressBar = QProgressBar(Form)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setMinimumSize(QSize(0, 15))
        self.progressBar.setMaximumSize(QSize(16777215, 15))
        self.progressBar.setValue(24)
        self.progressBar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progressBar.setTextVisible(True)
        self.progressBar.setTextDirection(QProgressBar.Direction.TopToBottom)

        self.verticalLayout.addWidget(self.progressBar)

        self.textEdit_comic_name = QTextEdit(Form)
        self.textEdit_comic_name.setObjectName(u"textEdit_comic_name")
        self.textEdit_comic_name.setMinimumSize(QSize(0, 50))
        self.textEdit_comic_name.setMaximumSize(QSize(16777215, 50))
        self.textEdit_comic_name.setFrameShape(QFrame.Shape.NoFrame)
        self.textEdit_comic_name.setFrameShadow(QFrame.Shadow.Plain)
        self.textEdit_comic_name.setLineWidth(0)
        self.textEdit_comic_name.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.textEdit_comic_name.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.textEdit_comic_name.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored)
        self.textEdit_comic_name.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        self.textEdit_comic_name.setReadOnly(True)

        self.verticalLayout.addWidget(self.textEdit_comic_name)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.book_cover.setText("")
    # retranslateUi

