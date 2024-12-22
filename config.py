import os

class Config:
    MYSQL_HOST = os.environ.get('MYSQL_HOST', '98.82.14.185')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'admin')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'admin123')
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'usersdb')
    
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
