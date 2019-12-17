from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify
                   )
from werkzeug import secure_filename
app = Flask(__name__)

import bcrypt
import sys,os,random,math
import databaseAccess as dba
import automatics as atm

#TODO: (ELLIE) emissions don't update to the database after calculations
#TODO: (ELLIE) Figure out team database
#TODO: (ESTRELLA) finish go & completed buttons
#TODO: (ESTRELLA) make templates more inheritey
#TODO: run all the code through WAVE (whoever pushes last)
#TODO: (ESTRELLA) make sure we always use url_for (even in templates)
#TODO: (ELLIE) make a powerpoint/outline for the presentation
#TODO: (ESTRELLA) submit a request for a team shell account, and email him when you do it

currDB = dba.d
debug = dba.debug
debugLong = dba.debugLong

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
    conn = dba.getConn(currDB)
    #--accessing current user information
    #userID will either be the user's number or None if they're not logged in
    userID = session.get('uID')
    
    if debug:
        print('++ (app.py) userID in index route: ' + str(userID))

    username = ""
    if userID != None:
        username = dba.getUserInfo(conn, userID)['username']
    #else:
        #not logged in profile won't show so we don't need to worry about
        #username being empty
    #--end of accessing current user information

    #generate a random number and use that to pick a fun fact to display
    randomFunFactInfo = dba.getFunFact(conn, random.randrange(1, 5))

    return render_template('main.html', title="Fueling Change",
                                        isLoggedIn=(True if userID!=None else False),
                                        funFact = randomFunFactInfo['fact_description'],
                                        factSource = randomFunFactInfo['source'],
                                        userURL=username)


'''handles the page where users can search for achievements'''
@app.route('/achievements/', methods = ['POST', 'GET'], defaults={'searchFor': ""})
@app.route('/achievements/<searchFor>', methods = ['POST', 'GET'])
def achievement(searchFor):
    conn = dba.getConn(currDB)

    #check achievements that we need to check for the user
    atm.updateAutomaticAchieves(conn)

    #--accessing current user information
    userID = session.get('uID')
    # stars is short for starred achievements
    stars = []

    username = ""
    if userID != None:
        username = dba.getUserInfo(conn, userID)["username"]
        items = dba.getStarAchieves(conn, userID) 

        for i in items:
            stars.append(i['AID'])
    #else:
        #not logged in
    #--end of accessing current user information

    #if the user is searching for something, access the database to get search results
    searchFor = request.form.get('searchterm')
    if request.method == 'POST':
        a = []
        if(searchFor==""):
            a = dba.getAllAchievements(conn)
        else:
            a = dba.getAchievements(conn,searchFor)

    #if the user is just loading the page, show them all the achievements
    elif request.method == 'GET':
        searchFor = ''
        a = dba.getAllAchievements(conn)


    return render_template('achievementSearch.html',title=searchFor,
                                                    achievements=a,
                                                    isLoggedIn=(True if userID!=None else False),
                                                    reps=stars,
                                                    userURL=username)


'''handles the page where users can search for users'''
@app.route('/users/', methods = ['POST', 'GET'], defaults={'userSearch': ""})
@app.route('/users/<userSearch>/', methods = ['POST', 'GET'])
def users(userSearch):
    conn = dba.getConn(currDB)

    #update before showing anything
    #check achievements that we need to check for the user
    atm.updateAutomaticAchieves(conn)

    #current user information
    userID=session.get('uID')
    username=""
    if userID != None:
        username=dba.getUserInfo(conn, userID)['username']

    #find the users that have a matching search term in their
    #first, last, or username
    userSearch = request.form.get('searchterm')
    if request.method == 'POST':
        a = []
        if(userSearch==""):
            a = dba.getAllUsers(conn)
            random.shuffle(a)
        else:
            a = dba.getUsers(conn,userSearch)
            #don't shuffle for real searches

    #if the user is just loading the page, show them the leaderboard
    elif request.method == 'GET':
        userSearch = ''
        a = dba.getAllUsers(conn)

    if debug:
        print("++ (app.py) a:", a)
        print("++ (app.py) len(a):", len(a))
        print("++ (app.py) userSearch: '" + userSearch + "'")
    
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

    #connect to database
    conn = dba.getConn(currDB)
    #TODO: see hwk6 to handle when user is an empty string (see movies route)

    if (userID!=None):
        #check that the username in the url matches this user's username
        uNameCheck = dba.checkCorrectUser(conn,username,userID)
        if not uNameCheck[0]:
            #user is trying to access a profile of someone other than themselves
            if userID != None:
                flash('redirecting to your profile')
                return redirect(url_for('profile', username=uNameCheck[1]))
            else:
                flash('you aren\'t logged in!')
                return redirect(url_for('index'))

        #if the user is logged in correctly we can grab data
        userInfo = dba.getUserInfo(conn, userID)

        #variables for formatting template
        titleString = userInfo['first_Name'] + ' ' + userInfo['last_Name']
        userURL = userInfo['username'].lower()
        userPhoto = "pictures/" + userInfo['photo']

        #TODO: this line doesn't work and I'm not sure what it was supposed to do?
        #currUser = (int(UID) == current_uID if current_uID else False) #boolean

        #get achievements
        allComps = dba.getCompAchieves(conn, userID)
        allStars = dba.getStarAchieves(conn, userID)
        
        #calculate emissions
        has_carbon_data = dba.doesUserHaveCarbonData(conn, userID)
        if debug:
            print('++ (app.py) has_carbon_data in profile route: ' + str(has_carbon_data))
        
        if has_carbon_data:
            emissionsRAW = dba.calculateUserFootprint(conn, userID)
            emissions = dba.prettyRound(emissionsRAW)
        else:
            #TODO: maybe figure out a better thing to display when a user doesn't have emissions data than just a 0?
            #fix this by forcing them to fill out data on sign up or on login until they do it.
            emissions = 0
    
        return render_template('profile.html',  title=titleString,
                                                emissions = format(emissions, ','),
                                                isLoggedIn=(True if userID!=None else False),
                                                userURL=userURL,
                                                thisUser=userID, #will this be -1 if it needs to be?
                                                compAchis=allComps,
                                                starAchis=allStars,
                                                photohere=userPhoto)
    #TODO: make it so users can view other peoples profiles if they're logged in (add an elif here)
    else:
        #user isn't logged in
        flash('you aren\'t logged in!')
        return redirect(url_for('login'))

'''route to handle profile photo updates'''
@app.route('/useraction/changephoto/<username>/', methods=['POST'])
def upload_file(username):
    UID = session.get('uID')

    #get information
    conn = dba.getConn(currDB)

    #must be logged in to get to this point so no issues with null here
    username = dba.getUserInfo(conn, UID)['username']

    f = request.files['file']
    fileParts = os.path.splitext(f.filename)

    print("++ fileParts:", fileParts)

    extension = fileParts[1]
    acceptableTypes = {".png", ".jpg", ".gif", ".jpeg"}
    if len(extension)==0:
        flash("photo not changed")
        return(redirect(url_for('profile', user=username)))

    elif not (extension in acceptableTypes):
        flash("unnacceptable file type: please use .png, .jpg, .gif, or .jpeg")
        return(redirect(url_for('profile', user=username)))

    saveFile = username + extension

    f.save(os.path.join('static/pictures/', saveFile))

    #take photo inputted to the form and put it's path in the database before re-rendering
    defaultChanged = dba.updatePhoto(conn, UID, saveFile)

    if defaultChanged:
        flash("photo changed successfully!")

    return(redirect(url_for('profile', user=username)))







'''route to handle user updating or entering new data through the reporting form'''
@app.route('/useraction/report/<user>/', methods=['POST'])
def reportData(user):
    UID = session.get('uID')
    #get information
    conn = dba.getConn(currDB)
    #take data user inputted to the form and put it in the database before re-rendering
    dba.updateUserInfo(conn, UID, 
                                    request.form.get('flights'), 
                                    request.form['drives'], 
                                    request.form['lamb'], 
                                    request.form['beef'], 
                                    request.form['cheese'], 
                                    request.form['pork'], 
                                    request.form['turkey'], 
                                    request.form['chicken'], 
                                    request.form['laundry'])
    
    #check achievements that we need to check for the user
    atm.updateAutomaticAchieves(conn) #right now these are leadership achieves

    return(redirect(url_for('profile', user=user)))


'''route to handle actions users can take from their profile, including:
report achievements
view statistics
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
    conn = dba.getConn(currDB)
    userInfo = dba.getUserInfo(conn, UID)

    #check achievements that we need to check for the user
    atm.updateAutomaticAchieves(conn) #right now these are leadership achieves

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
    conn = dba.getConn(currDB)
    #need for if the user selects their profile tab
    userID = session.get('uID')

    #username of the logged in user
    username = ""

    if userID != None:
        username = dba.getUserInfo(conn, userID)["username"]

    #this is the searched for information
    searchedInfo = dba.getUserByUsername(conn, user)
    nameTitle = searchedInfo['first_Name'] + " " + searchedInfo['last_Name']
    searchedID = searchedInfo['UID']

    #achievements of the seached user that we want to look at
    allComps = dba.getCompAchieves(conn, searchedID)
    allStars = dba.getStarAchieves(conn, searchedID)

    #calculate emissions of the searched user
    has_carbon_data = dba.doesUserHaveCarbonData(conn, searchedID)
    if debug:
        print('++ (app.py) has_carbon_data in searched-profile route: ' + str(has_carbon_data))
    if has_carbon_data:
        emissionsRAW = dba.calculateUserFootprint(conn, searchedID)
        emissions = dba.prettyRound(emissionsRAW)
    else:
        emissions = dba.getUserFootprint(conn, searchedID)

    return render_template('searchedProfile.html', title = nameTitle,
                                                   thisUser = userID, #in nav bar
                                                   isLoggedIn = (True if userID!=None else False),
                                                   emissions = format(emissions, ','),
                                                   compAchis = allComps,
                                                   starAchis = allStars,
                                                   userURL=username)


'''route to display information for a given achievement and allows the user 
to mark as completed if logged in '''
@app.route('/achievement/<AID>/', methods= ['POST', 'GET'])
def achieveinfo(AID):
    conn = dba.getConn(currDB)
    #--accessing current user information
    #if the user is logged in then allow to self report
    user_info = None
    completed_info = None
    completed = False
    count = None
    userID = session.get('uID') # will be none if not logged in
    username = ""

    if userID != None:
        username = dba.getUserInfo(conn, userID)["username"]
        user_info = dba.getUserInfo(conn, userID)
        #check if the user has already completed this achievement
        completed_info = dba.getUserCompletedAchiev(conn, userID, AID)
        if completed_info != None :
            completed = True
            count = completed_info["count"] 
    #else:
        #not logged in
    #--end of accessing current user information

    achieve_info = dba.getAchieveInfo(conn, AID)
    #returns the UID, first name, last name of users who completed
    users = dba.getAchievePeople(conn, AID)

    return render_template('achieveinfo.html', achieveID = AID, 
                                               info = achieve_info,
                                               users = users,
                                               thisUser = userID, 
                                               user_info = user_info,
                                               completed = completed,
                                               count = count,
                                               isLoggedIn = (True if userID!=None else False),
                                               userURL=username)

'''route to update the database when the user clicked "yes" under completed 
to mark as completed if logged in '''
@app.route('/updateCompleted/', methods= ['POST'])
def updateCompleted():
    conn = dba.getConn(currDB)
    aid = request.form['aid'] #gets the achievement ID to update 
    #don't need to check if logged in because they need to be logged in to click on the yes button
    userID = session.get('uID')

    #update the backend
    dba.insertCompleted(conn, userID, aid)
    
    grabData = dba.getUserForAchievement(conn, userID, aid)
    user_info = grabData[0]
    hasCount = grabData[1]
    
    return jsonify({'UID': userID,
                    'first': user_info['first_Name'],
                    'last': user_info['last_Name'],
                    'username': user_info['username'],
                    'count': user_info['count'] if hasCount else 1})


@app.route('/updateRepeatedAchiev/', methods= ['POST'])
def updateRepeatedAchiev():
    conn = dba.getConn(currDB)
    userID = session.get('uID')
    aid = request.form["aid"]
    new_count = request.form["new_count"]
    dba.updateCompletedCount(conn, userID, aid, new_count)
    return redirect(url_for('achieveinfo', AID = aid))

@app.route('/resetAchieveAjax/', methods = ['POST'])
def resetAchieveAjax():
    conn = dba.getConn(currDB)
    userID = session.get('uID')
    aid = request.form['aid']
    dba.deleteCompletedAchiev(conn, userID, aid)
    return jsonify({"reload": "true"})

#updates the starred table  when a user stars an achievement 
@app.route('/addStar/', methods = ['POST'])
def addStar():
    conn = dba.getConn(currDB)
    userID = session.get('uID')
    aid = request.form['aid']
    dba.addStarAchiev(conn, userID, aid)
    return jsonify({"status": "true"})

#updates the starred table when a user unstars an achievement
@app.route('/removeStar/', methods = ['POST'])
def removeStar():
    conn = dba.getConn(currDB)
    userID = session.get('uID')
    aid = request.form['aid']
    dba.removeStarAchiev(conn, userID, aid)
    return jsonify({"status": "true"})

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
                                userURL="",
                                title="Login")
            

@app.route('/setUID/', methods=["POST"])
def setUID():
    #gets called when a user presses submit on the login form
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        conn = dba.getConn(currDB)
        #userID will either be the user's ID or -1 if it was an invalid username/password combo. this also returns the hashed password
        row = dba.getUIDOnLogin(conn, username)
        userID = row['UID']
        hashed_password = row['password']
        
        if debug:
            print('++ (app.py) got all necessary data in login')
        if userID == -1:
            if debug:
                print("++ (app.py) the database didn't think your username was legit")
            flash("login incorrect. Try again or join")
            return redirect(url_for('index'))
        else:
            hashed2 = bcrypt.hashpw(password.encode('utf-8'),hashed_password.encode('utf-8'))
            hashed2_str = hashed2.decode('utf-8')

            if hashed2_str == hashed_password:
                #log in success!
                if debug:
                    print('++ (app.py) your password was right! logging you in')
                flash('successfully logged in as '+username)
                session['uID'] = userID

                currentUser = session.get('uID')
                if debug:
                    print("++ (app.py) uID:", currentUser)

                #check achievements that we need to check for the user
                atm.updateAutomaticAchieves(conn)

                #redirect!
                username=dba.getUserInfo(conn, currentUser)['username']
                return redirect(url_for('profile', username=username))
            else:
                if debug:
                    print('++ (app.py) your password was probably wrong')
                flash('login incorrect. Try again or join')
                return redirect(url_for('login'))
    except Exception as err:
        print('*** ERROR (login): ' + str(err) + ' ***')
        flash('form submission error '+ str(err))
        return redirect( url_for('login') )

@app.route('/signup/', methods=["GET", "POST"])
def signup():
    signupSuccessful=False
    if request.method == "GET":
        #get method renders a page w a form
        return render_template('signup.html', title="Sign Up")
    else:
        try:
            username = request.form['username']
            passwd1 = request.form['password1']
            passwd2 = request.form['password2']
            if passwd1 != passwd2:
                print('++ (app.py) passwords do not match')
                flash('passwords do not match')
                return redirect(url_for('signup'))
            #hash the password the user provided
            hashed = bcrypt.hashpw(passwd1.encode('utf-8'), bcrypt.gensalt())
            #convert it from bytes to string
            hashed_str = hashed.decode('utf-8')

            #post also takes the first and last name for database and URL purposes
            fName = request.form.get('firstName')
            lName = request.form.get('lastName')
            conn = dba.getConn(currDB)
            uID = dba.setUIDOnSignup(conn, username, hashed_str, fName, lName)['UID']
            #if this is a dictionary make it a string
            print('++ (app.py) uID after signup: ' + str(uID))
            if uID != -1:
                print('++ (app.py) logging you in! after signup')
                #actually log them in in the session
                session['uID'] = uID

                #add them to the joined fueling-change achievement
                dba.insertCompleted(conn, session.get('uID'), 1)
                
                username = username=dba.getUserInfo(conn, session.get('uID'))['username']
                return redirect(url_for('profile', username=username))
            else:
                print('++ (app.py) username already taken on signup')
                session['uID'] = None
                flash("that username is already taken! try again")
                return redirect(url_for('signup'))
            
        except Exception as e:
            print('*** ERROR (Signup): ' + str(e) + ' ***')
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
