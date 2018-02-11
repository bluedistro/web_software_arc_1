# TODO: PREVENT URL NAVIGATION OR BACK ARROW TO DASHBOARD PAGE FROM WORKING AFTER LOGOUT
# TODO: SEARCH FOR THE RIGHT WAY TO ACTUALLY REDIRECT TO THE HOMEPAGE OF A WEB APP
# TODO: GET THE USERNAME OF THE USER LOGGED IN

from flask import Flask, render_template, request, url_for, flash, redirect, session, abort, Response
from flask.ext.login import LoginManager, UserMixin, login_required, login_user, logout_user
from database_setup import database
import json

# config
app = Flask(__name__)
app.secret_key = 'some_secret_xxx'
db = database(db='wsa', user_collection='users')

bdr_db = database(db='bdr', user_collection='members')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin):

    def __init__(self, email):
        self.id = email

    def __repr__(self):
        return "%s%s" % (self.id)


# dashboard url
@app.route('/dashboard/')
@login_required
def dashboard():
    return render_template('dashboard.html')


# dummy login page
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # try thr state of remember me and manually set it to off when empty
        try:
            remember = request.form["remember"]
            remember = str(remember)
        except Exception as e:
            print(str(e))
            remember = 'off'
        if remember == 'on':
            remember_state = True
        else:
            remember_state = False
        status, firstname, lastname = db.login_user(email=username, password=password)
        next = request.args.get('dashboard')
        if status:
            # set user to User class and login user
            user = User(username)
            login_user(user, remember_state)
            # obtaining data of current session
            session['username'] = username
            session['firstname'] = firstname
            session['lastname'] = lastname
            return redirect(next or url_for('dashboard'))
        else:
            return abort(401)
    else:
        return render_template('header.html')


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/not_found/', methods=['GET', 'POST'])
def not_found():
    return render_template('not_found.html')


@app.errorhandler(404)
def non_existent_page(e):
    return redirect(url_for('not_found'))


@app.errorhandler(401)
def page_not_found(e):
    message = "Invalid Username or password,\nPlease check credentials and login again or \nSign up first if you haven't"
    flash(message)
    return redirect(url_for('home'))


@login_manager.user_loader
def load_user(userid):
    return User(userid)


@app.route('/')
def home_1():
    return render_template('header.html')


@app.route('/home/')
def home():
    return render_template('header.html')


@app.route('/email_validate/', methods=['POST', 'GET'])
def email_validate():
    email = request.args['email']
    message = database.validate_email(db, email=email)
    return json.dumps({"results": message})

@app.route('/panels_wells/', methods=['POST', 'GET'])
def panels_wells():
    return render_template('panels-wells.html')

@app.route('/notifications/', methods=['POST', 'GET'])
def notifications():
    return render_template('notifications.html')

@app.route('/blank/', methods=['POST', 'GET'])
def blank():
    return render_template('blank.html')

@app.route('/bdr/', methods=['POST', 'GET'])
def bdr():
    if request.method == 'POST':
        firstname = request.form['db_firstname']
        try:
            middlename = request.form['db_middlename']
        except Exception as e:
            print(str(e))
            middlename = ''
        lastname = request.form['db_lastname']
        dob = request.form['date']
        birthplace = request.form['db_birthplace']

        if firstname and lastname and dob and birthplace is not None:
            user_id, success = bdr_db.db_member_registration(firstname=firstname, middlename=middlename,
                                                             lastname=lastname, dob=dob,
                                                             birthplace=birthplace)
            flash('User has been registered successfully!')
            return render_template('bdr.html')
        else:
            message = 'Registration failed'
            flash(message)
            print(message)
            return render_template('bdr.html')

    elif request.method == 'GET':
        firstnames, middlenames, lastnames, dobs, birthplaces = bdr_db.fetch_db_members()
        items = []
        for fn, mn, ln, dob, bp in zip(firstnames, middlenames, lastnames, dobs, birthplaces):
            an_item = dict(firstname=fn, middlename=mn, lastname=ln, dob=dob, birthplace=bp)
            items.append(an_item)

        return render_template('bdr.html', items=items)

    return render_template('bdr.html')

@app.route('/dvla/', methods=['POST', 'GET'])
def dvla():
    return render_template('dvla.html')

@app.route('/gec/', methods=['POST', 'GET'])
def gec():
    return render_template('gec.html')

@app.route('/gps/', methods=['POST', 'GET'])
def gps():
    return render_template('gps.html')

@app.route('/nhis/', methods=['POST', 'GET'])
def nhis():
    return render_template('nhis.html')

@app.route('/nia/', methods=['POST', 'GET'])
def nia():
    return render_template('nia.html')


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
            user, success = db.register_user(firstname=first_name, lastname=last_name, email=email,
                                             password=password)
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
