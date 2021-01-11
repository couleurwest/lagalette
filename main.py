import os
import sys

from dreamtools import tools

from models.galette import CGalette
from resource import get_resource_path

from dreamtools.logmng import CTracker
from flask import Flask, render_template, request, url_for, flash, redirect

from models.galette import CGalette

if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    tools.makedirs('static')
    web_app = Flask(__name__, template_folder=template_folder)
else:
    web_app = Flask(__name__)

web_app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1
# No caching at all for API endpoints.
@web_app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store'
    return response

@web_app.route('/', methods= ['GET'])
def index():
    return render_template('index.html')


@web_app.route('/lagalette', methods= ['GET'])
@web_app.route('/lagalette/<user>', methods= ['GET'])
def lagalette(user=None):
    lagalette = {}
    user_participation = {}
    new = False

    if user is None:
        user = request.args.get('user')
        if user is  None:
            return redirect(url_for('index'))
        else:
            new = True
            user_participation = CGalette.newuser(user)
    else:
        user_participation = CGalette.state_user(user)

    part = request.args.get('part')
    tirage_ok = False
    if part:
        r = CTracker.fntracker(CGalette.newtirage, '', user, part)
        tirage_ok = r.data
        if r.ok and user_participation.get('count')<3:
            user_participation = CGalette.newuser(user)

    #je recois mes participations.
    if user_participation.get('count')<3 and (new or (part and not tirage_ok)):
        if part:
            flash('Désolé, part déjà mangé par un(e) autre participant(e)')
        return redirect(url_for('tirage', user=user))

    r = CTracker.fntracker(CGalette.participation, 'dashboard')
    lagalette = r.data

    if r.ok:
        return render_template('dashboard.html', user=user, galettes=lagalette, user_participation=user_participation)
    else:
        flash ('Ben ca marche pô !')
        return redirect(url_for('index'))



@web_app.route('/tirage/<user>', methods= ['GET'])
def tirage(user):
    r = CTracker.fntracker(CGalette.newgalette, 'Nouveau tirage')
    return render_template('tirage.html', user=user, galette=r.data[0], liste=[int(x) for x in r.data[1]] )
