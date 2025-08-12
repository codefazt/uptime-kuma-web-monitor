import os
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'supersecretkey')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://admin:admin@postgres:5432/APPFLOW')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
