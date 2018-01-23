#encoding=utf-8
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_script import Manager,Shell
from datetime import datetime
import os

app = Flask(__name__)
basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql3306@localhost/test'
app.config['SQLALCHEMY_COMMIT_ON_TEARDWON'] = True
db = SQLAlchemy(app)
manager = Manager(app)

def make_shell_context():
    return dict(app=app, db=db, Student=Student, Class=Class)
manager.add_command('shell', Shell(make_context=make_shell_context))

'''
普通多对多（只有对应关系）
registrations是完全由sqlalchemy掌握的内部表，将多对多关系分解为两个一对多关系
'''
registrations = db.Table('registrations',
                         db.Column('student_id', db.Integer, db.ForeignKey('students.id')),
                         db.Column('class_id', db.Integer, db.ForeignKey('classes.id')))
class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    classes = db.relationship('Class', secondary=registrations, backref='students')
    def __init__(self,id,name):
        self.id=id
        self.name=name
class Class(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    def __init__(self,id,name):
        self.id=id
        self.name=name

'''
高级多对多（可附加关联信息如关注时间）
'''
class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'),primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'),primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now)
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    followed = db.relationship('Follow',
                               foreign_keys=[Follow.follower_id],
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    followers = db.relationship('Follow',foreign_keys=[Follow.followed_id],
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')

@app.route('/create')
def create():
    db.create_all()
    return '<h1>create successfully!</h1>'

@app.route('/insert')
def insert():
    s=Student(1,'lyb')
    c=Class(300,'english')
    s.classes.append(c)

    s=Student(id=2,name='liyubin')
    c=Class(500,'computer')
    c.students.append(s)

    db.session.commit()

@app.route('/drop')
def drop():
    db.drop_all()
    return '<h1>drop successfully!</h1>'

if __name__ == '__main__':
    app.debug=True
    manager.run()