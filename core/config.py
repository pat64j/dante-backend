import os
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = os.getenv('TEST_SECRET_KET')