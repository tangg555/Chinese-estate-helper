"""
@Desc:
关于地图相关的工作，详情请参考folium的有关教学。
"""

import os
import folium
import webbrowser
import json
from tqdm import tqdm
from folium.plugins import HeatMap
from src.common.constants import VIEW_DIR
from src.modules.gaode_api import GaodeApi


class MapView(object):
    _class_name = "Map View"
    city_location_dict = {"上海": [31.2389, 121.4992]}

    @classmethod
    def parse_zhch(cls, string):
        """
        中文转换
        """
        return str(str(string).encode('ascii', 'xmlcharrefreplace'))[2:-1]

    @classmethod
    def draw_contour(cls, map, locations):
        folium.PolyLine(
            locations,  # 坐标点列表
            weight=3,  # 线宽
            color='blue',  # 线条颜色
            opacity=0.6  # 透明度
        ).add_to(map)

    @classmethod
    def show(cls, folium_map: folium.Map, render_path: str):
        folium_map.save(render_path)
        webbrowser.open(os.path.abspath(render_path))

    @classmethod
    def districts_draw(cls, city, districts):
        zoom_start = 11
        render_path = f'{VIEW_DIR}/{city}_districts_draw.html'
        folium_map = folium.Map(
            location=cls.city_location_dict[city],  # 经纬度，list 或者 tuple 格式，顺序为 latitude, longitude
            zoom_start=zoom_start,  # 缩放值，默认为 10，值越大比例尺越小，地图放大级别越大
            title=cls.parse_zhch(f"{city}_二手房")
        )

        heatmap_data = []
        # 添加marker到地图
        for district in districts:
            popup = folium.Popup(cls.parse_zhch(f'{district.name} 均价:{district.unit_price}'), show=True)
            folium.Marker([district.latitude, district.longitude],
                          popup=popup,
                          tooltip=cls.parse_zhch(f'在售小区:{district.count}'),
                          icon=folium.Icon(color='red')
                          ).add_to(folium_map)
            # 绘制行政区轮廓
            if district.name == "上海周边":
                continue
            locations = []

            for one in district.border.split(';'):
                longitude, latitude = one.strip().split(',')
                locations.append([float(latitude), float(longitude)])
            cls.draw_contour(folium_map, locations)
            heatmap_data.append([district.latitude, district.longitude, district.unit_price])

        # 绘制热力图 data: [lat, lng, weight]
        HeatMap(heatmap_data).add_to(folium_map)
        cls.show(folium_map, render_path)

    @classmethod
    def communities_draw(cls, city, district, communities):
        zoom_start = 12
        render_path = f'{VIEW_DIR}/{city}_{district.name}_communities_draw.html'
        folium_map = folium.Map(
            location=[district.latitude, district.longitude],  # 经纬度，list 或者 tuple 格式，顺序为 latitude, longitude
            zoom_start=zoom_start,  # 缩放值，默认为 10，值越大比例尺越小，地图放大级别越大
            title=cls.parse_zhch(f"{city}_{district.name}_二手房")
        )

        # 区房价
        popup = folium.Popup(cls.parse_zhch(f'{district.name} 均价:{district.unit_price}'), show=True)
        folium.Marker([district.latitude, district.longitude],
                      popup=popup,
                      tooltip=cls.parse_zhch(f'在售小区:{district.count}'),
                      icon=folium.Icon(color='red')
                      ).add_to(folium_map)

        heatmap_data = []
        # 添加marker到地图
        for community in communities:
            popup = folium.Popup(cls.parse_zhch(f'{community.name} 均价:{community.unit_price}'), show=True)
            folium.Marker([community.latitude, community.longitude],
                          popup=popup,
                          tooltip=cls.parse_zhch(f'dist:{community.distance_to_point}'),
                          icon=folium.Icon(color='blue')
                          ).add_to(folium_map)
            heatmap_data.append([community.latitude, community.longitude, community.unit_price])

        # 绘制热力图 data: [lat, lng, weight]
        HeatMap(heatmap_data).add_to(folium_map)
        cls.show(folium_map, render_path)

    @classmethod
    def d_communities_draw(cls, city, district, districts, communities, map_location=None, circle_radius=0):
        zoom_start = 12
        render_path = f'{VIEW_DIR}/{city}_{district.name}_d_communities_draw.html'
        folium_map = folium.Map(
            location=map_location,  # 经纬度，list 或者 tuple 格式，顺序为 latitude, longitude
            zoom_start=zoom_start,  # 缩放值，默认为 10，值越大比例尺越小，地图放大级别越大
            title=cls.parse_zhch(f"{city}_{district.name}_二手房")
        )

        # 展示地图中心位置和半径
        if circle_radius > 0:
            # 标明中心
            popup = folium.Popup(cls.parse_zhch(f'地图中心 threshold:{circle_radius}'), show=True)
            folium.Marker(map_location,
                          popup=popup,
                          tooltip=cls.parse_zhch(f'小区个数:{len(communities)}'),
                          icon=folium.Icon(color='green')
                          ).add_to(folium_map)
            # 画圈
            folium.Circle(
                location=map_location,
                radius=circle_radius*1000,  # 单位是米
                color="darkred",
                weight=3,
                fill=False,
                fill_opacity=0.6,
                opacity=1,
            ).add_to(folium_map)

        # 区房价
        # 添加区房价marker到地图
        for district in districts:
            popup = folium.Popup(cls.parse_zhch(f'{district.name} 均价:{district.unit_price}'), show=True)
            folium.Marker([district.latitude, district.longitude],
                          popup=popup,
                          tooltip=cls.parse_zhch(f'在售小区:{district.count}'),
                          icon=folium.Icon(color='red')
                          ).add_to(folium_map)
            # 绘制行政区轮廓
            if district.name == "上海周边":
                continue
            locations = []

            for one in district.border.split(';'):
                longitude, latitude = one.strip().split(',')
                locations.append([float(latitude), float(longitude)])
            cls.draw_contour(folium_map, locations)

        heatmap_data = []
        # 添加小区房价marker到地图
        for community in communities:
            popup = folium.Popup(cls.parse_zhch(f'{community.name} 均价:{community.unit_price}'), show=True)
            folium.Marker([community.latitude, community.longitude],
                          popup=popup,
                          tooltip=cls.parse_zhch(f'dist:{community.distance_to_point}'),
                          icon=folium.Icon(color='blue')
                          ).add_to(folium_map)
            heatmap_data.append([community.latitude, community.longitude, community.unit_price])

        # 绘制热力图 data: [lat, lng, weight]
        HeatMap(heatmap_data).add_to(folium_map)
        cls.show(folium_map, render_path)


