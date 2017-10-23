from flask import Flask, request, render_template, flash, redirect, url_for, session, logging
from flaskext.mysql import MySQL
from wtforms import Form, StringField ,TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
import pymysql.cursors
from functools import wraps


app =Flask(__name__)

#MYSQL THINGY
db=pymysql.connect(host="",user="admin",passwd="adminadmin",db="testdb",port=3306,local_infile=True,charset='utf8',cursorclass=pymysql.cursors.DictCursor)


	
@app.route('/')
def index():
	return render_template('home.html')






class RegisterForm(Form):
	email = StringField('Email',[validators.Length(min=9,max=50),validators.DataRequired()])
	password = PasswordField('Password',[
		validators.Length(min=1,max=16),
		validators.DataRequired(),
		validators.EqualTo('confirm', message='Does not match')
		])
	confirm = PasswordField('Confirm Password')



@app.route('/register', methods=['GET','POST'])
def register():
	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		email = form.email.data
		password = sha256_crypt.encrypt(str(form.password.data))
		cursor=db.cursor()
		cursor.execute("INSERT IGNORE  INTO user(email, password) VALUES(%s ,%s)", (email, password))
		flash('Success','success')
		db.commit()
		cursor.close()
		redirect(url_for('index'))
	return render_template('register.html', form=form)







@app.route('/login', methods=['GET','POST'])
def login():
	if request.method == 'POST':
		email = request.form['email']
		password_raw = request.form['password']

		#dbshizz
		cursor = db.cursor()
		result = cursor.execute("SELECT * FROM user WHERE email = %s",[email])
		if (result > 0):
			data = cursor.fetchone()
			password = data['password']

			if sha256_crypt.verify(password_raw, password):
				app.logger.info('Login Success')
				session['logged_in'] = True
				session['email'] = email

				flash('Welcome inSecure App','success')
				return redirect(url_for('upload'))
			else:
				error = 'Invalid Login'
				return render_template('login.html', error=error)
				app.logger.info("Login Fail")
		else:
			error = 'Invalid Login'
			return render_template('login.html', error=error)
			app.logger.info("Login Fail")
	
	return render_template('login.html')


#checking for session
def is_logged_in(f):
	@wraps(f)
	def wrap(*args ,**kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('Access Disabled inSecure App', 'danger')
			return redirect(url_for('login'))
	return wrap

@app.route('/logout')
@is_logged_in
def logout():
	session.clear()
	flash('Logged Out', 'success')
	return redirect(url_for('login'))










@app.route('/upload',methods=['GET', 'POST'])
@is_logged_in
def upload():


    
	return render_template('upload.html') 






























if __name__ == '__main__':
	app.secret_key='anchal'
	app.run(debug=True)