from os import environ
class Config:
    SECRET_KEY = 'zMq@aTjz@Za!RrT#4!YL63rP'
    SQLALCHEMY_DATABASE_URI = environ.get('dbURL')
    #SQLALCHEMY_DATABASE_URI = "mysql+pymysql://ESDPrj@localhost:3306/authentication"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'd4vidg0ggins2023@gmail.com'
    MAIL_PASSWORD = 'chsr bmhk urzj ayzd'
    MAIL_DEFAULT_SENDER = 'd4vidg0ggins2023@gmail.com'
    JWT_ISSUER = 'flask-jwt-auth'
