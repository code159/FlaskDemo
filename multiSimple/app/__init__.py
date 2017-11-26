#encoding=utf-8
from flask import Flask, render_template 
from flask_bootstrap import Bootstrap 
from flask_sqlalchemy import SQLAlchemy 
from config import config
from flask_login import LoginManager

bootstrap = Bootstrap() 
db = SQLAlchemy()
login_manager = LoginManager()

#程序工厂函数
def create_app(config_name): 
    app = Flask(__name__) 
    app.config.from_object(config[config_name]) 
    config[config_name].init_app(app)
    
    bootstrap.init_app(app) 
    db.init_app(app)
    # 附加路由和自定义的错误页面
    from .main import main as main_blueprint
    #蓝本在程序工厂函数中注册到程序上
    app.register_blueprint(main_blueprint)
    
    return app