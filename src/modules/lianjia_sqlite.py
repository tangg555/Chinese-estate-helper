import sqlite3
import numpy
import tqdm
from .lianjia_parser import LianJiaParser
from .constants import LianJiaConsts

DISTRICTS_CREATE_SQLITE_TEMPLATE = '''create table if not exists %s (
                id int PRIMARY KEY ,
                name text,
                longitude text,
                latitude text,
                border text,
                unit_price int,
                count int
                )'''

COMMUNITIES_CREATE_SQLITE_TEMPLATE = '''create table if not exists %s (
                    id int PRIMARY KEY ,
                    district text,
                    name text,
                    longitude text,
                    latitude text,
                    unit_price int,
                    count int
                    )'''

HOUSE_CREATE_SQLITE_TEMPLATE = '''create table if not exists %s (
            houseId PRIMARY KEY, 
            houseCode , title, appid, source, imgSrc, layoutImgSrc, imgSrcUri,
            layoutImgSrcUri, roomNum, square, buildingArea, buildYear, isNew, ctime,
            mtime, orientation, floorStat, totalFloor, decorateType, hbtName,
            isYezhuComment, isGarage, houseType, isFocus, status, isValid, signTime,
            signSource, signSourceCn, isDisplay, address, community, communityId,
            communityName, communityUrl, communityUrlEsf, districtId, districtUrl,
            districtName, regionId, regionUrl, regionName, bbdName, bbdUrl, houseCityId,
            subwayInfo, schoolName, schoolArr, bizcircleFullSpell, house_video_info , price,
            unitPrice, viewUrl, listPrice, publishTime, isVilla, villaNoFloorLevel,
            villaName, tags)'''

HOUSE_INSERT_SQLITE_TEMPLATE = '''insert into %s (houseId,
            houseCode,title,appid,source,imgSrc,layoutImgSrc,imgSrcUri,
            layoutImgSrcUri,roomNum,square,buildingArea,buildYear,isNew,ctime,
            mtime,orientation,floorStat,totalFloor,decorateType,hbtName,
            isYezhuComment,isGarage,houseType,isFocus,status,isValid,signTime,
            signSource,signSourceCn,isDisplay,address,community,communityId,
            communityName,communityUrl,communityUrlEsf,districtId,districtUrl,
            districtName,regionId,regionUrl,regionName,bbdName,bbdUrl,houseCityId,
            subwayInfo,schoolName,schoolArr,bizcircleFullSpell,
            house_video_info,price,
            unitPrice,viewUrl,listPrice,publishTime,isVilla,villaNoFloorLevel,villaName,tags) values 
            (:houseId,:houseCode,:title,:appid,:source,:imgSrc,:layoutImgSrc,:imgSrcUri,
            :layoutImgSrcUri,:roomNum,:square,:buildingArea,:buildYear,:isNew,:ctime,
            :mtime,:orientation,:floorStat,:totalFloor,:decorateType,:hbtName,
            :isYezhuComment,:isGarage,:houseType,:isFocus,:status,:isValid,:signTime,
            :signSource,:signSourceCn,:isDisplay,:address,:community,:communityId,
            :communityName,:communityUrl,:communityUrlEsf,:districtId,:districtUrl,
            :districtName,:regionId,:regionUrl,:regionName,:bbdName,:bbdUrl,:houseCityId,
            :subwayInfo,:schoolName,:schoolArr,:bizcircleFullSpell,:house_video_info,:price,
            :unitPrice,:viewUrl,:listPrice,:publishTime,:isVilla,:villaNoFloorLevel,
            :villaName,:tags)'''

class LianJiaSqlite(object):
    _class_name = "LianJia Sqlite"
    parser = LianJiaParser()

    @classmethod
    def save_districts(cls, city):
        """
        保存city的所有区域边缘经纬度并保存在目录下district.db文件内
        """
        districts = cls.parser.get_districts(city)
        conn = sqlite3.connect('districts.db')  # 链接数据库
        cursor = conn.cursor()

        cursor.execute(DISTRICTS_CREATE_SQLITE_TEMPLATE % city)  # 创建表

        pbar = tqdm.tqdm(districts)
        for district in tqdm.tqdm(pbar):
            sql = ''' 
                insert into %s
                (id, name, longitude,latitude,border,unit_price,count)
                values
                (:id, :name, :longitude, :latitude, :border, :unit_price, :count)
                ''' % city
            try:
                cursor.execute(sql, district)
                conn.commit()
                pbar.set_description(district['name'] + '已导入')
            except:
                pbar.set_description(district['name'] + '已存在')
        cursor.close()

    @classmethod
    def save_communities(cls, city):
        """
        保存市区内所有在售楼盘的信息并保存在目录下LianJia_area.db文件内
        """
        with sqlite3.connect('districts.db') as conn:
            c = conn.cursor()
            c.execute('SELECT border,name FROM %s' % city)
            area_list = c.fetchall()

        conn = sqlite3.connect('communities.db')
        cursor = conn.cursor()

        cursor.execute(COMMUNITIES_CREATE_SQLITE_TEMPLATE % city)

        for area in area_list:
            lat = []
            lng = []
            district_name = area[1]
            district_border = area[0]
            for coordinate in district_border.split(';'):
                lng.append(float(coordinate.split(',')[0]))
                lat.append(float(coordinate.split(',')[1]))
            squares = []
            step = 0.02
            for x in numpy.arange(min(lng), max(lng), step):
                for y in numpy.arange(min(lat), max(lat), step):
                    squares.append((round(y, 6), round(y - step, 6), round(x, 6), round(x - step, 6)))

            pbar = tqdm.tqdm(squares)
            for square in pbar:
                communities = cls.parser.get_communities(city, square[0], square[1], square[2], square[3])
                for community in communities:
                    try:
                        sql = ''' insert into %s
                                 (id, name, district,longitude,latitude,unit_price,count)
                                 values
                                 (:id, :name, :district,:longitude, :latitude, :unit_price, :count)
                                 ''' % city
                        community.update({'district': district_name})
                        cursor.execute(sql, community)
                        conn.commit()

                        pbar.set_description(district_name + community['name'] + '已导入')
                    except:
                        pbar.set_description(district_name + community['name'] + '住房已存在')


    @classmethod
    def save_houses(cls, city):
        """
        保存市区内所有在售楼盘的信息并保存在目录下LianJia_area.db文件内
        """
        with sqlite3.connect('houses.db') as conn1:
            cursor1 = conn1.cursor()
            cursor1.execute(HOUSE_CREATE_SQLITE_TEMPLATE % city)

        with sqlite3.connect('communities.db') as conn:
            c = conn.cursor()
            c.execute('SELECT id,count FROM %s' % city)
            area_list = c.fetchall()

        pbar = tqdm.tqdm(area_list)
        for area in pbar:
            house_infos = cls.parser.get_houses(area[0], area[1])
            with sqlite3.connect('houses.db') as conn:
                cursor = conn.cursor()
                for house_info in house_infos:
                    try:
                        sql = HOUSE_INSERT_SQLITE_TEMPLATE % city
                        house_info['house_video_info'] = str(house_info['house_video_info'])
                        house_info['tags'] = str(house_info['tags'])
                        cursor.execute(sql, house_info)
                        conn.commit()
                        pbar.set_description(house_info['title'] + '已导入')
                    except:
                        pbar.set_description(house_info['title'] + '已存在')

