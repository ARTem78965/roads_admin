from app.extensions import db
from app.models import Sing
from flask import request


def read_sings():
    sings_from_db = Sing.query.all()
    sings = [{'id': data.id, 'name_sing': data.name_sing} for data in sings_from_db]

    return {'items': sings}


def get_sing():
    id = request.args['id']

    sings_from_db = Sing.query.filter_by(id=id).first_or_404()
    sing = {'id': sings_from_db.id, 'name_sing': sings_from_db.name_sing}

    return {'items': sing}


def create_sing():
    name = request.json['name_sing']

    new_sing = Sing(name_sing=name)
    db.session.add(new_sing)
    db.session.commit()

    return {'id': new_sing.id, 'name_sing': new_sing.name_sing}, 201


def update_sing():
    id = request.args['id']

    name = request.json['name_sing']

    db.session.query(Sing).filter(Sing.id == id).update({'name_sing': name})
    db.session.commit()

    sings_from_db = Sing.query.filter_by(id=id).first_or_404()
    sing = {'id': sings_from_db.id, 'name_sing': sings_from_db.name_sing}

    return {'items': sing}


def delete_sing():
    id = request.args['id']

    sings_from_db = Sing.query.filter_by(id=id).first_or_404()

    db.session.query(Sing).filter(Sing.id == sings_from_db.id).delete()
    db.session.commit()

    return '', 204
