"""
@Desc:
"""

from src.modules.logger import MyLogger
from src.common.string_tools import StringTools
from src.common.data_tools import DataTools


class Community(object):
    _class_name = "Community"

    def __init__(self, community_, city: str):
        self.id = community_['id']
        self.district = community_['district']
        self.city = city
        self.name = community_['name']
        self.longitude = community_['longitude']
        self.latitude = community_['latitude']
        self.unit_price = community_['unit_price']
        self.count = community_['count']

    def __repr__(self):
        return f'f{self.city}市 {self.district}区 {self.name}小区 '


class CommunityList(object):
    _class_name = "HouseList"

    def __init__(self, communities=[], logger=None):
        self.name = self._class_name
        self.communities = communities
        self.logger = logger

    @property
    def size(self):
        return len(self.communities)

    def add_logger(self, logger: MyLogger):
        self.logger = logger

    '''
    ============================ filters ============================
    '''

    def containing_filter(self, attr: str, keyword: str):
        ret = DataTools.containing_filter(CommunityList, self.communities, attr, keyword)
        if isinstance(self.logger, MyLogger):
            self.logger.info(
                f'filtered by containing "{keyword}" in {attr} for {len(self.communities)} communities,'
                f' remaining {len(ret)}')
        return ret

    def or_containing_filter(self, attr: str, keywords: list):
        ret = DataTools.or_containing_filter(CommunityList, self.communities, attr, keywords)
        if isinstance(self.logger, MyLogger):
            self.logger.info(
                f'filtered by containing "{keywords}" in {attr} for {len(self.communities)} communities,'
                f' remaining {len(ret)}')
        return ret

    def and_containing_filter(self, attr: str, keywords: list):
        ret = DataTools.and_containing_filter(CommunityList, self.communities, attr, keywords)
        if isinstance(self.logger, MyLogger):
            self.logger.info(
                f'filtered by containing "{keywords}" in {attr} for {len(self.communities)} communities,'
                f' remaining {len(ret)}')
        return ret

    def group(self, attr: str) -> dict:
        return DataTools.and_containing_filter(CommunityList, self.communities, attr)

    def items(self):
        return self.communities

    def __and__(self, other):
        new = CommunityList(communities=list(set(self.communities) & set(other.houses)), logger=self.logger)
        return new

    def __or__(self, other):
        new = CommunityList(communities=list(set(self.communities) | set(other.houses)), logger=self.logger)
        return new

    def __iter__(self):
        for house in self.communities:
            yield house

    def __call__(self, *args, **kwargs):
        return self.communities

    def __repr__(self):
        repr_content = f'\n'
        for one in self.communities:
            repr_content += str(one)
        return repr_content

    def __len__(self):
        return len(self.communities)
