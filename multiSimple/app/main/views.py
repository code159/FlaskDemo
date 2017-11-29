#encoding=utf-8
from . import main
from flask_login import login_required
from flask import render_template

@main.route('/', methods=['GET', 'POST']) 
#login_required 修饰器保护路由只让认证用户访问
#@login_required
def index():
    return render_template('index.html')