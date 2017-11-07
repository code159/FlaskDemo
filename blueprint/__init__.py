from flask import Flask
from .admin import admin
from .user import user

app=Flask(__name__)

@app.route('/')
def index():
    return '<h1>this is index page!</h1>'
#@app.route('/user/tom')
#def user_tom():
#    return 'user tom'
#@app.route('/user/lucy')
#def user_lucy():
#    return 'user lucy'
#
#@app.route('/admin/jerry')
#def admin_jerry():
#    return 'admin jerry'
#@app.route('/admin/jack')
#def admin_jack():
#    return 'admin jack'

if __name__ == '__main__':
    app.register_blueprint(admin,url_prefix='/user')
    app.register_blueprint(user,url_prefix='/admin')
    app.run(debug=True)
