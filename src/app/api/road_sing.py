import os

from app import app
from app.extensions import db
from app.models import Road
from app.models import RoadSing
from app.models import Sing
from app.recognition.recognition_sign import recognition_sign
from flask import abort
from flask import request
from werkzeug.utils import secure_filename


def read_roads_sings():
    roads_sings_from_db = (
        RoadSing.query.join(Road, Road.id == RoadSing.road_id)
        .join(Sing, Sing.id == RoadSing.sing_id)
        .add_columns(
            RoadSing.id,
            Road.number_road,
            Road.name_road,
            RoadSing.sing_id,
            Sing.name_sing,
            RoadSing.latitude,
            RoadSing.longitude,
            RoadSing.image,
        )
    )

    items = [
        {
            'id': data.id,
            'number_road': data.number_road,
            'name_road': data.name_road,
            'sings': {
                'sing_id': data.sing_id,
                'name_sing': data.name_sing,
                'latitude': data.latitude,
                'longitude': data.longitude,
                'image': data.image,
            },
        }
        for data in roads_sings_from_db
    ]

    return {'items': items}


def create_road_sing():
    road_id = request.form['road_id']
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    image = request.files['image']

    imagename = secure_filename(image.filename)
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], imagename))
    path_to_img = recognition_sign(os.path.join(app.config['UPLOAD_FOLDER'], imagename))

    sings_from_db = Sing.query.filter_by(name_sing=path_to_img).one_or_none()
    roads_from_db = Road.query.filter_by(id=road_id).one_or_none()

    if roads_from_db is None or sings_from_db is None:
        abort(422)

    new_road_sing = RoadSing(
        road_id=roads_from_db.id,
        sing_id=sings_from_db.id,
        latitude=latitude,
        longitude=longitude,
        image=imagename,
    )
    db.session.add(new_road_sing)
    db.session.commit()

    roads_sings_from_db = (
        RoadSing.query.filter_by(id=new_road_sing.id)
        .join(Road, Road.id == RoadSing.road_id)
        .join(Sing, Sing.id == RoadSing.sing_id)
        .add_columns(
            RoadSing.id,
            Road.number_road,
            Road.name_road,
            RoadSing.sing_id,
            Sing.name_sing,
            RoadSing.latitude,
            RoadSing.longitude,
            RoadSing.image,
        )
        .first()
    )

    return {
        'id': roads_sings_from_db.id,
        'number_road': roads_sings_from_db.number_road,
        'name_road': roads_sings_from_db.name_road,
        'sings': {
            'sing_id': roads_sings_from_db.sing_id,
            'name_sing': roads_sings_from_db.name_sing,
            'latitude': roads_sings_from_db.latitude,
            'longitude': roads_sings_from_db.longitude,
            'image': roads_sings_from_db.image,
        },
    }, 201


def update_road_sing():
    id = request.args['id']
    road_id = request.form['road_id']
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    image = request.files['image']

    imagename = secure_filename(image.filename)
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], imagename))
    path_to_img = recognition_sign(os.path.join(app.config['UPLOAD_FOLDER'], imagename))

    road_sing_from_db = RoadSing.query.filter_by(id=id).first_or_404()
    sings_from_db = Sing.query.filter_by(name_sing=path_to_img).one_or_none()
    roads_from_db = Road.query.filter_by(id=road_id).one_or_none()

    if roads_from_db is None or sings_from_db is None:
        abort(422)

    db.session.query(RoadSing).filter(RoadSing.id == road_sing_from_db.id).update(
        {
            'road_id': roads_from_db.id,
            'sing_id': sings_from_db.id,
            'latitude': latitude,
            'longitude': longitude,
            'image': imagename,
        }
    )
    db.session.commit()

    roads_sings_from_db = (
        RoadSing.query.filter_by(id=id)
        .join(Road, Road.id == RoadSing.road_id)
        .join(Sing, Sing.id == RoadSing.sing_id)
        .add_columns(
            RoadSing.id,
            Road.number_road,
            Road.name_road,
            RoadSing.sing_id,
            Sing.name_sing,
            RoadSing.latitude,
            RoadSing.longitude,
            RoadSing.image,
        )
        .first()
    )

    item = {
        'id': roads_sings_from_db.id,
        'number_road': roads_sings_from_db.number_road,
        'name_road': roads_sings_from_db.name_road,
        'sings': {
            'sing_id': roads_sings_from_db.sing_id,
            'name_sing': roads_sings_from_db.name_sing,
            'latitude': roads_sings_from_db.latitude,
            'longitude': roads_sings_from_db.longitude,
            'image': road_sing_from_db.image,
        },
    }

    return {'items': item}


def delete_road_sing():
    id = request.args['id']

    roads_sings_from_db = RoadSing.query.filter_by(id=id).first_or_404()

    db.session.query(RoadSing).filter(RoadSing.id == roads_sings_from_db.id).delete()
    db.session.commit()

    return '', 204
