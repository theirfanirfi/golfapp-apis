class Config:
    SECRET_KEY = '123456789'
    SQL_USER = 'root'
    SQL_PASS = 'root'
    SQL_URI = 'mysql+pymysql://root:root@localhost/golfrica?charset=utf8mb4'
    SQLALCHEMY_DATABASE_URI = SQL_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = None
    MYSQL_DATABASE_CHARSET = 'utf8mb4'
    UPLOAD_FOLDER = './static'