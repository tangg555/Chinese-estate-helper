"""
@Desc:
@Reference:
MySQL链式操作工具
https://github.com/lizhenggan/ABuilder
"""

import os
from ABuilder.ABuilder import ABuilder
from src.modules.views.map_view import MapView
from src.modules.lianjia.houses import House, HouseList
from src.modules.lianjia.communities import Community, CommunityList
from src.modules.lianjia.districts import District, DistrictList


class BasicTask(object):
    @classmethod
    def run(cls):
        city = "上海"
        data = ABuilder().table(f'{city}_district').query()
        districts = cls.list_to_districts(data, city)
        key_vals = [[one.name, one.unit_price] for one in districts.items()]
        MapView.city_draw(city, key_vals)

    @classmethod
    def dict_to_house(cls, result: dict, city: str):
        return House(result, city)

    @classmethod
    def list_to_houses(cls, result: list, city: str):
        house_list = []
        for one in result:
            house_list.append(cls.dict_to_house(one, city))
        return HouseList(houses=house_list)

    @classmethod
    def dict_to_community(cls, result: dict, city: str):
        return Community(result, city)

    @classmethod
    def list_to_communities(cls, result: list, city: str):
        community_list = []
        for one in result:
            community_list.append(cls.dict_to_community(one, city))
        return CommunityList(communities=community_list)

    @classmethod
    def dict_to_district(cls, result: dict, city: str):
        return District(result, city)

    @classmethod
    def list_to_districts(cls, result: list, city: str):
        district_list = []
        for one in result:
            district_list.append(cls.dict_to_district(one, city))
        return DistrictList(districts=district_list)


if __name__ == '__main__':
    BasicTask.run()
