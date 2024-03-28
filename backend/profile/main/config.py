from os import environ
class Config:
    SQLALCHEMY_DATABASE_URI = environ.get('dbURL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False