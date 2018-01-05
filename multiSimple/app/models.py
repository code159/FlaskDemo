#encoding=utf-8
from flask_sqlalchemy import SQLAlchemy
from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin,AnonymousUserMixin
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
    
    #检查用户是否有指定的权限
    def can(self,permissions):
        return self.role is not None and (self.role.permissions & permissions) == permissions
    def is_administrator(self):
        return self.can(Permission.ADMINISTER)
        
    #Flask-Login 要求程序实现一个回调函数，加载用户的回调函数接收以 Unicode 字符串形式表示的用户标识符。如果能找到用户，这个函数必须返回用户对象；否则应该返回 None。
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    '''赋予角色，普通用户赋默认权限，管理员用户根据邮件配置赋管理员权限'''
    def __init__(self,**kwargs):
        #User 类的构造函数首先调用基类的构造函数，如果创建基类对象后还没定义角色，则根据电子邮件地址决定将其设为管理员还是默认角色。
        super(User,self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

class AnonymousUser(AnonymousUserMixin):
    def can(self,Permission):
        return False
    def is_administrator(self):
        return False

#将其设为用户未登录时current_user 的值。这样程序不用先检查用户是否登录，就能自由调用 current_user.can() 和current_user.is_administrator()
login_manager.anonymous_user = AnonymousUser
    
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')
    
    '''生成角色信息'''
    @staticmethod
    def insert_roles():
        roles = {
                 'User' : (Permission.FOLLOW | Permission.COMMENT | Permission.MODERATE_COMMENTS, True),
                 'Moderator' : (Permission.FOLLOW | Permission.COMMENT | Permission.MODERATE_COMMENTS | Permission.MODERATE_COMMENTS, False),
                 'Administrator' :(Permission.FOLLOW | Permission.COMMENT | Permission.MODERATE_COMMENTS | Permission.ADMINISTER, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.default = roles[r][1]
            role.permissions = roles[r][0]
            db.session.add(r)
        db.session.commit()
    
class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80