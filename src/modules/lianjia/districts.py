"""
@Desc:
"""

from src.modules.logger import MyLogger
from src.common.data_tools import DataTools


class District(object):
    _class_name = "District"

    def __init__(self, district_, city: str):
        self.city = city
        self.id = district_['id']
        self.name = district_['name']
        self.longitude = district_['longitude']
        self.latitude = district_['latitude']
        self.border = district_['border']
        self.unit_price = district_['unit_price']
        self.count = district_['count']

    def __repr__(self):
        return f'{self.city}市 {self.name}区'


class DistrictList(object):
    _class_name = "DistrictList"

    def __init__(self, districts=[], logger=None):
        self.name = self._class_name
        self.districts = districts
        self.logger = logger

    @property
    def size(self):
        return len(self.districts)

    def add_logger(self, logger: MyLogger):
        self.logger = logger

    '''
    ============================ filters ============================
    '''

    def containing_filter(self, attr: str, keyword: str):
        ret = DataTools.containing_filter(DistrictList, self.districts, attr, keyword)
        if isinstance(self.logger, MyLogger):
            self.logger.info(
                f'filtered by containing "{keyword}" in {attr} for {len(self.districts)} districts,'
                f' remaining {len(ret)}')
        return ret

    def or_containing_filter(self, attr: str, keywords: list):
        ret = DataTools.or_containing_filter(DistrictList, self.districts, attr, keywords)
        if isinstance(self.logger, MyLogger):
            self.logger.info(
                f'filtered by containing "{keywords}" in {attr} for {len(self.districts)} districts,'
                f' remaining {len(ret)}')
        return ret

    def and_containing_filter(self, attr: str, keywords: list):
        ret = DataTools.and_containing_filter(DistrictList, self.districts, attr, keywords)
        if isinstance(self.logger, MyLogger):
            self.logger.info(
                f'filtered by containing "{keywords}" in {attr} for {len(self.districts)} districts,'
                f' remaining {len(ret)}')
        return ret

    def group(self, attr: str) -> dict:
        return DataTools.and_containing_filter(DistrictList, self.districts, attr)

    def items(self):
        return self.districts

    def __and__(self, other):
        new = DistrictList(districts=list(set(self.districts) & set(other.houses)), logger=self.logger)
        return new

    def __or__(self, other):
        new = DistrictList(districts=list(set(self.districts) | set(other.houses)), logger=self.logger)
        return new

    def __iter__(self):
        for house in self.districts:
            yield house

    def __call__(self, *args, **kwargs):
        return self.districts

    def __repr__(self):
        repr_content = f'\n'
        for one in self.districts:
            repr_content += str(one)
        return repr_content

    def __len__(self):
        return len(self.districts)
