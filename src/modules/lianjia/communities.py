"""
@Desc:
"""
import os
from src.modules.logger import MyLogger
from src.common.data_tools import DataTools
import xlwt

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
        self.distance_to_point = 0

    def __repr__(self):
        return f'{self.city}市 {self.district}区 {self.name}小区 '


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

    def store(self,
              sheet_name : str = 'communities',
              local_path: str = './local_store/communities.xls'):
        if not os.path.exists(os.path.dirname(local_path)):
            os.makedirs(os.path.dirname(local_path))
            if self.logger:
                self.logger.warning(f'{os.path.abspath(os.path.dirname(local_path))} 不存在，现已创建')
        workbook = xlwt.Workbook()
        # 获取第一个sheet页
        sheet = workbook.add_sheet(sheet_name)
        # 头部
        headers = ["id", "名字", "均价", "房子数量", "到目标点距离"]
        for row in range(0, len(headers)):
            sheet.write(0, row, headers[row])
        # 写入小区信息
        for row, community in enumerate(self.communities):
            sheet.write(row + 1, 0, community.id)
            sheet.write(row + 1, 1, community.name)
            sheet.write(row + 1, 2, community.unit_price)
            sheet.write(row + 1, 3, community.count)
            sheet.write(row + 1, 4, community.distance_to_point)
        workbook.save(local_path)
        if self.logger:
            self.logger.info(f'{len(self.communities)}个小区的数据已经载入{os.path.abspath(local_path)}')

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
