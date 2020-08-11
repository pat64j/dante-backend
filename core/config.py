import os
from datetime import timedelta
class Config:
    ACCESS_EXPIRES = timedelta(minutes=60)
    REFRESH_EXPIRES = timedelta(days=30)

    SECRET_KEY = os.getenv('SECRET_KEY')
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
    CAT_UPLOAD_FOLDER = os.getenv('CAT_UPLOAD_FOLDER')
    VIDEO_MSG_THUMBS = os.getenv('VIDEO_MSG_THUMBS')
    AUDIO_MSG_THUMBS = os.getenv('AUDIO_MSG_THUMBS')
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg'}
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = ACCESS_EXPIRES
    JWT_REFRESH_TOKEN_EXPIRES = REFRESH_EXPIRES
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

class TestingConfig(Config):
    ACCESS_EXPIRES = timedelta(minutes=15)
    REFRESH_EXPIRES = timedelta(days=30)

    TESTING = True
    SECRET_KEY = os.getenv('TEST_SECRET_KET')

    JWT_ACCESS_TOKEN_EXPIRES = ACCESS_EXPIRES
    JWT_REFRESH_TOKEN_EXPIRES = REFRESH_EXPIRES
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']