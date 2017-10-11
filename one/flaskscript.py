from flask import Flask,render_template
from flask_script import Manager
app = Flask(__name__)
manager = Manager(app)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html',username=name)

@app.route('/comment/')
def comment():
    comments=['li','yu','bin','very','good']
    return render_template('for.html',comments=comments)

@app.route('/extends/')
def extends():
    return render_template('extends.html')

if __name__ == '__main__':
    app.debug = True
#    app.run()
    manager.run()