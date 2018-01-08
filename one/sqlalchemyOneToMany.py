#encoding=utf-8
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os

app = Flask(__name__)
basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mysql3306@localhost/test'
app.config['SQLALCHEMY_COMMIT_ON_TEARDWON'] = True
db = SQLAlchemy(app)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    users = db.relationship('User', backref='role', lazy='joined')
    def __repr__(self):
        return 'Role['+str(self.id)+' '+self.name+']'

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    def __init__(self,name,role_id):
        self.name=name
        self.role_id=role_id
    def __repr__(self):
        return 'User['+str(self.id)+' '+self.name+' '+str(self.role_id)+']'

@app.route('/create')
def create():
    db.create_all()
    return '<h1>create successfully!</h1>'

@app.route('/insert_role/<name>')
def insert_role(name):
    role = Role(name=name)
    db.session.add(role)
    db.session.commit()
    inserted = Role.query.filter_by(name=name).first()
    return 'insert '+str(inserted)+' successfully!'

@app.route('/insert_user/<name>/<role_id>')
def insert_user(name, role_id):
    user = User(name=name,role_id=role_id)
    db.session.add(user)
    db.session.commit()
    inserted = User.query.filter_by(name=name).first()
    return 'insert '+str(inserted)+' successfully!'

@app.route('/query')
def query():
    result='<h3>User:</h3>'
    for r in User.query.all():
        result+=('<p>'+str(r)+'</p>')
    result+='<h3>Role:</h3>'
    for r in Role.query.all():
        result+=('<p>'+str(r)+'</p>')
    # backref反向引用：Role通过users查看对应所有用户，User通过role查看对应角色
    role=Role.query.filter_by(id=1).first()
    for r in role.users:
        print r
    user=User.query.filter_by(id=7).first()
    print user.role

    return result

@app.route('/drop')
def drop():
    db.drop_all()
    return '<h1>drop successfully!</h1>'

if __name__ == '__main__':
    app.run(debug=True)