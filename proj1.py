from flask import Flask, render_template, request, url_for, redirect
import werkzeug
from database_setup import database

app = Flask(__name__)
db = database(database='wsa', user_collection='users')

@app.route('/')
def hello_world():
    return render_template('header.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/signup/', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            error = 'Passwords do not match'
            print(error)
        else:
            error = ''
            user_id = db.register_user(firstname=first_name, lastname=last_name, email=email, password=password)


    return render_template('header.html')


if __name__ == '__main__':
    app.run()
