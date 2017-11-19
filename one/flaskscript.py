#encoding=utf-8
from flask import Flask,render_template
from flask_script import Manager,Command,Option
app = Flask(__name__)
manager = Manager(app)

#一、使用装饰器
#使用@manager.command创建扩展命令，函数名hello会作为flask-script的一个扩展命令
@manager.command
def hello():
    print 'this is a hello command using @manager.command'
#使用@manager.option
@manager.option('--name','-n',dest='name',default='liyubin')
@manager.option('--url','-u',dest='url',default=None)
def hellooption(name,url):
    if url is None:
        print 'hello',name
    else:
        print 'hello',name,'from',url
    
#二、使用Command子类
#使用Command子类创建扩展命令
class HelloClass(Command):
    def run(self):
        print 'this is a hello command using HelloClass class extend Command'
manager.add_command('helloClass',HelloClass())
#使用Command子类和Option创建带附加命令的扩展方法
class HelloOption(Command):
    option_list = (
        Option('--name','-n',dest='dame',default='liyubin'),
    )
    def run(self,dame):
        print ('hello %s' % dame)
manager.add_command('helloOption',HelloOption())




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