from dreamtools.logmng import CTracker
from flask import Flask, render_template, request, url_for, flash, redirect

from models.galette import CGalette

app = Flask(__name__)


@app.route('/enter', methods= ['GET'])
def enter():
    user = request.args.get('user')

    if user:
        r = CTracker.fntracker(CGalette.newuser, '', user)

        if r.ok and r.data:
            flash('Choisis une part')
            return render_template('tirage.html', user=user, galette=r.data)
        else:
            flash('Désolée trois part maximum')
            return redirect(url_for('index', user='done'))
    else:
        return redirect(url_for('index'))

@app.route('/tirage/<user>', methods= ['GET'])
def tirage(user):
    part = request.args.get('part')

    r = CTracker.fntracker(CGalette.newtirage, '', user, part)

    if r.ok and r.data:
        flash('Merci d\'avoir participé')
        return redirect(url_for('index', user='done'))
    else:
        flash('Aie')
        r = CTracker.fntracker(CGalette.newuser, '', user)

        if r.ok and r.data:
            flash('Choisis une part')
            return render_template('tirage.html', user=user, galette=r.data)

        return redirect(url_for('index', user='done'))


@app.route('/', methods= ['GET'])
@app.route('/<user>', methods= ['GET'])
def index(user=None):

    return render_template('index.html', user=user, gagnant=CGalette.lesfeves())

