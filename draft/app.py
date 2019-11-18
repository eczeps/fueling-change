from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify
                   )
from werkzeug import secure_filename
app = Flask(__name__)

import sys,os,random
import databaseAccess

cur = databaseAccess.currDB
didSearch = False #used to tell apart (3) and (4) in profile.html
loggedIn = 1
# realistically, this will be an actual user's ID
# for now we will just set it to 1
# run makeAchieves and then webpageTest for this to work
# or make None to see the unlogged in pages
# also this should be retrieved from a session variable as well

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


# haven't actually implimented searching yet
@app.route('/achievements/', methods = ['POST', 'GET'], defaults={'searchFor': ""})
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


@app.route('/profile/', methods=['POST', 'GET'], defaults={'user': ""})
# Need to redirect it for the above but not going to do it yet
# redirect to /profile/searchedfirstname-searchedlastname-searchedUID
@app.route('/profile/<user>/', methods=['POST', 'GET'])
def profile(user):
    global loggedIn
    global didSearch
    
    #grab the user id
    UID = user.split('-')[2] #format first-lastname-UID

    #get information
    conn = databaseAccess.getConn(cur)
    userInfo = databaseAccess.getUser(conn, UID)

    #variables for formatting template
    titleString = userInfo['first_Name'].lower() + ' ' + userInfo['last_Name'].lower()
    currUser = (int(UID) == loggedIn) #boolean

    #get achievements
    allComps = databaseAccess.getCompAchievements(conn, UID)
    allStars = databaseAccess.getStarAchievements(conn, UID)

    
    return render_template('profile.html',  title=titleString,
                                                isLoggedIn=loggedIn,
                                                userURL=user,
                                                isUser=currUser,
                                                searched=didSearch,
                                                compAchis=allComps,
                                                starAchis=allStars)


# user searching not implimented yet
@app.route('/useraction/', methods=['POST', 'GET'], defaults={'user': ""})
@app.route('/useraction/<user>/', methods=['POST', 'GET'])
def useract(user):
    global loggedIn
    global didSearch
    
    #grab the user id
    UID = user.split('-')[2] #format first-lastname-UID

    #get information
    conn = databaseAccess.getConn(cur)
    userInfo = databaseAccess.getUser(conn, UID)

    #variables for formatting template
    titleString = userInfo['first_Name'].lower() + ' ' + userInfo['last_Name'].lower()
    currUser = (int(UID) == loggedIn) #boolean

    return render_template('useraction.html', isLoggedIn=loggedIn,
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
