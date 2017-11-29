#encoding=utf-8
from . import main
from flask_login import login_required

@main.route('/index2', methods=['GET', 'POST']) 
#@login_required
def index2():
    return 'this is app/main/views2'