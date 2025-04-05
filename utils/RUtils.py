from UIParts.part4 import Ui_Form as RArea
from UIParts import part4_pre_Item
from PySide6.QtGui import QMouseEvent
from PySide6.QtCore import QThread, Signal
import zipfile
from utils import *
import os
import math
import time
from 阅读器 import ImageViewer


class LTopPreviewItem(QWidget, part4_pre_Item.Ui_Form):
    def __init__(self, pixmap_cover, comic_name, comic_path, view_width, library_path, library_name, belong_path,
                 read_pages, pages, is_collected=False, show_title=True, right_area=None, cover=None):
        super().__init__()
        self.setupUi(self)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.set_menu)
        self.setToolTip(f'所属库:{library_name}\n漫画名:{comic_name[:-4]}\n文件夹:{belong_path}')
        self.setObjectName("preview_cover_container")
        self.view_width = view_width  # 预览宽度
        self.view_height = int(view_width * 1.4)  # 预览高度
        self.shelf_right_area = right_area  # 书柜右边展示区域
        self.library_path = library_path  # 漫画归属库
        self.library_name = library_name  # 漫画归属库名
        self.belong_path = belong_path  # 漫画归属文件夹
        self.is_collected = is_collected  # 判断是否收藏了漫画
        self.comic_name = comic_name  # 漫画名称
        self.comic_path = comic_path  # 漫画路径
        self.cover_path = cover  # 漫画封面路径
        self.pages = pages
        self.read_pages = read_pages
        self.textEdit_comic_name.setVisible(show_title)
        self.textEdit_comic_name.setText(self.comic_name[:-4])
        self.textEdit_comic_name.setFont(QFont("Arial", 10))
        self.textEdit_comic_name.setStyleSheet("color:white;")
        self.mark_size = 30  # 收藏标志大小
        self.mark_label = QLabel(self)
        self.mark_label.setCursor(Qt.CursorShape.PointingHandCursor)
        self.mark_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mark_label.setGeometry(self.view_width - 35, 5, self.mark_size, self.mark_size)
        self.mark_label.mousePressEvent = self.click_mark  # 点击（取消）收藏事件
        self.mark_label.setStyleSheet("background-color: transparent;")
        self.mark_label.setScaledContents(True)
        self.check_box = QCheckBox(self)
        self.check_box.setGeometry(15, 5, 30, 30)
        self.check_box.setFixedSize(30, 30)
        self.check_box.setVisible(False)
        self.check_box.setStyleSheet("background-color: transparent;width:30px;height:30x;")
        self.pixmap_collect = QPixmap("resource/heart_red.png")  # 已收藏图标
        self.pixmap_dis_collect = QPixmap("resource/heart_white.png")  # 未收藏图标
        self.mark_label.setPixmap(self.pixmap_collect if self.is_collected else self.pixmap_dis_collect)  # 设置收藏图标
        if show_title:
            self.setFixedSize(self.view_width,
                              self.view_height + self.textEdit_comic_name.height() + self.progressBar.height())  # 预览图片宽高度设置
        else:
            self.setFixedSize(self.view_width,
                              self.view_height + self.progressBar.height())  # 预览图片宽高度设置

        self.progressBar.setStyleSheet("""
            QProgressBar {
                border: 0px solid grey;
                background-color:transparent;
            }
            QProgressBar::chunk {
                background-color: #05B8CC;  /* 进度条块的颜色 */
                width: 5px;  /* 进度块的宽度 */
                border-radius: 10px;
            }
        """)
        try:
            self.progressBar.setValue(int(100*read_pages/pages))
        except:
            self.progressBar.setValue(0)
        self.set_cover(pixmap_cover, recent=True)

    def set_cover(self, pixmap_cover=None, recent=False):
        if pixmap_cover and recent:
            self.xxx(pixmap_cover)
        if not pixmap_cover and not recent:
            self.xxx(QPixmap(self.cover_path))

    def xxx(self, pixmap_cover):
        if pixmap_cover.height() / pixmap_cover.width() >= 2:
            self.book_cover.setScaledContents(False)
            self.book_cover.setPixmap(pixmap_cover.scaledToWidth(self.view_width,
                                                                 Qt.TransformationMode.SmoothTransformation))
        elif pixmap_cover.height() / pixmap_cover.width() < 0.5:
            self.book_cover.setScaledContents(False)
            self.book_cover.setPixmap(pixmap_cover.scaledToHeight(self.view_height,
                                                                  Qt.TransformationMode.SmoothTransformation))
        else:
            self.book_cover.setScaledContents(True)
            self.book_cover.setPixmap(pixmap_cover)

    def click_mark(self, event):
        print(self.is_collected)
        self.cancel_or_collect()
        super().mousePressEvent(event)

    def cancel_or_collect(self):
        self.is_collected = False if self.is_collected else True
        print("self.is_collected: ", int(self.is_collected))
        self.mark_label.setPixmap(self.pixmap_collect if self.is_collected else self.pixmap_dis_collect)
        # 数据库操作：
        query = f"""
            UPDATE comics SET collected={int(self.is_collected)}
            WHERE library_name='{self.library_name}' and library_path='{self.library_path}'
            and belong_path='{self.belong_path}' and name='{self.comic_name}'
        """
        database_operate(query, replace_path(os.path.join(self.library_path, ".library/comics.comic")))
        qsl_db = QSqlDatabase("QSQLITE")
        qsl_db.setDatabaseName("userdata/ComicList.comic")
        qsl_db.open()
        q = QSqlQuery(qsl_db)
        if not q.exec(f"""
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
        """):
            print(q.lastError())
        query_search = f"""
            SELECT * FROM comics
            WHERE comic_path='{self.comic_path}' and list_name='收藏'
        """
        q.prepare(query_search)
        if q.exec():
            if q.next():
                q.exec(f"""
                    UPDATE comics SET collected={int(self.is_collected)}
                    WHERE comic_path='{self.comic_path}'
                """)
            else:
                print("添加到收藏")
                self.add_to_list(list_name='收藏')
        qsl_db.close()

    # 双击事件
    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        print(f"you clicked me {self.comic_path} : {self.comic_name}")
        self.read_self()
        super().mouseDoubleClickEvent(event)

    def set_menu(self, position):  # 弹出子菜单
        menu = QMenu(self)
        delete_action = QAction('删除', self)
        delete_action.setIcon(QIcon("resource/delete_black.png"))
        delete_action.triggered.connect(self.delete_self)

        select_action = QAction('取消选中' if self.check_box.isChecked() else "选中", self)
        select_action.setIcon(QIcon("resource/check_unselect_black.png") if self.check_box.isChecked()
                              else QIcon("resource/select2_fill_black.png"))
        select_action.triggered.connect(self.select_self)

        open_action = QAction('在阅读器中打开', self)
        open_action.triggered.connect(self.read_self)
        open_action.setIcon(QIcon("resource/reading_black.png"))

        collect_action = QAction('取消收藏' if self.is_collected else "收藏", self)
        collect_action.setIcon(QIcon("resource/heart_red.png") if not self.is_collected
                               else QIcon("resource/heart_black.png"))
        collect_action.triggered.connect(self.collect_self)

        add_to_action = QAction('添加到列表', self)
        add_to_action.setIcon(QIcon("resource/添加到列表_black.png"))
        add_to_action.setMenu(self.get_sub_menu())

        copy_path_action = QAction('复制路径', self)
        copy_path_action.setIcon(QIcon("resource/复制_black.png"))
        copy_path_action.triggered.connect(self.copy_path)

        layout = QVBoxLayout()
        layout.setContentsMargins(6, 0, 0, 0)
        menu.setLayout(layout)

        menu.addAction(delete_action)
        menu.addAction(select_action)
        menu.addAction(collect_action)
        menu.addAction(add_to_action)
        menu.addAction(open_action)
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
        # print(position) ： 相对点击的位置
        menu.exec(self.mapToGlobal(position))

    def delete_self(self):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Warning)  # 设置图标类型
        msg_box.setWindowTitle("删除漫画")
        msg_box.setWindowIcon(QIcon("resource/delete_black.png"))
        msg_box.setText("(1) 从列表中删除\n(2) 从磁盘中删除")  # 设置显示的文本
        msg_box.addButton("(1)", QMessageBox.ButtonRole.AcceptRole)
        msg_box.addButton("(2)", QMessageBox.ButtonRole.AcceptRole)
        msg_box.addButton("取消", QMessageBox.ButtonRole.AcceptRole)

        # 显示消息框并获取用户的选择
        retval = msg_box.exec()
        print(retval)
        if retval == 2:  # delete from list
            query_delete = f"""DELETE FROM comics 
                WHERE belong_path='{self.belong_path}' and 
                name='{self.comic_name}' and 
                library_path='{self.library_path}' and 
                library_name='{self.library_name}'"""
            query_search = f"""
                SELECT COUNT(cover), cover FROM comics 
                WHERE belong_path='{self.belong_path}' and name='{self.comic_name}'"""
            db = QSqlDatabase("QSQLITE")
            db.setDatabaseName(replace_path(os.path.join(self.library_path, ".library/comics.comic")))
            db.open()
            query = QSqlQuery(db)
            query.prepare(query_search)
            query.exec()
            if query.next():
                cover = query.value(1)
                number = query.value(0)
                print(f"数量：{number}，cover：{cover}")
                if number <= 1:
                    print(f"删除封面：{cover}")
                    os.remove(cover)

                if query.exec(query_delete):
                    print(f"从列表删除成功\n{query_delete}")
                    db.close()
                    self.shelf_right_area.preview_list_label.pop(self.comic_path)
                    self.shelf_right_area.show_Ltop_previews()
                    self.deleteLater()

        elif retval == 3:  # delete from disk
            query_delete = f"""DELETE FROM comics 
                            WHERE belong_path='{self.belong_path}' and 
                            name='{self.comic_name}'"""
            query_search = f"""
                            SELECT DISTINCT cover FROM comics 
                            WHERE belong_path='{self.belong_path}' and name='{self.comic_name}'"""
            db = QSqlDatabase("QSQLITE")
            db.setDatabaseName(replace_path(os.path.join(self.library_path, ".library/comics.comic")))
            db.open()
            query = QSqlQuery(db)
            query.prepare(query_search)
            query.exec()
            while query.next():
                cover = query.value(0)
                print(f"从磁盘删除成功：\n封面 {cover}")
                # os.remove(cover)
                # os.remove(os.path.join(self.belong_path, self.comic_name))
            if query.exec(query_delete):
                print(f"漫画：{os.path.join(self.belong_path, self.comic_name)}")
                self.shelf_right_area.preview_list_label.pop(self.comic_path)
                self.shelf_right_area.show_Ltop_previews()
                self.deleteLater()
            pass
        elif retval == 4:
            print("cancel")
        else:
            pass

    def select_self(self):
        if self.check_box.isChecked():
            self.check_box.setVisible(False)
            self.check_box.setChecked(False)
        else:
            self.check_box.setVisible(True)
            self.check_box.setChecked(True)
        pass

    def get_sub_menu(self):
        sub_menu = QMenu("子菜单", self)
        sub_menu.setStyleSheet("""
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
        # 向子菜单中添加一些动作
        # list_name = get_list_names()
        list_name = get_list_names_except_added_list(self.comic_path)
        for l_name in list_name:
            q_a = QAction(l_name, self)
            q_a.setIcon(QIcon("resource/标签_black.png"))
            q_a.triggered.connect(self.add_to_list)
            sub_menu.addAction(q_a)
        # 将子菜单设置为action的子菜单
        return sub_menu

    # 将漫画添加到阅读列表
    def add_to_list(self, list_name=None):
        if list_name:
            insert_info_to_comic_list('收藏', self.comic_name,
                                      self.comic_path, self.cover_path,
                                      self.is_collected, self.pages, self.read_pages)
        else:
            insert_info_to_comic_list(self.sender().text(), self.comic_name,
                                      self.comic_path, self.cover_path,
                                      self.is_collected, self.pages, self.read_pages)

    def read_self(self):
        viewer = ImageViewer(load_last=False)
        viewer.load_old_comic(self.comic_path, self.library_name, self.library_path, self.comic_name, self.belong_path)
        # viewer.show()
        pass

    def collect_self(self):
        self.cancel_or_collect()
        pass

    def copy_path(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.comic_path)


class LBottomPreviewItem(QWidget, part4_pre_Item.Ui_Form):
    def __init__(self, list_name, pixmap_cover, comic_name, comic_path, view_width, read_pages, pages, is_collected=False, show_title=True, right_area=None, cover_path=None):
        super().__init__()
        self.setupUi(self)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.set_menu)
        self.setToolTip(f'列表名:{list_name}\n漫画名:{comic_name[:-4]}\n路径：{comic_path}')
        self.setObjectName("preview_cover_container")
        self.view_width = view_width  # 预览宽度
        self.view_height = int(view_width * 1.4)  # 预览高度
        self.shelf_right_area = right_area  # 书柜右边展示区域
        self.is_collected = is_collected  # 判断是否收藏了漫画
        self.comic_name = comic_name  # 漫画名称
        self.comic_path = comic_path  # 漫画路径
        self.cover_path = cover_path
        self.list_name = list_name
        self.textEdit_comic_name.setVisible(show_title)
        self.textEdit_comic_name.setText(self.comic_name[:-4])
        self.textEdit_comic_name.setFont(QFont("Arial", 10))
        self.textEdit_comic_name.setStyleSheet("color:white;")
        self.mark_size = 30  # 收藏标志大小
        self.mark_label = QLabel(self)
        self.mark_label.setCursor(Qt.CursorShape.PointingHandCursor)
        self.mark_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mark_label.setGeometry(self.view_width - 35, 5, self.mark_size, self.mark_size)
        self.mark_label.setStyleSheet("background-color: transparent;")
        self.mark_label.setScaledContents(True)
        self.check_box = QCheckBox(self)
        self.check_box.setGeometry(15, 5, 30, 30)
        self.check_box.setFixedSize(30, 30)
        self.check_box.setVisible(False)
        self.check_box.setStyleSheet("background-color: transparent;width:30px;height:30x;")
        self.pixmap_collect = QPixmap("resource/heart_red.png")  # 已收藏图标
        self.pixmap_dis_collect = QPixmap("resource/heart_white.png")  # 未收藏图标
        self.mark_label.setPixmap(self.pixmap_collect if self.is_collected else self.pixmap_dis_collect)  # 设置收藏图标
        if show_title:
            self.setFixedSize(self.view_width,
                              self.view_height + self.textEdit_comic_name.height() + self.progressBar.height())  # 预览图片宽高度设置
        else:
            self.setFixedSize(self.view_width,
                              self.view_height + self.progressBar.height())  # 预览图片宽高度设置

        self.progressBar.setStyleSheet("""
            QProgressBar {
                border: 0px solid grey;
                background-color:transparent;
            }
            QProgressBar::chunk {
                background-color: #05B8CC;  /* 进度条块的颜色 */
                width: 5px;  /* 进度块的宽度 */
                border-radius: 10px;
            }
        """)
        try:
            self.progressBar.setValue(int(100*read_pages/pages))
        except:
            self.progressBar.setValue(0)

        self.set_cover(pixmap_cover, recent=True)

    def set_cover(self, pixmap_cover=None, recent=False):
        if pixmap_cover and recent:
            self.xxx(pixmap_cover)
        if not pixmap_cover and not recent:
            self.xxx(QPixmap(self.cover_path))

    def xxx(self, pixmap_cover):
        if pixmap_cover.height() / pixmap_cover.width() >= 2:
            self.book_cover.setScaledContents(False)
            self.book_cover.setPixmap(pixmap_cover.scaledToWidth(self.view_width,
                                                                 Qt.TransformationMode.SmoothTransformation))
        elif pixmap_cover.height() / pixmap_cover.width() < 0.5:
            self.book_cover.setScaledContents(False)
            self.book_cover.setPixmap(pixmap_cover.scaledToHeight(self.view_height,
                                                                  Qt.TransformationMode.SmoothTransformation))
        else:
            self.book_cover.setScaledContents(True)
            self.book_cover.setPixmap(pixmap_cover)

    # 双击事件
    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        print(f"RUtils mouseDoubleClickEvent：you clicked me {self.comic_path} : {self.comic_name}")
        self.read_self()
        super().mouseDoubleClickEvent(event)

    def set_menu(self, position):  # 弹出子菜单
        menu = QMenu(self)
        delete_action = QAction('删除', self)
        delete_action.setIcon(QIcon("resource/delete_black.png"))
        delete_action.triggered.connect(self.delete_self)

        select_action = QAction('取消选中' if self.check_box.isChecked() else "选中", self)
        select_action.setIcon(QIcon("resource/check_unselect_black.png") if self.check_box.isChecked()
                              else QIcon("resource/select2_fill_black.png"))
        select_action.triggered.connect(self.select_self)

        open_action = QAction('在阅读器中打开', self)
        open_action.triggered.connect(self.read_self)
        open_action.setIcon(QIcon("resource/reading_black.png"))

        copy_path_action = QAction('复制路径', self)
        copy_path_action.setIcon(QIcon("resource/复制_black.png"))
        copy_path_action.triggered.connect(self.copy_path)
        layout = QVBoxLayout()
        layout.setContentsMargins(6, 0, 0, 0)
        menu.setLayout(layout)

        menu.addAction(delete_action)
        menu.addAction(select_action)
        menu.addAction(open_action)
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
        # print(position) ： 相对点击的位置
        menu.exec(self.mapToGlobal(position))

    def select_self(self):
        if self.check_box.isChecked():
            self.check_box.setVisible(False)
            self.check_box.setChecked(False)
        else:
            self.check_box.setVisible(True)
            self.check_box.setChecked(True)
        pass

    def read_self(self):
        print_or_not(f"RUtils -> LBottomPreviewItem -> def read_self(self):{self.comic_path}")
        viewer = ImageViewer(load_last=False)
        viewer.load_old_comic(self.comic_path, self.comic_name)
        # viewer.show()
        pass

    def delete_self(self):
        print_or_not(f"RUtils -> LBottomPreviewItem -> def read_self(self):{self.comic_path}")
        db = "userdata/ComicList.comic"
        query = f"DELETE FROM comics WHERE comic_path='{self.comic_path}' AND list_name='{self.list_name}'"
        if database_operate(query, db):
            self.deleteLater()
        pass

    def copy_path(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.comic_path)


class RightArea(QWidget, RArea):
    def __init__(self, shelf):
        super().__init__()
        self.setupUi(self)
        self.shelf = shelf
        self.setObjectName("RightArea")
        self.setStyleSheet("""
            QToolTip{color:white;background-color: #4D4849;}
            QWidget{background-color: #4D4849;}
            #pushButton_select, 
            #pushButton_collect, 
            #pushButton_delete{color: gray; background-color: #616161; border-radio:5px;}
            #pushButton_select:hover, 
            #pushButton_collect:hover, 
            #pushButton_delete:hover {color: white; background-color: #7A7A7A; }
            #scrollAreaWidgetContents{border:0;}
            #operates{border-bottom: 1px solid gray;}
            #viewtools{border-top: 1px solid gray;}
            #widget_recent{border-bottom: 1px solid gray;}
        """)
        self.bookcontainer.setStyleSheet("""
            QScrollArea { border:0;background-color: transparent; }
            QScrollBar:vertical { background-color: transparent; width:6px;}
            QScrollBar::handle:vertical { background-color: #D8D8D8; border-radius: 2px; }
            QScrollBar::add-line:vertical, 
            QScrollBar::sub-line:vertical { background-color: transparent; height: 0px; }
            QScrollBar::add-page:vertical, 
            QScrollBar::sub-page:vertical { background-color: transparent; }
        """)
        self.scrollArea.setStyleSheet("""
            QScrollBar:horizontal { background-color: transparent; height:10px;}
            QScrollBar::handle:horizontal { background-color: #D8D8D8; border-radius: 2px; }
            QScrollBar::add-line:horizontal, 
            QScrollBar::sub-line:horizontal { background-color: transparent;}
            QScrollBar::add-page:horizontal, 
            QScrollBar::sub-page:horizontal { background-color: transparent; }
        """)
        self.pushButton_small.setIcon(QIcon("resource/等宽排列_white_.png"))
        self.pushButton_big.setIcon(QIcon("resource/排列切换_white_.png"))
        self.pushButton_small.setToolTip("最小预览")
        self.pushButton_big.setToolTip("最大预览")
        self.pushButton_small.clicked.connect(self.smallest)
        self.pushButton_big.clicked.connect(self.biggest)
        self.pushButton_delete.setVisible(False)
        self.pushButton_collect.setVisible(False)
        self.cover_path = r"D:\Data\comics\.library\covers"
        self.preview_list_label = []                # 存储预览展示的所有comic
        self.preview_dir_list_label = []            # 存储预览选择文件夹中所有的comic
        self.current_preview_list_label = []        # 存储当前要预览的comic
        self.searching_preview_list_label = []      # 存储搜索的comic
        self.libraryPath = ""
        # self.recent_preview_layout = QHBoxLayout(self.widget_recent)
        self.preview_layout = QGridLayout(self.widget_comics)
        self.preview_layout.setContentsMargins(3, 3, 3, 3)
        self.horizontalSlider.valueChanged.connect(self.view_size_change)
        self.start_rows = 0                             # 当前窗口展示的封面的第一行
        self.end_rows = 1                               # 当前窗口展示的封面的最后一行
        self.preview_width = 150                        # 根据view_size_level 和base_preview_width 设置当前预览封面大小
        self.base_preview_width = 150                   # 预览基础大小--不变值
        self.view_size_level = 0                        # 用来设置预览封面的大小的等级
        self.columns = 0                                # 用来设置gridlayout的列数
        self.preview_index = 0                          # 用来标记是哪一个部分的展示预览：LTop、LBottom、LMid
        self.max_page = 0                               # 最大分页数
        self.current_page = 1                           # 当前所在页
        self.page_covers_numb = 40                      # 每页预览数量，默认40
        self.resize_timer = QTimer(self)
        self.resize_timer.setSingleShot(True)
        self.resize_timer.timeout.connect(self.reset_view_size)
        self.slider_value_timer = QTimer(self)
        self.slider_value_timer.setSingleShot(True)
        self.slider_value_timer.timeout.connect(self.view_change_reset_view_size)
        self.pushButton_select.clicked.connect(self.get_font)
        self.pushButton_search.setIcon(QIcon("resource/search_white.png"))
        self.pushButton_search.setToolTip("搜索当前库/文件夹/列表")
        self.pushButton_search.clicked.connect(self.search_comics_from_selected_item)
        self.pushButton_search_all.setIcon(QIcon("resource/全局搜索_white.png"))
        self.pushButton_search_all.setToolTip("搜索全库")
        self.pushButton_search_all.clicked.connect(self.search_comics_from_all_library)
        self.lineEdit_search.setStyleSheet("color:#B8ACB0;")
        self.pushButton_first_page.clicked.connect(self.go_to_first_page)
        self.pushButton_first_page.setIcon(QIcon('resource/first_page.png'))
        self.pushButton_first_page.setToolTip('首页')
        self.pushButton_last_page.clicked.connect(self.go_to_last_page)
        self.pushButton_last_page.setIcon(QIcon('resource/last_page.png'))
        self.pushButton_last_page.setToolTip('尾页')
        self.pushButton_next_page.clicked.connect(self.go_to_next_page)
        self.pushButton_pre_page.clicked.connect(self.go_to_pre_page)
        self.pushButton_jump_page.clicked.connect(self.jump_to_page)

        self.spinBox_page_numb.valueChanged.connect(self.reset_page_numbs)
        self.spinBox_page_numb.setValue(self.page_covers_numb)
        self.spinBox_page_index.dragEnterEvent = self.jump_to_page

        self.set_current_preview_timer = QTimer(self)
        self.set_current_preview_timer.setSingleShot(True)
        self.set_current_preview_timer.timeout.connect(lambda: self.set_page_preview(self.current_page))
        self.scrollArea.horizontalScrollBar().setCursor(Qt.CursorShape.SizeHorCursor)

    def reset_page_numbs(self):
        # print(self.page_covers_numb)
        self.page_covers_numb = self.spinBox_page_numb.value()
        self.max_page = math.ceil(len(self.current_preview_list_label) / self.page_covers_numb)
        self.spinBox_page_index.setMaximum(self.max_page)
        if self.preview_index == 1:
            self.show_Ltop_previews()
        elif self.preview_index == 3:
            self.show_LBottom_previews()
        self.spinBox_page_numb.clearFocus()

    def jump_to_page(self):
        page = self.spinBox_page_index.value()
        if page < 1 or page > self.max_page:
            self.spinBox_page_index.setValue(self.current_page)
            return
        self.current_page = page
        self.set_page_preview(self.current_page)
        self.spinBox_page_index.clearFocus()

    def go_to_first_page(self):
        if self.current_page == 1:
            return
        self.current_page = 1
        self.set_page_preview(self.current_page)

    def go_to_last_page(self):
        if self.current_page == self.max_page:
            return
        self.current_page = self.max_page
        self.set_page_preview(self.max_page)

    def go_to_next_page(self):
        self.current_page += 1
        if self.current_page > self.max_page:
            self.current_page = self.max_page
            return
        self.spinBox_page_index.setValue(self.current_page)
        if not self.set_current_preview_timer.isActive():
            self.set_current_preview_timer.start(100)
        # self.set_page_preview(self.current_page)

    def go_to_pre_page(self):
        self.current_page -= 1
        if self.current_page < 1:
            self.current_page = 1
            return
        self.spinBox_page_index.setValue(self.current_page)
        if not self.set_current_preview_timer.isActive():
            self.set_current_preview_timer.start(100)
        # self.set_page_preview(self.current_page)

    def get_font(self):
        font, _ = QFontDialog.getFont()
        if font:
            self.setFont(font)

    def smallest(self):
        self.horizontalSlider.setValue(0)

    def biggest(self):
        self.horizontalSlider.setValue(self.horizontalSlider.maximum())

    def set_dir_previews(self, dir_name, library_name):
        self.preview_dir_list_label = []
        for c in self.preview_list_label:
            if c[4] == library_name and dir_name == os.path.basename(c[5]):
                self.preview_dir_list_label.append(c)
        self.current_preview_list_label = self.preview_dir_list_label
        self.max_page = math.ceil(len(self.current_preview_list_label)/self.page_covers_numb)
        self.spinBox_page_index.setMaximum(self.max_page)
        self.spinBox_page_index.setValue(self.current_page)
        self.show_Ltop_previews()

    # 重新阅览当前library所有comic
    def show_root_library(self):
        if self.preview_index != 1:
            return
        if self.preview_list_label:
            self.current_preview_list_label = self.preview_list_label
            self.max_page = math.ceil(len(self.current_preview_list_label) / self.page_covers_numb)
            self.spinBox_page_index.setMaximum(self.max_page)
            self.spinBox_page_index.setValue(self.current_page)
            self.show_Ltop_previews()

    def set_previews(self, cover_list, preview_index):
        self.preview_index = preview_index
        # cover_[comic_path, name, collected, library_path, library_name, belong_path, read_pages, pages, cover]
        self.preview_list_label = []
        start = time.time()
        if preview_index == 1:
            for cover_ in cover_list:
                if os.path.exists(cover_[0]):
                    if os.path.exists(cover_[2]):
                        # if '協議換愛(無碼版) 1-30話' in cover_[0]:
                        #     print(cover_[2])
                        cover = cover_[2]
                    else:
                        cover = 'resource/图片加载失败_white.png'
                    self.preview_list_label.append([cover_[0], cover_[1], cover_[3], cover_[4],
                                                    cover_[5], cover_[6], cover_[7], cover_[8], cover])
            end = time.time()
            print("RUtils set_previews: set_previews：1 设置labels耗时：", end-start)
            self.current_preview_list_label = self.preview_list_label
            self.max_page = math.ceil(len(self.current_preview_list_label)/self.page_covers_numb)
            self.show_Ltop_previews()
        elif preview_index == 3:
            # [list_name, comic_name, comic_path, cover_path, collected, pages, read_pages]
            for cover_ in cover_list:
                if os.path.exists(cover_[2]):
                    if os.path.exists(cover_[3]):
                        cover = cover_[3]
                    else:
                        cover = 'resource/图片加载失败_white.png'
                    self.preview_list_label.append([cover_[0], cover_[1], cover_[2], cover,
                                                    cover_[4], cover_[5], cover_[6]])
            end = time.time()
            print("RUtils set_previews: set_previews：3 设置labels耗时：", end-start)
            self.current_preview_list_label = self.preview_list_label
            self.max_page = math.ceil(len(self.current_preview_list_label)/self.page_covers_numb)
            self.show_LBottom_previews()
        self.spinBox_page_index.setMaximum(self.max_page)
        self.spinBox_page_index.setValue(self.current_page)

    def act_set_current_preview_timer(self):
        if not self.set_current_preview_timer.isActive():
            self.set_current_preview_timer.start(100)

    # 设置当前页面应该展示的封面
    def set_page_preview(self, page, is_search_dir=False):
        num = 0
        self.spinBox_page_index.setValue(self.current_page)
        self.clear(clear_recent=False)
        print(f'RUtils set_page_preview: 总数{len(self.current_preview_list_label)} {self.max_page}')
        if not len(self.current_preview_list_label):
            return
        for i in range(self.page_covers_numb * (page - 1), self.page_covers_numb * page):
            if self.preview_index == 1 and not is_search_dir:
                comic_path, comic_name, collected, library_path, library_name, \
                    belong_path, read_pages, pages, cover = self.current_preview_list_label[i]
                book = LTopPreviewItem(QPixmap(cover), comic_name, comic_path, self.preview_width, library_path,
                                       library_name, belong_path, read_pages, pages, collected, True, self, cover)
                self.preview_layout.addWidget(book, num // self.columns, num % self.columns,
                                              alignment=Qt.AlignmentFlag.AlignVCenter)
                num += 1
                if i+1 >= len(self.current_preview_list_label):
                    print(f'RUtils set_page_preview: 当前第{page}页，共{num}本漫画，分页数：{self.page_covers_numb}')
                    return

            elif self.preview_index == 1 and is_search_dir:
                if not len(self.searching_preview_list_label):
                    return
                comic_path, comic_name, collected, library_path, library_name, \
                    belong_path, read_pages, pages, cover = self.searching_preview_list_label[i]
                book = LTopPreviewItem(QPixmap(cover), comic_name, comic_path, self.preview_width, library_path,
                                       library_name, belong_path, read_pages, pages, collected, True, self, cover)
                self.preview_layout.addWidget(book, num // self.columns, num % self.columns,
                                              alignment=Qt.AlignmentFlag.AlignVCenter)
                num += 1
                if i + 1 >= len(self.searching_preview_list_label):
                    print(f'RUtils set_page_preview: 当前第{page}页，共{num}本漫画，分页数：{self.page_covers_numb}')
                    return

            elif self.preview_index == 3:
                list_name, comic_name, comic_path, cover, collected, pages, \
                    read_pages = self.current_preview_list_label[i]

                book = LBottomPreviewItem(list_name, QPixmap(cover), comic_name, comic_path, self.preview_width,
                                          read_pages, pages, collected, True, self, cover)
                self.preview_layout.addWidget(book, num // self.columns, num % self.columns,
                                              alignment=Qt.AlignmentFlag.AlignVCenter)
                num += 1
                if i+1 >= len(self.current_preview_list_label):
                    print(f'RUtils set_page_preview: 当前第{page}页，共{num}本漫画')
                    return
        print(f'RUtils set_page_preview: 当前第{page}页，共{num}本漫画')

    def show_Ltop_previews(self):
        self.compute_columns()
        # self.preview_layout.columnCount = self.columns
        self.current_page = 1
        self.spinBox_page_index.setValue(self.current_page)
        self.clear()
        self.set_page_preview(self.current_page)
        self.preview_layout.update()
        if not self.preview_list_label:
            return
        start = time.time()
        no_recent_comic = True
        book_remain = None
        for i, (comic_path, comic_name, collected, library_path, library_name, belong_path,
                read_pages, pages, cover) in enumerate(self.current_preview_list_label):
            # PreviewItem(pixmap_cover, book_name, comic_path, view_width, library_path,
            #                                       belong_path, is_collected = False, right_area = None)
            if i == 0:
                book_remain = LTopPreviewItem(QPixmap(cover), comic_name, comic_path, 250, library_path, library_name,
                                              belong_path, read_pages, pages, collected, False, self, cover)
            if read_pages > 0 and read_pages != pages:
                no_recent_comic = False
                book_recent = LTopPreviewItem(QPixmap(cover), comic_name, comic_path, 250, library_path, library_name,
                                              belong_path, read_pages, pages, collected, False, self, cover)
                self.horizontalLayout_recent.insertWidget(self.horizontalLayout_recent.count()-1, book_recent)

        # 如果有“最近阅读”，则删除book_remain， 否则添加到recent预览
        if no_recent_comic and book_remain:
            self.horizontalLayout_recent.insertWidget(self.horizontalLayout_recent.count()-1, book_remain)
        else:
            book_remain.deleteLater() if book_remain else None
        end = time.time()
        print("RUtils show_Ltop_previews: show_previews：加载/更新预览图片耗时：", end - start)

    def show_LBottom_previews(self):
        self.compute_columns()
        # self.preview_layout.columnCount = self.columns
        self.current_page = 1
        self.spinBox_page_index.setValue(self.current_page)
        self.clear()
        self.set_page_preview(self.current_page)
        self.preview_layout.update()
        if not self.current_preview_list_label:
            return
        # self.preview_layout.columnCount = self.columns
        start = time.time()
        no_recent_comic = True
        book_remain = None
        # [list_name, comic_name, comic_path, cover_path, collected]
        for i, (list_name, comic_name, comic_path, cover,
                collected, pages, read_pages) in enumerate(self.current_preview_list_label):
            if i == 0:
                book_remain = LBottomPreviewItem(list_name, QPixmap(cover), comic_name, comic_path, 250,
                                                 read_pages, pages, collected, False, self, cover)
            if read_pages > 0 and read_pages != pages:
                no_recent_comic = False
                book_recent = LBottomPreviewItem(list_name, QPixmap(cover), comic_name, comic_path, 250,
                                                 read_pages, pages, collected, False, self, cover)
                self.horizontalLayout_recent.insertWidget(self.horizontalLayout_recent.count()-1, book_recent)
        if no_recent_comic:
            self.horizontalLayout_recent.insertWidget(self.horizontalLayout_recent.count()-1, book_remain)
        else:
            book_remain.deleteLater()
        end = time.time()
        print("RUtils show_LBottom_previews：加载/更新预览图片耗时：", end - start)

    # 清空预览
    def clear(self, clear_recent=True):
        while self.preview_layout.count():
            item = self.preview_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()
            self.preview_layout.removeItem(item)
            del item
        self.preview_layout.update()

        if not clear_recent:
            return

        for i in range(self.horizontalLayout_recent.count()):
            item = self.horizontalLayout_recent.itemAt(0)
            try:
                if item.widget():
                    item.widget().deleteLater()
                    self.horizontalLayout_recent.removeItem(item)
            except:
                continue
        self.horizontalLayout_recent.update()

    def compute_columns(self):
        self.columns = self.scrollAreaWidgetContents.width() // self.preview_width

    def resizeEvent(self, event: PySide6.QtGui.QResizeEvent) -> None:
        self.widget_comics.setFixedWidth(self.width() - 6)
        if not self.resize_timer.isActive():
            self.resize_timer.start(500)
        super().resizeEvent(event)

    def reset_view_size(self):
        # print("",self.width(), self.widget_comics.width())
        if self.columns == self.scrollAreaWidgetContents.width() // self.preview_width:
            return
        if self.columns * self.preview_width > self.widget_comics.width():
            while self.columns * self.preview_width > self.widget_comics.width():
                self.columns -= 1
        if (self.columns + 1) * self.preview_width < self.widget_comics.width():
            self.columns += 1
        try:
            self.compute_columns()
            self.set_page_preview(self.current_page)
            self.preview_layout.update()
        except:
            pass
        # self.compute_columns()

    def view_size_change(self):
        if not self.slider_value_timer.isActive():
            self.slider_value_timer.start(50)

    # 设置预览封面大小
    def view_change_reset_view_size(self):
        if self.horizontalSlider.value() // 20 != self.view_size_level:
            self.view_size_level = self.horizontalSlider.value() // 20
            self.preview_width = self.base_preview_width + int(50 * self.view_size_level / 4)
        self.show_preview_index()
        print('RUtils view_change_reset_view_size: ', self.horizontalSlider.value())

    # 定位到当前页
    def show_preview_index(self):
        self.compute_columns()
        self.set_page_preview(self.current_page)
        # if self.preview_index == 1:
        #     self.set_page_preview(self.current_page)
        #     # self.preview_layout.update()
        # elif self.preview_index == 3:
        #     self.show_LBottom_previews()

    # 从所有库中搜索漫画
    def search_comics_from_all_library(self):
        # print(self.l_id, self.library_path, self.library_name)
        self.shelf.selected_item = None
        # 1.恢复所有Item的默认样式
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
        # 2. 在所有库中查找漫画
        library_info_path = "userdata/LibraryName.comic"
        info_list = []
        dir_info = []
        search_content = self.lineEdit_search.text()
        if os.path.exists(library_info_path):
            db = QSqlDatabase("QSQLITE")
            db.setDatabaseName(library_info_path)
            db.open()
            query = QSqlQuery(db)
            query.exec("SELECT DISTINCT comic_info_db_path FROM library")
            while query.next():
                info_list += search_comics_from_library(search_content, query.value(0))
                for d_i in get_all_dirs_from_all_library(query.value(0), search_content):
                    if d_i not in dir_info:
                        dir_info.append(d_i)
            self.libraryPath = None
            self.set_previews(info_list, 1)
        self.shelf.findChild(QWidget, 'LMidMenu').update_item_from_list(dir_info)

    # 展示从库文件夹中搜索的结果
    def show_search_dir_previews(self):
        self.compute_columns()
        self.max_page = math.ceil(len(self.searching_preview_list_label)/self.page_covers_numb)
        self.spinBox_page_index.setMaximum(self.max_page)
        self.spinBox_page_index.setValue(self.current_page)
        # self.preview_layout.columnCount = self.columns
        self.current_page = 1
        self.spinBox_page_index.setValue(self.current_page)
        self.clear()
        self.set_page_preview(self.current_page, is_search_dir=True)
        self.preview_layout.update()
        if not self.preview_list_label:
            return
        start = time.time()
        no_recent_comic = True
        book_remain = None
        for i, (comic_path, comic_name, collected, library_path, library_name, belong_path,
                read_pages, pages, cover) in enumerate(self.searching_preview_list_label):
            # PreviewItem(pixmap_cover, book_name, comic_path, view_width, library_path,
            #                                       belong_path, is_collected = False, right_area = None)
            if i == 0:
                book_remain = LTopPreviewItem(QPixmap(cover), comic_name, comic_path, 250, library_path, library_name,
                                              belong_path, read_pages, pages, collected, False, self, cover)
            if read_pages > 0 and read_pages != pages:
                no_recent_comic = False
                book_recent = LTopPreviewItem(QPixmap(cover), comic_name, comic_path, 250, library_path, library_name,
                                              belong_path, read_pages, pages, collected, False, self, cover)
                self.horizontalLayout_recent.insertWidget(self.horizontalLayout_recent.count() - 1, book_recent)

        # 如果有“最近阅读”，则删除book_remain， 否则添加到recent预览
        if no_recent_comic and book_remain:
            self.horizontalLayout_recent.insertWidget(self.horizontalLayout_recent.count() - 1, book_remain)
        else:
            book_remain.deleteLater() if book_remain else None
        end = time.time()
        print("RUtils show_search_dir_previews：加载/更新预览图片耗时：", end - start)

    # 根据当前选择Item中的类型搜索漫画
    def search_comics_from_selected_item(self):
        if not self.shelf.selected_item:
            print('RUtils search_comics_from_selected_item: 没有选中Item')
            return
        search_content = self.lineEdit_search.text()
        if self.shelf.selected_item.item_type == "library":
            info_list = search_comics_from_library(search_content, self.shelf.selected_item.comic_info_db,
                                                   library_name=self.shelf.selected_item.library_name)
            self.libraryPath = None
            self.set_previews(info_list, 1)
            # 按搜索内容更新文件夹Item
            self.shelf.findChild(QWidget, 'LMidMenu').update_item(self.shelf.selected_item.comic_info_db,
                                                                  self.shelf.selected_item.library_name,
                                                                  filter_=search_content)
            print('RUtils search_comics_from_selected_item: ', self.shelf.selected_item.comic_info_db)

        elif self.shelf.selected_item.item_type == 'library_dir':
            self.searching_preview_list_label = []
            for c in self.current_preview_list_label:
                if search_content in c[1]:
                    self.searching_preview_list_label.append(c)
            self.libraryPath = None
            self.show_search_dir_previews()
            print('RUtils search_comics_from_selected_item: ', self.shelf.selected_library_item.comic_info_db)

        elif self.shelf.selected_item.item_type == "list":
            info_list = search_comics_from_list(search_content, self.shelf.selected_item.list_name)
            self.libraryPath = None
            self.set_previews(info_list, 3)
            print('RUtils search_comics_from_selected_item: ', self.shelf.selected_item.list_name)

        # if self.shelf.selected_item:
