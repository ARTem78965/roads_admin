import sys
import time

from flask import Flask
from sqlalchemy.exc import OperationalError
from sqlalchemy.exc import SQLAlchemyError

from .extensions import db
from .models import Road
from .models import Sing
from .models import RoadSing

TOTAL_ATTEMPTS = 15
DB_MODELS = (Road, Sing, RoadSing,)

def db_init(app: Flask) -> Flask:
    with app.app_context():
        for attempt in range(TOTAL_ATTEMPTS):
            app.logger.info(f"Database intilization attempt ({attempt}/{TOTAL_ATTEMPTS})!")
            
            try:
                db.engine.execute("SELECT version();")
            except OperationalError as e:
                app.logger.error(f"Database not available: {e}!")
                time.sleep(1)
                continue
            
            try:
                db.create_all()
                break
            except SQLAlchemyError as e:
                app.logger.error(f"Database not create {e}!")
                time.sleep(1)
                continue
        else:
            sys.exit()
            
    return app