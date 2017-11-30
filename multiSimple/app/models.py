#encoding=utf-8
from flask_sqlalchemy import SQLAlchemy
from . import db
from werkzeug import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

class User(UserMixin,db.Model):
    __tablename__='users'
    
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
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
    
    #生成确认令牌
    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm':self.id})
    #验证确认令牌
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            #loads()唯一的参数是令牌字符串。这个方法会检验签名和过期时间，如果通过，返回原始数据。如果提供给 loads()的令牌不正确或过期了，则抛出异常
            #若无异常只能保证令牌是正确的，但不能保证此令牌是当前用户的
            data = s.loads(token)
        except:
            return False
        #防止恶意用户知道生产令牌的方法来确认其他用户
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True
        
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