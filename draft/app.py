from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify
                   )
from werkzeug import secure_filename
app = Flask(__name__)

import sys,os,random,math
import databaseAccess

currDB = databaseAccess.d
didSearch = False #used to tell apart (3) and (4) in profile.html
loggedIn = 1
# realistically, this will be an actual user's ID
# for now we will just set it to 1 until we implement sessions & logging in
# run makeAchieves and then webpageTest for this to work
# or make None to see the unlogged in pages

app.secret_key = 'your secret here'
# replace that with a random key
app.secret_key = ''.join([ random.choice(('ABCDEFGHIJKLMNOPQRSTUVXYZ' +
                                          'abcdefghijklmnopqrstuvxyz' +
                                          '0123456789'))
                           for i in range(20) ])

# This gets us better error messages for certain common request errors
app.config['TRAP_BAD_REQUEST_ERRORS'] = True


'''handles the homepage route, and handles both when users are logged in and when they aren't'''
@app.route('/')
def index():
    global loggedIn 
    conn = databaseAccess.getConn(currDB)
    user = ""

    if loggedIn != None:
        userInfo = databaseAccess.getUser(conn, loggedIn)
        user = userInfo['first_Name'].lower() + '-' + userInfo['last_Name'].lower()
        user += '-' + str(userInfo['UID'])

    return render_template('main.html', title="Fueling Change",
                                        isLoggedIn=loggedIn,
                                        userURL=user)


'''handles the page where users can search for achievements and self-report them'''
@app.route('/achievements/', methods = ['POST', 'GET'], defaults={'searchFor': ""})
@app.route('/achievements/<searchFor>', methods = ['POST', 'GET'])
def achievement(searchFor):
    global loggedIn
    conn = databaseAccess.getConn(currDB)
    user = ""
    # rep is short for reportable
    rep = []

    if loggedIn != None:
        userInfo = databaseAccess.getUser(conn, loggedIn)
        user = userInfo['first_Name'].lower() + '-' + userInfo['last_Name'].lower()
        user += '-' + str(userInfo['UID'])
        rep = databaseAccess.getReportedAchieves(conn, loggedIn) 

    #if the user is searching for something, access the database to get search results
    searchFor = request.form.get('searchterm')
    if request.method == 'POST':
        a = []
        if(searchFor==""):
            a = databaseAccess.getAllAchievements(conn)
        else:
            a = databaseAccess.getAchievements(conn,searchFor)

    #if the user is just loading the page, show them all the achievements
    elif request.method == 'GET':
        searchFor = ''
        a = databaseAccess.getAllAchievements(conn)

    return render_template('achievementSearch.html',title=searchFor,
                                                    achievements=a,
                                                    isLoggedIn=loggedIn,
                                                    reps=rep,
                                                    userURL=user)

'''handles the user profile route, which displays user info
user is NOT found using session variables; it's found based on the URL
this will be re-implemented later when we've implemented sessions & sign in flow'''
@app.route('/profile/', methods=['POST', 'GET'], defaults={'user': ""})
# Need to redirect it for the above but not going to do it yet
# redirect to /profile/searchedfirstname-searchedlastname-searchedUID
@app.route('/profile/<user>/', methods=['POST', 'GET'])
def profile(user):
    global loggedIn
    global didSearch
    
    #grab the user id
    UID = user.split('-')[2] #format first-lastname-UID

    #get user information
    conn = databaseAccess.getConn(currDB)
    userInfo = databaseAccess.getUser(conn, UID)

    #variables for formatting template
    titleString = userInfo['first_Name'].lower() + ' ' + userInfo['last_Name'].lower()
    currUser = (int(UID) == loggedIn) #boolean

    #get achievements
    allComps = databaseAccess.getCompAchievements(conn, UID)
    allStars = databaseAccess.getStarAchievements(conn, UID)

    #calculate emissions
    emissionsRAW = databaseAccess.calculateUserFootprint(conn, UID)
    emissions = databaseAccess.prettyRound(emissionsRAW)
    
    return render_template('profile.html',  title=titleString,
                                                emissions = format(emissions, ','),
                                                isLoggedIn=loggedIn,
                                                userURL=user,
                                                isUser=currUser,
                                                searched=didSearch,
                                                compAchis=allComps,
                                                starAchis=allStars)

'''route to handle user updating or entering new data through the reporting form'''
@app.route('/useraction/report/<user>/', methods=['POST'])
def reportData(user):
    global loggedIn
    global didSearch
    UID = user.split('-')[2] #format first-lastname-UID
    #get information
    conn = databaseAccess.getConn(currDB)
    #take data user inputted to the form and put it in the database before re-rendering
    databaseAccess.updateUserInfo(conn, UID, 
                                    request.form.get('flights'), 
                                    request.form['drives'], 
                                    request.form['lamb'], 
                                    request.form['beef'], 
                                    request.form['cheese'], 
                                    request.form['pork'], 
                                    request.form['turkey'], 
                                    request.form['chicken'], 
                                    request.form['laundry'])
    return(redirect('/useraction/' + user + '/'))


'''route to handle actions users can take from their profile, including:
report achievements
view statistics
search users
'''
@app.route('/useraction/', methods=['POST', 'GET'], defaults={'user': ""})
@app.route('/useraction/<user>/', methods=['POST', 'GET'])
def useract(user):
    global loggedIn
    global didSearch
    
    #grab the user id
    UID = user.split('-')[2] #format first-lastname-UID

    #get information
    conn = databaseAccess.getConn(currDB)
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
