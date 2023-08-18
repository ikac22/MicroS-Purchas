import os

class Configuration:
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:root@{os.environ.get('DATABASE_URL') or 'localhost:3306'}/shop"
    JWT_SECRET_KEY = "JWT_SECRET_KEY"
