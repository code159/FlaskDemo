#encoding=utf-8
from flask_sqlalchemy import SQLAlchemy
from . import db
from werkzeug import generate_password_hash,check_password_hash

class User(db.Model):
    __tablename__='users'
    
    id = db.Column(db.Integer,primary_key=True)
    
    password_hash = db.Column(db.String(128))
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