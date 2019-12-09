from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify
                   )
from werkzeug import secure_filename
app = Flask(__name__)

import bcrypt
import sys,os,random,math
import databaseAccess

#TODO: change the navbar word "Log Out" to say "Log In" when the user isn't logged in
    #it's currently supposed to do this now, but the log in isn't working for me
#TODO: (ALISSA) implement flashing!!! it doesn't show up in the template right now
#TODO: (ELLIE) Figure out team database
#TODO: (ELLIE) figure out salts
#TODO: (ESTRELLA) finish go & completed buttons
#TODO: (ALISSA) fixing the profile routes so people can view other peoples' profiles
#TODO: (ALISSA) implement user search
#TODO: (ESTRELLA) if there's time, add more Go buttons & skeleton for starring
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
    session['didSearch'] = False #used to tell apart (3) and (4) in profile.html
    conn = databaseAccess.getConn(currDB)
    #--accessing current user information
    user = ""
    #userID will either be the user's number or None if they're not logged in
    userID = session.get('uID')

    if userID != None:
        userInfo = databaseAccess.getUser(conn, userID)
        user = userInfo['first_Name'].lower() + '-' + userInfo['last_Name'].lower()
        user += '-' + str(userInfo['UID'])
    #else:
        #not logged in
    #--end of accessing current user information

    return render_template('main.html', title="Fueling Change",
                                        isLoggedIn=(True if userID!=None else False),
                                        userURL=user)


'''handles the page where users can search for achievements and self-report them'''
@app.route('/achievements/', methods = ['POST', 'GET'], defaults={'searchFor': ""})
@app.route('/achievements/<searchFor>', methods = ['POST', 'GET'])
def achievement(searchFor):
    conn = databaseAccess.getConn(currDB)
    #--accessing current user information
    user = ""
    userID = session.get('uID')
    # rep is short for reportable
    rep = []

    if userID != None:
        userInfo = databaseAccess.getUser(conn, userID)
        user = userInfo['first_Name'].lower() + '-' + userInfo['last_Name'].lower()
        user += '-' + str(userInfo['UID'])
        rep = databaseAccess.getReportedAchieves(conn, userID) 
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
                                                    reps=rep,
                                                    userURL=user)


#want to use below for user searches which will display a list based on search result.
#similar to the actor search in one of our assignments
@app.route('/profile/', methods=['POST', 'GET'], defaults={'user': ""})
# redirect to /profile/searchedfirstname-searchedlastname-searchedUID/
@app.route('/profile/<user>/', methods=['POST', 'GET'])
def profile(user):
    #TODO: make the URls just the username, don't have them include the UID
    userID = session.get('uID')

    #get user information
    #TODO: we really shouldn't be getting userInfo if current_uID is None. More generally,
    #we need to decide how to handle loading this page if the user is not logged in (and therefore current_uID is None)
    conn = databaseAccess.getConn(currDB)
    #TODO: see hwk6 to handle when user is an empty string (see movies route)
    if (userID!=None): #TODO: add another condition here so that this only happens when a user is viewing their own page (right now this happens when they're viewing ANY profile)
        #if the user is logged in
        userInfo = databaseAccess.getUser(conn, current_uID)


        #variables for formatting template
        titleString = userInfo['first_Name'].lower() + ' ' + userInfo['last_Name'].lower()
        userURL = userInfo['first_Name'].lower() + '-' + userInfo['last_Name'].lower() + '-' + str(current_uID)
        #TODO: is there a better way to format this line: (basically converting from None to False if we have to)
        #TODO: this line doesn't work and I'm not sure what it was supposed to do?
        #currUser = (int(UID) == current_uID if current_uID else False) #boolean

        #get achievements
        allComps = databaseAccess.getCompAchievements(conn, current_uID)
        allStars = databaseAccess.getStarAchievements(conn, current_uID)

        #calculate emissions
        emissionsRAW = databaseAccess.calculateUserFootprint(conn, current_uID)
        emissions = databaseAccess.prettyRound(emissionsRAW)
    
        return render_template('profile.html',  title=titleString,
                                                emissions = format(emissions, ','),
                                                #TODO: ditto -- can we reformat this next line better?
                                                isLoggedIn=(True if userID!=None else False),
                                                userURL=userURL,
                                                #this is what used to be here, unsure what currUser was supposed to be for?
                                                #isUser=currUser, #currUser was an id of the logged in person
                                                isUser=current_uID, #will this be -1 if it needs to be?
                                                searched=didSearch,
                                                compAchis=allComps,
                                                starAchis=allStars)
    #TODO: make it so users can view other peoples profiles if they're logged in (add an elif here)
    else:
        didSearch = session.get('didSearch') #boolean
        #user isn't logged in
        #they should be able to view a limited version of anybody's profile though.
        flash('you aren\'t logged in!')
        return redirect(url_for('login'))

'''route to handle user updating or entering new data through the reporting form'''
@app.route('/useraction/report/<user>/', methods=['POST'])
def reportData(user):
    didSearch = session.get('didSearch') #boolean
    UID = user.split('-')[2] #format was first-lastname-UID
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
    didSearch = session.get('didSearch') #boolean
    

    #TODO: do we want to change this so that you can only view your own profile?
    #the way it is right now, profiles are publicly viewable and we should really
    #think about whether randos are able to edit other peoples' profiles this way
    #The if/else's I (alissa) set up should prevent randos from editing: see profile.html

    #grab the user id
    UID = user.split('-')[2] #format first-lastname-UID

    #get information
    conn = databaseAccess.getConn(currDB)
    userInfo = databaseAccess.getUser(conn, UID)

    #variables for formatting template
    titleString = userInfo['first_Name'].lower() + ' ' + userInfo['last_Name'].lower()
    currUser = (int(UID) == session['uID']) #boolean
    return render_template('useraction.html', isLoggedIn=currUser,
                                                userURL=user,
                                                isUser=session['uID'])

'''route to display information for a given achievement and allows the user 
to mark as completed if logged in '''
@app.route('/achievement/<AID>/', methods= ['POST', 'GET'])
def achieveinfo(AID):
    #get information
    conn = databaseAccess.getConn(currDB)
    info = databaseAccess.getAchieveInfo(conn, AID)
    users = databaseAccess.getAchievePeople(conn, AID)
    return render_template('achieveinfo.html', achieveID = AID, 
                    info = info, users = users)


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
        row = databaseAccess.getUIDOnLogin(conn, username, hashed_password)
        row['UID'] = userID
        row['password'] = hashed_password
        if userID == -1:
            flash("login incorrect. Try again or join")
            return redirect(url_for('index'))
        else:
            hashed2 = bcrypt.hashpw(password.encode('utf-8'),hashed_password.encode('utf-8'))
            hashed2_str = hashed2.decode('utf-8')
            if hashed2_str == hashed:
                flash('successfully logged in as '+username)
                session['uID'] = userID
                #TODO: change this redirect to go to the profile page. Currently can't
                #because of the way the profile URL relies on having the user's name in it
                #^^have the form ask for the user's name too!
                return redirect(url_for('index'))
            else:
                flash('login incorrect. Try again or join')
                return redirect(url_for('index'))
    except Exception as err:
        flash('form submission error '+str(err))
        return redirect( url_for('index') )



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
                flash('passwords do not match')
                return redirect( url_for('signup'))
            #hash the password the user provided
            hashed = bcrypt.hashpw(passwd1.encode('utf-8'), bcrypt.gensalt())
            #convert it from bytes to string
            hashed_str = hashed.decode('utf-8')

            #post also takes the first and last name for database and URL purposes
            fName = request.form.get('firstName')
            lName = request.form.get('lastName')
            conn = databaseAccess.getConn(currDB)
            uID = databaseAccess.setUIDOnSignup(conn, username, hashed_str, fName, lName)
            if uID != -1:
                #actually log them in in the session
                session['uID'] = uID
                #TODO: change this redirect to go to the user's profile
                return redirect(url_for('index'))
            else:
                session['uID'] = None
                flash("that username is already taken! try again")
                return redirect( url_for('signup'))
            return redirect(url_for('profile', user=session.get('uID')))
        except Exception as e:
            flash("form submission error :( try again!")
            return redirect( url_for('index'))
    



if __name__ == '__main__':

    if len(sys.argv) > 1:
        # arg, if any, is the desired port number
        port = int(sys.argv[1])
        assert(port>1024)
    else:
        port = os.getuid()
    app.debug = True
    app.run('0.0.0.0',port)
