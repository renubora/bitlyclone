from flask import Flask, url_for,request,redirect,render_template,session
from os import environ
import datetime,sqlite3
from model import *
import sys
from config import *


app = Flask(__name__)



#app.APPLICATION_ROOT = '/~rohans/server/'


def initialize():
	init_db()

# DATABASE SETUP CODE
               			
def initsession(email):
	session['logged_in'] = True
	session['user'] = email
	

def closesession():
	session.pop('logged_in',None)
	session.pop('user',None)

	# close the database session too
	db_session.remove()

def checkforuser(email,pwd = None, login = False,register = False):
	
	if login:
		result = db_session.query(User).filter_by(email = email,password = pwd)
		if result.count() == 1:
			initsession(email)
			return {'error':False}		
		else:
			msg = 'invalid username or password'
			return {'error':True,'msg':msg}


	if register:
		result = db_session.query(User).filter_by(email = email)
		if result.count() > 0:
			msg = 'this user name already exists'
			
			return {'error':True,'msg':msg}

		else:
			#print email+pwd
			u = User(email,pwd)
			db_session.add(u)
			db_session.commit()
			initsession(email)

			return {'error':False}

# register functions

@app.route('/register', methods = ['GET'])
def register():
	return render_template('register.html')

@app.route('/registerverify', methods = ['POST'])
def registerverify():
	email = request.form['email']
	pwd = request.form['password']

	result = checkforuser(email,pwd,False,True)
	if result['error']:
		return render_template('register.html', message = result)
	else:
		return render_template('homepage.html')
		
		
							
		
#login functions		

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/verify', methods = ['POST'])
def verify():
	email = request.form['email']
	pwd = request.form['password']
	result = checkforuser(email,pwd,True,False)

	if result['error']:
		return render_template('login.html',message = result)
	else:
		print result
		return redirect(url_for('homepage'))

		
# logout functions
@app.route('/logout')
def logout():
	closesession()
	return render_template('homepage.html')	


# homepages
@app.route('/')
def default_url():
	return render_template('homepage.html')

@app.route('/home')
def homepage():
	return render_template('homepage.html')

# create association function

@app.route('/create')
def create():
	return render_template('create.html')

@app.route('/createshort', methods = ['POST'])
def createshort():
	rootdomain = 'bit.ly/'
	shorturl = rootdomain+request.form['shorturl']
	longurl = request.form['longurl']
	

	userrecs = db_session.query(User).filter_by(email = session['user']).all()
	shortrec = Short(shorturl,longurl)
	userrecs[0].children.append(shortrec)
	db_session.commit()
	
	return redirect(url_for('assoc'))
	#return redirect('http://people.ischool.berkeley.edu/~rohans/server/assoc')

#show association
@app.route('/assoc', methods = ['GET','POST'])
def assoc():
	if session.has_key('user'):
		userrec = db_session.query(User).filter_by(email = session['user']).all()
		shortrecs = userrec[0].children

		shorts = {}

		for i in range(len(shortrecs)):
			shorts[shortrecs[i].shorturl] = {'longurl' : shortrecs[i].longurl, 'created': shortrecs[i].created}

		# { short url , {longurl,created }


		return render_template('seeshorts.html', shorts = shorts)
	else:
		return render_template('seeshorts.html')	
	

#search association
@app.route('/searchrequest', methods = ['POST'])
def searchrequest():
	shorturl = request.form['shorturl']
	
	userrec = db_session.query(User).filter_by(email = session['user']).all()
	shortrecs = userrec[0].children
	
	for i in range(len(shortrecs)):
			if shorturl == shortrecs[i].shorturl:
				return redirect(shortrecs[i].longurl)

	


@app.route('/short/<name>', methods = ['GET'])
def searchreq(name):
	shorturl = name
	
	userrec = db_session.query(User).filter_by(email = session['user']).all()
	shortrecs = userrec[0].children
	
	for i in range(len(shortrecs)):
			if shorturl == shortrecs[i].shorturl:
				return redirect(shortrecs[i].longurl)



@app.route('/search', methods = ['GET'])
def search():
	return render_template('searchshorts.html')
			

@app.route('/nf')
def nf():
	return render_template('notfound.html')


def configureserver():
	app.debug = True
	app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
	#app.config['SERVER_NAME'] = '/~rohans/server'



if __name__ == '__main__':
	
	#app.run()
	configureserver()
	app.run()
	
	#app.run(port=int(environ['FLASK_PORT']))


	
 
