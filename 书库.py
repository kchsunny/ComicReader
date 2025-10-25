# from PySide6.QtWidgets import (QWidget, QScrollArea, QSplitter, QApplication, QHBoxLayout, QPushButton, QVBoxLayout,
#                                QListWidget, QFileDialog, QSpacerItem, QSizePolicy,QMessageBox)
# from PySide6.QtCore import Qt, QObject, QEvent, QSize, Signal, Slot
# from PySide6.QtSql import *
# import PySide6
from PySide6.QtGui import QIcon, QPixmap, QResizeEvent
from utils.LTopUtils import *
from utils.LMidUtils import *
from utils.LBottomUtils import *
from utils.RUtils import *
import os
# from PDF import ImageBrowser


class QBookShelf(QWidget):
    def __init__(self):
        super(QBookShelf, self).__init__()
        self.setWindowIcon(QIcon("resource/BookShelf.png"))
        self.setWindowTitle("书柜")
        self.setStyleSheet("QPushButton{shadow: none;}")
        self.librarycount = 0
        self.leftTopListCount = 0                   # 记录书库的数量
        self.BOOKSIZE = [[50, 100], [100, 200]]     # 预览的最大与最小尺寸
        self.setMinimumHeight(400)
        self.setMinimumWidth(950)
        self.setGeometry(200, 200, 916, 500)
        self.selected_item = None                   # 当前选中的Item，上、中、下
        self.selected_library_item = None           # 当前选中的LTopItem
        self.SplitWindow = QSplitter(self)
        self.SplitWindow.setGeometry(0, 0, self.width(), self.height())
        self.SplitWindow.setStyleSheet("""
            QSplitter::handle {
                background-color: #B8ACB0; /* 设置分割线的颜色 */
            }
        """)
        self.BookListArea = QSplitter(Qt.Orientation.Vertical)
        self.BookListArea.setMinimumWidth(201)
        self.BookListArea.setStyleSheet("""
                    QSplitter::handle {
                        background-color: #B8ACB0; /* 设置分割线的颜色 */
                    }
                    # {"border-bottom: 1px solid gray;background-color: #4D4849;"}
                """)
        self.SplitWindow.addWidget(self.BookListArea)
        if not os.path.exists("./userdata"):
            os.makedirs("userdata")
        # 设置右边预览
        self.BookViewArea = RightArea(self)
        self.BookViewArea.setMinimumWidth(715)
        # self.BookViewArea.installEventFilter(self.fileter)
        self.SplitWindow.addWidget(self.BookViewArea)

        # 设置左边书库列表
        self.LATop = LTop(self)

        # 设置书库中文件夹列表
        self.LAMid = LMid(self)  # 书库目录操作栏

        # 设置阅读列表
        self.LABottom = LBottom(self)

        # 设置左边书库区域布局
        self.BookListArea.addWidget(self.LATop)
        self.BookListArea.addWidget(self.LAMid)
        self.BookListArea.addWidget(self.LABottom)

        # self.set_areas()
        # print(self.findChild(QWidget, "scrollAreaWidgetContents_LTop"))

    def resizeEvent(self, event: PySide6.QtGui.QResizeEvent) -> None:  # 刷新界面元素大小布局
        self.SplitWindow.setGeometry(0, 0, self.width(), self.height())
        super().resizeEvent(event)


if __name__ == "__main__":
    app = QApplication([])
    window = QBookShelf()
    window.show()
    app.exec()
