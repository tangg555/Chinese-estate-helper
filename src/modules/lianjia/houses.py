"""
@Desc:
"""

from src.modules.logger import MyLogger
from src.common.string_tools import StringTools


class House(object):
    _class_name = "House"

    def __init__(self, house_, city: str):
        self.houseId = house_['houseId']
        self.title = house_['title']
        self.city = city
        self.square = house_['square']
        self.roomNum = house_['roomNum']
        self.buildingArea = house_['buildingArea']
        self.buildYear = house_['buildYear']
        self.floorStat = house_['floorStat']
        self.totalFloor = house_['totalFloor']
        self.houseType = house_['houseType']

        self.districtId = house_['districtId']
        self.districtName = house_['districtName']
        self.communityId = house_['communityId']
        self.communityName = house_['communityName']
        self.price = house_['price']
        self.unitPrice = house_['unitPrice']
        self.listPrice = house_['listPrice']
        self.publishTime = house_['publishTime']
        self.tags = list(house_['tags'])
        self.unitPrice = house_['unitPrice']

        self.longitude = None
        self.latitude = None

    def __repr__(self):
        return f'{self.city}市 {self.districtName}区 {self.communityName}小区 {self.title}'


class HouseList(object):
    _class_name = "HouseList"

    def __init__(self, houses=[], logger=None):
        self.name = self._class_name
        self.houses = houses
        self.logger = logger

    @property
    def size(self):
        return len(self.houses)

    def add_logger(self, logger: MyLogger):
        self.logger = logger

    '''
    ============================ filters ============================
    '''

    def containing_filter(self, attr: str, keyword: str):
        filtered = []
        for house in self.houses:
            if StringTools.contain(eval(f'paper.{attr}'), keyword):
                filtered.append(house)
        if isinstance(self.logger, MyLogger):
            self.logger.info(
                f'filtered by containing "{keyword}" in {attr} for {len(self.houses)} houses,'
                f' remaining {len(filtered)}')
        return HouseList(filtered)

    def or_containing_filter(self, attr: str, keywords: list):
        filtered = []
        for house in self.houses:
            if StringTools.multi_or_contain(eval(f'paper.{attr}'), keywords):
                filtered.append(house)
        if isinstance(self.logger, MyLogger):
            self.logger.info(
                f'filtered by containing [{" or ".join(keywords)}] in {attr} for {len(self.houses)} houses,'
                f' remaining {len(filtered)}')
        return HouseList(filtered)

    def and_containing_filter(self, attr: str, keywords: list):
        filtered = []
        for house in self.houses:
            if StringTools.multi_and_contain(eval(f'paper.{attr}'), keywords):
                filtered.append(house)
        if isinstance(self.logger, MyLogger):
            self.logger.info(
                f'filtered by containing [{" and ".join(keywords)}] in {attr} for {len(self.houses)} houses,'
                f' remaining {len(filtered)}')
        return HouseList(filtered)

    def group(self, attr: str) -> dict:
        group_dict = {}
        for house in self.houses:
            key = eval(f'paper.{attr}')
            if key not in group_dict:
                group_dict[key] = HouseList(houses=[])
            group_dict[key].houses.append(house)
        return group_dict

    def items(self):
        return self.houses

    def __and__(self, other):
        new = HouseList(houses=list(set(self.houses) & set(other.houses)), logger=self.logger)
        return new

    def __or__(self, other):
        new = HouseList(houses=list(set(self.houses) | set(other.houses)), logger=self.logger)
        return new

    def __iter__(self):
        for house in self.houses:
            yield house

    def __call__(self, *args, **kwargs):
        return self.houses

    def __repr__(self):
        repr_content = f'\n'
        for one in self.houses:
            repr_content += str(one)
        return repr_content

    def __len__(self):
        return len(self.houses)
