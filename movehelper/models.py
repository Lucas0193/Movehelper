from datetime import datetime
from movehelper.tools import db
from sqlalchemy import func
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class UserAccount(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, index=True)
    email = db.Column(db.String(254), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    reg = db.Column(db.DateTime(timezone=True), server_default=func.now())
    fname = db.Column(db.String(70))
    mname = db.Column(db.String(70))
    lname = db.Column(db.String(70))
    birth = db.Column(db.Date)
    gender = db.Column(db.String(20))
    img = db.Column(db.String(200))
    phone = db.Column(db.String(16))
    onid = db.Column(db.String(16))
    license = db.Column(db.String(200))
    def create_password(self, password):
        self.password_hash = generate_password_hash(password)
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    confirmed = db.Column(db.Boolean, default=False)
    certificated = db.Column(db.Boolean, default=False)
    status = db.Column(db.Boolean, default=True)
    ut = db.relationship('UserTasks', back_populates='ua')
    to = db.relationship('TaskOrders', back_populates='ua')
    def __repr__(self):
        return '%s %s' % (self.id, self.username)


class UserTasks(db.Model):
    id = db.Column( db.Integer, primary_key=True)
    pubtime = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    title = db.Column(db.String(70))
    context = db.Column(db.Text)
    contact = db.Column(db.String(20))
    location = db.Column(db.String(100))
    mpnum = db.Column(db.Integer)
    mpnume = db.Column(db.Integer, default=0)
    status = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_account.id'))
    ua = db.relationship('UserAccount', back_populates='ut')
    to = db.relationship('TaskOrders', back_populates='ut')
    def __repr__(self):
        return '%s %s %s %s %s %s %s %s %s %s' % (self.id, self.pubtime, self.title, self.context, self.contact, self.location, self.mpnum, self.mpnume, self.status, self.user_id)


class TaskOrders(db.Model):
    id = db.Column( db.Integer, primary_key=True)
    createtime = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    status = db.Column(db.Boolean, default=True)
    manpower = db.Column(db.Integer, db.ForeignKey('user_account.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('user_tasks.id'))
    ut = db.relationship('UserTasks', back_populates='to')
    ua = db.relationship('UserAccount', back_populates='to')
    def __repr__(self):
        return '%s %s %s %s %s' % (self.id, self.createtime, self.manpower, self.status, self.task_id)