import sys
sys.path.insert(0, '..') # 在tasks文件夹中可以直接运行程序

from src.modules.lianjia.lianjia_sqlite import LianJiaSqlite


class LianJiaSqliteTask(object):
    @classmethod
    def run(cls):
        downloader = LianJiaSqlite()
        city = '上海'
        downloader.save_districts(city)
        downloader.save_communities(city)
        downloader.save_houses(city)


if __name__ == '__main__':
    LianJiaSqliteTask.run()
