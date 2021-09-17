from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.faker import Faker
from src.common.constants import VIEW_DIR
import os


class MapView(object):
    _class_name = "Map View"
    render_path = f'{VIEW_DIR}/render.html'

    @classmethod
    def city_draw(cls, city, key_vals):
        dir_ = os.path.dirname(cls.render_path)
        os.makedirs(dir_, exist_ok=True)

        Map().add(city, [list(one) for one in key_vals], city).set_global_opts(
            title_opts=opts.TitleOpts(title=f"{city}市地图"), visualmap_opts=opts.VisualMapOpts()
        ).render(path=cls.render_path)

