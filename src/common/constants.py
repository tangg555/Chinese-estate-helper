"""
@Desc:
"""

CACHE_DIR = './cache'
VIEW_DIR = './view'

class LianJiaConsts(object):
    LIANJIA_DB = 'lianjia'

    #     e.g.
    #     https://ajax.lianjia.com/map/search/ershoufang/?callback=jQuery111109719454800982295_1562045315950&
    #     city_id=410100&group_type=district&max_lat=34.961967&min_lat=34.473941&max_lng=113.50206&min_lng=112.899549&sug_id=&sug_type=&
    #     filters=%7B%7D&request_ts=1562045339940&source=ljpc&authorization=a83c1b0e615c19505b0a399051fcb87f&_=1562045315957
    CITY_DICT = {
        '上海': {'city_id': '310000', 'max_lat': '31.36552', 'min_lat': '31.106158', 'max_lng': '121.600985',
               'min_lng': '121.360095'},
        '北京': {'city_id': '110000', 'max_lat': '40.074766', 'min_lat': '39.609408', 'max_lng': '116.796856',
               'min_lng': '115.980476'},
        '广州': {'city_id': '440100', 'max_lat': '23.296086', 'min_lat': '22.737277', 'max_lng': '113.773905',
               'min_lng': '113.038013'},
        '深圳': {'city_id': '440300', 'max_lat': '22.935891', 'min_lat': '22.375581', 'max_lng': '114.533683',
               'min_lng': '113.797791'},
        '长沙': {'city_id': '430100', 'max_lat': '28.368467', 'min_lat': '28.101143', 'max_lng': '113.155889',
               'min_lng': '112.735051'},
        '烟台': {'city_id': '370600', 'max_lat': '37.590234', 'min_lat': '37.349651', 'max_lng': '121.698469',
               'min_lng': '121.210365'},
        '厦门': {'city_id': '350200', 'max_lat': '24.794145', 'min_lat': '24.241819', 'max_lng': '118.533083',
               'min_lng': '117.892627'},
        '郑州': {'city_id': '410100', 'max_lat': '34.961967', 'min_lat': '34.473941', 'max_lng': '113.50206',
               'min_lng': '112.899549'}
    }

    # eg.
    # select_city=110000;
    # _jzqa=1.3180246719396510700.1534145942.1537530221.1541866760.3;
    # _jzqc=1;
    # _jzqckmp=1;
    # _gid=GA1.2.178601063.1541866763;
    # _jzqb=1.2.10.1541866760.1
    COOKIES = {'lianjia_uuid': '9bdccc1a-7584-4639-ba95-b42cf21bbbc7',
               'jzqa': '1.3180246719396510700.1534145942.1534145942.1534145942.1',
               'jzqckmp': '1',
               'ga': 'GA1.2.964691746.1534145946',
               'gid': 'GA1.2.826685830.1534145946',
               'UM_distinctid': '165327625186a-029cf60b1994ee-3461790f-fa000-165327625199d3',
               'lianjia_ssid': '34fc4efa-7fcc-4f3f-82ae-010401f27aa8',
               '_smt_uid': '5b72c5f7.5815bcdf',
               'Hm_lvt_9152f8221cb6243a53c83b956842be8a': '1537530243',
               'select_city': '110000',
               '_jzqc': '1',
               '_gid': 'GA1.2.178601063.1541866763',
               '_jzqb': '1.2.10.1541866760.1'

               }

    HEADERS = {
        'Host': 'ajax.lianjia.com',
        'Referer': 'https://sh.lianjia.com/ditu/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }

    DISTRICTS_CREATE_SQL_TEMPLATE = '''create table if not exists %s_district (
                    id int PRIMARY KEY ,
                    name text,
                    longitude text,
                    latitude text,
                    border text,
                    unit_price int,
                    count int
                    )'''

    COMMUNITIES_CREATE_SQL_TEMPLATE = '''create table if not exists %s_community (
                        id varchar(20) PRIMARY KEY ,
                        district text,
                        name text,
                        longitude text,
                        latitude text,
                        unit_price int,
                        count int
                        )'''

    # e.g. {'houseId': '107103138219', 'houseCode': '107103138219', 'title': '地铁五号线+封闭小区，精装修，采光好，配套设施齐全',
    # 'appid': '104', 'source': 'link', 'imgSrc': 'https://image1.ljcdn.com/110000-inspection/pc1_r9NmDZgdQ_1.jpg.280x210.jpg',
    # 'layoutImgSrc': 'https://image1.ljcdn.com/x-se/hdic-frame/standard_5fe0417c-d36b-4d9f-b793-55b5e9e720e2.png.280x210.jpg',
    # 'imgSrcUri': 'https://image1.ljcdn.com/110000-inspection/pc1_r9NmDZgdQ_1.jpg',
    # 'layoutImgSrcUri': 'https://image1.ljcdn.com/x-se/hdic-frame/standard_5fe0417c-d36b-4d9f-b793-55b5e9e720e2.png',
    # 'roomNum': '2室2厅', 'square': 96.98, 'buildingArea': 96.98, 'buildYear': '1997年建', 'isNew': False,
    # 'ctime': '2020-10-05', 'mtime': '2021-09-17', 'orientation': '南 北', 'floorStat': '高楼层', 'totalFloor': '6',
    # 'decorateType': '精装', 'hbtName': '暂无数据', 'isYezhuComment': True, 'isGarage': False, 'houseType': '107500000003',
    # 'isFocus': False, 'status': 'sell', 'isValid': 1, 'signTime': '1970.01.02', 'signSource': '链家成交',
    # 'signSourceCn': '链家成交', 'isDisplay': 1, 'address': '新建西路101弄', 'community': 509821540057808,
    # 'communityId': 509821540057808, 'communityName': '新建西路101弄',
    # 'communityUrl': 'https://sh.lianjia.com/xiaoqu/509821540057808/',
    # 'communityUrlEsf': 'https://sh.lianjia.com/ershoufang/c509821540057808/', 'districtId': 310120,
    # 'districtUrl': 'https://sh.lianjia.com/ershoufang/fengxian/', 'districtName': '奉贤', 'regionId': 613000258,
    # 'regionUrl': 'https://sh.lianjia.com/ershoufang/nanqiao/', 'regionName': '南桥', 'bbdName': '南桥',
    # 'bbdUrl': 'https://sh.lianjia.com/ershoufang/nanqiao/', 'houseCityId': '310000', 'subwayInfo': '',
    # 'schoolName': '', 'schoolArr': None, 'bizcircleFullSpell': 'fengxian', 'isVr': False, 'isVrFutureHome': True,
    # 'isGoodHouse': '', 'isYezhuPay': False, 'new_house_status': 'zai_shou', 'new_price_str_unit': '万',
    # 'new_unit_price_str_unit': '元/平', 'new_price_str': '170', 'new_unit_price_str': '17530', 'copy_writing': '暂无价格',
    # 'house_video_info': '[]', 'price': 170, 'unitPrice': 17530, 'viewUrl': 'https://sh.lianjia.com/ershoufang/107103138219.html',
    # 'listPrice': 170, 'publishTime': '11个月以前发布', 'isVilla': False, 'villaNoFloorLevel': False, 'villaName': '',
    # 'tags': "[['isVrFutureHome', 'VR看装修'], ['five', '房本满两年']]"}
    HOUSE_CREATE_SQL_TEMPLATE = '''create table if not exists %s_house (
                houseId varchar(20) PRIMARY KEY, 
                houseCode text, title text, appid text, source text, imgSrc text, 
                layoutImgSrc text, imgSrcUri text,
                layoutImgSrcUri text, roomNum text, square text, buildingArea text, buildYear text, isNew boolean, ctime text,
                mtime text, orientation text, floorStat text, totalFloor int, decorateType text, hbtName text,
                isYezhuComment boolean, isGarage boolean, houseType text, isFocus boolean, status text, isValid int, signTime text,
                signSource text, signSourceCn text, isDisplay int, address text, community varchar(20), communityId varchar(20),
                communityName text, communityUrl text, communityUrlEsf text, districtId int, districtUrl text,
                districtName text, regionId int, regionUrl text, regionName text, bbdName text, bbdUrl text, houseCityId text,
                subwayInfo text, schoolName text, schoolArr text, bizcircleFullSpell text, house_video_info text, price int,
                unitPrice int, viewUrl text, listPrice int, publishTime text, isVilla boolean, villaNoFloorLevel boolean,
                villaName text, tags text)'''

    HOUSE_INSERT_SQL_TEMPLATE = '''insert ignore into %s_house (houseId,
                houseCode,title,appid,source,imgSrc,layoutImgSrc,imgSrcUri,
                layoutImgSrcUri,roomNum,square,buildingArea,buildYear,isNew,ctime,
                mtime,orientation,floorStat,totalFloor,decorateType,hbtName,
                isYezhuComment,isGarage,houseType,isFocus,status,isValid,signTime,
                signSource,signSourceCn,isDisplay,address,community,communityId,
                communityName,communityUrl,communityUrlEsf,districtId,districtUrl,
                districtName,regionId,regionUrl,regionName,bbdName,bbdUrl,houseCityId,
                subwayInfo,schoolName,schoolArr,bizcircleFullSpell,house_video_info,price,
                unitPrice,viewUrl,listPrice,publishTime,isVilla,villaNoFloorLevel,villaName,tags) 
                values 
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


    # request template
    AJAX_GET_TEMPLATE = 'https://ajax.lianjia.com/map/search/ershoufang/?callback=jQuery1111012389114747347363_1534230881479' \
                        '&city_id=%s' \
                        '&group_type=%s' \
                        '&max_lat=%s' \
                        '&min_lat=%s' \
                        '&max_lng=%s' \
                        '&min_lng=%s' \
                        '&filters=%s' \
                        '&request_ts=%d' \
                        '&source=ljpc' \
                        '&authorization=%s' \
                        '&_=%d'

    HOUSE_AJAX_GET_TEMPLATE = 'https://ajax.lianjia.com/map/resblock/ershoufanglist/?callback=jQuery11110617424919783834_1541868368031' \
                              '&id=%s' \
                              '&order=0' \
                              '&page=%d' \
                              '&filters=%s' \
                              '&request_ts=%d' \
                              '&source=ljpc' \
                              '&authorization=%s' \
                              '&_=%d'
