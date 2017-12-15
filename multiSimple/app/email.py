#encoding=utf-8
from flask_mail import Message
from threading import Thread
from . import mail
from flask import current_app,render_template


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
    #非常重要，app是通过程序工厂函数创建的，不能直接导入
    app = current_app._get_current_object()
    
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,sender=app.config['MAIL_USERNAME'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email,args=[app,msg])
    thr.start()
    return thr