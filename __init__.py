# from flask import Flask, render_template, request, url_for, redirect, flash, session
# from werkzeug.contrib.fixers import ProxyFix
# #from content_management import Content
# from ready import server
# import os, re
#
# server = server(size=50000)
#
# app = Flask(__name__)
# app.secret_key = os.urandom(24)
#
# def local_explore_work():
#     # email = explore_emails()
#     email = "phillip.allen@enron.com"
#     print(server.email_stats(email=email))
#
# def local_classify_work():
#     email = classify_emails()
#     return server.classify_emails(email=email)
#
# @app.route('/')
# def homepage():
#     return render_template('main.html')
#
# @app.route('/dashboard/')
# def dashboard():
#     return render_template('dashboard.html')
#
# @app.route('/about_enron/')
# def about_enron():
#     return render_template('aboutEnron.html')
#
#
# @app.route('/explore_emails/')
# def explore_emails():
#     return render_template('exploreEmails.html')
#
# @app.route('/ee/', methods=['POST', 'GET'])
# def ee():
#     error = None
#     try:
#         if request.method == 'POST':
#             email = request.form['email_explore']
#             print(email)
#
#             if email != '':
#                 content = server.get_individual_email(email=email)
#                 print(content)
#                 if not content:
#                     error = 'No email(s) belonging to {} was found'.format(str(email).upper())
#                 else:
#                     error = ''
#                     # session['content'] = content
#                 # return redirect(url_for('explore_emails', email=email))
#                 return render_template('exploreEmails.html', content=content, email=email, error = error)
#             else:
#                 error = "Name is Invalid"
#                 print(error)
#                 return redirect(url_for('dashboard'))
#
#         return render_template('dashboard.html')
#
#     except Exception as e:
#         flash(e)
#         return render_template("dashboard.html", error = error)
#
#
# @app.route('/classify_emails/')
# def classify_emails():
#     return render_template('classifyEmails.html')
#
# @app.route('/ce/', methods=['POST', 'GET'])
# def ce():
#     error = None
#     try:
#         if request.method == 'POST':
#             email = request.form['email_classify']
#             print(email)
#
#             if email != '':
#                 content = server.classify_emails(email=email)
#                 print(content)
#                 if not content:
#                     error = 'No email(s) belonging to {}  was suspected' \
#                             ' to have any relation with the scandal' \
#                             ' after analysis.'.format(str(email).upper())
#                 else:
#                     error = ''
#                 # session['content'] = content
#                 return render_template('classifyEmails.html', content=content, email=email, error = error)
#             else:
#                 error = "Name is Invalid"
#                 print(error)
#                 return redirect(url_for('dashboard'))
#
#         return render_template('dashboard.html')
#
#     except Exception as e:
#         flash(e)
#         return render_template("dashboard.html", error = error)
#
#
# @app.route('/statistic_emails/')
# def statistic_emails():
#     return render_template('stats.html')
#
# @app.route('/ss/', methods=['POST', 'GET'])
# def ss():
#     error = None
#     try:
#         if request.method == 'POST':
#             email = request.form['email_classify']
#             print(email)
#
#             if email != '':
#                 content = server.email_stats(email=email)
#                 print(content)
#                 if not content:
#                     error = 'This address did not send any email' \
#                             ' to any other address'
#                 else:
#                     error = ''
#                 # session['content'] = content
#                 return render_template('stats.html', content=content, email=email, error = error)
#             else:
#                 error = "Name is Invalid"
#                 print(error)
#                 return redirect(url_for('dashboard'))
#
#         return render_template('dashboard.html')
#
#     except Exception as e:
#         flash(e)
#         return render_template("dashboard.html", error = error)
#
#
#
# @app.route('/general_overview/')
# def general_overview():
#     return render_template('generalOverview.html')
#
# @app.route('/ge/', methods=['POST', 'GET'])
# def ge():
#     error = None
#     try:
#         if request.method == 'GET' or request.method == 'POST':
#             _ , emails =  server.get_affiliate_details()
#             # stringed_emails = ','.join(emails)
#             # session['emails'] = emails
#             # print(type(stringed_emails))
#             return render_template('generalOverview.html', emails=emails)
#
#         return render_template('dashboard.html')
#
#     except Exception as e:
#         flash(e)
#         return render_template("dashboard.html", error = error)
#
# # app.wsgi_app = ProxyFix(app.wsgi_app)
#
# if __name__ == "__main__":
#     # from gevent.wsgi import WSGIServer
#     # app.debug = True
#     # http_server = WSGIServer(('', 5000), app)
#     # http_server.serve_forever()
#     app.run(threaded=True)
#
