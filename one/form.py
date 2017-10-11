from flask import Flask,render_template,session,redirect,url_for,flash
from flask_wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import Required
from flask_bootstrap import Bootstrap

app=Flask(__name__)
app.config['SECRET_KEY']='password!!!'
bootstrap=Bootstrap(app)


@app.route('/',methods=['GET','POST'])
def index():
    form=NameForm()
    if form.validate_on_submit():
	    session['name']=form.name.data
	    return redirect(url_for('index'))
    return render_template('form.html',form=form,name=session.get('name'))

@app.route('/flash',methods=['GET','POST'])
def flash_msg():
    form=NameForm()
    if form.validate_on_submit():
	    old_name=session.get('name')
	    if old_name is not None and old_name!=form.name.data:
	        flash('you have changed the name!')
	    session['name']=form.name.data
	    return redirect(url_for('flash_msg'))
    return render_template('form.html',form=form,name=session.get('name'))

#@app.route('/',methods=['GET','POST'])
#def index():
#    name=None
#    form=NameForm()
#    if form.validate_on_submit():
#	    name=form.name.data
#	    form.name.data=''
#    print name
#    return render_template('form.html',form=form,name=name)

class NameForm(Form):
    name = StringField('your message:',validators=[Required()])
    to = StringField('recipients:',validators=[Required()])
    submit = SubmitField('Submit')
	
	
if __name__ == '__main__':
    app.run(debug=True)