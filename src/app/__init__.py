from flask import Flask
from flask import jsonify
from flask import make_response

from .extensions import register_extensions
from .migrations import db_init

UPLOAD_FOLDER = './app/recognition/img'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:super_secret@roads_postgres:5432/roads'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FIRST_RESPONSE_VALIDATION'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

register_extensions(app)
db_init(app)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)


@app.errorhandler(422)
def not_found_args(error):
    return make_response(jsonify({'error': 'Unprocessable Entity'}), 422)


if __name__ == '__main__':
    app.run()
