import os
from dotenv import load_dotenv
load_dotenv()


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'quiz.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY', '')