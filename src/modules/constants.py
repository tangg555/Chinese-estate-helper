"""
@Desc:
"""

CACHE_DIR = './cache'


class LianJiaConsts(object):
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

    DETAIL_INFO_CREATE_SQL_TEMPLATE = '''create table  if not exists %s (houseId PRIMARY KEY, 
                houseCode, title, appid, source, imgSrc, layoutImgSrc, imgSrcUri,
                layoutImgSrcUri, roomNum, square, buildingArea, buildYear, isNew, ctime,
                mtime, orientation, floorStat, totalFloor, decorateType, hbtName,
                isYezhuComment, isGarage, houseType, isFocus, status, isValid, signTime,
                signSource, signSourceCn, isDisplay, address, community, communityId,
                communityName, communityUrl, communityUrlEsf, districtId, districtUrl,
                districtName, regionId, regionUrl, regionName, bbdName, bbdUrl, houseCityId,
                subwayInfo, schoolName, schoolArr, bizcircleFullSpell, house_video_info , price,
                unitPrice, viewUrl, listPrice, publishTime, isVilla, villaNoFloorLevel,
                villaName, tags)'''

    DETAIL_INFO_INSERT_SQL_TEMPLATE = '''insert into %s(houseId,
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


    CITY_CREATE_SQL_TEMPLATE = '''create table if not exists %s (
                    id int PRIMARY KEY ,
                    name text,
                    longitude text,
                    latitude text,
                    border text,
                    unit_price int,
                    count int
                    )'''

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
