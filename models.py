from flask_sqlalchemy import SQLAlchemy

#Creating a new SQLAlchemy object
db = SQLAlchemy()

#Base model for other classes to inherit
class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),onupdate=db.func.current_timestamp())

#Model to store poll topics
class Topics(Base):
    title = db.Column(db.String(500))

    #Representation of Topics class
    def __repr__(self):
        return self.title

#Model for poll options
class Options(Base):
    name = db.Column(db.String(200))

#Model to connect topics and options
class Polls(Base):
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'))
    option_id = db.Column(db.Integer, db.ForeignKey('options.id'))
    vote_count = db.Column(db.Integer, default=0)
    #Status tells us whether the poll is open or closed
    status = db.Column(db.Boolean)

    # Relationship declaration (makes it easier for us to access the polls model
    # from the other models it's related to)
    topic = db.relationship('Topics', foreign_keys=[topic_id],backref=db.backref('options', lazy='dynamic'))
    option = db.relationship('Options',foreign_keys=[option_id])

    def __repr__(self):
        return self.option.name

class Users(Base):
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200))
