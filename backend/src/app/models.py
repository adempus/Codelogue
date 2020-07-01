"""
Data models used for MySql migrations
"""

from flask_sqlalchemy import SQLAlchemy
import sqlalchemy


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    first_name = db.Column(db.String(75), unique=False, nullable=False)
    last_name = db.Column(db.String(75), unique=False, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    def __init__(self, firstName, lastName, userName, email, password):
        self.first_name = firstName
        self.last_name = lastName
        self.username = userName
        self.email = email
        self.password = password

    def __repr__(self):
        return  f'user id: {self.id}'
