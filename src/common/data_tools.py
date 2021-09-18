"""
@Reference:
根据经纬度坐标计算距离-python
https://www.cnblogs.com/andylhc/p/9481636.html
"""

from geopy.distance import geodesic
from .string_tools import StringTools


class DataTools(object):
    @classmethod
    def cal_distance(cls, subj_lat, subj_lng, obj_lat, obj_lng):
        """
        单位：km
        """
        return geodesic((subj_lat, subj_lng), (obj_lat, obj_lng)).km

    @classmethod
    def containing_filter(cls, class_type: type, obj_list: list, attr: str, keyword: str):
        filtered = []
        for obj in obj_list:
            if StringTools.contain(eval(f'{obj}.{attr}'), keyword):
                filtered.append(obj)
        return class_type(filtered)

    @classmethod
    def or_containing_filter(cls, class_type: type, obj_list: list, attr: str, keywords: list):
        filtered = []
        for obj in obj_list:
            if StringTools.multi_or_contain(eval(f'{obj}.{attr}'), keywords):
                filtered.append(obj)
        return class_type(filtered)

    @classmethod
    def and_containing_filter(cls, class_type: type, obj_list: list, attr: str, keywords: list):
        filtered = []
        for obj in obj_list:
            if StringTools.multi_and_contain(eval(f'{obj}.{attr}'), keywords):
                filtered.append(obj)
        return class_type(filtered)

    @classmethod
    def group(cls, class_type: type, obj_list: list, attr: str) -> dict:
        group_dict = {}
        for obj in obj_list:
            key = eval(f'paper.{attr}')
            if key not in group_dict:
                group_dict[key] = class_type()
            group_dict[key].houses.append(obj)
        return group_dict
