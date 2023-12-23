import os
basedir = os.path.abspath(os.path.dirname(__file__))
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config(object):
    # ...
    # Database configuration
    DB_USER = os.environ.get('DB_USER')
    DB_PASS = os.environ.get('DB_PASS')
    DB_HOST = os.environ.get('DB_HOST')  # Default to localhost if not set
    DB_PORT = os.environ.get('DB_PORT', '3306')      # Default to 5432 if not set
    DB_NAME = os.environ.get('DB_NAME')

    # SQLAlchemy database URI
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

