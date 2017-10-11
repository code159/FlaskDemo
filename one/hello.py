from flask import Flask,url_for,request
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'
	
@app.route('/flask')
@app.route('/flask1')
def hello_flask():
    return 'Hello Flask!'

@app.route('/user/<username>')
def user(username):
    return '<h1>Hello,%s!</h1>' % username

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/req_ctx')
def req_context():
    req_ctx=app.test_request_context()
    req_ctx.push()
    user_agent=request.headers.get('Host')
    return '<h2>Your brower is %s</h2>' % user_agent
	
@app.route('/req')
def req():
    return '<h1>Bad Request!</h1>',400

with app.test_request_context():
    print url_for('hello_flask',_external=True)
    print url_for('hello_flask', next='/')
    print url_for('show_user_profile', username='LiYuBin')

if __name__ == '__main__':
    app.debug = True
    app.run()