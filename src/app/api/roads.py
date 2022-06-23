from app.extensions import db
from app.models import Road
from flask import request


def read_roads():
    roads_from_db = Road.query.all()
    roads = [
        {'id': data.id, 'number_road': data.number_road, 'name_road': data.name_road}
        for data in roads_from_db
    ]

    return {'roads': roads}


def get_road():
    id = request.args['id']

    roads_from_db = Road.query.filter_by(id=id).first_or_404()
    road = {
        'id': roads_from_db.id,
        'number_road': roads_from_db.number_road,
        'name_road': roads_from_db.name_road,
    }

    return {'roads': road}


def create_road():
    number_road = request.json['number_road']
    name_road = request.json['name_road']

    new_road = Road(number_road=number_road, name_road=name_road)
    db.session.add(new_road)
    db.session.commit()

    return {
        'id': new_road.id,
        'number_road': new_road.number_road,
        'name_road': new_road.name_road,
    }, 201


def update_road():
    id = request.args['id']

    number_road = request.json['number_road']
    name_road = request.json['name_road']

    db.session.query(Road).filter(Road.id == id).update(
        {'number_road': number_road, 'name_road': name_road}
    )
    db.session.commit()

    roads_from_db = Road.query.filter_by(id=id).first_or_404()
    road = {
        'id': roads_from_db.id,
        'number_road': roads_from_db.number_road,
        'name_road': roads_from_db.name_road,
    }

    return {'roads': road}


def delete_road():
    id = request.args['id']

    roads_from_db = Road.query.filter_by(id=id).first_or_404()

    db.session.query(Road).filter(Road.id == roads_from_db.id).delete()
    db.session.commit()

    return '', 204
