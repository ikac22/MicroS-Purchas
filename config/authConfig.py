from datetime import timedelta
import os


class Configuration:
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:root@{os.environ.get('DATABASE_URL') or 'localhost:3307'}/authentication"

    JWT_SECRET_KEY = "JWT_SECRET_KEY"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
