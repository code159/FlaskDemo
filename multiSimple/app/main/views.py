#encoding=utf-8
from . import main

@main.route('/', methods=['GET', 'POST']) 
def index2():
    return 'this is app/main/views'