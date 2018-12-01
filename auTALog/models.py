from auTALog import db
from datetime import datetime
import flask_security


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session = db.Column(db.Integer, db.ForeignKey('tutoring_session.id'))
    student = db.Column(db.Integer, nullable=False)
    subject = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now())
    comment = db.Column(db.Text, nullable=True)


roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class TutoringSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ta = db.Column(db.Integer, db.ForeignKey('user.id'))
    started = db.Column(db.DateTime)
    ended = db.Column(db.DateTime)

    def __repr__(self):
        return "Tutoring session {}".format(self.id)


class Role(db.Model, flask_security.RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, flask_security.UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
        backref=db.backref('users', lazy='dynamic'))    


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(80), nullable=False, unique=True)
