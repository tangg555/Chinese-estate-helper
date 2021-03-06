import sys
sys.path.insert(0, '..') # 在tasks文件夹中可以直接运行程序

from src.modules.lianjia.lianjia_mysql import LianJiaMySQL


class LianJiaSqliteTask(object):
    @classmethod
    def run(cls):
        downloader = LianJiaMySQL()
        city = '上海'
        downloader.create_tables(city)
        downloader.insert_districts(city)
        downloader.insert_communities(city)
        downloader.insert_houses(city)


if __name__ == '__main__':
    LianJiaSqliteTask.run()
