from flask import Flask
from admin.admin_views import admin as admin_bp
from user.user_views import user as user_bp

app=Flask(__name__)
app.register_blueprint(admin_bp,url_prefix='/admin')
app.register_blueprint(user_bp,url_prefix='/user')

@app.route('/')
def index():
    return '<h1>this is index page!</h1>'

