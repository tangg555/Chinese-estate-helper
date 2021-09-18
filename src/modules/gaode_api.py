import requests
import json
from src.configuration.gaode_api_cfg import GaodeApiCFG

class Coordinate(object):
    def __init__(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude

class GaodeApi(object):
    api_url = 'https://restapi.amap.com/v3/geocode/geo'  # 输入API问号前固定不变的部分

    @classmethod
    def geo_encode(cls, address: str):
        params = {'key': f'{GaodeApiCFG.KEY}',
                  'address': f'{address}'}  # 将两个参数放入字典
        res = requests.get(cls.api_url, params)
        jd = json.loads(res.text)  # 将json数据转化为Python字典格式
        coordinates = jd['geocodes'][0]['location'].strip().split(',')
        return Coordinate(coordinates[0], coordinates[1])
