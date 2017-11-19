#encoding=utf-8
from flask import Flask,render_template,session,redirect,url_for
from flask_mail import Mail,Message
import flaskmigrate
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from form import NameForm
from threading import Thread
import os

app = Flask(__name__)

app.config['SECRET_KEY']='password'

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(os.path.abspath(__file__),'data.sqlite')
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:mysql3306@localhost/flask'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN']=True

app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
#需要首先在当前环境中配置MAIL_USERNAME、MAIL_PASSWORD
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'

mail = Mail(app)
boostrap = Bootstrap(app)
db=SQLAlchemy(app)

#在多线程中要手动创建激活上下文，这样扩展才能使用
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

#同步发送邮件
def send_sync_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,sender=app.config['MAIL_USERNAME'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)
#异步发送邮件
def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,sender=app.config['MAIL_USERNAME'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email,args=[app,msg])
    thr.start()
    return thr

@app.route('/',methods=['GET','POST'])
def index():
    form=NameForm()
    if form.validate_on_submit():
        reload(flaskmigrate)
        #db.session.remove()
        role=flaskmigrate.Role.query.filter_by(name=form.name.data).first()
        if role is None:
            role=flaskmigrate.Role(name=form.name.data)
            db.session.add(role)
            session['known']=False
            send_email(form.to.data, 'New Role','mail/new_role', role=role)
            db.session.commit()    
        else:
            session['known']=True    
            
        session['name']=form.name.data
        form.name.data=''
        form.to.data=''
        
        return redirect(url_for('index'))
    return render_template('mailform.html',form=form,name=session.get('name'),known=session.get('known',False))    
@app.route('/query_all')
def query_all():
    reload(flaskmigrate)
    out='Role:\n<ul>'
    print flaskmigrate.Role.query.all()
    for result in flaskmigrate.Role.query.all():
        out=out+'<li>'+str(result.name)+'</li>\n'
    out=out+'</ul>\n'    
    return out
@app.route('/insert/<name>')
def insert_role(name):
    role=flaskmigrate.Role(name=name)
    db.session.add(role)
    db.session.commit()
    return '<h1>insert '+role.name+' successfully</h1>'

if __name__ == '__main__':
    print os.path.abspath(os.path.dirname(__file__))
    print os.environ.get('MAIL_USERNAME')
    app.debug = True
#    app.run()
    app.run()