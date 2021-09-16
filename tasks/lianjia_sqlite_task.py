from src.modules.lianjia_sqlite import LianjiaSqliteDownloader


class LianjiaSqliteTask(object):
    @classmethod
    def run(cls):
        downloader = LianjiaSqliteDownloader()
        city = '上海'
        downloader.save_city_border_to_db(city)
        downloader.hole_city_down(city)
        downloader.get_complete_housing_info(city)


if __name__ == '__main__':
    LianjiaSqliteTask.run()
