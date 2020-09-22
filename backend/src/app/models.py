"""
Data models used for MySql migrations
"""

import sqlalchemy
from flask_sqlalchemy import SQLAlchemy


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


class Folder(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    snippets = db.relationship('Snippet', backref='folder', lazy=True)

snippetTags = db.Table('tagged_snippets',
                         db.Column('tag_id', db.BigInteger, db.ForeignKey('tag.id')),
                         db.Column('snippet_id', db.BigInteger, db.ForeignKey('snippet.id')))

class Snippet(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False)
    folder_id = db.Column(db.BigInteger, db.ForeignKey('folder.id'), nullable=True)
    language_id = db.Column(db.BigInteger, db.ForeignKey('programming_language.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=True)
    programmingLanguage = db.relationship('ProgrammingLanguage', backref='Snippet', lazy=True)
    tags = db.relationship('Tag', secondary=snippetTags, lazy='subquery',
        backref=db.backref('snippets', lazy=True))
    taggedSnippets = db.relationship('TaggedSnippets',  backref='snippet', lazy=True)
    date_created = db.Column(db.DateTime, nullable=False)


class ProgrammingLanguage(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    snippets = db.relationship('Snippet', backref='ProgrammingLanguage', lazy=True)


class Tag(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False)
    keyword = db.Column(db.String(100), nullable=False)


class TaggedSnippets(db.Model):
    __table_args__ = {'extend_existing': True}
    tag_id = db.Column(db.BigInteger, db.ForeignKey('tag.id'), primary_key=True)
    snippet_id = db.Column(db.BigInteger, db.ForeignKey('snippet.id'), primary_key=True)
    tag = db.relationship('Tag')