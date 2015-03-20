from flask import Flask, flash, request, jsonify, url_for, render_template, redirect

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bootstrap import Bootstrap
from functools import wraps
from datetime import datetime
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.login import LoginManager

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Email,Length
from flask import make_response
from functools import update_wrapper
from datetime import datetime 


app = Flask (__name__, static_url_path='/home/wa/Documents/test3/static')

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:aaggss@localhost/dreadger'
app.secret_key = 'my secret key is this'


logInStatus =dict()
logInStatus['logged_in'] = False

def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response
    return update_wrapper(no_cache, view) 

class LoginForm(Form):
    email = StringField('Username', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    
    submit = SubmitField('Log In')


class dieselLevel(db.Model):
	__tablename__ = 'dieselLevel'
	id = db.Column(db.Integer, primary_key=True)
	device = db.Column(db.String(25))
	level = db.Column(db.Integer)
	mTime = db.Column(db.DateTime)
	ip = db.Column(db.String(15))

class user(db.Model):
    __tablename__ = 'userTable'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40),unique=True)
    password = db.Column(db.String(40))
    email = db.Column(db.String(50))
    registered_on = db.Column(db.DateTime)

    def __init__(self,id,username,password,email,registered_on):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.registered_on = datetime.utcnow()
        


def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if logInStatus['logged_in']:
			return f(*args, **kwargs)
		else:
			flash('You need to login first')
			return redirect(url_for('login'))
	return decorated_function

@app.route('/', methods=['GET', 'POST'])
def login():
	name = None
	form = LoginForm()
	if form.validate_on_submit():
		logInStatus['logged_in'] = True
                if form.email.data != 'admin' or form.password.data != 'admin':
		    form.email.data = ' '
		    flash('The username or password you entered is incorrect.')
                    return render_template('login.html',form=form)
		return redirect(url_for('home'))
                
		#name = form.name.data
		#form.name.data = ''
	return render_template('login.html', form=form)

"""@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials.'
        else:
            session['logged_in'] = True
            flash('You have logged in')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)"""


"""@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user_auth = user.query.filter(user.username==request.form['username']).all() 
        if user_auth[0].password == request.form['password']:
	#if True:
            session['logged_in'] = True
            flash('You have logged in')
            return redirect(url_for('home'))
        else:
            error = 'Invalid Credentials'
        return render_template('Login.html',error=error)
    if session.get('logged_in'):
        return redirect(url_for('home'))
    return render_template('Login.html',error=error)
"""
@app.route('/user', methods=['GET', 'POST'])
def test():
    return render_template('user.html')


@app.route ("/index", methods=['GET'])
@nocache
@login_required
def home():
	results = dieselLevel.query.order_by(dieselLevel.mTime.desc()).all()
	return render_template('Home.html',results=results)	
	#return render_template('Home.html',results=results)	

	
@app.route('/logout')
def logout():
    logInStatus['logged_in']=False
    flash('You were just logged out')
    return redirect(url_for('login'))

def validate(data):
	try:
		datetime.strptime(data, '%d/%m/%Y %H:%M') 
		return 1 
	except:
		return None

def conTime(param):
	return datetime.strptime(param, '%d/%m/%Y %H:%M')


@app.route('/logs', methods=['GET', 'POST'])
@login_required
def logs():
    if request.method == 'POST':
        result = []
        if (validate(request.form['param1'])):
            if (validate(request.form['param2'])):
		#print '1'
                results = dieselLevel.query.filter(conTime(request.form['param1']) < dieselLevel.mTime).filter(dieselLevel.mTime < conTime(request.form['param2'])).order_by(dieselLevel.mTime.desc()).all()
            else:
		#print '2'
                results = dieselLevel.query.filter(conTime(request.form['param1']) < dieselLevel.mTime).order_by(dieselLevel.mTime.desc()).all()
        else:
            if (validate(request.form['param2'])):
		#print '3'                
		results = dieselLevel.query.filter(dieselLevel.mTime < conTime(request.form['param2'])).order_by(dieselLevel.mTime.desc()).all()
            else:
                return render_template('log.html')
        json_results = []
	for result in results:
		d = { 'device' : result.device,
			'level': result.level,
			'datetime' : result.mTime, 
			'ip' : result.ip}
		json_results.append(d)
	return jsonify(items=json_results)    
    return render_template('log.html')


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500

"""@app.errorhandler(404)
def page_not_found(error):
	return 'This page does not exist',404"""

if __name__ == "__main__":
	app.run(debug=True)

