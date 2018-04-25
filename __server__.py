import json
from random import randint
import sys, requests, ast
import gmplot
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from full_countries import countries

from flask import Flask, render_template, request, url_for, flash, redirect, session, abort
from flask.ext.login import LoginManager, UserMixin, login_required, login_user, logout_user

# link to dbs path
sys.path.append('dbconns')

# database connections
from mariadb_setup import maria
from mongodb_setup import database
from postgresdb_setup import pgdb
from pymysqldb_setup import mysql
from sqlitedb_setup import sqldb
from pymssqldb_setup import pms2ql
from firebase_setup import firebee
from gisdb_setup import gisdb

# config
app = Flask(__name__)
app.config['GOOGLEMAPS_KEY'] = " AIzaSyAmWVYvtUGO73UWOqUq4hnANEHn9zJEvQI "
# initialize google maps
GoogleMaps(app)
app.jinja_env.filters['zip'] = zip
app.secret_key = str(randint(1000, 10000))
# app.permanent_session_lifetime = timedelta(seconds=1)

# mongodb for system users sign ups and authentication
db = database(db='wsa', collection='users')

# bdr_db = database(db='bdr', collection='members')
# firebase database creation
bdr_db = firebee()

# mysql database creation
gps_db = mysql()

# sqlite database creation
dvla_db = sqldb(db='dvla')

# mariadb database creation
nhis_db = maria()

# postgres database creation
nia_db = pgdb()

# mssql database creation
gec_db = pms2ql()

# gis database creation
gis_db = gisdb()

# user authentication config
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# User authentication class with UserMixin
class User(UserMixin):

    def __init__(self, email):
        self.id = email

    def __repr__(self):
        return "%s" % (self.id)


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
        # try the state of remember me and manually set it to off when empty
        try:
            remember = str(request.form["remember"])
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
        return render_template('hp.html')


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
    message = "Invalid Username or password,\nPlease check credentials and log in again or \nSign up first if you haven't"
    flash(message)
    return redirect(url_for('home'))


@login_manager.user_loader
def load_user(userid):
    return User(userid)


@app.route('/')
def home():
    # session.permanent = True
    return render_template('hp.html')


@app.route('/email_validate/', methods=['POST', 'GET'])
def email_validate():
    email = request.args['email']
    message = database.validate_email(db, email=email)
    return json.dumps({"results": message})


@app.route('/settings/', methods=['GET', 'POST'])
@login_required
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
''' Routing for the six database connections are basically the same'''
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
            success = bdr_db.db_member_registration(firstname=firstname, middlename=middlename,
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
        items = [] # fetch the info of users into a dict and push into list
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
            success = dvla_db.db_member_registration(firstname=firstname, middlename=middlename,
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
            success = gec_db.db_member_registration(firstname=firstname, middlename=middlename,
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
            success = gps_db.db_member_registration(firstname=firstname, middlename=middlename,
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
            success = nhis_db.db_member_registration(firstname=firstname, middlename=middlename,
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


@app.route('/crawl_results_disp/', methods=['GET'])
@login_required
def crawl_results_disp():
    return render_template('crawl_results.html')

@app.route('/crawl_return/', methods=['GET', 'POST'])
@login_required
def crawl_return():

    if request.method == 'GET':
        render_template('crawley.html')
    elif request.method == 'POST':
        full_url = request.form['url']
        json_url = {'url':str(full_url)}
        url = 'http://localhost:8100/api/url'
        try:
            # response is a json dump of all the crawled urls
            response = requests.post(url=url, data=json.dumps(json_url))
            # extract the value portion (of type list) from the unicode response,
            # convert the unicode to type string and re-convert to type dict, and
            # take only a single list to avoid duplicates
            response = (ast.literal_eval(str(response.text))).values()[0]
            # get unique urls to avoid duplicates
            info_list = set()
            for res in response:
                info_list.add(res.split('/')[2])
            info_list = list(info_list)


            # Fetch the url information of the urls
            url_info_api = 'http://localhost:8100/api/get_url_info'
            url_lists = {'url_list': info_list}
            url_info_api_response  = requests.post(url=url_info_api, data=json.dumps(url_lists))
            url_info_api_response = (ast.literal_eval(str(url_info_api_response.text))).values()[0]
            # print('URL INFORMATION')
            # print(url_info_api_response)

            # insert the data into the gisdb
            result, error = gis_db.insertDictData(url_info_api_response)
            if result:
                flash('Url information has been saved to database successfully!')
                print('Url information has been saved to database successfully!')
            else:
                flash('Problems encountered saving information to database.'
                          ' Please refresh page to try again!'+' ('+str(error)+')')
                print('Problems encountered saving information to database!.'
                              ' Please refresh page to try again')

            # get a string list of the longitude and latitude sep by a comma
            long_lat_list = []
            for dict_item in url_info_api_response:
                long_lat_list.append(dict_item.get("loc"))

            # segregate into only longitudes and latitudes
            longitudes = []
            latitudes = []

            for val in long_lat_list:
                longitudes.append(float(val.split(',')[0]))
                latitudes.append(float(val.split(',')[1]))

            # plot with google maps beginning with a random destination (I chose UG location :)
            mymap = Map(
                identifier="view-side",
                lat = float(long_lat_list[0].split(',')[1]),
                lng = float(long_lat_list[0].split(',')[0]),
                zoom = 1,
                markers = [(longitude, latitude) for longitude, latitude in zip(longitudes, latitudes)],
                fit_markers_to_bounds=True
            )

            return render_template('crawl_results.html', code=303, response = response, inf_url = info_list,
                                  url_info_response = url_info_api_response,  f_u = str(full_url),
                                   mymap = mymap)
        except Exception as e:
            print(str(e))
            return render_template('internal_server_error.html')
    return render_template('crawley.html')


# @app.route('/crawl_return/', methods=['GET', 'POST'])
# def crawl_return():
#     if request.method == 'GET':
#         render_template('crawley.html')
#
#     elif request.method == 'POST':
#         # The following four lines send a command to start the crawler
#         full_url = request.form['url']
#         json_url = {'url': str(full_url)}
#         post_url = 'http://localhost:8100/api/start_crawler'
#         post_url_response = requests.post(url=post_url, data=json.dumps(json_url))
#
#         # These lines also sends a get_request to get the fetched data available
#         get_data_url = 'http://localhost:8100/api/fetch_data'
#         get_data_url_response = requests.get(get_data_url)
#         get_data_url_response = (ast.literal_eval(str(get_data_url_response.text))).values()[0]
#         print(get_data_url_response)
#         return render_template('crawl_results.html', code=303, response = get_data_url_response, f_u = str(full_url))
#     return render_template('crawley.html')


if __name__ == '__main__':
    app.run()
