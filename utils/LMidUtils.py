from PySide6.QtWidgets import (QWidget, QMenu, QMessageBox, QApplication)
from PySide6.QtGui import QIcon, QPixmap, QAction
from PySide6.QtSql import QSqlDatabase, QSqlQuery
from PySide6.QtCore import Qt
from UIParts.part2 import Ui_Form as MidArea
from UIParts import part2_Item  # 库文件列表
from utils import get_all_dirs_from_library
import PySide6


# 库中文件列表区域
class LMid(QWidget, MidArea):
    def __init__(self, shelf):
        super(LMid, self).__init__()
        self.setupUi(self)
        self.shelf = shelf
        # self.setFixedHeight(32)
        self.setObjectName("LMidMenu")
        self.pushButton_add.setIcon(QIcon("resource/add_white.png"))
        self.pushButton_add.setToolTip("在文件夹中创建新文件夹")
        self.pushButton_add.hide()
        self.pushButton_delete.setIcon(QIcon("resource/delete_white.png"))
        self.pushButton_delete.setToolTip("从库中删除文件夹")
        self.pushButton_delete.clicked.connect(self.delete_dir_item)
        self.pushButton_root.setIcon(QIcon("resource/home_white.png"))
        self.pushButton_root.setToolTip("回到当前库目录")
        self.pushButton_root.clicked.connect(self.root_dir)
        self.pushButton_expand.setIcon(QIcon("resource/展开_white.png"))
        self.pushButton_expand.setToolTip("全部展开")
        self.pushButton_expand.hide()
        self.pushButton_close.setIcon(QIcon("resource/折叠_white.png"))
        self.pushButton_close.setToolTip("全部折叠")
        self.pushButton_close.hide()
        self.line.setStyleSheet("border-color:black;")
        self.setStyleSheet("""
                    QLabel{color:white;border:0;} 
                    QPushButton{border:0;}
                    QToolTip{color:white;background-color: #4D4849;}
                    QWidget{background-color: #4D4849;}
                    #widget{border-bottom: 1px solid gray;}
                """)
        self.scrollArea.setStyleSheet("""
            QScrollArea { border:0;background-color: transparent; }
            QScrollBar:vertical { background-color: transparent; width:6px;}
            QScrollBar::handle:vertical { background-color: #D8D8D8; border-radius: 2px; }
            QScrollBar::add-line:vertical, 
            QScrollBar::sub-line:vertical { background-color: transparent; height: 0px; }
            QScrollBar::add-page:vertical, 
            QScrollBar::sub-page:vertical { background-color: transparent; }
        """)

    def clear_item(self):
        while self.verticalLayout_3.count():
            item = self.verticalLayout_3.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                self.verticalLayout_3.removeItem(item)
                del item
        self.verticalLayout_3.update()

    def delete_dir_item(self):
        for item in self.widget_2.children():
            print(item)
            if item.objectName() == "Form" and item.selected:
                item.delete_self()
                return

    def update_item(self, comic_info_db_path, library_name, filter_=None):
        self.clear_item()
        dir_info_list = get_all_dirs_from_library(comic_info_db_path, library_name, filter_=filter_)
        for d in dir_info_list:
            dir_list_item = LMidItem(d[0], d[1], d[2], comic_info_db_path, self.shelf, self)
            # print((d[0], d[1], d[2]))
            self.verticalLayout_3.insertWidget(self.verticalLayout_3.count() - 1, dir_list_item)
        pass

    def update_item_from_list(self, dir_info_list):
        self.clear_item()
        for d in dir_info_list:
            dir_list_item = LMidItem(d[0], d[1], d[2], d[3], self.shelf, self)
            # print((d[0], d[1], d[2]))
            self.verticalLayout_3.insertWidget(self.verticalLayout_3.count() - 1, dir_list_item)
        pass

    def root_dir(self):
        if self.shelf.selected_item.item_type == 'list':
            return
        for item in self.shelf.findChild(QWidget, "scrollAreaWidgetContents_LBottom").children():
            if item.objectName() == "Form":
                item.setStyleSheet("""
                        QWidget{border:0;}
                        QLabel{color:white;border:0;} 
                        QPushButton{border:0;}
                    """)
                item.pushButton_3.setDisabled(True)
                item.pushButton_3.setVisible(False)
                item.selected = False
        for item in self.shelf.findChild(QWidget, "scrollAreaWidgetContents_LTop").children():
            if item.objectName() == "Form":
                item.selected = False
        for item in self.widget_2.children():
            if item.objectName() == "Form":
                item.setStyleSheet("""
                        QWidget{border:0;}
                        QLabel{color:white;border:0;} 
                        QPushButton{border:0;}
                    """)
                item.pushButton.setDisabled(True)
                item.pushButton.setVisible(False)
                item.selected = False
        self.shelf.selected_item = self.shelf.selected_library_item
        self.shelf.selected_item.selected = True
        self.shelf.findChild(QWidget, "RightArea").show_root_library()


# 库文件列表
class LMidItem(QWidget, part2_Item.Ui_Form):
    def __init__(self, dir_name, belong_path, library_name, comic_info_db_path, shelf, l_mid_area):
        super().__init__()
        self.setupUi(self)
        pixmap = QPixmap("resource/文件夹_white.png")  # 替换为你的图片文件路径
        # 设置 QLabel 的 pixmap
        self.setToolTip(f'所属库:{library_name}\n路  径:{belong_path}')
        self.pushButton.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.pushButton.customContextMenuRequested.connect(self.set_menu)
        self.label.setPixmap(pixmap)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.selected = False  # 判断是否被选中
        # 调整 QLabel 的大小以适应图片的大小
        self.label.setScaledContents(True)
        self.label_dir_name.setText(dir_name)
        self.shelf = shelf
        self.item_type = "library_dir"
        self.dir_name = dir_name
        self.belong_path = belong_path
        self.library_name = library_name
        self.l_mid_area = l_mid_area
        self.comic_info_db_path = comic_info_db_path
        # self.comic_info_db = replace_path(os.path.join(self.library_path, ".library/comics.comic"))
        self.pushButton.setIcon(QIcon("resource/setting_white.png"))
        self.pushButton.setDisabled(True)
        self.pushButton.setVisible(False)
        self.setStyleSheet("color:white")
        self.objectName()
        self.setStyleSheet("""
            QWidget{border:0;}
            QLabel{color:white;border:0;} 
            QPushButton{border:0;}
        """)

    def mouseReleaseEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        # print(self.parent().objectName())
        if event.button() != Qt.MouseButton.LeftButton:
            return
        for item in self.shelf.findChild(QWidget, "scrollAreaWidgetContents_LBottom").children():
            if item.objectName() == "Form":
                item.setStyleSheet("""
                        QWidget{border:0;}
                        QLabel{color:white;border:0;} 
                        QPushButton{border:0;}
                    """)
                item.pushButton_3.setDisabled(True)
                item.pushButton_3.setVisible(False)
                item.selected = False
        for item in self.shelf.findChild(QWidget, "scrollAreaWidgetContents_LTop").children():
            if item.objectName() == "Form":
                item.selected = False
        for item in self.parent().children():
            if item.objectName() == "Form":
                item.setStyleSheet("""
                        QWidget{border:0;}
                        QLabel{color:white;border:0;} 
                        QPushButton{border:0;}
                    """)
                item.pushButton.setDisabled(True)
                item.pushButton.setVisible(False)
                item.selected = False
        self.setStyleSheet("""
            QWidget{background-color: rgba(255, 255, 255, 0.1);border:0;}
            QLabel{background-color: rgba(255, 255, 255, 0);color:white;border:0;} 
            QPushButton{background-color: rgba(255, 255, 255, 0);border:0;}
        """)
        self.pushButton.setDisabled(False)
        self.pushButton.setVisible(True)
        self.shelf.selected_item = self
        self.selected = True
        super().mouseReleaseEvent(event)

    # 点击当前Item后
    def mousePressEvent(self, event: PySide6.QtGui.QMouseEvent = None):
        if event.button() != Qt.MouseButton.LeftButton:
            return
        self.shelf.findChild(QWidget, "RightArea").set_dir_previews(self.dir_name, self.library_name)
        pass

    def set_menu(self, position):  # 弹出子菜单
        menu = QMenu(self)
        menu.setStyleSheet("color:white;background-color: rgba(0, 0, 0,0.9);")
        delete_action = QAction('删除', self)
        delete_action.setIcon(QIcon("resource/delete_black.png"))
        delete_action.triggered.connect(self.delete_self)
        copy_path_action = QAction('复制路径', self)
        copy_path_action.setIcon(QIcon("resource/复制_black.png"))
        copy_path_action.triggered.connect(self.copy_path)
        menu.addAction(delete_action)
        menu.addAction(copy_path_action)
        menu.setStyleSheet("""
                            QMenu {
                                background-color: #D3D3D3; 
                                border-radius: 10px;
                            }
                            QMenu::Item:selected {
                                background-color: #A9A9A9;
                                text-align: center;
                                border-radius: 10px;
                            }
                        """)
        # print(position)  # 相对点击按钮的位置
        menu.exec(self.pushButton.mapToGlobal(position))

    def delete_self(self):
        sql_db = QSqlDatabase("QSQLITE")
        sql_db.setDatabaseName(self.comic_info_db_path)
        if sql_db.open():
            q = QSqlQuery(sql_db)
            if not q.exec(f"DELETE FROM comics WHERE dir_name='{self.dir_name}' and library_name='{self.library_name}'"):
                QMessageBox.critical(self, "error", "删除失败")
            else:
                QMessageBox.information(self, "info", "删除成功")
            sql_db.close()
        self.deleteLater()
        pass

    def copy_path(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.belong_path)
