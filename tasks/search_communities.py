"""
@Desc:
@Reference:
MySQL链式操作工具
https://github.com/lizhenggan/ABuilder
"""

from ABuilder.ABuilder import ABuilder
from src.modules.views.map_view import MapView
from src.common.data_tools import DataTools
from src.modules.lianjia.communities import CommunityList
from src.modules.gaode_api import GaodeApi
from tasks.basic_task import BasicTask


class MyTask(BasicTask):
    @classmethod
    def run(cls):
        city = "上海"
        my_house_address = "上海市 徐汇区 漕河泾"
        obj = GaodeApi.geo_encode(address=my_house_address)
        my_house_locations = [obj.latitude, obj.longitude]
        print(f'{my_house_address} {str(my_house_locations)}')

        data = ABuilder().table(f'{city}_district').query()
        districts = cls.list_to_districts(data, city)

        data = ABuilder().table(f'{city}_district').where({'name': ['=', '闵行']}).query()
        district = cls.list_to_districts(data, city).districts[0]
        data = ABuilder().table(f'{city}_community').where({'district': ['=', '闵行']}).query()
        communities = cls.list_to_communities(data, city)

        # 过滤
        threshold = 10
        cls.cal_dist_for_communities(my_house_locations, communities)
        communities = cls.cm_filter_by_dist(communities, threshold)
        print(f'范围{threshold}公里内过滤')

        MapView.d_communities_draw(city, district, districts, communities, map_location=my_house_locations, circle_radius=threshold)

    @classmethod
    def cal_dist_for_communities(cls, subj_locations, communities: CommunityList):
        """
        :param subj_locations: lat, lng
        :param communities:
        :return:
        """
        for community in communities.items():
            community.distance_to_point = DataTools.cal_distance(subj_locations[0], subj_locations[1],
                                                                 community.latitude, community.longitude)

    @classmethod
    def cm_filter_by_dist(cls, communities: CommunityList, threshold: float):
        filtered = []
        for community in communities.items():
            if community.distance_to_point < threshold:
                filtered.append(community)
        return CommunityList(filtered)


if __name__ == '__main__':
    MyTask.run()
