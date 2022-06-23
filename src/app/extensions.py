import os

from flask_first import First
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
path_to_spec = os.path.join(basedir, 'api/openapi.yaml')

db = SQLAlchemy()

first = First(path_to_spec, swagger_ui_path='/docs')


def register_extensions(app):
    from .api.roads import create_road
    from .api.roads import read_roads
    from .api.roads import get_road
    from .api.roads import update_road
    from .api.roads import delete_road

    from .api.sings import create_sing
    from .api.sings import get_sing
    from .api.sings import read_sings
    from .api.sings import update_sing
    from .api.sings import delete_sing

    from .api.road_sing import create_road_sing
    from .api.road_sing import read_roads_sings
    from .api.road_sing import update_road_sing
    from .api.road_sing import delete_road_sing

    db.init_app(app)
    first.init_app(app)

    first.add_view_func(create_road)
    first.add_view_func(read_roads)
    first.add_view_func(get_road)
    first.add_view_func(update_road)
    first.add_view_func(delete_road)

    first.add_view_func(create_sing)
    first.add_view_func(read_sings)
    first.add_view_func(get_sing)
    first.add_view_func(update_sing)
    first.add_view_func(delete_sing)

    first.add_view_func(create_road_sing)
    first.add_view_func(read_roads_sings)
    first.add_view_func(update_road_sing)
    first.add_view_func(delete_road_sing)
