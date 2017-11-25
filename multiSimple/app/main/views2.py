#encoding=utf-8
from . import main

@main.route('/index2', methods=['GET', 'POST']) 
def index():
    return 'this is app/main/views2'