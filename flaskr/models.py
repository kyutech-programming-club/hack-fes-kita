from sqlalchemy.orm import synonym
from werkzeug import check_password_hash, generate_password_hash

from flaskr import db


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), default='', nullable=False)
    description = db.Column(db.String(100), default='', nullable=False)
    day = db.Column(db.String(100), default='', nullable=False)
    room = db.Column(db.String(100), default='', nullable=False)
    time = db.Column(db.String(100), default='', nullable=False)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), default='', nullable=False)

    @classmethod
    def authenticate(cls, query, name):
        user = query(cls).filter(cls.name==name).first()
        return user

    def __repr__(self):
        return u'<User id={self.id} name={self.name!r}>'.format(
                self=self)

class Entry(db.Model):
    __tablename__ = 'entries'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    text = db.Column(db.Text)

    def __repr__(self):
        return '<Entry id={id} title={title!r}>'.format(
                id=self.id, title=self.title)

def init():
    db.create_all() 
