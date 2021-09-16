"""
@Reference:
"""

import os
import itertools
import pymysql
from tqdm import tqdm
from logging import DEBUG
from .lianjia_parser import LianJiaParser
from src.modules.logger import MyLogger
from src.modules.constants import LianJiaConsts
from src.configuration.mysql_cfg import MySQLCFG



class LianJiaMySQL(object):
    _class_name = "LianJia MySQL"

    def __init__(self):
        self.logger = MyLogger(self._class_name, DEBUG)
        self.parser = LianJiaParser()

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
