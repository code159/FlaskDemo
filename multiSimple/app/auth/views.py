#encoding=utf-8
from flask import render_template,flash,redirect,request,url_for
from . import auth
from .forms import LoginForm,RegistrationForm
from ..models import User
from flask_login import login_user,logout_user,login_required
from .. import db

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.checkPassword(form.password.data):
            #login_user() 函数的参数是要登录的用户，以及可选的“记住我”布尔值，“记住我”也在表单中填写。底层是从load_user回调函数中返回用户的
            #如果值为 False，那么关闭浏览器后用户会话就过期了，所以下次用户访问时要重新登录。 
            #如果值为 True，那么会在用户浏览器中写入一个长期有效的 cookie，使用这个 cookie 可以复现用户会话。
            login_user(user, form.remember_me.data)
            #用户访问未授权的 URL 时会显示登录表单， Flask-Login会把原地址保存在查询字符串的 next 参数中，这个参数可从 request.args 字典中读取。
            #如果查询字符串中没有 next 参数，则重定向到首页。
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,username=form.username.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You can now login.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',form=form)