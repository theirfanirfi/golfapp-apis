class Config:
    SECRET_KEY = '123456789'
    SQL_USER = 'root'
    SQL_PASS = 'root'
    SQL_URI = 'mysql+pymysql://root:root@localhost/golfrica'
    SQLALCHEMY_DATABASE_URI = SQL_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = None