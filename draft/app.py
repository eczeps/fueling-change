from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify
                   )
from werkzeug import secure_filename
app = Flask(__name__)

import sys,os,random,math
import databaseAccess

#TODO: implement flashing!!! it doesn't show up in the template right now

currDB = databaseAccess.d
didSearch = False #used to tell apart (3) and (4) in profile.html
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
    conn = databaseAccess.getConn(currDB)
    user = ""
    #userID will either be the user's number or None if they're not logged in
    userID = session['uID']

    if userID:
        userInfo = databaseAccess.getUser(conn, userID)
        user = userInfo['first_Name'].lower() + '-' + userInfo['last_Name'].lower()
        user += '-' + str(userInfo['UID'])

    return render_template('main.html', title="Fueling Change",
                                        isLoggedIn= (userID if userID else False),
                                        userURL=user)


'''handles the page where users can search for achievements and self-report them'''
@app.route('/achievements/', methods = ['POST', 'GET'], defaults={'searchFor': ""})
@app.route('/achievements/<searchFor>', methods = ['POST', 'GET'])
def achievement(searchFor):
    conn = databaseAccess.getConn(currDB)
    user = ""
    # rep is short for reportable
    rep = []

    if session['uID']:
        userInfo = databaseAccess.getUser(conn, session['uID'])
        user = userInfo['first_Name'].lower() + '-' + userInfo['last_Name'].lower()
        user += '-' + str(userInfo['UID'])
        rep = databaseAccess.getReportedAchieves(conn, session['uID']) 

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
                                                    isLoggedIn=session['uID'],
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
    #TODO: reimplement global didSearch some other way
    global didSearch

    current_uID = session.get('uID')

    #get user information
    #TODO: we really shouldn't be getting userInfo if current_uID is None. More generally,
    #we need to decide how to handle loading this page if the user is not logged in (and therefore current_uID is None)
    conn = databaseAccess.getConn(currDB)

    if (current_uID):
        #if the user is logged in
        userInfo = databaseAccess.getUser(conn, current_uID)


        #variables for formatting template
        titleString = userInfo['first_Name'].lower() + ' ' + userInfo['last_Name'].lower()
        #TODO: is there a better way to format this line: (basically converting from None to False if we have to)
        currUser = (int(UID) == current_uID if current_uID else False) #boolean

        #get achievements
        allComps = databaseAccess.getCompAchievements(conn, UID)
        allStars = databaseAccess.getStarAchievements(conn, UID)

        #calculate emissions
        emissionsRAW = databaseAccess.calculateUserFootprint(conn, UID)
        emissions = databaseAccess.prettyRound(emissionsRAW)
    
        return render_template('profile.html',  title=titleString,
                                                emissions = format(emissions, ','),
                                                #TODO: ditto -- can we reformat this next line better?
                                                isLoggedIn= (current_uID if current_uID else False),
                                                userURL=user,
                                                isUser=currUser,
                                                searched=didSearch,
                                                compAchis=allComps,
                                                starAchis=allStars)

    else:
        #user isn't logged in
        flash('you aren\'t logged in!')
        return redirect(url_for('login'))

'''route to handle user updating or entering new data through the reporting form'''
@app.route('/useraction/report/<user>/', methods=['POST'])
def reportData(user):
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
    #TODO: get rid of didSearch, re-implement some other way
    global didSearch
    

    #TODO: do we want to change this so that you can only view your own profile?
    #the way it is right now, profiles are publicly viewable and we should really
    #think about whether randos are able to edit other peoples' profiles this way

    #grab the user id
    UID = user.split('-')[2] #format first-lastname-UID

    #get information
    conn = databaseAccess.getConn(currDB)
    userInfo = databaseAccess.getUser(conn, UID)

    #variables for formatting template
    titleString = userInfo['first_Name'].lower() + ' ' + userInfo['last_Name'].lower()
    currUser = (int(UID) == session['uID']) #boolean
    return render_template('useraction.html', isLoggedIn=session['uID'],
                                                userURL=user,
                                                isUser=currUser)




@app.route('/login/', methods=['GET'])
def login():
    #current_id is the id of the user currently logged in (if any)
    current_uid = session.get('uID')
    if current_uid:
        #user is logged in; they're trying to log out
        flash('Logging out!')
        session['uID'] = None
        return redirect(url_for(index))
    else:
        #user isn't logged in; they're trying to log in
        return render_template('login_page.html')
            

@app.route('/setUID/', methods=["POST"])
def setUID():
    #gets called when a user presses submit on the login form
    username = request.form.get('username')
    password = request.form.get('password')
    conn = databaseAccess.getConn(currDB)
    #userID will either be the user's ID or -1 if it was an invalid username/password combo
    userID = databaseAccess.getUIDOnLogin(conn, username, password)
    if userID != -1:
        session['uID'] = userID
        #TODO: change this redirect to go to the profile page. Currently can't
        #because of the way the profile URL relies on having the user's name in it
        return redirect(url_for('index'))
    else:
        return redirect(request.referrer)



@app.route('/signup/', methods=["GET"])
def signup():
    return "<p> this page hasn't been implemented yet!! we have to figure out how to store passwords in the database first</p>"



if __name__ == '__main__':

    if len(sys.argv) > 1:
        # arg, if any, is the desired port number
        port = int(sys.argv[1])
        assert(port>1024)
    else:
        port = os.getuid()
    app.debug = True
    app.run('0.0.0.0',port)
