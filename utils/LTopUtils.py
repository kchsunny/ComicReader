import os
import time
from PySide6.QtGui import QMouseEvent
from PySide6.QtCore import QThread, Signal
import zipfile
from PIL import Image
import hashlib
from UIParts.part1_Item import Ui_Form as bookDirArea0111_1  # 库列表
from UIParts.subwindow_create_storage import Ui_Form as Ui_Form_SubWindowCreateStorage
from UIParts.subwindow_import_storage import Ui_Form as Ui_Form_SubWindowImportStorage
from UIParts.part1 import Ui_Form as TopArea
from UIParts import rename_library_ui, update_storage
from utils import *


class CreateStorageThreat(QThread):
    process_signal = Signal(int, int, str)
    finish_signal = Signal(int)

    def __init__(self):
        super().__init__()
        self.library_path = ''
        self.library_name = ''
        self.library_info_path = ''
        self.covers_path = ''
        self.comics_list = []
        self.t = ''
        self.t1 = ''
        self.running = False

    def set_library_path(self, library_path, library_name):
        self.running = True
        self.library_path = library_path
        self.library_name = library_name
        self.library_info_path = replace_path(os.path.join(library_path, ".library"))
        self.covers_path = replace_path(os.path.join(self.library_info_path, "covers"))
        if not os.path.exists(self.library_info_path):
            os.makedirs(self.library_info_path)
        if not os.path.exists(self.covers_path):
            os.makedirs(self.covers_path)

    def run(self) -> None:
        self.comics_list = []
        self.find_all_comics(self.library_path, os.path.basename(self.library_path))
        delete_not_exist_comic_from_library(self.library_info_path, self.library_name)
        for i in range(len(self.comics_list)):
            self.t = check_exist_comic(self.library_info_path, self.comics_list[i][1], self.comics_list[i][0], self.library_name)
            if self.t[0]:
                self.process_signal.emit(i + 1, len(self.comics_list), self.t[1])
                pass
            else:
                self.extract_cover(self.comics_list[i][0], self.comics_list[i][1], self.comics_list[i][2])
                self.process_signal.emit(i + 1, len(self.comics_list), self.t1)
            # 停止进程
            if not self.running:
                break
        if self.running:
            self.finish_signal.emit(1)
        else:
            self.finish_signal.emit(2)

    def find_all_comics(self, path, dir_name):
        if not os.path.isdir(path):
            # print("不是目录", path)
            pass
        else:
            files = os.listdir(path)
            for f in files:
                if f == ".library":
                    continue
                if os.path.isdir(replace_path(os.path.join(path, f))):
                    self.find_all_comics(replace_path(os.path.join(path, f)), f)
                else:
                    if f.lower().endswith(".zip"):
                        self.comics_list.append([path, f, dir_name])

    def extract_cover(self, path, f_n, dir_name):
        # print("文件名", f)
        # comic_path = os.path.join(path, f)
        comic_pages = 0
        with zipfile.ZipFile(replace_path(os.path.join(path, f_n)), 'r') as zip_file:
            img_names = zip_file.namelist()
            img_names = img_sort(img_names)
            for n in img_names:
                if n.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    comic_pages += 1
            for origin_name in img_names:
                if origin_name.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    hash_object = hashlib.sha256()
                    # 更新哈希对象，需要将字符串编码为字节
                    hash_object.update(f_n.encode())
                    # 获取16进制格式的哈希值
                    hash_digest = hash_object.hexdigest()
                    new_name = str(hash_digest) + "." + origin_name.split(".")[-1]
                    # print(new_name)
                    save_cover_path = replace_path(os.path.join(self.covers_path, new_name))
                    # 读取图片并按new_name保存在covers_path目录下
                    if os.path.exists(save_cover_path):  # 如果已经存在，则跳过
                        pass
                    else:
                        # print(img_cover)
                        # 提取图片并保存在covers_path目录下
                        img_cover = zip_file.extract(origin_name, path=self.covers_path)
                        img = Image.open(img_cover)
                        if img.mode == "P":
                            img.convert("RGB").save(save_cover_path)
                        else:
                            img.save(save_cover_path)
                    try:
                        os.remove(replace_path(os.path.join(self.covers_path, origin_name)))
                    except:
                        pass
                    self.t1 = save_comic_info(save_cover_path, path, self.library_info_path,
                                              comic_pages, f_n, dir_name, self.library_name, self.library_path)
                    break

    def stop(self):
        self.running = False
        self.wait()


# 导入已有库的子界面
class SubWindowImportStorage(QWidget, Ui_Form_SubWindowImportStorage):
    def __init__(self, add_to, shelf):
        super().__init__()
        self.setupUi(self)
        self.add_area = add_to
        self.shelf = shelf
        self.setWindowTitle("导入书库")
        self.setWindowIcon(QIcon("resource/db-import150_black.png"))
        self.label.setPixmap(QPixmap("resource/db-import150_black.png"))
        self.label.setScaledContents(True)
        self.open_folder.setIcon(QIcon("resource/search_black.png"))
        self.open_folder.clicked.connect(self.openfolder)
        self.pushButton_cancel.clicked.connect(self.hide)
        self.pushButton_build.clicked.connect(self.click_import)
        self.label.mouseDoubleClickEvent = self.openfolder
        self.comic_info_db_path = ""

    def hide(self):
        self.setVisible(False)
        self.lineEdit_path.setText("")

    def openfolder(self, event):
        self.comic_info_db_path = QFileDialog.getOpenFileName(self, "选择comics.comic文件", filter="comics.comic")[0]
        if self.comic_info_db_path:
            self.lineEdit_path.setText(self.comic_info_db_path)
        # print('LTopUtils line 147:', self.comic_info_db_path)
        self.lineEdit_path.setText(self.comic_info_db_path)

    def click_import(self):
        if not self.comic_info_db_path.lower().endswith(".comic"):
            QMessageBox.critical(self, "Warning", "文件路径错误！")
            return
        db = QSqlDatabase("QSQLITE")
        db.setDatabaseName(self.comic_info_db_path)
        db.open()
        query = QSqlQuery(db)
        query.prepare(f"""
            SELECT DISTINCT library_name, library_path FROM comics
        """)
        db_library = QSqlDatabase("QSQLITE")
        db_library.setDatabaseName("userdata/LibraryName.comic")
        db_library.open()
        query_library = QSqlQuery(db_library)
        if query.exec():
            while query.next():
                query_library.prepare(f"""
                    SELECT * FROM library 
                    WHERE name='{query.value(0)}' and path='{query.value(1)}'
                """)
                if not query_library.exec():
                    print(f"LTopUtils click_import: SELECT * FROM library "
                          f"WHERE name='{query.value(0)}' and path='{query.value(1)}'")
                    continue
                if not query_library.next():
                    if not query_library.exec(f"""
                        INSERT INTO library(name, old_name, path, comic_info_db_path) 
                        VALUES('{query.value(0)}','{query.value(0)}','{query.value(1)}','{self.comic_info_db_path}')
                    """):
                        print(f"LTopUtils click_import: INSERT INTO library(name, path) "
                              f"VALUES('{query.value(0)}','{query.value(0)}','{query.value(1)}')")
                        continue
                    if not query_library.exec(f"""
                            SELECT id FROM library 
                            WHERE name='{query.value(0)}' and path='{query.value(1)}'
                    """):
                        print(f"LTopUtils click_import: SELECT id FROM library "
                              f"WHERE name='{query.value(0)}' and path='{query.value(1)}'")
                        continue
                    else:
                        query_library.next()
                        ku_list_item = LTopItem(query.value(0), query.value(0), query.value(1),
                                                query_library.value(0), self.comic_info_db_path, self.shelf)
                        self.add_area.verticalLayout_2.insertWidget(self.add_area.verticalLayout_2.count()-1, ku_list_item)
        db.close()
        db_library.close()
        self.hide()


# 初始化库子界面
class UpdateStorage(QWidget, update_storage.Ui_Form):
    def __init__(self, library_path, library_name):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon("resource/BookShelf.png"))
        self.setWindowTitle("更新书库")
        self.library_path = library_path
        self.library_name = library_name
        self.library_info_path = replace_path(os.path.join(library_path, ".library"))
        self.covers_path = replace_path(os.path.join(self.library_info_path, "covers"))
        try:
            if not os.path.exists(self.library_info_path):
                os.makedirs(self.library_info_path)
            if not os.path.exists(self.covers_path):
                os.makedirs(self.covers_path)
        except:
            pass
        self.create_storage_thread = CreateStorageThreat()
        self.create_storage_thread.process_signal.connect(self.update_process)
        self.create_storage_thread.finish_signal.connect(self.finish)
        self.pushButton.clicked.connect(self.hide_p)
        self.pushButton_cancel.clicked.connect(self.cancel)

    def cancel(self):
        self.create_storage_thread.running = False

    def hide_p(self):
        self.hide()

    def update_(self):
        self.create_storage_thread.set_library_path(self.library_path, self.library_name)
        self.create_storage_thread.start()

    def update_process(self, n, total, t):
        self.progressBar.setValue(n)
        self.progressBar.setMaximum(total)
        self.textEdit.append(t)

    def finish(self):
        # self.pushButton_cancel.setDisabled(True)
        if self.create_storage_thread.running:
            QMessageBox.information(self, "info", f"库名：{self.library_name}\n路径：{self.library_path}\n更新完成!")
        else:
            QMessageBox.information(self, "info", f"库名：{self.library_name}\n路径：{self.library_path}\n中断更新!")
        self.close()


# 创建新库的子界面
class SubWindowCreateStorage(QWidget, Ui_Form_SubWindowCreateStorage):
    def __init__(self, add_to, shelf):
        super().__init__()
        self.add_area = add_to
        self.shelf = shelf
        self.setupUi(self)
        self.open_folder.setIcon(QIcon("resource/search_black.png"))
        self.open_folder.clicked.connect(self.import_folder)
        self.pushButton_cancel.clicked.connect(self.button_hide)
        self.pushButton_build.clicked.connect(self.button_create)
        self.label.setPixmap(QPixmap("resource/创建数据库150_black.png"))
        self.label.setScaledContents(True)
        self.setWindowTitle("创建新书库")
        self.setWindowIcon(QIcon("resource/创建数据库150_black.png"))
        self.label.mouseDoubleClickEvent = self.double_click_label
        self.widget_7.setVisible(False)
        self.create_storage_thread = CreateStorageThreat()
        self.create_storage_thread.process_signal.connect(self.update_process)
        self.create_storage_thread.finish_signal.connect(self.finish)
        self.pushButton_cancel.setDisabled(True)
        self.widget_8.setVisible(False)

    def closeEvent(self, event: PySide6.QtGui.QCloseEvent) -> None:
        self.lineEdit_path.setText("")
        self.lineEdit_name.setText("")

    def button_create(self):
        self.textEdit.setText('')
        library_name = self.lineEdit_name.text()
        path = self.lineEdit_path.text()
        if not library_name or not os.path.isdir(path):
            QMessageBox.critical(self, "info error", "名称为空或路径不对")
            return

        # 1.将信息添加到书库表
        sql_db = QSqlDatabase("QSQLITE")
        sql_db.setDatabaseName("userdata/LibraryName.comic")
        if sql_db.open():
            if 'library' not in sql_db.tables():  # 如果表不存在就创建
                # QMessageBox.critical(self, "DB error", "button_create：library 不存在")
                sql_db.exec("""
                    CREATE TABLE IF NOT EXISTS library(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name text NOT NULL,
                        old_name text NOT NULL,
                        path text NOT NULL,
                        comic_info_db_path TEXT NOT NULL
                    )
                """)
            sql_db.close()

        # 如果已经有相同信息，添加库失败
        if sql_db.open():
            q = QSqlQuery(sql_db)
            q.prepare(f"SELECT * from library where name='{library_name}' and path='{path}'")
            q.exec()
            if q.next():
                QMessageBox.critical(self, "warning", "已有重复库！")
                sql_db.close()
                return
        # 如果没有相同信息，则添加
        if sql_db.open():
            q = QSqlQuery(sql_db)
            q.prepare("""
                INSERT INTO library (name, old_name, path, comic_info_db_path)
                VALUES (:name, :old_name, :path, :comic_info_db_path)
            """)
            comic_info_db_path = replace_path(os.path.join(path, ".library", "comics.comic"))
            q.bindValue(":name", library_name)
            q.bindValue(":old_name", library_name)
            q.bindValue(":path", path)
            q.bindValue(":comic_info_db_path", comic_info_db_path)
            if not q.exec():
                QMessageBox.critical(self, "warning", "创建失败!")
            else:
                q.exec(f"SELECT id from library WHERE name='{library_name}' and path='{path}'")
                q.next()
                ku_list_item = LTopItem(library_name, library_name, path, q.value(0), comic_info_db_path, self.shelf)
                self.add_area.verticalLayout_2.insertWidget(self.add_area.verticalLayout_2.count()-1, ku_list_item)
                # 2.创建书库相关文件及添加表信息
                self.create_storage_thread.set_library_path(path, library_name)
                self.create_storage_thread.start()
                self.widget_7.setVisible(True)
                self.widget_8.setVisible(True)
                self.pushButton_cancel.setDisabled(False)
            sql_db.close()
        pass

    def button_hide(self):
        qm = QMessageBox()
        qm.addButton('确定', QMessageBox.ButtonRole.AcceptRole)
        qm.addButton('取消', QMessageBox.ButtonRole.NoRole)
        qm.setText("是否中断？！")
        qm.setWindowTitle('Warning')
        # qm.setIcon(QMessageBox.Icon.Warning)
        qm.setWindowIcon(QIcon('resource/warning-fill.png'))
        r = qm.exec()
        if r == 2:
            self.create_storage_thread.stop()
            # self.lineEdit_path.setText("")
            # self.lineEdit_name.setText("")
            # self.setVisible(False)

    def update_process(self, n, total, t):
        self.progressBar.setValue(n)
        self.progressBar.setMaximum(total)
        self.textEdit.append(t)

    def double_click_label(self, event):
        self.import_folder()

    def finish(self, flag):
        self.pushButton_cancel.setDisabled(True)
        if flag == 1:
            QMessageBox.information(self, "info", "创建完成!")
        elif flag == 2:
            QMessageBox.information(self, "info", "已中断，可在库中更新以继续!")

    #  添加新库事件
    def import_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        # print('LTopUtils line 353:', folder_path)
        # lb = InitLibrary(folder_path)
        # L = LTopMenuSub1(folder_path.split("/")[-1], folder_path)
        # item = LTopItem(folder_path.split("/")[-1], folder_path)
        # self.add_to.LAtop2_layout.insertWidget(self.add_to.LAtop2_layout.count() - 1, item)
        self.lineEdit_path.setText(folder_path)


# 库列表区域
class LTop(QWidget, TopArea):
    def __init__(self, shelf):
        super(LTop, self).__init__()
        self.setupUi(self)
        self.shelf = shelf
        # self.setFixedHeight(32)
        self.setObjectName("LTopMenu")
        self.pushButton_add.setIcon(QIcon("resource/add_white.png"))
        self.pushButton_add.setToolTip("添加新库")
        self.pushButton_import.setIcon(QIcon("resource/import_white.png"))
        self.pushButton_import.setToolTip("导入已有的库")
        self.setStyleSheet("""
            QLabel{color:white;border:0;} 
            QPushButton{border:0;}
            QToolTip{color:white;border:0;background-color: #4D4849;}
            QWidget{background-color: #4D4849;}
            #widget_top_menu{border-bottom: 1px solid gray;}
        """)
        self.scrollArea_top_list.setStyleSheet("""
            QScrollArea { border:0;background-color: transparent; }
            QScrollBar:vertical { background-color: transparent; width:6px;}
            QScrollBar::handle:vertical { background-color: #D8D8D8; border-radius: 2px; }
            QScrollBar::add-line:vertical, 
            QScrollBar::sub-line:vertical { background-color: transparent; height: 0px; }
            QScrollBar::add-page:vertical, 
            QScrollBar::sub-page:vertical { background-color: transparent; }
        """)
        self.pushButton_add.clicked.connect(self.open_create_sub_window)
        self.pushButton_import.clicked.connect(self.open_import_sub_window)
        self.subWindow_create = SubWindowCreateStorage(self, self.shelf)
        self.subWindow_import = SubWindowImportStorage(self, self.shelf)
        self.init_library()
        # self.browser = ImageBrowser()
        # self.browser.show()

    def open_import_sub_window(self):
        self.subWindow_import.show()

    def open_create_sub_window(self):
        self.subWindow_create.show()

    def init_library(self):
        # print("LTopUtils line 404: 初始化")
        sql = QSqlDatabase("QSQLITE")
        sql.setDatabaseName("userdata/LibraryName.comic")
        if sql.open():
            if 'library' not in sql.tables():
                QMessageBox.critical(self, "DB error", "init_library：library 不存在")
                sql.exec("""
                    CREATE TABLE IF NOT EXISTS library(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name text NOT NULL,
                        old_name text NOT NULL,
                        path text NOT NULL,
                        comic_info_db_path TEXT NOT NULL
                    )
                """)

            # print("LTopUtils line 420: 打开成功")
            q = QSqlQuery(sql)
            q.exec("SELECT * FROM library")
            while q.next():
                id_ = q.value("id")
                name = q.value("name")
                old_name = q.value("old_name")
                path = q.value("path")
                comic_info_db = q.value("comic_info_db_path")
                ku_list_item = LTopItem(name, old_name, path, id_, comic_info_db, self.shelf)
                # print("LTopUtils line 430: ", (name, path, id_, comic_info_db))
                self.verticalLayout_2.insertWidget(self.verticalLayout_2.count()-1, ku_list_item)
            sql.close()
        else:
            print("LTopUtils init_library: 打开失败")
        # query = QSqlQuery(sql)
        # query.exec()


# 库列表单项
class LTopItem(QWidget, bookDirArea0111_1):
    def __init__(self, name, old_name, path, l_id=1, comic_info_db=None, shelf=None):
        super().__init__()
        self.setupUi(self)
        pixmap = QPixmap("resource/line-bookshelf-white.png")  # 替换为你的图片文件路径
        self.pushButton_3.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.pushButton_3.customContextMenuRequested.connect(self.set_menu)
        # 设置 QLabel 的 pixmap
        self.label.setPixmap(pixmap)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.selected = False  # 判断是否被选中
        # 调整 QLabel 的大小以适应图片的大小
        self.label.setScaledContents(True)
        self.label_2.setText(name)
        self.shelf = shelf
        self.item_type = "library"
        self.library_path = path
        self.setToolTip(f'库路径：{path}')
        self.library_name = name
        self.library_old_name = old_name
        self.comic_info_db = comic_info_db
        # self.comic_info_db = replace_path(os.path.join(self.library_path, ".library/comics.comic"))
        self.l_id = l_id
        self.update_ui = UpdateStorage(self.library_path, self.library_old_name)
        self.r_UI = RenameUI(self.library_name, l_id, self)
        self.pushButton_3.setIcon(QIcon("resource/setting_white.png"))
        self.pushButton_3.setDisabled(True)
        self.pushButton_3.setVisible(False)
        self.setStyleSheet("color:white")
        self.objectName()
        self.setStyleSheet("""
                            QWidget{border:0;}
                            QLabel{color:white;border:0;} 
                            QPushButton{border:0;}
                        """)

    # 释放鼠标当前Item后更新样式
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
        self.pushButton_3.setDisabled(False)
        self.pushButton_3.setVisible(True)
        self.shelf.selected_item = self
        self.shelf.selected_library_item = self
        self.selected = True
        super().mouseReleaseEvent(event)

    # 点击当前Item后
    def mousePressEvent(self, event: PySide6.QtGui.QMouseEvent = None):
        # print(self.l_id, self.library_path, self.library_name)
        # if self.selected:  # 如果当前Item已被选中，则不重新加载previews
        #     return
        if event.button() != Qt.MouseButton.LeftButton:
            return
        library_info_path = self.comic_info_db
        if os.path.exists(library_info_path):
            db = QSqlDatabase("QSQLITE")
            db.setDatabaseName(library_info_path)
            db.open()
            query = QSqlQuery(db)
            info_list = []
            # PreviewItem(pixmap_cover, book_name, comic_path, view_width, library_path,
            #                                       belong_path, is_collected = False, right_area = None)
            query.exec(f"""
                SELECT DISTINCT belong_path, name, cover, collected, library_path, library_name, read_pages, pages
                FROM comics 
                WHERE library_name='{self.library_old_name}'
                ORDER BY name
            """)
            start = time.time()
            while query.next():
                # print(f"查询到：{query.value(0)}, {query.value(1)}, {query.value(5), query.value(6), query.value(7)}")
                info_list.append([replace_path(os.path.join(query.value(0), query.value(1))),
                                  query.value(1), query.value(2), query.value(3), query.value(4),
                                  query.value(5), query.value(0), query.value(6), query.value(7)])
            sub_start = time.time()
            print("LTopUtils mousePressEvent: 查询时间：", sub_start - start)

            self.shelf.findChild(QWidget, "RightArea").libraryPath = self.library_path
            self.shelf.findChild(QWidget, "RightArea").set_previews(info_list, 1)
            end_time = time.time()
            print("LTopUtils mousePressEvent: 加载图片时间总耗时：", end_time - sub_start)
            self.shelf.findChild(QWidget, 'LMidMenu').update_item(self.comic_info_db, self.library_old_name)
            # self.findChild()
        else:
            QMessageBox.critical(self, "info error", "库信息不存在，请重新导入！")
            db = QSqlDatabase("QSQLITE")
            db.setDatabaseName("userdata/LibraryName.comic")
            db.open()
            db.exec(f"DELETE FROM library WHERE id = {self.l_id}")
            self.deleteLater()
        super().mousePressEvent(event)

    def update_mid_item(self):
        library_info_path = self.comic_info_db
        if os.path.exists(library_info_path):
            db = QSqlDatabase("QSQLITE")
            db.setDatabaseName(library_info_path)
            db.open()
            query = QSqlQuery(db)
            info_list = []
            # PreviewItem(pixmap_cover, book_name, comic_path, view_width, library_path,
            #                                       belong_path, is_collected = False, right_area = None)
            query.exec(f"""
                        SELECT DISTINCT belong_path, name, cover, collected, library_path, library_name, read_pages, pages
                        FROM comics 
                        WHERE library_name='{self.library_old_name}'
                        ORDER BY name
                    """)
            start = time.time()
            while query.next():
                # print(f"查询到：{query.value(0)}, {query.value(1)}, {query.value(5), query.value(6), query.value(7)}")
                info_list.append([replace_path(os.path.join(query.value(0), query.value(1))),
                                  query.value(1), query.value(2), query.value(3), query.value(4),
                                  query.value(5), query.value(0), query.value(6), query.value(7)])
            sub_start = time.time()
            print("LTopUtils mousePressEvent: 查询时间：", sub_start - start)

            self.shelf.findChild(QWidget, "RightArea").libraryPath = self.library_path
            self.shelf.findChild(QWidget, "RightArea").set_previews(info_list, 1)
            end_time = time.time()
            print("LTopUtils mousePressEvent: 加载图片时间总耗时：", end_time - sub_start)
            self.shelf.findChild(QWidget, 'LMidMenu').update_item(self.comic_info_db, self.library_old_name)

    def set_l_mid_item(self, library_info_path):
        db = QSqlDatabase("QSQLITE")
        db.setDatabaseName(library_info_path)
        db.open()
        query = QSqlQuery(db)
        info_list = []
        # PreviewItem(pixmap_cover, book_name, comic_path, view_width, library_path,
        #                                       belong_path, is_collected = False, right_area = None)
        query.exec(f"""
                        SELECT DISTINCT dir_name, belong_path
                        FROM comics 
                        WHERE library_name='{self.library_old_name} and library_path='{self.library_path}'
                        ORDER BY belong_path
                    """)
        start = time.time()
        while query.next():
            # print(f"查询到：{query.value(0)}, {query.value(1)}, {query.value(5), query.value(6), query.value(7)}")
            info_list.append([replace_path(os.path.join(query.value(0), query.value(1))),
                              query.value(1), query.value(2), query.value(3), query.value(4),
                              query.value(5), query.value(0), query.value(6), query.value(7)])
        sub_start = time.time()
        print("LTopUtils set_l_mid_item: 查询时间：", sub_start - start)

        self.shelf.findChild(QWidget, "RightArea").libraryPath = self.library_path
        self.shelf.findChild(QWidget, "RightArea").set_previews(info_list)

    def set_menu(self, position):  # 弹出子菜单
        menu = QMenu(self)
        menu.setStyleSheet("color:white;background-color: rgba(0, 0, 0,0.9);")
        delete_action = QAction('删除', self)
        delete_action.setIcon(QIcon("resource/delete_black.png"))
        delete_action.triggered.connect(self.delete_self)
        rename_action = QAction('重命名', self)
        rename_action.setIcon(QIcon("resource/Edit_black.png"))
        rename_action.triggered.connect(self.rename_self)
        update_action = QAction('更新库', self)
        update_action.setIcon(QIcon("resource/recover_black.png"))
        update_action.triggered.connect(self.update_self)
        copy_path_action = QAction('复制路径', self)
        copy_path_action.setIcon(QIcon("resource/复制_black.png"))
        copy_path_action.triggered.connect(self.copy_path)
        menu.addAction(delete_action)
        menu.addAction(rename_action)
        menu.addAction(update_action)
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
        menu.exec(self.pushButton_3.mapToGlobal(position))

    def delete_self(self):
        # print('LTopUtils line 629: ', self.l_id)
        sql_db = QSqlDatabase("QSQLITE")
        sql_db.setDatabaseName("userdata/LibraryName.comic")
        if sql_db.open():
            q = QSqlQuery(sql_db)
            if not q.exec(f"DELETE FROM library WHERE id={self.l_id}"):
                QMessageBox.critical(self, "error", "删除失败")
            else:
                QMessageBox.information(self, "info", "删除成功")
            sql_db.close()
        self.deleteLater()
        pass

    def rename_self(self):
        self.r_UI.show()
        pass

    def update_self(self):
        self.update_ui.show()
        self.update_ui.update_()
        # self.mousePressEvent()
        pass

    def copy_path(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.library_path)


# 重命名库子界面
class RenameUI(QWidget, rename_library_ui.Ui_Form):
    def __init__(self, old_name, l_id, rename_item):
        super().__init__()
        self.setupUi(self)
        self.l_id = l_id
        self.rename_item = rename_item
        self.setWindowIcon(QIcon("resource/BookShelf.png"))
        self.setWindowTitle("重命名库")
        self.label_oldname.setText(old_name)
        self.pushButton_rename.clicked.connect(self.rename)
        self.pushButton_cancel.clicked.connect(self.cancel)

    def cancel(self):
        self.hide()
        self.lineEdit_newname.setText("")

    def rename(self):
        new_name = self.lineEdit_newname.text()
        if new_name:
            # print('LTopUtils line 672: ', self.l_id)
            sql_db = QSqlDatabase("QSQLITE")
            sql_db.setDatabaseName("userdata/LibraryName.comic")
            if sql_db.open():
                q = QSqlQuery(sql_db)
                if not q.exec(f"UPDATE library SET name = '{new_name}' where id={self.l_id}"):
                    QMessageBox.critical(self, "info error", "重命名失败")
                else:
                    self.rename_item.label_2.setText(new_name)
                    self.lineEdit_newname.setText("")
                    self.hide()
                    QMessageBox.information(self, "info error", "重命名成功")
                sql_db.close()
        else:
            QMessageBox.critical(self, "info error", "新名称不能为空")
