#encoding=utf-8
from flask import Flask, render_template 
from flask_bootstrap import Bootstrap 
from flask_sqlalchemy import SQLAlchemy 
from config import config
from flask_login import LoginManager
from flask_mail import Mail

bootstrap = Bootstrap() 
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
#提供不同的安全等级防止用户会话遭篡改。 设为 'strong' 时， Flask-Login 会记录客户端 IP地址和浏览器的用户代理信息， 如果发现异动就登出用户。 
login_manager.session_protection='strong'
#login_view设置登陆页面的端口
login_manager.login_view='auth.login'

#程序工厂函数
def create_app(config_name): 
    app = Flask(__name__) 
    app.config.from_object(config[config_name]) 
    config[config_name].init_app(app)
    
    bootstrap.init_app(app) 
    db.init_app(app)
    login_manager.init_app(app)
    main.init_app(app)
    # 附加路由和自定义的错误页面
    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
    #蓝本在程序工厂函数中注册到程序上
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint,url_prefix='/auth')
    
    return app