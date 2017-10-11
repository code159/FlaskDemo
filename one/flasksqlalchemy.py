#encoding=utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#flaskmigrate.py里有模型，但像这样导入后不能返回最新的数据，不是动态的。。。
#from flaskmigrate import Role,User
import flaskmigrate
import os

basedir=os.path.abspath(os.path.dirname(__file__))

app=Flask(__name__)

#sqlite
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqlite')
#mysql
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:mysql3306@localhost/flask'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True

db=SQLAlchemy(app)

#注意在改删数据时，对象要从数据库里查出数据后重建
@app.route('/create')
def create():
    db.create_all()
    return '<h1>create table successfully</h1>'
@app.route('/drop')
def drop():
    db.drop_all()
    return '<h1>drop table successfully</h1>'
@app.route('/insert')
def insert():
    id1 = admin_role.id
    if id1 is None:
        id1='None'
    db.session.add_all([flaskmigrate.admin_role, flaskmigrate.mod_role, flaskmigrate.user_role, flaskmigrate.user_john, flaskmigrate.user_susan, flaskmigrate.user_david])
    db.session.commit()
    id2 = admin_role.id
    return '<h1>insert '+str(id1)+' '+str(id2)+' successfully</h1>'
@app.route('/insert_user/<username>')
def insert_user(username):
    user=flaskmigrate.User(username=username)
    db.session.add(user)
    db.session.commit()
    return '<h1>insert '+user.username+' successfully</h1>'
@app.route('/insert_role/<name>')
def insert_role(name):
    role=flaskmigrate.Role(name=name)
    db.session.add(role)
    db.session.commit()
    return '<h1>insert '+role.name+' successfully</h1>'
@app.route('/update')
def update():
    reload(flaskmigrate)
    admin_role = flaskmigrate.Role.query.filter_by(id='2').first()
    admin_role.name='master'
    #db.session.add()也可以
    db.session.merge(admin_role)
    db.session.commit()
    return '<h1>update successfully</h1>'
@app.route('/delete/<rolename>')
def delete(rolename):
    reload(flaskmigrate)
    deleted_role = flaskmigrate.Role.query.filter_by(name=rolename).first()
    if deleted_role is None:
        return 'Nothing to delete'
    db.session.delete(deleted_role)
    db.session.commit()
    return '<h1>delete successfully</h1>'
@app.route('/query_all')
def query_all():
    reload(flaskmigrate)
    out='Role:\n<ul>'
    print flaskmigrate.Role.query.all()
    for result in flaskmigrate.Role.query.all():
        out=out+'<li>'+str(result.name)+'</li>\n'
    out=out+'</ul>\nUser:\n<ul>'
    for result in flaskmigrate.User.query.all():
        out=out+'<li>'+str(result.username)+'</li>\n'
    out=out+'</ul>\n'    
    return out
@app.route('/query_filter/<rolename>')
def query_filter(rolename):
    reload(flaskmigrate)
    out=rolename+':\n<ul>'
    queryed_role = flaskmigrate.Role.query.filter_by(name=rolename).first()
    for result in flaskmigrate.User.query.filter_by(role=queryed_role).all():
        out=out+'<li>'+str(result.username)+'</li>\n'
    out=out+'</ul>\n'
    return out

if __name__ == '__main__':
    app.debug=True
    app.run()
