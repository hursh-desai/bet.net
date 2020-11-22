from app import db,migrate
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Index,func,cast
from sqlalchemy.dialects import postgresql
import datetime


def create_tsvector(*args):
    exp = args[0]
    for e in args[1:]:
        exp += ' ' + e
    return func.to_tsvector('english', exp)

class Bet(db.Model):
    __tablename__ = 'bets'
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_name = db.Column(db.String(30), db.ForeignKey('events.name'))
    amount = db.Column(db.Integer)
    y_n = db.Column(db.Boolean())
    date = db.Column(db.DateTime(timezone=True), index=True, default=datetime.datetime.utcnow)
    __ts_vector__ = create_tsvector(
        cast(func.coalesce(event_name, ''), postgresql.TEXT)
    )

    Index('event_name_tsv', __ts_vector__, postgresql_using='gin')

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    moderator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    access = db.Column(db.Boolean())
    decision = db.Column(db.Boolean())
    date = db.Column(db.DateTime(timezone=True), index=True, default=datetime.datetime.utcnow)
    bets = db.relationship('Bet', backref='event')
    __ts_vector__ = create_tsvector(
        cast(func.coalesce(name, ''), postgresql.TEXT)
    )

    Index('name_tsv', __ts_vector__, postgresql_using='gin')

class Agreement(db.Model):
    __tablename__ = 'agreements'
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    engagor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    bet_id = db.Column(db.Integer, db.ForeignKey('bets.id'))
    final = db.Column(db.Boolean())
    event = db.relationship(
        'Event', 
        secondary='bets',
        backref=db.backref('agreements', lazy='dynamic'), 
        uselist=False,
        viewonly=True,
        sync_backref=False
        )
    bet = db.relationship('Bet', backref='agreements', lazy='joined')
    date = db.Column(db.DateTime(timezone=True), index=True, default=datetime.datetime.utcnow)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True)
    password_hash = db.Column(db.String())
    bets_created = db.relationship('Bet', backref='creator')
    events_created = db.relationship('Event', primaryjoin=(Event.creator_id == id), backref='creator')
    events_moderated = db.relationship('Event', primaryjoin=(Event.moderator_id == id),  backref='moderator')
    date = db.Column(db.DateTime(timezone=True), index=True, default=datetime.datetime.utcnow)
    
    bets_engaged_in = db.relationship(
        'Bet', 
        secondary='agreements',
        primaryjoin=(Agreement.engagor_id == id),
        backref=db.backref('engaged_in', lazy='dynamic'),
        )
    
    agreements_engaged_in = db.relationship(
        'Agreement',
        primaryjoin=(Agreement.engagor_id == id),
        lazy='dynamic',
        backref=db.backref('engagor'),
        )

    agreements_created = db.relationship(
        'Agreement',
        primaryjoin=(Agreement.creator_id == id),
        lazy='dynamic',
        backref=db.backref('creator'),
        )
    
    agreements_in = db.relationship(
        'Agreement', 
        primaryjoin="or_(User.id==Agreement.creator_id, "
                        "User.id==Agreement.engagor_id)",
        lazy='dynamic',
        )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)
    


    