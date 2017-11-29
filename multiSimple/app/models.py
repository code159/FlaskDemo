#encoding=utf-8
from flask_sqlalchemy import SQLAlchemy
from . import db
from werkzeug import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager

class User(UserMixin,db.Model):
    __tablename__='users'
    
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    
    @property
    def password(self):
        raise AttributeError('password is not readable!')
    @password.setter
    def password(self,value):
        self.password_hash = generate_password_hash(value)
    def checkPassword(self,value):
        return check_password_hash(self.password_hash,value)
    #即使是相同的明文，产生的散列值也是不一样的，因为盐值不同
    def getHash(self,value):
        return ' password_hash:'+self.password_hash+' value:'+generate_password_hash(value)
    
    #Flask-Login 要求程序实现一个回调函数，加载用户的回调函数接收以 Unicode 字符串形式表示的用户标识符。如果能找到用户，这个函数必须返回用户对象；否则应该返回 None。
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')