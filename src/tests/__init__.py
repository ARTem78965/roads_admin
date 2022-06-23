import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
tst = load_dotenv(os.path.join(basedir, '..', 'dev.env'))

os.environ['POSTGRES_HOST'] = '127.0.0.1'
