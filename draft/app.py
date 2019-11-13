from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify
                   )
from werkzeug import secure_filename
app = Flask(__name__)

import sys,os,random
import databaseAccess
loggedIn = False
# realistically, this will probably need to come from the database somehow
# it depends on if we want our site to remember our users

app.secret_key = 'your secret here'
# replace that with a random key
app.secret_key = ''.join([ random.choice(('ABCDEFGHIJKLMNOPQRSTUVXYZ' +
                                          'abcdefghijklmnopqrstuvxyz' +
                                          '0123456789'))
                           for i in range(20) ])

# This gets us better error messages for certain common request errors
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

@app.route('/')
def index():
    global loggedIn
    return render_template('main.html', title="Fueling Change",
                                        isLoggedIn=loggedIn)


@app.route('/search/', methods = ['POST'])
def search():
    conn = databaseAccess.getConn('wmdb')

    return redirect(url_for('achievement',title=request.form.get('searchterm')))


@app.route('/achievements/', defaults={'title': ""})
@app.route('/achievements/<title>', methods = ['POST'])
def achievement(title):
    a = []
    if(title==""):
        a = databaseAccess.getAllAchievements(conn)
    else:
        a = databaseAccess.getAchievements(conn,title)

    return render_template('achievementSearch.html',title=title, achievements=a)


if __name__ == '__main__':

    if len(sys.argv) > 1:
        # arg, if any, is the desired port number
        port = int(sys.argv[1])
        assert(port>1024)
    else:
        port = os.getuid()
    app.debug = True
    app.run('0.0.0.0',port)
