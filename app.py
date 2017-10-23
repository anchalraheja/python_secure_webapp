from flask import Flask, request, render_template, flash, redirect, url_for, session, logging
from flaskext.mysql import MySQL
from wtforms import Form, StringField ,TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
import pymysql.cursors

app =Flask(__name__)

#MYSQL THINGY
db=pymysql.connect(host="localhost",user="root",passwd="",db="insecureapp",port=3306,local_infile=True,charset='utf8'
         ,cursorclass=pymysql.cursors.DictCursor)


	
@app.route('/')
def index():
	return render_template('home.html')

@app.route('/login')
def login():
	return render_template('login.html')




class RegisterForm(Form):
	email = StringField('Email',[validators.Length(min=15,max=50),validators.DataRequired()])
	password = PasswordField('Password',[
		validators.Length(min=15,max=50),
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
		cursor.execute("INSERT INTO user(email, password) VALUES(%s ,%s)", (email, password))
		db.commit()
		cursor.close()
		flash('Success','success')
		redirect(url_for('index'))
	return render_template('register.html', form=form)




if __name__ == '__main__':
	app.secret_key='anchal'
	app.run(debug=True)