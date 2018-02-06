from flask import Flask, render_template, request, url_for, flash, redirect
import werkzeug
from database_setup import database

app = Flask(__name__)
app.secret_key = 'some_secret'
db = database(database='wsa', user_collection='users')

@app.route('/')
def home_1():
    return render_template('header.html')

@app.route('/home/')
def home():
    return render_template('header.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    return render_template('header.html')

@app.route('/signup/', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            message = 'Registration failed. Passwords do not match'
            print(message)
            flash('Registration failed. Passwords do not match')
            return redirect(url_for('home'))
        else:
            user_id, success = db.register_user(firstname=first_name, lastname=last_name, email=email, password=password)
            if success == True:
                message = 'Registration successful'
                print('Registration successful')
                flash('Registration successful')
            else:
                message = 'Registration failed'
                flash('Registration failed')
                print('Registration failed!')

            return redirect(url_for('home'))

        # return render_template('header.html', signup_message = message)


if __name__ == '__main__':
    app.run()
