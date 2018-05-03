import area_plots
from flask import request
from flask import redirect
from flask import url_for
from flask import Flask
from flask import session

app = Flask(__name__)

login_template = "<form action=\"/login\" method=\"POST\">" \
                 "Username: <input type=\"text\" " \
                 "name=\"username\" ><br>PW: <input type=\"password\" name=\"password\"><br>" \
                 "<input type=\"submit\" value=\"Submit\"></form>"

landing_template = "<form action=\"/plot\" method=\"POST\">" \
                 "Enter a movie title: <input type=\"text\" " \
                 "name=\"movie\" ><br>" \
                 "<input type=\"submit\" value=\"Submit\"></form>"


@app.route('/')
def hello_world():
    return login_template


@app.route('/plot', methods=['POST', 'GET'])
def make_plot():
    ploots = area_plots.AreaPlot()
    ploots.connect_RS_source(session['username'], session['passw'])
    movie = request.form['movie']
    ploots.title = movie

    return ploots.get_data(movie)


@app.route('/landing', methods=['POST', 'GET'])
def movie_select():

    return landing_template


@app.route('/login', methods=['POST', 'GET'])
def login():
    session['username'] = request.form['username']
    session['passw'] = request.form['password']
    return redirect(url_for('movie_select'))


if __name__ == '__main__':
    app.secret_key = 'sooper secret'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run()
