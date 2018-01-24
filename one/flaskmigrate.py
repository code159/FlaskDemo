#encoding=utf-8
'''
#创建迁移仓库
python flaskmigrate.py db init
#创建迁移脚本
python flaskmigrate.py db migrate -m "initial migration"
#更新数据库
python flaskmigrate.py db upgrade
#取消更新
python flaskmigrate.py db downgrade
'''
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Shell
from flask_migrate import Migrate,MigrateCommand
from flask import Flask
from datetime import datetime
import os

basedir=os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

#sqlite
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqlite')
#mysql
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:mysql3306@localhost/test'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True

#db=SQLAlchemy(app)
db=SQLAlchemy(app)

#flask-migrate可在不用删除数据的情况下修改表结构，可回滚修改。
manager = Manager(app)
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)

#定义模型
class Role(db.Model): 
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User',backref='role')
    def __repr__(self): 
        return '<Role %r>' % self.name
class User(db.Model): 
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    def __repr__(self):
        return '<User %r>' % self.username
    #followed被此人关注，follower关注此人
    #使用join关联Follow、Post，再过滤此人用户id，查出此人关注的所有人写的所有文章
    def followed_posts(self):
        return Post.query.join(Follow, Follow.followed_id == Post.author_id).filter(Follow.follower_id == self.id)

admin_role=Role(name='Admin')
mod_role = Role(name='Moderator') 
user_role = Role(name='User')
user_john = User(username='john', role=admin_role) 
user_susan = User(username='susan', role=user_role)
user_david = User(username='david', role=user_role)

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

#shell下可操作变量
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Post=Post, Follow=Follow)
manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    #app.run()
    manager.run()