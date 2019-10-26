from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import synonym, relationship
from werkzeug import check_password_hash, generate_password_hash
from sqlalchemy.ext.declarative import declarative_base


from flaskr import db

category_post_association = Table('category_post_association', db.Model.metadata,
        Column('category_id', Integer, ForeignKey('categories.id')),
        Column('post_id', Integer, ForeignKey('posts.id'))
)
category_event_association = Table('category_event_association', db.Model.metadata,
        Column('category_id', Integer, ForeignKey('categories.id')),
        Column('event_id', Integer, ForeignKey('events.id'))
)
category_user_association = Table('category_user_association', db.Model.metadata,
        Column('category_id', Integer, ForeignKey('categories.id')),
        Column('user_id', Integer, ForeignKey('users.id'))
)

class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), default='', nullable=False)
    description = db.Column(db.String(100), default='', nullable=False)
    day = db.Column(db.String(100), default='', nullable=False)
    room = db.Column(db.String(100), default='', nullable=False)
    time = db.Column(db.String(100), default='', nullable=False)
    categories = relationship("Category", secondary=category_event_association, back_populates="events")
    #  email = db.Column(db.String(100), unique=True, nullable=False)
    #  _password = db.Column('password', db.String(100), nullable=False)

#    def _get_password(self):
#        return self._password
#    def _set_password(self, password):
#        if password:
#            password = password.strip()
#        self._password = generate_password_hash(password)
#    password_descriptor = property(_get_password, _set_password)
#    password = synonym('_password', descriptor=password_descriptor)

#    def check_password(self, password):
#        password = password.strip()
#        if not password:
#            return False
#        return check_password_hash(self.password, password)

#    @classmethod
#    def authenticate(cls, query, email, password):
#        user = query(cls).filter(cls.email==email).first()
#        if user is None:
#            return None, False
#        return user, user.check_password(password)
#
#    def __repr__(self):
#        return u'<User id={self.id} email={self.email!r}>'.format(
#                self=self)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), default='', nullable=False)
    categories = relationship("Category", secondary=category_user_association, back_populates="users")

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


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    posts = relationship("Post", secondary=category_post_association, back_populates="categories")
    events = relationship("Event", secondary=category_event_association, back_populates="categories")
    users = relationship("User", secondary=category_user_association, back_populates="categories")

    def __repr__(self):
        return '<Entry id={id} name={name!r}>'.format(
                id=self.id, name=self.name)


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    body = db.Column(db.Text)
    categories = relationship("Category", secondary=category_post_association, back_populates="posts")

    def __repr__(self):
        return '<Entry id={id} title={title!r}>'.format(
                id=self.id, title=self.title)


def init():
    db.create_all() 
