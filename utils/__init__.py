import os
from PySide6.QtWidgets import (QWidget, QScrollArea, QSplitter, QApplication, QHBoxLayout, QPushButton, QVBoxLayout,
                               QListWidget, QFileDialog, QMenu, QMessageBox, QLabel, QGridLayout, QCheckBox,
                               QAbstractButton, QFontDialog)
from PySide6.QtCore import Qt, QObject, QEvent, QSize, Signal, Slot, QPoint, QTimer
from PySide6.QtGui import QMouseEvent, QFont
from PySide6.QtSql import *
from PySide6.QtGui import QIcon, QPixmap, QResizeEvent, QAction, QCursor
import PySide6
import re

# 漫画图片的类型，按需追加
IMG_TYPE = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp')


# 保存漫画每页的宽高信息
def save_comic_pages_info(comic_path, page_name, page_width, page_height):
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
    query.exec(f"""
        INSERT INTO ComicsPagesInfo(comic_path, page_name, page_width, page_height)
        VALUES('{comic_path}', '{page_name}', '{page_width}','{page_height}')
    """)
    db.close()


# 检查指定库中是否存在该comic
def check_exist_comic(library_info_path, comic_name, belong_path, library_name):
    db = QSqlDatabase("QSQLITE")
    db.setDatabaseName(replace_path(os.path.join(library_info_path, "comics.comic")))
    if db.open():
        query = QSqlQuery(db)
        if "comics" not in db.tables():
            db.exec("""
                   CREATE TABLE IF NOT EXISTS comics(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT NOT NULL,
                       library_path TEXT NOT NULL,
                       library_info_path TEXT NOT NULL,
                       pages INTEGER NOT NULL,
                       belong_path TEXT NOT NULL,
                       dir_name TEXT NOT NULL,
                       library_name TEXT NOT NULL,
                       cover TEXT,
                       read_pages INTEGER DEFAULT 0,
                       collected BOOLEAN DEFAULT 0
                   )
               """)
        # 如果已经存在相同信息，提前返回：用于更新库信息时
        query.exec(f"""
           SELECT * FROM comics 
           WHERE name = '{comic_name}' AND belong_path='{belong_path}' AND library_name='{library_name}'
           """)
        if query.next():
            db.close()
            return [True, f'已有：{library_name}, {comic_name}, {belong_path}']
        else:
            db.close()
            return [False, None]


# 保存漫画所属库、封面等信息
def save_comic_info(cover, belong_path, library_info_path, pages,
                    comic_name, dir_name, library_name, library_path):
    db = QSqlDatabase("QSQLITE")
    db.setDatabaseName(replace_path(os.path.join(library_info_path, "comics.comic")))
    t = ''
    if db.open():
        query = QSqlQuery(db)
        if "comics" not in db.tables():
            db.exec("""
                CREATE TABLE IF NOT EXISTS comics(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    library_path TEXT NOT NULL,
                    library_info_path TEXT NOT NULL,
                    pages INTEGER NOT NULL,
                    belong_path TEXT NOT NULL,
                    dir_name TEXT NOT NULL,
                    library_name TEXT NOT NULL,
                    cover TEXT,
                    read_pages INTEGER DEFAULT 0,
                    collected BOOLEAN DEFAULT 0
                )
            """)
        # 如果已经存在相同信息，提前返回：用于更新库信息时
        query.exec(f"""
        SELECT * FROM comics 
        WHERE name = '{comic_name}' AND belong_path='{belong_path}' AND library_name='{library_name}'
        """)
        if not query.next():
            # print(f"""
            # INSERT INTO comics (name,library_path,library_info_path,belong_path,pages,dir_name,library_name,cover)
            # VALUES ('{comic_name}','{library_path}','{library_info_path}',
            # '{belong_path}',{pages},'{dir_name}','{library_name}','{cover}')
            # """)
            # print(f'utils save_comic_info line69: \n    新增：{library_name}, {comic_name}, {belong_path}')
            t = f'新增: library:{library_name}, comic:{comic_name}, path:{belong_path}'
            query.exec(f"""
            INSERT INTO comics (name,library_path,library_info_path,belong_path,pages,dir_name,library_name,cover) 
            VALUES ('{comic_name}','{library_path}','{library_info_path}',
            '{belong_path}',{pages},'{dir_name}','{library_name}','{cover}')
            """)
        else:
            t = f'已有: library:{library_name}, comic:{comic_name}, path:{belong_path}'
    db.close()
    return t


# 获取阅读列表名称
def get_list_names():
    list_names = []
    db = QSqlDatabase("QSQLITE")
    db.setDatabaseName("userdata/ComicList.comic")
    db.open()
    query = QSqlQuery(db)
    query.exec("select name from list_name")
    while query.next():
        list_names.append(query.value(0))
    return list_names


# 获取阅读列表名称
def get_list_names_except_added_list(comic_path):
    list_names = []
    db = QSqlDatabase("QSQLITE")
    db.setDatabaseName("userdata/ComicList.comic")
    db.open()
    query = QSqlQuery(db)
    query.exec(f"""
        SELECT name FROM list_name WHERE name
        NOT IN 
        (select DISTINCT list_name from comics WHERE comic_path='{comic_path}')
    """)
    while query.next():
        list_names.append(query.value(0))
    return list_names


# 创建新的阅读列表
def create_list(name):
    db = QSqlDatabase("QSQLITE")
    db.setDatabaseName("userdata/ComicList.comic")
    db.open()
    query = QSqlQuery(db)
    query.exec(f"select * from list_name WHERE name='{name}'")
    if query.next():
        return False
    if query.exec(f"INSERT INTO list_name(name) VALUES('{name}')"):
        return True


# 无需返回值的常规数据库操作
def database_operate(s, database):
    db = QSqlDatabase("QSQLITE")
    db.setDatabaseName(database)
    query = QSqlQuery(db)
    if db.open():
        if query.exec(s):
            db.close()
            return True
        else:
            db.close()
            return False


# 对图片进行排序
def img_sort(img_list):
    def extract_numbers_first(filename):
        # 使用正则表达式匹配所有数字序列-对每一章的图片相对排序
        filename = filename.split("/")[-1]
        numbers = re.findall(r'\d+', filename)
        if numbers:
            first_number = int(numbers[0])
            return first_number
        else:
            return 0

    def extract_numbers_last(filename):
        # 使用正则表达式匹配所有数字序列-利用排序算法的稳定性对章节排序后，各章图片相对顺序不变
        numbers = re.findall(r'\d+', filename)
        if numbers:
            last_number = int(numbers[-1])
            return last_number
        else:
            return 0
    img_star_with_number = []
    img_star_with_str = []
    for n in img_list:
        name = os.path.basename(n)
        if re.match(r'^\d', name):
            img_star_with_number.append(n)
        else:
            img_star_with_str.append(n)
    # 根据提取的数字对文件名进行排序
    img_star_with_number = sorted(img_star_with_number, key=extract_numbers_last)
    img_star_with_number = sorted(img_star_with_number, key=extract_numbers_first)
    img_star_with_str = sorted(img_star_with_str, key=extract_numbers_first)
    img_star_with_str = sorted(img_star_with_str, key=extract_numbers_last)
    return img_star_with_number+img_star_with_str
    # img_list = sorted(img_list, key=extract_numbers_last)
    # img_list = sorted(img_list, key=extract_numbers_first)
    # return img_list


# 替换字符串中的\
def replace_path(old_path):
    # print("替换\\为/：\n", old_path, '\n', old_path.replace("\\", "/"))
    return old_path.replace("\\", "/")


# 更新阅读列表中漫画的阅读进度
def update_info_to_comic_list(comic_path, read_pages):
    sql = QSqlDatabase("QSQLITE")
    sql.setDatabaseName("userdata/ComicList.comic")
    if sql.open():
        if 'comic_list' not in sql.tables():
            sql.exec("""
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
        print("打开成功")
        q = QSqlQuery(sql)
        q.exec(f"SELECT * FROM comics WHERE comic_path='{comic_path}'")
        if q.next():
            q.exec(f"UPDATE comics SET read_pages={read_pages} WHERE comic_path='{comic_path}")
    else:
        print("打开失败")


# 向阅读列表中添加漫画
def insert_info_to_comic_list(list_name, comic_name, comic_path, cover_path, collected, pages, read_pages):
    sql = QSqlDatabase("QSQLITE")
    sql.setDatabaseName("userdata/ComicList.comic")
    if sql.open():
        if 'comic_list' not in sql.tables():
            sql.exec("""
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

        print("打开成功")
        q = QSqlQuery(sql)
        q.exec(f"SELECT * FROM comics WHERE comic_path='{comic_path}' AND list_name='{list_name}'")
        if q.next():
            return False

        if q.exec(f"""
            INSERT INTO comics(list_name,comic_name,comic_path,cover_path,collected,pages,read_pages) 
            VALUES('{list_name}', '{comic_name}','{comic_path}','{cover_path}',{collected},{pages},{read_pages})
        """):
            return True
    return False


def delete_comic_list(list_name):
    sql = QSqlDatabase("QSQLITE")
    sql.setDatabaseName("userdata/ComicList.comic")
    if sql.open():
        print("打开成功")
        q = QSqlQuery(sql)
        q.exec(f"DELETE FROM comics WHERE list_name='{list_name}'")
        q.exec(f"DELETE FROM list_name WHERE name='{list_name}'")
    sql.close()


def search_comics_from_library(search_content, library, library_name=None):
    info_list = []
    db = QSqlDatabase("QSQLITE")
    db.setDatabaseName(library)
    db.open()
    query = QSqlQuery(db)
    if not library_name:
        sub_query = ''
    else:
        sub_query = f" AND library_name='{library_name}'"
    query.prepare(f"""
        SELECT DISTINCT belong_path, name, cover, collected, library_path, library_name, read_pages, pages
        FROM comics 
        WHERE name LIKE '%{search_content}%'{sub_query}
        ORDER BY name
    """)
    query.exec()
    while query.next():
        # print(f"查询到：{query.value(0)}, {query.value(1)}, {query.value(5), query.value(6), query.value(7)}")
        info_list.append([replace_path(os.path.join(query.value(0), query.value(1))),
                          query.value(1), query.value(2), query.value(3), query.value(4),
                          query.value(5), query.value(0), query.value(6), query.value(7)])
    db.close()
    return info_list


# 从当前库中选择文件夹
def get_all_dirs_from_library(comic_info_db_path, library_name, filter_=None):
    info_list = []
    db = QSqlDatabase("QSQLITE")
    db.setDatabaseName(comic_info_db_path)
    db.open()
    query = QSqlQuery(db)
    if filter_:
        sub_query = f" AND name LIKE '%{filter_}%'"
    else:
        sub_query = f''
    query.exec(f"""
        SELECT DISTINCT dir_name, belong_path, library_name  
        FROM comics 
        WHERE library_name='{library_name}'{sub_query}
        ORDER BY dir_name
    """)
    while query.next():
        dir_name = query.value("dir_name")
        belong_path = query.value("belong_path")
        library_name = query.value("library_name")
        info_list.append([dir_name, belong_path, library_name])
    db.close()
    return info_list


# 从库中选择文件夹, 返回列表。引用：LMidUtils：update_item_from_list(dir_info_list):
def get_all_dirs_from_all_library(comic_info_db_path, filter_=None):
    info_list = []
    db = QSqlDatabase("QSQLITE")
    db.setDatabaseName(comic_info_db_path)
    db.open()
    query = QSqlQuery(db)
    if filter_:
        sub_query = f"WHERE name LIKE '%{filter_}%'"
    else:
        sub_query = f''
    query.exec(f"""
        SELECT DISTINCT dir_name, belong_path, library_name  
        FROM comics 
        {sub_query}
        ORDER BY dir_name
    """)
    while query.next():
        dir_name = query.value("dir_name")
        belong_path = query.value("belong_path")
        library_name = query.value("library_name")
        info_list.append([dir_name, belong_path, library_name, comic_info_db_path])
    db.close()
    return info_list


def search_comics_from_list(search_content, list_name):
    info_list = []
    db = QSqlDatabase("QSQLITE")
    db.setDatabaseName("userdata/ComicList.comic")
    db.open()
    query = QSqlQuery(db)
    sub_query = " and collected=1" if list_name == '收藏' else ""
    query.exec(f"""
                    SELECT list_name,comic_name,comic_path,cover_path,collected,pages,read_pages 
                    FROM comics 
                    WHERE list_name='{list_name}'{sub_query} AND comic_name LIKE '%{search_content}%'
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
    db.close()
    return info_list


# 重命名阅读列表
def rename_list(new_list_name, old_list_name):
    if new_list_name == old_list_name:
        return False
    if new_list_name == "收藏":
        return False
    db = QSqlDatabase("QSQLITE")
    db.setDatabaseName("userdata/ComicList.comic")
    db.open()
    query = QSqlQuery(db)
    query.exec(f"""SELECT name FROM list_name WHERE list_name='{new_list_name}'""")
    if query.next():
        db.close()
        return False
    if query.exec(f"UPDATE list_name SET name='{new_list_name}' WHERE name='{old_list_name}'"):
        if query.exec(f"UPDATE comics SET list_name='{new_list_name}' WHERE list_name='{old_list_name}'"):
            db.close()
            return True
    return False


# 更新库时，删除因更改文件名、删除文件而导致的数据库中找不到的漫画
def delete_not_exist_comic_from_library(library_info_path, library_name):
    db = QSqlDatabase("QSQLITE")
    db.setDatabaseName(replace_path(os.path.join(library_info_path, "comics.comic")))
    print(library_info_path, library_name)
    if db.open():
        query = QSqlQuery(db)
        query_delete = QSqlQuery(db)
        if "comics" not in db.tables():
            db.exec("""
                       CREATE TABLE IF NOT EXISTS comics(
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           name TEXT NOT NULL,
                           library_path TEXT NOT NULL,
                           library_info_path TEXT NOT NULL,
                           pages INTEGER NOT NULL,
                           belong_path TEXT NOT NULL,
                           dir_name TEXT NOT NULL,
                           library_name TEXT NOT NULL,
                           cover TEXT,
                           read_pages INTEGER DEFAULT 0,
                           collected BOOLEAN DEFAULT 0
                       )
                   """)
            # return
        # 如果已经存在相同信息，提前返回：用于更新库信息时
        query.exec(f"""
               SELECT * FROM comics 
               WHERE library_name = '{library_name}'
               """)

        while query.next():
            # print("----", query.value('id'), query.value('belong_path'), query.value('name'))
            if not os.path.exists(os.path.join(query.value('belong_path'), query.value('name'))):
                query_delete.exec(f"DELETE FROM comics WHERE id={query.value('id')}")

        db.close()
        return


def print_or_not(strs, p=True):
    if p:
        print(strs)
