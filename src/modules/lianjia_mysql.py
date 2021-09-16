"""
@Reference:
ABuilder 对MySQL的链式操作
https://github.com/lizhenggan/ABuilder
"""

import numpy
import pymysql
from tqdm import tqdm
from logging import DEBUG
from ABuilder.ABuilder import ABuilder
from .lianjia_parser import LianJiaParser
from src.modules.logger import MyLogger
from src.modules.constants import LianJiaConsts
from src.configuration.mysql_cfg import MySQLCFG



class LianJiaMySQL(object):
    _class_name = "LianJia MySQL"

    def __init__(self):
        self.logger = MyLogger(self._class_name, DEBUG)
        self.parser = LianJiaParser()
        self.abuilder = ABuilder()

        self.conn = None
        self.cursor = None

    def db_connect(self):
        self.conn = pymysql.connect(host=MySQLCFG.HOST,
                                    port=MySQLCFG.PORT,
                                    user=MySQLCFG.USER,
                                    password=MySQLCFG.PASSWORD,
                                    db=MySQLCFG.DB,
                                    charset='utf8mb4')
        self.cursor = self.conn.cursor()

    def db_close_with_commit(self):
        self.cursor.close()
        # 提交事务:
        self.conn.commit()
        # 关闭Connection:
        self.conn.close()

    def db_close_without_commit(self):
        self.cursor.close()
        # 关闭Connection:
        self.conn.close()

    def create_tables(self, city: str):
        self.db_connect()
        # cities
        self.cursor.execute(LianJiaConsts.DISTRICTS_CREATE_SQL_TEMPLATE % city)
        # areas
        self.cursor.execute(LianJiaConsts.COMMUNITIES_CREATE_SQL_TEMPLATE % city)
        # # houses
        # self.cursor.execute(LianJiaConsts.HOUSE_CREATE_SQL_TEMPLATE % city)
        self.db_close_with_commit()

    def insert_districts(self, city):
        """
        +--------------+------------+
        | name         | unit_price |
        +--------------+------------+
        | 黄浦         |      80305 |
        | 徐汇         |      90880 |
        ......
        """
        self.db_connect()

        self.logger.info(f'解析{city}的地区...')
        districts = self.parser.get_districts(city)
        self.logger.info(f'解析{city}的地区 完毕！')
        sql_values = []
        self.logger.info("Insert districts......")
        for district in districts:
            unit_price = 0 if not district["unit_price"] else district["unit_price"]
            sql = f'("{district["id"]}", "{district["name"]}", "{district["longitude"]}", \
                 "{district["latitude"]}", "{district["border"]}", \
                 "{unit_price}", "{district["count"]}")'
            sql_values.append(sql)
        bulk_sql = f''' 
                  insert into {city}_district
                  (id, name, longitude,latitude,border,unit_price,count)
                  values
                  {', '.join(sql_values)};
                  '''
        self.logger.info("Sqls assembled......")
        self.cursor.execute(bulk_sql)
        self.logger.info("Districts inserted......")
        self.db_close_with_commit()

    def insert_communities(self, city):
        areas = self.abuilder.table(f'{city}_district').field("border, name").query()
        for area in areas:
            lat = []
            lng = []
            district_name = area["name"]
            district_border = area["border"]
            for coordinate in district_border.split(';'):
                lng.append(float(coordinate.split(',')[0]))
                lat.append(float(coordinate.split(',')[1]))
            squares = []
            step = 0.02
            for x in numpy.arange(min(lng), max(lng), step):
                for y in numpy.arange(min(lat), max(lat), step):
                    squares.append((round(y, 6), round(y - step, 6), round(x, 6), round(x - step, 6)))

            for square in squares:
                communities = self..parser.get_communities(city, square[0], square[1], square[2], square[3])
                for community in communities:
                    # try:
                    #     sql = ''' insert into %s
                    #              (id, name, district,longitude,latitude,unit_price,count)
                    #              values
                    #              (:id, :name, :district,:longitude, :latitude, :unit_price, :count)
                    #              ''' % city
                    #     community.update({'district': district_name})
                    #     cursor.execute(sql, z)
                    #     conn.commit()
                    #
                    #     pbar.set_description(district_name + community['name'] + '已导入')
                    # except:
                    #
                    #     pbar.set_description(district_name + community['name'] + '住房已存在')
                    pass
