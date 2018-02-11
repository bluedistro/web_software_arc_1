# TODO: PREVENT URL NAVIGATION OR BACK ARROW TO DASHBOARD PAGE FROM WORKING AFTER LOGOUT

from flask import Flask, render_template, request, url_for, flash, redirect, session, abort, Response
from flask.ext.login import LoginManager, UserMixin, login_required, login_user, logout_user
from database_setup import database
import json
from datetime import timedelta

# config
app = Flask(__name__)
app.secret_key = 'some_secret_xxx'
# app.permanent_session_lifetime = timedelta(seconds=1)
db = database(db='wsa', user_collection='users')

# databases creation
bdr_db = database(db='bdr', user_collection='members')
nhis_db = database(db='nhis', user_collection='members')
dvla_db = database(db='dvla', user_collection='members')
gec_db = database(db='gec', user_collection='members')
nia_db = database(db='nia', user_collection='members')
gps_db = database(db='gps', user_collection='members')

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
        return render_template('homepage.html')


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
    # session.permanent = True
    return render_template('homepage.html')


@app.route('/home/')
def home():
    session.permanent = True
    return render_template('homepage.html')


@app.route('/email_validate/', methods=['POST', 'GET'])
def email_validate():
    email = request.args['email']
    message = database.validate_email(db, email=email)
    return json.dumps({"results": message})

@app.route('/settings/', methods=['GET', 'POST'])
def settings():
    return render_template('settings.html')

# ------------------- Mini Applications Routing ----------------------------
@app.route('/face_swap/', methods=['POST', 'GET'])
@login_required
def face_swap():
    return render_template('face_swap.html')

@app.route('/mag/', methods=['POST', 'GET'])
@login_required
def mag():
    return render_template('mag.html')

@app.route('/crawley/', methods=['POST', 'GET'])
@login_required
def crawley():
    return render_template('crawley.html')

# --------------- DATABASE ACCESS AND INTERACTIONS --------------------------
# Birth and Death Routing
@app.route('/bdr/', methods=['POST', 'GET'])
@login_required
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

# Driver and Vehicle Licensing Authority Routing
@app.route('/dvla/', methods=['POST', 'GET'])
@login_required
def dvla():
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
            user_id, success = dvla_db.db_member_registration(firstname=firstname, middlename=middlename,
                                                             lastname=lastname, dob=dob,
                                                             birthplace=birthplace)
            flash('User has been registered successfully!')
            return render_template('dvla.html')
        else:
            message = 'Registration failed'
            flash(message)
            print(message)
            return render_template('dvla.html')

    elif request.method == 'GET':
        firstnames, middlenames, lastnames, dobs, birthplaces = dvla_db.fetch_db_members()
        items = []
        for fn, mn, ln, dob, bp in zip(firstnames, middlenames, lastnames, dobs, birthplaces):
            an_item = dict(firstname=fn, middlename=mn, lastname=ln, dob=dob, birthplace=bp)
            items.append(an_item)

        return render_template('dvla.html', items=items)

    return render_template('dvla.html')

# Ghana Electoral Commission Routing
@app.route('/gec/', methods=['POST', 'GET'])
@login_required
def gec():
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
            user_id, success = gec_db.db_member_registration(firstname=firstname, middlename=middlename,
                                                             lastname=lastname, dob=dob,
                                                             birthplace=birthplace)
            flash('User has been registered successfully!')
            return render_template('gec.html')
        else:
            message = 'Registration failed'
            flash(message)
            print(message)
            return render_template('gec.html')

    elif request.method == 'GET':
        firstnames, middlenames, lastnames, dobs, birthplaces = gec_db.fetch_db_members()
        items = []
        for fn, mn, ln, dob, bp in zip(firstnames, middlenames, lastnames, dobs, birthplaces):
            an_item = dict(firstname=fn, middlename=mn, lastname=ln, dob=dob, birthplace=bp)
            items.append(an_item)

        return render_template('gec.html', items=items)

    return render_template('gec.html')

# Ghana Passport Service Routing
@app.route('/gps/', methods=['POST', 'GET'])
@login_required
def gps():
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
            user_id, success = gps_db.db_member_registration(firstname=firstname, middlename=middlename,
                                                              lastname=lastname, dob=dob,
                                                              birthplace=birthplace)
            flash('User has been registered successfully!')
            return render_template('gps.html')
        else:
            message = 'Registration failed'
            flash(message)
            print(message)
            return render_template('gps.html')

    elif request.method == 'GET':
        firstnames, middlenames, lastnames, dobs, birthplaces = gps_db.fetch_db_members()
        items = []
        for fn, mn, ln, dob, bp in zip(firstnames, middlenames, lastnames, dobs, birthplaces):
            an_item = dict(firstname=fn, middlename=mn, lastname=ln, dob=dob, birthplace=bp)
            items.append(an_item)

        return render_template('gps.html', items=items)

    return render_template('gps.html')

# National Health Insurance Scheme Routing
@app.route('/nhis/', methods=['POST', 'GET'])
@login_required
def nhis():
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
            user_id, success = nhis_db.db_member_registration(firstname=firstname, middlename=middlename,
                                                             lastname=lastname, dob=dob,
                                                             birthplace=birthplace)
            flash('User has been registered successfully!')
            return render_template('nhis.html')
        else:
            message = 'Registration failed'
            flash(message)
            print(message)
            return render_template('nhis.html')

    elif request.method == 'GET':
        firstnames, middlenames, lastnames, dobs, birthplaces = nhis_db.fetch_db_members()
        items = []
        for fn, mn, ln, dob, bp in zip(firstnames, middlenames, lastnames, dobs, birthplaces):
            an_item = dict(firstname=fn, middlename=mn, lastname=ln, dob=dob, birthplace=bp)
            items.append(an_item)

        return render_template('nhis.html', items=items)

    return render_template('nhis.html')

# National Identification Authority Routing
@app.route('/nia/', methods=['POST', 'GET'])
@login_required
def nia():
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
            user_id, success = nia_db.db_member_registration(firstname=firstname, middlename=middlename,
                                                             lastname=lastname, dob=dob,
                                                             birthplace=birthplace)
            flash('User has been registered successfully!')
            return render_template('nia.html')
        else:
            message = 'Registration failed'
            flash(message)
            print(message)
            return render_template('nia.html')

    elif request.method == 'GET':
        firstnames, middlenames, lastnames, dobs, birthplaces = nia_db.fetch_db_members()
        items = []
        for fn, mn, ln, dob, bp in zip(firstnames, middlenames, lastnames, dobs, birthplaces):
            an_item = dict(firstname=fn, middlename=mn, lastname=ln, dob=dob, birthplace=bp)
            items.append(an_item)

        return render_template('nia.html', items=items)

    return render_template('nia.html')

# ---------------------- END OF DATABASE ACCESS AND ROUTING -------------------------


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
