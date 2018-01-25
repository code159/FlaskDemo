#encoding=utf-8
#flaskmigrate.py里有模型，但像这样导入后不能返回最新的数据，不是动态的。。。
#from flaskmigrate import Role,User


from flaskmigrate import app,db, admin_role, mod_role, user_role, user_john, user_susan, user_david, User, Role, Post
from flask import request,render_template

#注意在改删数据时，对象要从数据库里查出数据后重建
@app.route('/create')
def create():
    db.create_all()
    return '<h1>create table successfully</h1>'
@app.route('/drop')
def drop():
    db.drop_all()
    return '<h1>drop table successfully</h1>'
@app.route('/insert')
def insert():
    id1 = admin_role.id
    if id1 is None:
        id1='None'
    db.session.add_all([admin_role, mod_role, user_role, user_john, user_susan, user_david])
    db.session.commit()
    id2 = admin_role.id
    return '<h1>insert '+str(id1)+' '+str(id2)+' successfully</h1>'
@app.route('/insert_user/<username>')
def insert_user(username):
    user=User(username=username)
    db.session.add(user)
    db.session.commit()
    return '<h1>insert '+user.username+' successfully</h1>'
@app.route('/insert_role/<name>')
def insert_role(name):
    role=Role(name=name)
    db.session.add(role)
    db.session.commit()
    return '<h1>insert '+role.name+' successfully</h1>'
@app.route('/update')
def update():
    admin_role = Role.query.filter_by(id='3').first()
    admin_role.name='master1'
    #db.session.add()也可以
    db.session.add(admin_role)
    db.session.commit()
    return '<h1>update successfully</h1>'
@app.route('/delete/<rolename>')
def delete(rolename):
    deleted_role = Role.query.filter_by(name=rolename).first()
    if deleted_role is None:
        return 'Nothing to delete'
    db.session.delete(deleted_role)
    db.session.commit()
    return '<h1>delete successfully</h1>'
@app.route('/query_all')
def query_all():
    out='Role:\n<ul>'
    print Role.query.all()
    for result in Role.query.all():
        out=out+'<li>'+str(result.name)+'</li>\n'
    out=out+'</ul>\nUser:\n<ul>'
    for result in User.query.all():
        out=out+'<li>'+str(result.username)+'</li>\n'
    out=out+'</ul>\n'    
    return out
@app.route('/query_filter/<rolename>')
def query_filter(rolename):
    out=rolename+':\n<ul>'
    queryed_role = Role.query.filter_by(name=rolename).first()
    for result in User.query.filter_by(role=queryed_role).all():
        out=out+'<li>'+str(result.username)+'</li>\n'
    out=out+'</ul>\n'
    return out
#显示所有文章
@app.route('/posts')
def posts():
    posts = Post.query.all()
    print Post.query.count()
    text=''
    for post in posts:
        print str(post)
        text=text+'<p>'+str(post.id)+'---'+str(post.body)+'</p>'
    return text
#分页显示文章
@app.route('/paginate')
def paginate():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page=page, per_page=3,error_out=False
    )
    posts = pagination.items
    print '查询返回的总数:'+str(pagination.total)
    print posts
    for post in posts:
        print post.body
    return render_template('pagination.html', pagination=pagination, posts=posts, endpoint='.paginate')
    #return '1'

if __name__ == '__main__':
    app.debug=True
    app.run()
