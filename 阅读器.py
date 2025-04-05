import sys
import time
import zipfile
# import rarfile
import os
import PySide6
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QFileDialog, QMessageBox
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtSql import QSqlDatabase, QSqlQuery
from PySide6.QtCore import Qt, QTimer, QSettings, QThread, Signal
from UIParts.reader import Ui_Form as Reader
from utils import img_sort, replace_path, save_comic_pages_info, IMG_TYPE
from UIParts import load_new_comic_process
from PIL import Image


class LoadComicThread(QThread):
    loading_process = Signal(int, int)
    loading_finish = Signal()

    def __init__(self, parent):
        super().__init__()
        self.init()
        self.parent = parent

    def init(self):
        self.file_path = ''

    def set_file_path(self, file_path):
        self.file_path = file_path

    def set_preview_comic(self, preview):
        self.preview = preview

    def run(self) -> None:
        self.loading()

    def loading(self):
        start = time.time()
        with zipfile.ZipFile(self.parent.file_path, 'r') as zip_ref:
            # 将图片文件添加到列表
            for n in zip_ref.namelist():
                if n.lower().endswith(IMG_TYPE):
                    self.parent.imageListName.append(n)
            # 根据提取的数字对文件名进行排序
            self.parent.imageListName = img_sort(self.parent.imageListName)
            # 设置总页数
            self.parent.label.setText(str(len(self.parent.imageListName)))
            num = 0
            self.parent.size_scale = {}
            total = len(self.parent.imageListName)
            for page_name in self.parent.imageListName:
                num += 1
                if page_name.lower().endswith(IMG_TYPE):
                    label = QLabel()
                    size = Image.open(zip_ref.open(page_name)).size
                    self.parent.size_origin[page_name] = size
                    save_comic_pages_info(self.parent.file_path, page_name, size[0], size[1])
                    size = [self.parent.imgWidth, int(size[1] * self.parent.imgWidth / size[0])]
                    self.parent.size_scale[page_name] = size
                    self.parent.totalHeight += size[1]
                    label.setFixedSize(size[0], size[1])
                    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    label.setObjectName(page_name)
                    label.setScaledContents(True)
                    self.parent.labels[page_name] = label
                    self.parent.fill_contents(label)
                self.loading_process.emit(num, total)
        # print("393 从压缩包加载页面数据耗时：", time.time() - start)
        self.loading_finish.emit()


class LoadComicProcess(QWidget, load_new_comic_process.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class ImageViewer(QWidget, Reader):
    def __init__(self, load_last=True):
        """
        :param load_last: bool：True/False 是否自动加载上次打开的漫画
        """
        super().__init__()
        self.setWindowIcon(QIcon("./resource/reading_black.png"))
        self.setWindowTitle("阅读器")
        self.file_path = ""
        self.setupUi(self)
        self.pushButton.clicked.connect(self.get_file)
        self.current_index = 0  # 当前图片所在序号
        self.imageListName = []  # 所有图片的名称列表
        self.totalHeight = 1  # 所有缩放图片的总高度
        self.labels = {}  # 按图片名称展示每张图片的容器
        self.size_origin = {}  # 按图片名称存放每张图片的原始的大小
        self.size_scale = {}  # 按图片名称存放每张图片缩放后的大小
        self.size_scale_height = [0]  # 按图片顺序存储每张图片缩放后的高度
        self.show_list = []  # 当前显示的图片列表，会不断变化
        self.first_load_flag = True  # 是否是第一次加载标志
        self.open_type = ''  # 标示打开漫画的类型：全新漫画、阅读过的漫画、单独漫画文件
        self.load_finish = False
        self.imgWidth = self.scrollAreaWidgetContents.width()
        self.scrollAreaWidgetContents.setStyleSheet("background-color:#4D4D4D;")
        self.scrollArea.verticalScrollBar().valueChanged.connect(self.on_scroll)
        self.background = ["background-color: transparent;",
                           "background-color: transparent;",
                           "background-color: transparent;"]
        # self.background = ["background-color: red;", "background-color: #4D4D4D;", "background-color: #4D4D4D;"]
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(lambda: self.on_time_out(self.scrollArea.verticalScrollBar().value()))
        self.resize_timer = QTimer(self)
        self.resize_timer.setSingleShot(True)
        self.resize_timer.timeout.connect(self.resize_timer_event)
        self.pushButton_3.clicked.connect(self.jump_to_page)
        self.pushButton_2.clicked.connect(self.show_or_hidden_process)
        self.horizontalSlider.sliderReleased.connect(self.slid_horizontal_slider)
        self.verticalLayout_2.setSpacing(0)
        self.lineEdit.setText("0")
        self.settings = QSettings("YourCompany", "YourApp")
        self.last_comic_path = ""
        self.read_pages = 0
        self.library_name = None
        self.library_path = None
        self.comic_name = None
        self.belong_path = None
        self.load_process = LoadComicProcess()
        self.load_process.setWindowIcon(QIcon("./resource/reading_black.png"))
        self.load_process.setWindowTitle("初始化页面")
        self.load_process_thread = LoadComicThread(self)
        self.load_process_thread.loading_process.connect(self.loading)
        self.load_process_thread.loading_finish.connect(self.loading_finish)
        if load_last:
            self.load_last_comic()

    def loading(self, n, total):
        # print_(f"阅读器：def loading(self, {n}, {total}):")
        self.load_process.progressBar.setValue(n)
        self.load_process.progressBar.setMaximum(total)
        pass

    def loading_finish(self):
        self.load_process.progressBar.setValue(0)
        self.load_process.hide()
        print_(f"阅读器：def loading_finish(self):{self.file_path}, {self.imageListName}")
        self.load_old_comic(self.file_path, self.library_name, self.library_path, self.comic_name, self.belong_path)

        # self.scrollAreaWidgetContents.setFixedHeight(self.totalHeight)
        # # 按图片顺序存储每张图片缩放后的高度
        # for i, n in enumerate(self.imageListName):
        #     self.size_scale_height.append(self.size_scale[n][1])
        #
        # self.lineEdit.setText("1")
        # self.get_location(self.scrollArea.verticalScrollBar().value())  # 第二部展示当前进度应该展示的几张图片
        # self.jump_to_page()
        # self.setWindowTitle(f"阅读器:{os.path.basename(self.file_path)[:-4]}")
        # self.load_finish = True
        # self.resize_timer_event()
        self.show()

    def load_last_comic(self):
        print_(f"阅读器：def load_last_comic(self):打开上次的漫画")
        # if not os.path.exists(self.file_path):
        #     return
        db = QSqlDatabase("QSQLITE")
        db.setDatabaseName("userdata/ComicReadInfo.comic")
        db.open()
        # print(db.tables())
        query = QSqlQuery(db)
        query.prepare("""
        SELECT path, read_pages FROM recent WHERE id=1;
        """)
        if query.exec():
            if query.next():
                self.last_comic_path = query.value(0)
                self.load_old_comic(self.last_comic_path)
            else:
                print_("169 load_last_comic没有上次打开信息")
        else:
            print_("171 load_last_comic上次打开漫画失败")
            pass
        db.close()
        self.jump_to_page()

    def load_old_comic(self, path, library_name=None, library_path=None, comic_name=None, belong_path=None):
        print_(f"阅读器：def load_old_comic 打开漫画{path}")
        self.library_name = library_name
        self.library_path = library_path
        self.comic_name = comic_name
        self.belong_path = belong_path
        db = QSqlDatabase("QSQLITE")
        db.setDatabaseName("userdata/ComicReadInfo.comic")
        db.open()
        # print(db.tables())
        query = QSqlQuery(db)
        query.prepare(f"""
        SELECT path, read_pages FROM comics WHERE path='{path}';
        """)
        if query.exec():
            if query.next():
                self.last_comic_path = query.value(0)
                self.read_pages = query.value(1)
                self.init_self()
                self.file_path = self.last_comic_path
                # print("上次打开漫画：", self.last_comic_path, self.read_pages)
                if self.read_pages:
                    self.first_load_flag = False
                self.open_type = 'load_old_comic_1'
                self.load_images()
                index = self.read_pages
                height = sum(self.size_scale_height[:index])
                self.lineEdit.setText(str(self.read_pages))
                self.horizontalSlider.setValue(int(self.horizontalSlider.maximum()*height/self.totalHeight))
                self.get_location(self.scrollArea.verticalScrollBar().value())
                self.setWindowTitle(f"阅读器:{os.path.basename(self.last_comic_path)[:-4]},上次阅读到{self.read_pages}页")
            else:
                print_("\t\tload_old_comic没有上次打开信息")
                self.init_self()
                self.file_path = path
                self.open_type = 'load_old_comic_2'
                self.load_images()  # 第一步，先获取所有图片信息
                self.lineEdit.setText("1")
                self.get_location(self.scrollArea.verticalScrollBar().value())  # 第二部展示当前进度应该展示的几张图片
                self.setWindowTitle(f"阅读器:{os.path.basename(self.file_path)[:-4]}")
        else:
            self.init_self()
            self.file_path = path
            self.load_images()  # 第一步，先获取所有图片信息
            self.lineEdit.setText("1")
            self.get_location(self.scrollArea.verticalScrollBar().value())  # 第二部展示当前进度应该展示的几张图片
            print_("load_old_comic上次打开漫画失败")
            pass
        db.close()
        self.jump_to_page()

    def init_self(self):
        print_(f"阅读器：def init_self(self):")
        self.current_index = 0
        self.imageListName = []
        self.totalHeight = 0
        self.labels = {}
        self.size_origin = {}
        self.size_scale = {}
        self.size_scale_height = [0]
        self.first_load_flag = True
        self.show_list = []
        # 清除所有Qlabel
        for child in self.scrollAreaWidgetContents.children():
            if isinstance(child, QLabel):
                self.verticalLayout_2.removeWidget(child)
                # print("child.objectName", child.objectName())
        self.scrollAreaWidgetContents.setFixedHeight(0)

    def on_time_out(self, value):
        print_(f"阅读器：def on_time_out(self, {value})")
        # print("滚动距离为：", value, " 总高度为：", self.totalHeight)
        self.get_location(value)

    # 滚动滚轮事件
    def on_scroll(self):
        # print_(f"阅读器：def on_scroll(self)")
        for i in range(0, len(self.size_scale_height)-1):
            if sum(self.size_scale_height[:i+1]) >= self.scrollArea.verticalScrollBar().value():
                self.lineEdit.setText(str(i+1))
                break
        if self.totalHeight > 0:
            self.horizontalSlider.setValue(int(100*self.scrollArea.verticalScrollBar().value()/self.totalHeight))
        if not self.timer.isActive():
            self.timer.start(100)

    # 判断打开文件是否已经打开过
    def is_opened(self, file):
        print_(f"阅读器：def is_opened(self, {file})")
        db = QSqlDatabase("QSQLITE")
        db.setDatabaseName("userdata/ComicReadInfo.comic")
        db.open()
        query = QSqlQuery(db)
        query.prepare(f"SELECT * FROM comics WHERE path='{file}'")
        if query.exec():
            if query.next():
                db.close()
                return True
        db.close()
        return False

    # 打开单独漫画文件时
    def get_file(self):
        print_(f"阅读器：def get_file(self)")
        last_path = self.settings.value("lastOpenPath", "")
        new_path = QFileDialog.getOpenFileName(self, "选择文件", last_path, filter='*.zip')[0]
        if new_path:
            if not new_path.lower().endswith("zip"):
                QMessageBox.critical(self, "warning", "仅支持ZIP压缩包！")
                return
            # 先更新/保存当前阅读进度
            if self.file_path:
                save_comic_read_info(self.file_path, int(self.lineEdit.text()))
            self.init_self()
            self.file_path = new_path
            # 如果打开以前度过的漫画：
            if self.is_opened(self.file_path):
                self.load_old_comic(self.file_path)
            # 打开全新的漫画
            else:
                self.settings.setValue("lastOpenPath", self.file_path)
                self.open_type = 'get_file'
                self.load_images()  # 第一步，先获取所有图片信息
                self.lineEdit.setText("1")
                self.get_location(self.scrollArea.verticalScrollBar().value())  # 第二部展示当前进度应该展示的几张图片
                self.setWindowTitle(f"阅读器:{os.path.basename(self.file_path)[:-4]}")
        else:
            pass
        self.jump_to_page()

    def fill_contents(self, label):
        self.verticalLayout_2.addWidget(label)

    # 从数据库中加载当前漫画所有页面信息，并加载所有页面对应的label，
    # 但不设置pixmap，只在set_pictures()中更新当前窗口应该展示的页面
    def get_img_name_list_from_database(self, comic_path):
        print_(f"阅读器：def get_img_name_list_from_database(self, {comic_path}):")
        comic_path = replace_path(comic_path)
        db = QSqlDatabase("QSQLITE")
        db.setDatabaseName("userdata/ComicsPagesInfo.comic")
        db.open()
        query = QSqlQuery(db)
        query.exec("""
            CREATE TABLE IF NOT EXISTS ComicsPagesInfo(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                comic_path TEXT NOT NULL,
                page_name TEXT NOT NULL,
                page_width INTEGER NOT NULL,
                page_height INTEGER NOT NULL
            )
        """)
        if query.exec(f"""
            SELECT DISTINCT page_name, page_width, page_height FROM ComicsPagesInfo WHERE comic_path='{comic_path}'
        """):
            try:
                while query.next():
                    self.imageListName.append(query.value(0))
                    self.size_origin[query.value(0)] = [query.value(1), query.value(2)]
                    size = [self.imgWidth, int(query.value(2) * self.imgWidth / query.value(1))]
                    self.size_scale[query.value(0)] = size
                    self.totalHeight += size[1]
                self.imageListName = img_sort(self.imageListName)
                self.label.setText(str(len(self.imageListName)))  # 设置总页数
                if len(self.imageListName) <= 0:
                    return False

                for page_name in self.imageListName:
                    if page_name.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                        label = QLabel()
                        label.setFixedSize(self.size_scale[page_name][0], self.size_scale[page_name][1])
                        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                        label.setStyleSheet(self.background[0])
                        label.setObjectName(page_name)
                        label.setScaledContents(True)
                        self.labels[page_name] = label
                        self.fill_contents(label)
                return True
            except:
                return False
        return False

    # 用于加载展示图片的labels，将漫画所有页面对应的label全不加载，
    # 但不设置pixmap，只在set_pictures()中更新当前窗口应该展示的页面
    def load_images(self):
        print_(f"阅读器：def load_images(self): {self.file_path}")
        no_pages_flag = True
        if is_saved_comic_page_info(self.file_path):  # 如果保留了页面信息
            self.get_img_name_list_from_database(self.file_path)
            no_pages_flag = False
            self.show()
            self.load_finish = True
            self.scrollAreaWidgetContents.setFixedHeight(self.totalHeight)
            # 按图片顺序存储每张图片缩放后的高度
            for i, n in enumerate(self.imageListName):
                self.size_scale_height.append(self.size_scale[n][1])
            pass
        if self.file_path.lower().endswith('.zip') and no_pages_flag:  # 没有保留页面信息，则从zip文件读取图片信息保留
            # 启动子线程初始化页面信息，完成后再调用self.load_old_comic()，即可在数据库中加载数据
            self.load_process.show()
            self.load_process_thread.start()

    # 调整阅读界面的大小
    def resizeEvent(self, event: PySide6.QtGui.QResizeEvent) -> None:
        if not self.resize_timer.isActive():
            self.resize_timer.start(300)
        super().resizeEvent(event)

    # 调整阅读界面的大小
    def resize_timer_event(self):
        print_(f"阅读器：def resize_timer_event(self)")
        # print("界面变化调整")
        if self.totalHeight > 0:
            old_ratio = self.scrollArea.verticalScrollBar().value()/self.totalHeight
        else:
            old_ratio = False
        self.imgWidth = self.scrollArea.width()
        self.totalHeight = 0
        self.size_scale = {}
        self.size_scale_height = [0]
        try:
            for n in self.imageListName:
                self.totalHeight += int(self.size_origin[n][1]*self.imgWidth/self.size_origin[n][0])
                size = [self.imgWidth, int(self.size_origin[n][1]*self.imgWidth/self.size_origin[n][0])]
                self.labels[n].setFixedSize(size[0], size[1])
                self.size_scale[n] = size
                self.size_scale_height.append(size[1])
        except Exception:
            print(f"\t\t阅读器：def resize_timer_event(self)：except {Exception}")
            return
        self.scrollAreaWidgetContents.setFixedHeight(self.totalHeight)
        # print("界面大小变化")
        for n in self.show_list:
            with zipfile.ZipFile(self.file_path, 'r') as zip_ref:
                img = zip_ref.open(n).read()
                pixmap = QPixmap()
                pixmap.loadFromData(img)
                self.labels[n].setPixmap(pixmap)
        if old_ratio:  # 保持当前画面
            self.scrollArea.verticalScrollBar().setValue(self.totalHeight*old_ratio)

    # 计算当前窗口滚动页面对应哪张图片
    def get_location(self, value):
        print_(f"阅读器：def get_location(self, {value}), self.current_index={self.current_index}")
        if self.first_load_flag:  # 判断是否为第一次加载
            self.first_load_flag = False
            self.set_pictures(0)
            return
        # if self.current_index - 1 < 0:
        #     if sum(self.size_scale_height[:self.current_index + 2]) > value:
        #         return
        # elif self.current_index + 1 > len(self.imageListName)-1:
        #     if sum(self.size_scale_height[:self.current_index - 2]) < value:
        #         return
        # else:
        #     if sum(self.size_scale_height[:self.current_index]) < value < sum(self.size_scale_height[:self.current_index+2]):
        #         return
        for i, n in enumerate(self.imageListName):
            if sum(self.size_scale_height[:i+1]) > value:
                self.current_index = i
                self.set_pictures(i-4, 4)  # 只显示当前页面前后4页，共8页。
                return

    # 从zip文件中读取应该显示的图片
    def set_pictures(self, index, list_len=4):
        print_(f"阅读器：def set_pictures(self, {index}, {list_len}):")
        old_show_list = self.show_list
        self.show_list = []
        for i in range(2 * list_len):  # 只显示当前页面前后list_len页，共2*list_len页。
            if index+i < 0 or index + i > len(self.imageListName) - 1:
                pass
            else:
                self.show_list.append(self.imageListName[index+i])
        # print(self.show_list)
        for old_p in old_show_list:
            if old_p not in self.show_list:
                # print("清除old_p ", old_p)
                self.labels[old_p].clear()
        for n in self.show_list:
            if self.labels[n].pixmap():
                # print("存在new_p ", n)
                pass
            else:
                if self.file_path.lower().endswith('.zip'):
                    with zipfile.ZipFile(self.file_path, 'r') as zip_ref:
                        img = zip_ref.open(n).read()
                        pixmap = QPixmap()
                        pixmap.loadFromData(img)
                        self.labels[n].setPixmap(pixmap)

    # 跳转到指定页面
    def jump_to_page(self, j_page=0):
        print_(f"阅读器：def jump_to_page(self):")
        if j_page:
            index = int(self.lineEdit.text())
            height = sum(self.size_scale_height[:index])
            self.scrollArea.verticalScrollBar().setValue(height)
            return
        index = int(self.lineEdit.text())
        height = sum(self.size_scale_height[:index])
        if height < 0:
            self.scrollArea.verticalScrollBar().setValue(0)
            return
        self.scrollArea.verticalScrollBar().setValue(height)

    # 显示进度条和隐藏进度条：
    def show_or_hidden_process(self):
        if self.horizontalSlider.isHidden():
            self.horizontalSlider.setHidden(False)
            self.pushButton_2.setText("隐藏进度")
        else:
            self.horizontalSlider.setHidden(True)
            self.pushButton_2.setText("显示进度")

    # 滑动进度条事件
    def slid_horizontal_slider(self):
        value = self.horizontalSlider.value()
        # if value == self.horizontalSlider.maximum():
        #     self.jump_to_page(int(self.label.text()))
        #     return
        self.scrollArea.verticalScrollBar().setValue(self.totalHeight*(value/self.horizontalSlider.maximum()))

    # 上下左右(W S A D)按钮事件
    def keyPressEvent(self, event: PySide6.QtGui.QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_A:
            self.lineEdit.setText(str(int(self.lineEdit.text())-1))
            self.jump_to_page()
        elif event.key() == Qt.Key.Key_S:
            add_height = int(self.height()*0.3)
            self.scrollArea.verticalScrollBar().setValue(self.scrollArea.verticalScrollBar().value() + add_height)
        elif event.key() == Qt.Key.Key_D:
            self.lineEdit.setText(str(int(self.lineEdit.text()) + 1))
            self.jump_to_page()
        elif event.key() == Qt.Key.Key_W:
            add_height = int(self.height()*0.3)
            self.scrollArea.verticalScrollBar().setValue(self.scrollArea.verticalScrollBar().value() - add_height)
        else:
            pass
        super().keyPressEvent(event)

    # 程序结束前保存此次comic的信息
    def closeEvent(self, event: PySide6.QtGui.QCloseEvent) -> None:
        start = time.time()
        save_comic_read_info(self.file_path, int(self.lineEdit.text()))
        save_read_info_to_comic_list(self.file_path, int(self.lineEdit.text()))
        if self.library_path:
            print("\t\t更新阅读进度到漫画所在库")
            update_read_pages(self.library_path, self.library_name, self.belong_path,
                              self.comic_name, int(self.lineEdit.text()))
        print_(f"阅读器：def closeEvent：保存阅读进度耗时：{time.time()-start}")
        super().closeEvent(event)


# 判断所打开漫画是否保存了每页的宽高信息
def is_saved_comic_page_info(comic_path):
    db = QSqlDatabase("QSQLITE")
    db.setDatabaseName("userdata/ComicsPagesInfo.comic")
    db.open()
    query = QSqlQuery(db)
    query.exec("""
        CREATE TABLE IF NOT EXISTS ComicsPagesInfo(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            comic_path TEXT NOT NULL,
            page_name TEXT NOT NULL,
            page_width INTEGER NOT NULL,
            page_height INTEGER NOT NULL
        )
    """)
    if query.exec(f"""
        SELECT * FROM ComicsPagesInfo WHERE comic_path='{comic_path}'
    """):
        if query.next():
            db.close()
            return True
    db.close()
    return False


# 更新漫画阅读页数到所在库目录下comics.comic
def update_read_pages(library_path, library_name, belong_path, comic_name, read_pages):
    print_(f"阅读器：def update_read_pages({library_path}, {library_name}, {belong_path}, {comic_name}, {read_pages})")
    db = QSqlDatabase("QSQLITE")
    db.setDatabaseName(replace_path(os.path.join(library_path, ".library/comics.comic")))
    db.open()
    query = QSqlQuery(db)
    query_udate = f"""
        UPDATE comics SET read_pages={read_pages} 
        WHERE belong_path='{belong_path}' and library_path='{library_path}' and
        library_name='{library_name}' and name='{comic_name}'
    """
    # print(query_udate)
    if query.exec(query_udate):
        print("\t\t更新进度成功")
    else:
        print(query.lastError())


# 保存本次打开漫画阅读到的页数
def save_comic_read_info(comic_path, read_pages):
    print_(f"阅读器：def save_comic_read_info({comic_path}, {read_pages})")
    db = QSqlDatabase("QSQLITE")
    db.setDatabaseName("userdata/ComicReadInfo.comic")
    db.open()
    query = QSqlQuery(db)
    if 'comics' not in db.tables():
        query.exec("""
        CREATE TABLE comics(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        path TEXT NOT NULL,
        read_pages INTEGER
        );
        """)
    query.exec(f"""
        SELECT * FROM comics WHERE path='{comic_path}' 
    """)
    if not query.next():
        query.exec(f"""
        INSERT INTO comics (path, read_pages)
        VALUES('{comic_path}',{read_pages});
        """)
    else:
        query.exec(f"""
                    UPDATE comics SET read_pages={read_pages} WHERE path='{comic_path}';
                """)
        # print("更新 comics 成功")
    if "recent" not in db.tables():
        query.exec("""
            CREATE TABLE recent(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT NOT NULL,
            read_pages INTEGER
            );
        """)
    query.exec(f"""
        SELECT * FROM recent where id=1;
        """)
    if not query.next():
        query.exec(f"""
            INSERT INTO recent (path, read_pages)
            VALUES('{comic_path}',{read_pages});
        """)
    else:
        query.exec(f"""
            UPDATE recent SET path='{comic_path}', read_pages={read_pages}
            WHERE id=1;
        """)
        # print("更新 recent 成功")
    db.close()


def save_read_info_to_comic_list(comic_path, read_pages):
    print_(f"阅读器：def save_read_info_to_comic_list({comic_path}, {read_pages})")
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
                WHERE comic_path='{comic_path}'
            """
    q.prepare(query_search)
    if q.exec():
        if q.next():
            q.exec(f"""
                        UPDATE comics SET read_pages={read_pages}
                        WHERE comic_path='{comic_path}'
                    """)
    qsl_db.close()


def print_(str_, flag=False):
    if flag:
        print(str_)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = ImageViewer(load_last=False)
    viewer.show()
    app.exec()
