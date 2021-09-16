import requests
import time
import json
import math
import os

from .constants import LianJiaConsts, CACHE_DIR
from src.common.parser_tools import ParserTools
from .logger import MyLogger, DEBUG
from .cache import LocalCache


class LianJiaParser(object):
    _class_name = "LianJia Api Parser"

    def __init__(self, cache_enable=True, cache_dir=CACHE_DIR, log_path=''):
        self.city_dict = LianJiaConsts.CITY_DICT
        self.url_fang = LianJiaConsts.HOUSE_AJAX_GET_TEMPLATE

        self.url = LianJiaConsts.AJAX_GET_TEMPLATE

        self.cookies = LianJiaConsts.COOKIES

        self.headers = LianJiaConsts.HEADERS

        self.gen_md5 = ParserTools.generate_md5

        self.logger = MyLogger(self._class_name, DEBUG, log_path)

        self.cache_enable = cache_enable
        if self.cache_enable:
            self.cache = LocalCache('lianjia_parser', cache_dir, self.logger)
            self.cache.smart_load()
        else:
            self.cache = None

    def get_authorization(self, dict_) -> str:
        data_str = "vfkpbin1ix2rb88gfjebs0f60cbvhedlcity_id={city_id}group_type={group_type}max_lat={max_lat}" \
                   "max_lng={max_lng}min_lat={min_lat}min_lng={min_lng}request_ts={request_ts}".format(
                    city_id=dict_["city_id"],
                    group_type=dict_["group_type"],
                    max_lat=dict_["max_lat"],
                    max_lng=dict_["max_lng"],
                    min_lat=dict_["min_lat"],
                    min_lng=dict_["min_lng"],
                    request_ts=dict_["request_ts"])
        authorization = self.gen_md5(data_str)
        return authorization

    def get_districts(self, city) -> list:
        """
        :str max_lat: 最大经度 六位小数str型max_lat='40.074766'
        :str min_lat: 最小经度 六位小数str型min_lat='39.609408'
        :str max_lng: 最大纬度 六位小数str型max_lng='40.074766'
        :str min_lng: 最小纬度 六位小数str型min_lng='39.609408'
        :str city_id: 北京:110000  上海:310000
        #获取上海的各个区域，例如浦东，长宁，徐汇
        :return: list

        [{'id': 310115, 'name': '浦东', 'longitude': 121.60653130552, 'latitude': 31.208001618509,
        'border': '121.54148868942,31.347913060234', 'unit_price': 58193, 'count': 18866},
        {'id': 310112, 'name': '闵行', 'longitude': 121.40817118429, 'latitude': 31.091185835136,
        'border': '121.34040533465,31.037672798655;121.34022400061,31.022622576909;
        121.33932297393,31.020472421859;121.35006370183,31.020640362869',
        'unit_price': 51866, 'count': 9024},
        .........
        """
        time_13 = int(round(time.time() * 1000))
        authorization = self.get_authorization(
            {'group_type': 'district',
             'city_id': self.city_dict[city]['city_id'],
             'max_lat': self.city_dict[city]['max_lat'],
             'min_lat': self.city_dict[city]['min_lat'],
             'max_lng': self.city_dict[city]['max_lng'],
             'min_lng': self.city_dict[city]['min_lng'],
             'request_ts': time_13})

        url = self.url % (
            self.city_dict[city]['city_id'], 'district', self.city_dict[city]['max_lat'],
            self.city_dict[city]['min_lat'], self.city_dict[city]['max_lng'], self.city_dict[city]['min_lng'],
            '%7B%7D', time_13, authorization, time_13)

        with requests.Session() as sess:
            ret = sess.get(url=url, headers=self.headers, cookies=self.cookies)

            house_json = json.loads(ret.text[43:-1])

            if house_json['errno'] == 0:
                districts = house_json['data']['list'].values()
                return districts

            else:
                return []

    def get_communities(self, city, max_lat, min_lat, max_lng, min_lng) -> list:
        """
        :param city: String 如：上海
        :param max_lat: String 最大经度 六位小数str型max_lat='40.074766'
        :param min_lat: String 最小经度 六位小数str型min_lat='39.609408'
        :param max_lng: String 最大纬度 六位小数str型max_lng='40.074766'
        :param min_lng: String 最小纬度 六位小数str型min_lng='39.609408'
        :return: list
        e.g.
        [{'id': '5011000012693', 'name': '陈湾小区', 'longitude': 121.455211, 'latitude': 30.966981,
        'unit_price': 24407, 'count': 9}]
        """
        city_id = self.city_dict[city]['city_id']
        time_13 = int(round(time.time() * 1000))
        authorization = self.get_authorization(
            {'group_type': 'community', 'city_id': city_id, 'max_lat': max_lat, 'min_lat': min_lat,
             'max_lng': max_lng, 'min_lng': min_lng, 'request_ts': time_13})
        url = self.url % (
            city_id, 'community', max_lat, min_lat, max_lng, min_lng, '%7B%7D', time_13, authorization, time_13)
        with requests.Session() as sess:
            ret = sess.get(url=url, headers=self.headers, cookies=self.cookies)
            house_json = json.loads(ret.text[43:-1])
            if house_json['errno'] == 0:
                data_list = []
                if type(house_json['data']['list']) is dict:
                    for x in house_json['data']['list']:
                        data_list.append(house_json['data']['list'][x])
                    return data_list
                else:
                    return house_json['data']['list']
            else:
                return []

    def get_houses(self, id, count) -> list:
        house_infos = []
        for page in range(1, math.ceil(count / 10) + 1):
            time_13 = int(round(time.time() * 1000))
            authorization = self.gen_md5(
                "vfkpbin1ix2rb88gfjebs0f60cbvhedlid={id}order={order}page={page}request_ts={request_ts}".format(
                    id=id, order=0, page=1, request_ts=time_13))
            url = self.url_fang % (id, page, '%7B%7D', time_13, authorization, time_13)
            with requests.Session() as sess:
                ret = sess.get(url=url, headers=self.headers, cookies=self.cookies)

                house_json = json.loads(ret.text[41:-1])

                for x in house_json['data']['ershoufang_info']['list']:
                    house_infos.append(house_json['data']['ershoufang_info']['list'][x])
        return house_infos
