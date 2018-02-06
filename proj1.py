from flask import Flask, render_template, request, url_for, redirect
import werkzeug
import database_setup

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('header.html')

@app.route('/login/')
def login():
    return render_template('login.html')

@app.route('/signup/')
def signup():
    return render_template('signup.html')


if __name__ == '__main__':
    app.run()
