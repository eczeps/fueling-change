from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify
                   )
from werkzeug import secure_filename
app = Flask(__name__)

import sys,os,random
import databaseAccess

cur = databaseAccess.currDB
loggedIn = 1
# realistically, this will be a real user's ID
# for now we will just set it to 1 (run makeAchievements for this to work)
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


@app.route('/achievements/', defaults={'searchFor': ""})
@app.route('/achievements/<searchFor>', methods = ['POST', 'GET'])
def achievement(searchFor):
    conn = databaseAccess.getConn(cur)

    if request.method == 'POST':
        a = []
        if(searchFor==""):
            a = databaseAccess.getAllAchievements(conn)
        else:
            a = databaseAccess.getAchievements(conn,searchFor)
    
    if request.method == 'GET':
        searchFor = ''
        a = databaseAccess.getAllAchievements(conn)

    return render_template('achievementSearch.html',title=searchFor,
                                                    achievements=a,
                                                    isLoggedIn=loggedIn,
                                                    DB=cur)


if __name__ == '__main__':

    if len(sys.argv) > 1:
        # arg, if any, is the desired port number
        port = int(sys.argv[1])
        assert(port>1024)
    else:
        port = os.getuid()
    app.debug = True
    app.run('0.0.0.0',port)
