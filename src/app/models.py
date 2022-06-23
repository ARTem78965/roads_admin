from .extensions import db


class Road(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, comment='ID')
    number_road = db.Column(db.String, unique=True, nullable=False, comment='Number_Road')
    name_road = db.Column(db.String, unique=True, nullable=False, comment='Name_Road')


class Sing(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, comment='ID')
    name_sing = db.Column(db.String, unique=True, nullable=False, comment='Name_Sing')


class RoadSing(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, comment='ID')
    road_id = db.Column(db.Integer, db.ForeignKey('road.id'), nullable=False, comment='Road_ID')
    sing_id = db.Column(db.Integer, db.ForeignKey('sing.id'), nullable=False, comment='Sing_ID')
    latitude = db.Column(db.Float, nullable=False, comment='Latitude')
    longitude = db.Column(db.Float, nullable=False, comment='Longitude')
    image = db.Column(db.String, nullable=False, comment='Image')
