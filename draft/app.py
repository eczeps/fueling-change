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
    conn = databaseAccess.getConn(cur)
    user = ""

    if loggedIn != None:
        userInfo = databaseAccess.getUser(conn, loggedIn)
        user = userInfo['first_Name'].lower() + '-' + userInfo['last_Name'].lower()
        user += '-' + str(userInfo['UID'])

    return render_template('main.html', title="Fueling Change",
                                        isLoggedIn=loggedIn,
                                        userURL=user)


@app.route('/achievements/', defaults={'searchFor': ""})
@app.route('/achievements/<searchFor>', methods = ['POST', 'GET'])
def achievement(searchFor):
    global loggedIn
    conn = databaseAccess.getConn(cur)
    user = ""

    if loggedIn != None:
        userInfo = databaseAccess.getUser(conn, loggedIn)
        user = userInfo['first_Name'].lower() + '-' + userInfo['last_Name'].lower()
        user += '-' + str(userInfo['UID'])

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
                                                    DB=cur,
                                                    userURL=user)


@app.route('/profile/<user>/', methods=['POST', 'GET'])
def profile(user):
    global loggedIn
    print(user)
    UID = user.split('-')[2] #format first-lastname-UID
    conn = databaseAccess.getConn(cur)
    userInfo = databaseAccess.getUser(conn, UID)


    titleString = userInfo['first_Name'].lower() + ' ' + userInfo['last_Name'].lower()
    currUser = (int(UID) == loggedIn) #boolean
    print(currUser)

    
    return render_template('profile.html',  title=titleString,
                                                isLoggedIn=loggedIn,
                                                userURL=user,
                                                isUser=currUser)



if __name__ == '__main__':

    if len(sys.argv) > 1:
        # arg, if any, is the desired port number
        port = int(sys.argv[1])
        assert(port>1024)
    else:
        port = os.getuid()
    app.debug = True
    app.run('0.0.0.0',port)
