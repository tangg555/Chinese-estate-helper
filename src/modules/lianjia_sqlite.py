import sqlite3
import numpy
import tqdm
from .lianjia_parser import LianJiaParser
from .constants import LianJiaConsts


class LianjiaSqliteDownloader(object):
    @classmethod
    def save_city_border_to_db(cls, city):
        """
        保存city的所有区域边缘经纬度并保存在目录下district.db文件内
        """
        ret = LianJiaParser(city).get_district_info()
        conn = sqlite3.connect('district.db')  # 链接数据库
        cursor = conn.cursor()

        # 创建城市便捷table
        cursor.execute(LianJiaConsts.CITY_CREATE_SQL_TEMPLATE % city)

        pbar = tqdm.tqdm(ret)
        for x in pbar:
            sql = ''' 
                insert into %s
                (id, name, longitude,latitude,border,unit_price,count)
                values
                (:id, :name, :longitude, :latitude, :border, :unit_price, :count)
                ''' % city
            try:
                cursor.execute(sql, x)
                conn.commit()
                pbar.set_description(x['name'] + '已导入')
            except Exception:
                pbar.set_description(x['name'] + '已存在')

        cursor.close()

    @classmethod
    def hole_city_down(cls, city):
        """
        保存市区内所有在售楼盘的信息并保存在目录下LianJia_area.db文件内
        """
        with sqlite3.connect('district.db') as conn:
            c = conn.cursor()
            c.execute('SELECT border,name FROM %s' % city)
            area_list = c.fetchall()

        conn = sqlite3.connect('LianJia_area.db')
        cursor = conn.cursor()

        cursor.execute(LianJiaConsts.CITY_CREATE_SQL_TEMPLATE % city)

        for x in area_list:
            lat = []
            lng = []
            district = x[1]
            for y in x[0].split(';'):
                lng.append(float(y.split(',')[0]))
                lat.append(float(y.split(',')[1]))
            li = []
            step = 0.02
            for x in numpy.arange(min(lng), max(lng), step):
                for y in numpy.arange(min(lat), max(lat), step):
                    li.append((round(y, 6), round(y - step, 6), round(x, 6), round(x - step, 6)))
            pbar = tqdm.tqdm(li)
            for x in pbar:

                ret = LianJiaParser(city).get_community_info(x[0], x[1], x[2], x[3])

                if ret is not None:
                    for z in ret:
                        try:
                            sql = ''' insert into %s
                                     (id, name, district,longitude,latitude,unit_price,count)
                                     values
                                     (:id, :name, :district,:longitude, :latitude, :unit_price, :count)
                                     ''' % city
                            z.update({'district': district})
                            cursor.execute(sql, z)
                            conn.commit()

                            pbar.set_description(district + z['name'] + '已导入')
                        except Exception:
                            pbar.set_description(district + z['name'] + '住房已存在')

    @classmethod
    def get_complete_housing_info(cls, city):
        """
        保存市区内所有在售楼盘的信息并保存在目录下LianJia_area.db文件内
        """
        with sqlite3.connect('DetailInfo.db') as conn1:
            cursor1 = conn1.cursor()
            cursor1.execute(LianJiaConsts.DETAIL_INFO_CREATE_SQL_TEMPLATE % city)

        with sqlite3.connect('LianJia_area.db') as conn:
            c = conn.cursor()
            c.execute('SELECT id,count FROM %s' % city)
            area_list = c.fetchall()

        pbar = tqdm.tqdm(area_list)
        for x in pbar:
            ret = LianJiaParser(city).get_house_info(x[0], x[1])
            with sqlite3.connect('DetailInfo.db') as conn:
                cursor = conn.cursor()
                for y in ret:
                    try:
                        sql = LianJiaConsts.DETAIL_INFO_INSERT_SQL_TEMPLATE % city
                        y['house_video_info'] = str(y['house_video_info'])
                        y['tags'] = str(y['tags'])
                        cursor.execute(sql, y)
                        conn.commit()
                        pbar.set_description(y['title'] + '已导入')
                    except Exception:
                        pbar.set_description(y['title'] + '已存在')
