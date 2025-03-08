# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file '右半区域WEBNzK.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QScrollArea,
    QSizePolicy, QSlider, QSpacerItem, QSpinBox,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(715, 628)
        Form.setMinimumSize(QSize(715, 0))
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.operates = QWidget(Form)
        self.operates.setObjectName(u"operates")
        self.operates.setMinimumSize(QSize(0, 30))
        self.operates.setMaximumSize(QSize(16777215, 30))
        self.horizontalLayout_2 = QHBoxLayout(self.operates)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(6, 0, 6, 0)
        self.pushButton_select = QPushButton(self.operates)
        self.pushButton_select.setObjectName(u"pushButton_select")
        self.pushButton_select.setMinimumSize(QSize(0, 25))
        self.pushButton_select.setMaximumSize(QSize(50, 25))
        self.pushButton_select.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout_2.addWidget(self.pushButton_select)

        self.pushButton_delete = QPushButton(self.operates)
        self.pushButton_delete.setObjectName(u"pushButton_delete")
        self.pushButton_delete.setMinimumSize(QSize(0, 25))
        self.pushButton_delete.setMaximumSize(QSize(50, 25))
        self.pushButton_delete.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout_2.addWidget(self.pushButton_delete)

        self.pushButton_collect = QPushButton(self.operates)
        self.pushButton_collect.setObjectName(u"pushButton_collect")
        self.pushButton_collect.setMinimumSize(QSize(0, 25))
        self.pushButton_collect.setMaximumSize(QSize(50, 25))
        self.pushButton_collect.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout_2.addWidget(self.pushButton_collect)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.lineEdit_search = QLineEdit(self.operates)
        self.lineEdit_search.setObjectName(u"lineEdit_search")
        self.lineEdit_search.setMaximumSize(QSize(200, 28))
        self.lineEdit_search.setFrame(False)

        self.horizontalLayout_2.addWidget(self.lineEdit_search)

        self.pushButton_search = QPushButton(self.operates)
        self.pushButton_search.setObjectName(u"pushButton_search")
        self.pushButton_search.setMinimumSize(QSize(28, 28))
        self.pushButton_search.setMaximumSize(QSize(28, 28))
        self.pushButton_search.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout_2.addWidget(self.pushButton_search)

        self.pushButton_search_all = QPushButton(self.operates)
        self.pushButton_search_all.setObjectName(u"pushButton_search_all")
        self.pushButton_search_all.setMinimumSize(QSize(28, 28))
        self.pushButton_search_all.setMaximumSize(QSize(28, 28))
        self.pushButton_search_all.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout_2.addWidget(self.pushButton_search_all)


        self.verticalLayout.addWidget(self.operates)

        self.bookcontainer = QScrollArea(Form)
        self.bookcontainer.setObjectName(u"bookcontainer")
        self.bookcontainer.setFrameShape(QFrame.Shape.NoFrame)
        self.bookcontainer.setLineWidth(0)
        self.bookcontainer.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.bookcontainer.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.bookcontainer.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 715, 548))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 9)
        self.scrollArea = QScrollArea(self.scrollAreaWidgetContents)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setMinimumSize(QSize(0, 400))
        self.scrollArea.setMaximumSize(QSize(16777215, 400))
        self.scrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea.setFrameShadow(QFrame.Shadow.Plain)
        self.scrollArea.setWidgetResizable(True)
        self.widget_recent = QWidget()
        self.widget_recent.setObjectName(u"widget_recent")
        self.widget_recent.setGeometry(QRect(0, 0, 715, 400))
        self.horizontalLayout_recent = QHBoxLayout(self.widget_recent)
        self.horizontalLayout_recent.setObjectName(u"horizontalLayout_recent")
        self.horizontalSpacer_3 = QSpacerItem(541, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_recent.addItem(self.horizontalSpacer_3)

        self.scrollArea.setWidget(self.widget_recent)

        self.verticalLayout_2.addWidget(self.scrollArea)

        self.widget_comics = QWidget(self.scrollAreaWidgetContents)
        self.widget_comics.setObjectName(u"widget_comics")
        self.widget_comics.setMinimumSize(QSize(0, 0))

        self.verticalLayout_2.addWidget(self.widget_comics)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.bookcontainer.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.bookcontainer)

        self.viewtools = QWidget(Form)
        self.viewtools.setObjectName(u"viewtools")
        self.viewtools.setMinimumSize(QSize(0, 50))
        self.viewtools.setMaximumSize(QSize(16777215, 50))
        self.horizontalLayout = QHBoxLayout(self.viewtools)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(6, 0, 6, 0)
        self.pushButton_first_page = QPushButton(self.viewtools)
        self.pushButton_first_page.setObjectName(u"pushButton_first_page")
        self.pushButton_first_page.setMinimumSize(QSize(28, 28))
        self.pushButton_first_page.setMaximumSize(QSize(28, 28))
        self.pushButton_first_page.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButton_first_page.setStyleSheet(u"")

        self.horizontalLayout.addWidget(self.pushButton_first_page)

        self.pushButton_pre_page = QPushButton(self.viewtools)
        self.pushButton_pre_page.setObjectName(u"pushButton_pre_page")
        self.pushButton_pre_page.setMinimumSize(QSize(0, 28))
        font = QFont()
        font.setFamilies([u"\u65b9\u6b63\u7c97\u9ed1\u5b8b\u7b80\u4f53"])
        font.setPointSize(9)
        font.setBold(False)
        font.setItalic(False)
        self.pushButton_pre_page.setFont(font)
        self.pushButton_pre_page.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButton_pre_page.setStyleSheet(u"color:white;")

        self.horizontalLayout.addWidget(self.pushButton_pre_page)

        self.spinBox_page_index = QSpinBox(self.viewtools)
        self.spinBox_page_index.setObjectName(u"spinBox_page_index")
        self.spinBox_page_index.setMinimumSize(QSize(60, 28))
        self.spinBox_page_index.setStyleSheet(u"color:white;")
        self.spinBox_page_index.setWrapping(False)
        self.spinBox_page_index.setFrame(False)
        self.spinBox_page_index.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spinBox_page_index.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.spinBox_page_index.setCorrectionMode(QAbstractSpinBox.CorrectionMode.CorrectToNearestValue)
        self.spinBox_page_index.setKeyboardTracking(True)
        self.spinBox_page_index.setMinimum(1)
        self.spinBox_page_index.setMaximum(999999)

        self.horizontalLayout.addWidget(self.spinBox_page_index)

        self.pushButton_next_page = QPushButton(self.viewtools)
        self.pushButton_next_page.setObjectName(u"pushButton_next_page")
        self.pushButton_next_page.setMinimumSize(QSize(0, 28))
        self.pushButton_next_page.setFont(font)
        self.pushButton_next_page.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButton_next_page.setStyleSheet(u"color:white;")

        self.horizontalLayout.addWidget(self.pushButton_next_page)

        self.pushButton_last_page = QPushButton(self.viewtools)
        self.pushButton_last_page.setObjectName(u"pushButton_last_page")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_last_page.sizePolicy().hasHeightForWidth())
        self.pushButton_last_page.setSizePolicy(sizePolicy)
        self.pushButton_last_page.setMinimumSize(QSize(28, 28))
        self.pushButton_last_page.setMaximumSize(QSize(28, 28))
        self.pushButton_last_page.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout.addWidget(self.pushButton_last_page)

        self.pushButton_jump_page = QPushButton(self.viewtools)
        self.pushButton_jump_page.setObjectName(u"pushButton_jump_page")
        self.pushButton_jump_page.setMinimumSize(QSize(0, 28))
        font1 = QFont()
        font1.setFamilies([u"\u65b9\u6b63\u7c97\u9ed1\u5b8b\u7b80\u4f53"])
        self.pushButton_jump_page.setFont(font1)
        self.pushButton_jump_page.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pushButton_jump_page.setStyleSheet(u"color:white;")

        self.horizontalLayout.addWidget(self.pushButton_jump_page)

        self.label = QLabel(self.viewtools)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(16777215, 30))
        self.label.setFont(font1)
        self.label.setStyleSheet(u"color:white;")

        self.horizontalLayout.addWidget(self.label)

        self.spinBox_page_numb = QSpinBox(self.viewtools)
        self.spinBox_page_numb.setObjectName(u"spinBox_page_numb")
        self.spinBox_page_numb.setMinimumSize(QSize(50, 28))
        self.spinBox_page_numb.setStyleSheet(u"color:white;")
        self.spinBox_page_numb.setFrame(False)
        self.spinBox_page_numb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.spinBox_page_numb.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.spinBox_page_numb.setMinimum(20)
        self.spinBox_page_numb.setMaximum(100)
        self.spinBox_page_numb.setSingleStep(5)
        self.spinBox_page_numb.setValue(100)

        self.horizontalLayout.addWidget(self.spinBox_page_numb)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.pushButton_small = QPushButton(self.viewtools)
        self.pushButton_small.setObjectName(u"pushButton_small")
        self.pushButton_small.setMinimumSize(QSize(28, 28))
        self.pushButton_small.setMaximumSize(QSize(28, 28))
        self.pushButton_small.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout.addWidget(self.pushButton_small)

        self.horizontalSlider = QSlider(self.viewtools)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setMinimumSize(QSize(200, 0))
        self.horizontalSlider.setMaximumSize(QSize(200, 16777215))
        self.horizontalSlider.setCursor(QCursor(Qt.CursorShape.SizeHorCursor))
        self.horizontalSlider.setOrientation(Qt.Orientation.Horizontal)

        self.horizontalLayout.addWidget(self.horizontalSlider)

        self.pushButton_big = QPushButton(self.viewtools)
        self.pushButton_big.setObjectName(u"pushButton_big")
        self.pushButton_big.setMinimumSize(QSize(28, 28))
        self.pushButton_big.setMaximumSize(QSize(28, 28))
        self.pushButton_big.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout.addWidget(self.pushButton_big)


        self.verticalLayout.addWidget(self.viewtools)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.pushButton_select.setText(QCoreApplication.translate("Form", u"\u591a\u9009", None))
        self.pushButton_delete.setText(QCoreApplication.translate("Form", u"\u5220\u9664", None))
        self.pushButton_collect.setText(QCoreApplication.translate("Form", u"\u6536\u85cf", None))
        self.lineEdit_search.setPlaceholderText(QCoreApplication.translate("Form", u"\u641c\u7d22\u6f2b\u753b", None))
        self.pushButton_search.setText("")
        self.pushButton_search_all.setText("")
        self.pushButton_first_page.setText("")
        self.pushButton_pre_page.setText(QCoreApplication.translate("Form", u"\u4e0a\u4e00\u9875", None))
        self.spinBox_page_index.setSpecialValueText("")
        self.pushButton_next_page.setText(QCoreApplication.translate("Form", u"\u4e0b\u4e00\u9875", None))
        self.pushButton_last_page.setText("")
        self.pushButton_jump_page.setText(QCoreApplication.translate("Form", u"\u8df3\u8f6c", None))
#if QT_CONFIG(tooltip)
        self.label.setToolTip(QCoreApplication.translate("Form", u"20~100", None))
#endif // QT_CONFIG(tooltip)
        self.label.setText(QCoreApplication.translate("Form", u"\u5206\u9875\u6570:", None))
#if QT_CONFIG(tooltip)
        self.pushButton_small.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.pushButton_small.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_big.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.pushButton_big.setText("")
    # retranslateUi

