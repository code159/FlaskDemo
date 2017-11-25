#encoding=utf-8
from flask import Blueprint

main = Blueprint('main',__name__)

#避免循环导入依赖，因为在views.py、errors.py还要导入蓝本main
from . import views,errors,views2