from PySide6.QtGui import QIcon
from UIParts import part3
from UIParts import part3_Item
from UIParts import rename_list_ui
from UIParts import subwindow_create_list
from PySide6.QtGui import *
from utils import *


class SubWindowCreateList(QWidget, subwindow_create_list.Ui_Form):
    def __init__(self, LBottomArea):
        super().__init__()
        self.setupUi(self)
        self.l_bottom_area = LBottomArea
        self.pushButton_cancel.clicked.connect(self.cancel)
        self.pushButton_build.clicked.connect(self.create_list)
        self.label.setPixmap(QPixmap("resource/新建标签_black.png"))
        self.label.setScaledContents(True)

    def create_list(self):
        name = self.lineEdit_name.text()
        if not name:
            QMessageBox.critical(self, "创建失败", "不能为空名称")
            return
        if create_list(name):
            self.l_bottom_area.add_to_show_area(name, True)
        else:
            QMessageBox.critical(self, "创建失败", "已有同名阅读列表")
        self.cancel()

    def cancel(self):
        self.lineEdit_name.setText("")
        self.hide()


# 阅读列表区域
class LBottom(QWidget, part3.Ui_Form):
    def __init__(self, shelf):
        super(LBottom, self).__init__()
        self.setupUi(self)
        self.shelf = shelf
        # self.setFixedHeight(32)
        self.rename_ui = RenameUI(None, None)
        self.setObjectName("LBottomMenu")
        self.pushButton_add.setIcon(QIcon("resource/add_white.png"))
        self.pushButton_add.setToolTip("添加新列表")
        self.pushButton_color.setIcon(QIcon("resource/标签_white.png"))
        self.pushButton_color.setToolTip("设置标签")
        self.pushButton_edit.setIcon(QIcon("resource/Edit_white.png"))
        self.pushButton_edit.setToolTip("编辑列表")
        self.pushButton_delete.setIcon(QIcon("resource/delete_white.png"))
        self.pushButton_delete.setToolTip("删除列表")
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
        comic_list_item = LBottomItem("收藏", self.shelf, False, "resource/heart_red.png")
        self.verticalLayout_2.insertWidget(self.verticalLayout_2.count() - 1, comic_list_item)
        self.create_list_window = SubWindowCreateList(self)
        self.create_list_window.hide()
        self.pushButton_add.clicked.connect(self.create_list)
        self.pushButton_delete.clicked.connect(self.delete_list)
        self.pushButton_edit.clicked.connect(self.rename_list)
        self.init_list()

    def add_to_show_area(self, name, is_change_able):
        # LBottomItem __init__(self, list_name, shelf, is_change_able, label):
        comic_list_item = LBottomItem(name, self.shelf, is_change_able, "resource/标签_white.png")
        self.verticalLayout_2.insertWidget(self.verticalLayout_2.count() - 1, comic_list_item)

    def init_list(self):
        print("LBottom init_list: 初始化")
        sql = QSqlDatabase("QSQLITE")
        sql.setDatabaseName("userdata/ComicList.comic")
        query = QSqlQuery(sql)
        if sql.open():
            if 'comics' not in sql.tables():
                query.exec("""
                    CREATE TABLE IF NOT EXISTS comics(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        list_name text NOT NULL,
                        comic_name text NOT NULL,
                        comic_path text NOT NULL,
                        cover_path text NOT NULL,
                        collected INTEGER DEFAULT 0,
                        pages INTEGER DEFAULT 0,
                        read_pages INTEGER DEFAULT 0
                    )
                """)
            if 'list_name' not in sql.tables():
                query.exec("""
                    CREATE TABLE IF NOT EXISTS list_name(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name text NOT NULL
                    )
                """)

            print("LBottom init_list: 打开成功")
            q = QSqlQuery(sql)
            q.exec("SELECT * FROM list_name")
            while q.next():
                id_ = q.value("id")
                name = q.value("name")
                comic_list_item = LBottomItem(name, self.shelf, True, None)
                print('LBottom init_list: ', (name, id_))
                self.verticalLayout_2.insertWidget(self.verticalLayout_2.count()-1, comic_list_item)
            sql.close()
        else:
            print("LBottom init_list: 打开失败")
        # query = QSqlQuery(sql)
        # query.exec()

    def create_list(self):
        self.create_list_window.show()

    def delete_list(self):
        for item in self.scrollAreaWidgetContents_LBottom.children():
            if item.objectName() == "Form":
                if item.selected:
                    if not item.is_change_able:
                        return
                    msg_box = QMessageBox()
                    msg_box.setIcon(QMessageBox.Icon.Warning)  # 设置图标类型
                    msg_box.setWindowTitle("删除")
                    msg_box.setWindowIcon(QIcon("resource/delete_black.png"))
                    msg_box.setText(f"确定删除阅读列表：{item.list_name} 吗？")  # 设置显示的文本
                    msg_box.addButton("确定", QMessageBox.ButtonRole.AcceptRole)  # 2
                    msg_box.addButton("取消", QMessageBox.ButtonRole.AcceptRole)  # 3
                    # 显示消息框并获取用户的选择
                    retval = msg_box.exec()
                    if retval == 2:
                        delete_comic_list(item.list_name)
                        item.deleteLater()
                        self.shelf.findChild(QWidget, "RightArea").clear()

    def rename_list(self):
        r_item = None
        for item in self.scrollAreaWidgetContents_LBottom.children():
            if item.objectName() == "Form":
                if item.selected:
                    r_item = item
                    break
        if not r_item:
            return
        self.rename_ui.old_name = r_item.list_name
        self.rename_ui.rename_item = r_item
        self.rename_ui.label_oldname.setText(r_item.list_name)
        self.rename_ui.show()
        print("LBottom rename_list: name", r_item.list_name)
        pass


class LBottomItem(QWidget, part3_Item.Ui_Form):
    def __init__(self, list_name, shelf, is_change_able, label):
        super().__init__()
        self.setupUi(self)
        self.list_name = list_name
        self.is_change_able = is_change_able
        pixmap = QPixmap(label if label else "resource/标签_white.png")  # 替换为你的图片文件路径
        self.pushButton_3.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.pushButton_3.customContextMenuRequested.connect(self.set_menu)
        # 设置 QLabel 的 pixmap
        self.label.setPixmap(pixmap)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.selected = False  # 判断是否被选中
        # 调整 QLabel 的大小以适应图片的大小
        self.label.setScaledContents(True)
        self.label_2.setText(list_name)
        self.shelf = shelf
        self.item_type = "list"
        self.pushButton_3.setIcon(QIcon("resource/setting_white.png"))
        self.pushButton_3.setDisabled(True)
        self.pushButton_3.setVisible(False)
        self.setStyleSheet("color:white")
        self.objectName()
        self.r_UI = RenameUI(self.list_name, self)
        self.setStyleSheet("""
            QWidget{border:0;}
            QLabel{color:white;border:0;} 
            QPushButton{border:0;}
        """)

        # 释放鼠标当前Item后更新样式

    def mouseReleaseEvent(self, event: PySide6.QtGui.QMouseEvent) -> None:
        if event.button() != Qt.MouseButton.LeftButton:
            return
        for item in self.shelf.findChild(QWidget, "scrollAreaWidgetContents_LTop").children():
            if item.objectName() == "Form":
                item.setStyleSheet("""
                        QWidget{border:0;}
                        QLabel{color:white;border:0;} 
                        QPushButton{border:0;}
                    """)
                item.pushButton_3.setDisabled(True)
                item.pushButton_3.setVisible(False)
                item.selected = False
        for item in self.shelf.findChild(QWidget, "widget_2").children():
            if item.objectName() == "Form":
                item.setStyleSheet("""
                        QWidget{border:0;}
                        QLabel{color:white;border:0;} 
                        QPushButton{border:0;}
                    """)
                item.pushButton.setDisabled(True)
                item.pushButton.setVisible(False)
                item.selected = False

        for item in self.parent().children():
            if item.objectName() == "Form":
                item.setStyleSheet("""
                                QWidget{border:0;}
                                QLabel{color:white;border:0;} 
                                QPushButton{border:0;}
                            """)
                item.pushButton_3.setDisabled(True)
                item.pushButton_3.setVisible(False)
                item.selected = False
        self.setStyleSheet("""
                    QWidget{background-color: rgba(255, 255, 255, 0.1);border:0;}
                    QLabel{background-color: rgba(255, 255, 255, 0);color:white;border:0;} 
                    QPushButton{background-color: rgba(255, 255, 255, 0);border:0;}
                """)
        if self.is_change_able:
            self.pushButton_3.setDisabled(False)
            self.pushButton_3.setVisible(True)
        self.selected = True
        self.shelf.selected_item = self
        super().mouseReleaseEvent(event)

        # 点击当前Item后

    def mousePressEvent(self, event: PySide6.QtGui.QMouseEvent = None):
        # print(self.l_id, self.library_path, self.library_name)
        if event.button() != Qt.MouseButton.LeftButton:
            return
        sql = QSqlDatabase("QSQLITE")
        sql.setDatabaseName("userdata/ComicList.comic")
        info_list = []
        if sql.open():
            print("LBottom mousePressEvent: 打开成功")
            query = QSqlQuery(sql)
            sub_query = " and collected=1" if self.list_name == '收藏' else ""
            query.exec(f"""
                SELECT list_name,comic_name,comic_path,cover_path,collected,pages,read_pages 
                FROM comics 
                WHERE list_name='{self.list_name}'{sub_query}
            """)
            while query.next():
                list_name = query.value("list_name")
                comic_name = query.value("comic_name")
                comic_path = query.value("comic_path")
                cover_path = query.value("cover_path")
                collected = query.value("collected")
                pages = query.value("pages")
                read_pages = query.value("read_pages")
                info_list.append([list_name, comic_name, comic_path, cover_path, collected, pages, read_pages])
            self.shelf.findChild(QWidget, "RightArea").libraryPath = None
            self.shelf.findChild(QWidget, 'LMidMenu').clear_item()
            self.shelf.findChild(QWidget, "RightArea").set_previews(info_list, preview_index=3)

            sql.close()
        else:
            print("LBottom mousePressEvent: 打开失败")

    def set_menu(self, position):  # 弹出子菜单
        menu = QMenu(self)
        menu.setStyleSheet("color:white;background-color: rgba(0, 0, 0,0.9);")
        delete_action = QAction('删除', self)
        delete_action.setIcon(QIcon("resource/delete_black.png"))
        delete_action.triggered.connect(self.delete_self)
        rename_action = QAction('重命名', self)
        rename_action.setIcon(QIcon("resource/Edit_black.png"))
        rename_action.triggered.connect(self.rename_self)
        menu.addAction(delete_action)
        menu.addAction(rename_action)
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
        menu.exec(self.pushButton_3.mapToGlobal(position))

    def delete_self(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Warning)  # 设置图标类型
        msg_box.setWindowTitle("删除")
        msg_box.setWindowIcon(QIcon("resource/delete_black.png"))
        msg_box.setText(f"确定删除阅读列表：{self.list_name} 吗？")  # 设置显示的文本
        msg_box.addButton("确定", QMessageBox.ButtonRole.AcceptRole)  # 2
        msg_box.addButton("取消", QMessageBox.ButtonRole.AcceptRole)  # 3
        # 显示消息框并获取用户的选择
        retval = msg_box.exec()
        if retval == 2:
            delete_comic_list(self.list_name)
            self.deleteLater()
            self.shelf.findChild(QWidget, "RightArea").clear()

    def rename_self(self):
        self.r_UI.show()
        pass


# 重命名库子界面
class RenameUI(QWidget, rename_list_ui.Ui_Form):
    def __init__(self, old_name, rename_item):
        super().__init__()
        self.setupUi(self)
        self.rename_item = rename_item
        self.old_name = old_name
        self.setWindowIcon(QIcon("resource/BookShelf.png"))
        self.setWindowTitle("重命名列表")
        self.label_oldname.setText(old_name)
        self.pushButton_rename.clicked.connect(self.rename)
        self.pushButton_cancel.clicked.connect(self.cancel)

    def cancel(self):
        self.hide()
        self.lineEdit_newname.setText("")

    def rename(self):
        new_name = self.lineEdit_newname.text()
        if new_name and new_name != self.old_name:
            if rename_list(new_name, self.old_name):
                self.rename_item.label_2.setText(new_name)
                self.rename_item.list_name = new_name
                self.cancel()
                return
        QMessageBox.critical(self, "info error", "新名称不能为空或重复")

