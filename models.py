from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()


class User(database.Model):
    __tablename__ = "user"
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(256), nullable=False)
    password = database.Column(database.String(256), nullable=False)
    forename = database.Column(database.String(256), nullable=False)
    surname = database.Column(database.String(256), nullable=False)
    def __repr__(self):
        return f"({self.id},{self.username})"