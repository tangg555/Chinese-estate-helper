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
from .logger import MyLogger
from .constants import LianJiaConsts
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
                  insert ignore into {city}_district
                  (id, name, longitude,latitude,border,unit_price,count)
                  values
                  {', '.join(sql_values)};
                  '''
        self.logger.info("bulk_sql组装完毕......")
        self.cursor.execute(bulk_sql)
        self.logger.info("Districts inserted......")
        self.db_close_with_commit()

    def insert_communities(self, city):
        self.db_connect()

        areas = self.abuilder.table(f'{city}_district').field("border, name").query()
        self.logger.info(f"遍历{city}市的{len(areas)}个区域......")
        for count, area in enumerate(areas):
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

            sql_values = []
            self.logger.info("Insert communities......")
            for square in tqdm(squares, desc=f'{city}市 {district_name}区 组装communitie sqls中......'):
                communities = self.parser.get_communities(city, square[0], square[1], square[2], square[3])
                for community in communities:
                    unit_price = 0 if not community["unit_price"] else community["unit_price"]
                    sql = f'("{community["id"]}", "{community["name"]}", "{community["longitude"]}", \
                         "{community["latitude"]}", "{unit_price}", "{community["count"]}")'
                    sql_values.append(sql)
            bulk_sql = f''' 
                      insert ignore into {city}_community
                      (id, name, longitude, latitude, unit_price, count)
                      values
                      {', '.join(sql_values)};
                      '''
            self.logger.info("bulk_sql组装完毕......")
            self.cursor.execute(bulk_sql)
            self.logger.info("Communities inserted......")
            # 提交事务:
            self.conn.commit()
            self.logger.info(f"遍历{city}市的{len(areas)}个区域， 完成进度{count + 1}/{len(areas)}")
        self.db_close_without_commit()
