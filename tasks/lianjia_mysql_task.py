from src.modules.lianjia_mysql import LianJiaMySQL


class LianJiaSqliteTask(object):
    @classmethod
    def run(cls):
        downloader = LianJiaMySQL()
        city = '上海'
        # downloader.create_tables(city)
        # downloader.insert_districts(city)



if __name__ == '__main__':
    LianJiaSqliteTask.run()