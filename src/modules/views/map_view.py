import folium
from src.common.constants import VIEW_DIR
import os


class MapView(object):
    _class_name = "Map View"
    render_path = f'{VIEW_DIR}/render.html'
    city_dict = ''


    @classmethod
    def city_draw(cls, city, key_vals):
        folium.Map(location=[31.2389, 121.4992])
        dir_ = os.path.dirname(cls.render_path)
        os.makedirs(dir_, exist_ok=True)

        vals = [one[1] for one in key_vals]
        map = Map()
        map.add(city, key_vals, city)
        map.set_global_opts(
            title_opts=opts.TitleOpts(title=f"{city}市地图"),
            visualmap_opts=opts.VisualMapOpts()
        )
        map.render(path=cls.render_path)

