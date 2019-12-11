from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify
                   )
from werkzeug import secure_filename
app = Flask(__name__)

import bcrypt
import sys,os,random,math
import databaseAccess

#TODO: (ELLIE) Figure out team database
#TODO: (ELLIE) figure out salts
#TODO: (ESTREL  LA) finish go & completed buttons
#TODO: (ALISSA) implement user search
#TODO: (ESTRELLA) make templates more inheritey
#TODO: (ESTRELLA) create google doc for alpha version
#TODO: run all the code through WAVE (whoever pushes last)
#TODO: (ESTRELLA) make sure we always use url_for (even in templates)
#TODO: (ALISSA) comment all the code & do all documentation
#TODO: (ELLIE) make a powerpoint/outline for the presentation
#TODO: (ESTRELLA) submit a request for a team shell account, and email him when you do it

currDB = databaseAccess.d
# currUser = 1
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
    #--accessing current user information
    #userID will either be the user's number or None if they're not logged in
    userID = session.get('uID')
    print('userID in index route: ' + str(userID))

    username = ""
    if userID != None:
        username = databaseAccess.getUser(conn, userID)['username']
    #else:
        #not logged in profile won't show so we don't need to worry about
        #username being empty
    #--end of accessing current user information

    return render_template('main.html', title="Fueling Change",
                                        isLoggedIn=(True if userID!=None else False),
                                        userURL=username)


'''handles the page where users can search for achievements'''
@app.route('/achievements/', methods = ['POST', 'GET'], defaults={'searchFor': ""})
@app.route('/achievements/<searchFor>', methods = ['POST', 'GET'])
def achievement(searchFor):
    conn = databaseAccess.getConn(currDB)
    #--accessing current user information
    userID = session.get('uID')
    # stars is short for starred achievements
    stars = []

    username = ""
    if userID != None:
        username = databaseAccess.getUser(conn, userID)["username"]
        stars = databaseAccess.getStarredAchieves(conn, userID) 
    #else:
        #not logged in
    #--end of accessing current user information

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
                                                    isLoggedIn=(True if userID!=None else False),
                                                    reps=stars,
                                                    userURL=username)


'''handles the page where users can search for users'''
@app.route('/users/', methods = ['POST', 'GET'], defaults={'userSearch': ""})
@app.route('/users/<userSearch>', methods = ['POST', 'GET'])
def users(userSearch):
    conn = databaseAccess.getConn(currDB)
    #find the users that have a matching search term in their
    #first, last, or username
    #if the user is searching for something, access the database to get search results
    userSearch = request.form.get('searchterm')
    userID=session.get('uID')

    username=""
    if userID != None:
        username=databaseAccess.getUser(conn, userID)['username']

    if request.method == 'POST':
        a = []
        if(userSearch != ""):
            print("RIGHT HERE")
            print(userSearch)
            a = databaseAccess.getUsers(conn,userSearch)

    #if the user is just loading the page, show them nothing
    elif request.method == 'GET':
        userSearch = ''
        a = []
    
    return render_template('userSearch.html',title=userSearch,
                                             users=a,
                                             isLoggedIn=(True if userID!=None else False),
                                             userURL=username)

#want to use below for user searches which will display a list based on search result.
#similar to the actor search in one of our assignments
@app.route('/profile/', methods=['POST', 'GET'], defaults={'username': ""})
@app.route('/profile/<username>/', methods=['POST', 'GET'])
def profile(username):
    #TODO: make the URls just the username, don't have them include the UID
    userID = session.get('uID')

    #get user information
    #TODO: we really shouldn't be getting userInfo if current_uID is None. More generally,
    #we need to decide how to handle loading this page if the user is not logged in (and therefore current_uID is None)
    conn = databaseAccess.getConn(currDB)
    #TODO: see hwk6 to handle when user is an empty string (see movies route)
    
    if (userID!=None): #TODO: add another condition here so that this only happens when a user is viewing their own page (right now this happens when they're viewing ANY profile)
        #if the user is logged in
        userInfo = databaseAccess.getUser(conn, userID)

        #variables for formatting template
        titleString = userInfo['first_Name'].lower() + ' ' + userInfo['last_Name'].lower()
        userURL = userInfo['username'].lower()

        #TODO: this line doesn't work and I'm not sure what it was supposed to do?
        #currUser = (int(UID) == current_uID if current_uID else False) #boolean

        #get achievements
        allComps = databaseAccess.getCompAchievements(conn, userID)
        allStars = databaseAccess.getStarredAchieves(conn, userID)

        #calculate emissions
        has_carbon_data = databaseAccess.doesUserHaveCarbonData(conn, userID)
        print('has_carbon_data in profile route: ' + str(has_carbon_data))
        if has_carbon_data:
            print('has carbon data!!')
            emissionsRAW = databaseAccess.calculateUserFootprint(conn, userID)
            emissions = databaseAccess.prettyRound(emissionsRAW)
        else:
            #TODO: maybe figure out a better thing to display when a user doesn't have emissions data than just a 0?
            emissions = 0
    
        return render_template('profile.html',  title=titleString,
                                                emissions = format(emissions, ','),
                                                isLoggedIn=(True if userID!=None else False),
                                                userURL=userURL,
                                                thisUser=userID, #will this be -1 if it needs to be?
                                                compAchis=allComps,
                                                starAchis=allStars)
    #TODO: make it so users can view other peoples profiles if they're logged in (add an elif here)
    else:
        #user isn't logged in
        flash('you aren\'t logged in!')
        return redirect(url_for('login'))

'''route to handle user updating or entering new data through the reporting form'''
@app.route('/useraction/report/<user>/', methods=['POST'])
def reportData(user):
    UID = session.get('uID') #format was first-lastname-UID
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
    

    #TODO: do we want to change this so that you can only view your own profile?
    #the way it is right now, profiles are publicly viewable and we should really
    #think about whether randos are able to edit other peoples' profiles this way
    #The if/else's I (alissa) set up should prevent randos from editing: see profile.html

    #grab the user id
    UID = session.get('uID')

    #get information
    conn = databaseAccess.getConn(currDB)
    userInfo = databaseAccess.getUser(conn, UID)

    #variables for formatting template
    titleString = userInfo['first_Name'].lower() + ' ' + userInfo['last_Name'].lower()
    currUser = (int(UID) == session['uID']) #boolean
    return render_template('useraction.html', isLoggedIn=currUser,
                                                userURL=user,
                                                thisUser=session['uID'])


'''route to display information for a given achievement and allows the user 
to mark as completed if logged in '''
@app.route('/searched-profile/<user>/', methods= ['POST', 'GET'])
def searchedProfile(user):
    conn = databaseAccess.getConn(currDB)
    #need for if the user selects their profile tab
    userID = session.get('uID')

    #this is the searched for information
    searchedInfo = databaseAccess.getUserByUsername(conn, user)
    nameTitle = searchedInfo['first_Name'] + " " + searchedInfo['last_Name']
    searchedID = searchedInfo['UID']

    #achievements of the seached user that we want to look at
    allComps = databaseAccess.getCompAchievements(conn, searchedID)
    allStars = databaseAccess.getStarredAchieves(conn, searchedID)

    #calculate emissions of the searched user
    has_carbon_data = databaseAccess.doesUserHaveCarbonData(conn, searchedID)
    # print('has_carbon_data in profile route: ' + str(has_carbon_data))
    if has_carbon_data:
        print('has carbon data!!')
        emissionsRAW = databaseAccess.calculateUserFootprint(conn, searchedID)
        emissions = databaseAccess.prettyRound(emissionsRAW)
    else:
        #TODO: maybe figure out a better thing to display when a user doesn't have emissions data than just a 0?
        emissions = 0

    return render_template('searchedProfile.html', title = nameTitle,
                                                   thisUser = userID, #in nav bar
                                                   isLoggedIn = (True if userID!=None else False),
                                                   emissions = emissions,
                                                   compAchis = allComps,
                                                   starAchis = allStars)


'''route to display information for a given achievement and allows the user 
to mark as completed if logged in '''
@app.route('/achievement/<AID>/', methods= ['POST', 'GET'])
def achieveinfo(AID):
    conn = databaseAccess.getConn(currDB)
    #get information
    #if the user is logged in then allow to self report
    userID = None
    user_info = None
    if (session.get('uID') != None):
        userID = session.get('uID')
        user_info = databaseAccess.getUser(conn, userID)

    achieve_info = databaseAccess.getAchieveInfo(conn, AID)
    #returns the UID, first name, last name of users who completed
    users = databaseAccess.getAchievePeople(conn, AID)  
    return render_template('achieveinfo.html', achieveID = AID, 
                                               info = achieve_info,
                                               users = users,
                                               thisUser = userID, 
                                               user_info = user_info,
                                               isLoggedIn = (True if userID!=None else False))

'''route to update the database when the user clicked "yes" under completed 
to mark as completed if logged in '''
@app.route('/updateCompleted/', methods= ['POST'])
def updateCompleted():
    conn = databaseAccess.getConn(currDB)
    aid = request.form['aid'] #gets the achievement ID to update 
    print("achieve id" + aid) 
    #don't need to check if logged in because they need to be logged in to click on the yes button
    userID = session.get('uID')
    print(userID)

    #update the backend
    databaseAccess.insertCompleted(conn, userID, aid)
    
    grabData = databaseAccess.getUserForAchievement(conn, userID, aid)
    user_info = grabData[0]
    hasCount = grabData[1]
    print(user_info)

    print("HERE")
    return jsonify({'UID': userID,
                    'first': user_info['first_Name'],
                    'last': user_info['last_Name'],
                    'username': user_info['username'],
                    'count': user_info['count'] if hasCount else 1})


@app.route('/login/', methods=['GET'])
def login():
    #userID is the id of the user currently logged in (if any)
    userID = session.get('uID') 
    if userID!=None: #TODO:i don't think this logic works right I think it's backwards
        #user is logged in; they're trying to log out
        flash('Logging out!')
        #how can they be logging out if the userID is already None
        #wouldn't they already be logged out?
        session['uID'] = None
        return redirect(url_for('index'))
    else:
        #user isn't logged in; they're trying to log in
        return render_template('login_page.html',
                                isLoggedIn=False,
                                userURL="")
            

@app.route('/setUID/', methods=["POST"])
def setUID():
    #gets called when a user presses submit on the login form
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        conn = databaseAccess.getConn(currDB)
        #userID will either be the user's ID or -1 if it was an invalid username/password combo. this also returns the hashed password
        row = databaseAccess.getUIDOnLogin(conn, username)
        print(str(row))
        userID = row['UID']
        hashed_password = row['password']
        print('got all necessary data in login')
        if userID == -1:
            print('database didnt think your username was legit')
            flash("login incorrect. Try again or join")
            return redirect(url_for('index'))
        else:
            hashed2 = bcrypt.hashpw(password.encode('utf-8'),hashed_password.encode('utf-8'))
            hashed2_str = hashed2.decode('utf-8')
            print('hashed_password: ' + hashed_password)
            print('hashed2_str: ' + hashed2_str)
            if hashed2_str == hashed_password:
                print('your password was right! logging you in')
                flash('successfully logged in as '+username)
                session['uID'] = userID
                username=databaseAccess.getUser(conn, session.get('uID'))['username']
                return redirect(url_for('profile', username=username))
            else:
                print('your password was prob wrong')
                flash('login incorrect. Try again or join')
                return redirect(url_for('login'))
    except Exception as err:
        print('error in login: ' + str(err))
        flash('form submission error '+ str(err))
        return redirect( url_for('login') )



@app.route('/signup/', methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        #get method renders a page w a form
        return render_template('signup.html')
    else:
        try:
            username = request.form['username']
            passwd1 = request.form['password1']
            passwd2 = request.form['password2']
            if passwd1 != passwd2:
                print('passwords do not match')
                flash('passwords do not match')
                return redirect(url_for('signup'))
            #hash the password the user provided
            hashed = bcrypt.hashpw(passwd1.encode('utf-8'), bcrypt.gensalt())
            #convert it from bytes to string
            hashed_str = hashed.decode('utf-8')

            #post also takes the first and last name for database and URL purposes
            fName = request.form.get('firstName')
            lName = request.form.get('lastName')
            conn = databaseAccess.getConn(currDB)
            uID = databaseAccess.setUIDOnSignup(conn, username, hashed_str, fName, lName)['UID']
            #if this is a dictionary make it a string
            print('uID after signup: ' + str(uID))
            if uID != -1:
                print('logging you in! after signup')
                #actually log them in in the session
                session['uID'] = uID
                username = username=databaseAccess.getUser(conn, session.get('uID'))['username']
                return redirect(url_for('profile', username=username))
            else:
                print('username already taken on signup')
                session['uID'] = None
                flash("that username is already taken! try again")
                return redirect(url_for('signup'))
            username=databaseAccess.getUser(conn, session.get('uID'))['username']
            return redirect(url_for('profile', username=username))
        except Exception as e:
            print('form submission error in signup: ' + str(e))
            flash("form submission error :( try again!")
            return redirect( url_for('login'))
    



if __name__ == '__main__':

    if len(sys.argv) > 1:
        # arg, if any, is the desired port number
        port = int(sys.argv[1])
        assert(port>1024)
    else:
        port = os.getuid()
    app.debug = True
    app.run('0.0.0.0',port)
