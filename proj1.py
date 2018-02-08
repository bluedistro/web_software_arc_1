from flask import Flask, render_template, request, url_for, flash, redirect, session, abort, Response
from flask.ext.login import LoginManager, UserMixin, login_required, login_user, logout_user
import json

from database_setup import database

# config
app = Flask(__name__)
app.secret_key = 'some_secret_xxx'
db = database(database='wsa', user_collection='users')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin):

    def __init__(self, email):
        self.id = email

    def __repr__(self):
        return "%s%s" % (self.id)

# protected url
@app.route('/protected')
@login_required
def protected():
    return render_template('protecteed_test.html')

@app.route('/login_try/')
def login_try():
    return render_template('login.html')

# dummy login page
@app.route('/login/', methods=['GET', 'POST'])
def login_alt():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        status = db.login_user(email=username, password=password)
        next = request.args.get('protected')
        if status:
            user = User(username)
            login_user(user)
            return redirect(next or url_for('protected'))
        else:
            return abort(401)
    else:
        return render_template('login.html')

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return render_template('login.html')


@app.errorhandler(401)
def page_not_found(e):
    # return Response('<p>Login Failed</p>')
    return render_template('login.html')


@login_manager.user_loader
def load_user(userid):
    return User(userid)

@app.route('/')
def home_1():
    return render_template('header.html')

@app.route('/home/')
def home():
    return render_template('header.html')

@app.route('/login_alt/', methods=['GET', 'POST'])
def login():
    return render_template('header.html')

@app.route('/email_validate/', methods=['POST', 'GET'])
def email_validate():
    email = request.args['email']
    message = database.validate_email(db, email=email)
    return json.dumps({"results": message})

@app.route('/signup/', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        email = request.form['email']
        password = request.form['pass_confirmation']
        confirm_password = request.form['pass']

        if password != confirm_password:
            message = 'Registration failed. Passwords do not match'
            print(message)
            flash(message)
            return redirect(url_for('home'), code=302)
        else:
            user, success = db.register_user(firstname=first_name, lastname=last_name, email=email, password=password)
            if success:
                message = 'Registration successful'
                print(message)
                flash(message)
            else:
                message = 'Registration failed'
                flash(message)
                print(message)

            return redirect(url_for('home'), code=302)



if __name__ == '__main__':
    app.run()
