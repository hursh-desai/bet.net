from app import db,migrate
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Index,func,cast
from sqlalchemy.dialects import postgresql
import datetime

class Agreement(db.Model):
    __tablename__ = 'agreements'
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    engagor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    bet_id = db.Column(db.Integer, db.ForeignKey('bets.id'))
    final = db.Column(db.Boolean())
    bet = db.relationship('Bet', backref='agreements')

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True)
    password_hash = db.Column(db.String())
    bets = db.relationship('Bet', backref='creator')

    agreed = db.relationship(
        'User', 
        secondary='agreements',
        primaryjoin=(Agreement.creator_id == id),
        secondaryjoin=(Agreement.engagor_id == id),
        backref=db.backref('engaged_in', lazy='dynamic'), 
        lazy='dynamic',
        )
    
    bets_engaged_in = db.relationship(
        'Bet', 
        secondary='agreements',
        primaryjoin=(Agreement.engagor_id == id),
        backref=db.backref('engaged_in', lazy='dynamic'),
        )
    
    agreements_engaged_in = db.relationship(
        'Agreement', 
        primaryjoin=(Agreement.engagor_id == id), 
        backref=db.backref("engagor"),
        )

#     registered_on = db.Column(db.DateTime(timezone=True))
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    access = db.Column(db.Boolean())
    decider_url = db.Column(db.String(30))
    date = db.Column(db.DateTime(timezone=True), index=True, default=datetime.datetime.utcnow)

def create_tsvector(*args):
    exp = args[0]
    for e in args[1:]:
        exp += ' ' + e
    return func.to_tsvector('english', exp)

class Bet(db.Model):
    __tablename__ = 'bets'
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_name = db.Column(db.String(30))
    bet_amount = db.Column(db.Integer)
    access = db.Column(db.Boolean())
    date = db.Column(db.DateTime(timezone=True), index=True, default=datetime.datetime.utcnow)
    __ts_vector__ = create_tsvector(
        cast(func.coalesce(event_name, ''), postgresql.TEXT)
    )
    

    __table_args__ = (
        Index(
            'event_name_tsv',
            __ts_vector__,
            postgresql_using='gin'
            ),
        )
    

    