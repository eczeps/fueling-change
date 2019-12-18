from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify
                   )
import dbi
import calculator as calculator
import sys,math,os
# the database to use:
d = "fchange8_db"
# script testingSetup.sh replaces this like so:
# $ ./testingSetup.sh atinney_db

#set the below to True to increase console output
debug=False
debugLong=False


# ==========================================================

    # ==== KEY ====
    # for scroll search purposes. (use find)
    # (alpha)-(alpha)-(numeral) such as A-B-1
    # first (alpha) can be A or M
    #   A stands for Access
    #   M stands for Modify
    # second (alpha) can be A, U, or B
    #   A means function has parameters for achievements only
    #   U means function has parameters for users only
    #   B means function has parameters for both.
    # (numeral) can be any numeric quantity
    #   purpose of (numeral) is to incrementally count functions
    #       within a category.


# ==== GENERAL PURPOSE ====
def getConn(db):
    '''Returns a database connection for that db'''
    dsn = dbi.read_cnf('../../.my.team_cnf') # for group db
    #dsn = dbi.read_cnf() #for own db
    conn = dbi.connect(dsn)
    conn.select_db(db)
    return conn

def prettyRound(number):
    return math.floor(round(number,0))


# ==== ACCESS INFORMATION BASED ON ACHIEVEMENTS ====
# A-A-1
def getAchieveInfo(conn, AID):
    '''Returns the title, description, isRepeatable, isSelfReport of given AID'''
    curs = dbi.dictCursor(conn)
    curs.execute('''select title, description, isRepeatable, isSelfReport
                    from achievement
                    where AID = %s''', [AID])
    return curs.fetchone()

# A-A-2
def getAchievements(conn, searchFor):
    '''Returns the AID, title, description, isRepeatable, isSelfReport
    of all achievements that have a similar field to the search,
    as a list of dictionaries.
    '''
    curs = dbi.dictCursor(conn)
    searchFor = "%" + searchFor + "%"
    curs.execute('''select AID, title, description, isRepeatable, isSelfReport
                    from achievement
                    where title like %s
                    or description like %s
                    or isRepeatable like %s
                    or isSelfReport like %s''',
                    [searchFor,searchFor,searchFor,searchFor])
    return curs.fetchall()

# A-A-3
def getAllAchievements(conn):
    '''Returns the AID, title, description, isRepeatable, isSelfReport 
    of all achievements, as a list of dictionaries.
    '''
    curs = dbi.dictCursor(conn)
    curs.execute('''select AID, title, description, isRepeatable, isSelfReport
                    from achievement''')
    return curs.fetchall()

# A-A-4
def getIsRepeatable(conn, AID):
    '''Returns whether or not this achievement is eligible
    for repetition. This is a Boolean return.
    '''
    curs = dbi.dictCursor(conn)
    curs.execute('''select isRepeatable from achievement where AID=%s''', [AID])
    
    #not checking for null cause if that happens it was our fault
    res = curs.fetchone()

    return (res == 1) #in our world, 0 is false and 1 is true

# A-A-5
def getIsSelfReport(conn, AID):
    '''Returns whether or not this achievement is eligible
    for self report. This is a Boolean return.
    '''
    curs = dbi.dictCursor(conn)
    curs.execute('''select isSelfReport from achievement where AID=%s''', [AID])
    
    #not checking for null cause if that happens it was our fault
    res = curs.fetchone()

    return (res == 1) #in our world, 0 is false and 1 is true

# A-A-6
def getAchievePeople(conn, AID):
    '''Returns the UID, first_Name, last_Name, username, footprint,
    and count for people who have completed this achievement
    Listed by ascending order of count then footprint.'''
    curs = dbi.dictCursor(conn)
    curs.execute('''select UID, first_Name, last_Name, username, footprint, count 
                    from completed inner join user using (UID) 
                    where AID = %s''', [AID])
    return sorted(curs.fetchall(), key=lambda u: (u['count'], u['footprint']))

def addStarAchiev(conn, userID, aid):
    ''' Inserts into the starred table this user's favorites achievement'''
    curs = dbi.dictCursor(conn)
    curs.execute('''insert into 
                    starred (UID, AID) 
                    values(%s, %s)''', [userID, aid])

def removeStarAchiev(conn, userID, aid):
    ''' Deletes the pair of (UID , AID ) from the starred table'''
    curs = dbi.dictCursor(conn)
    curs.execute('''delete from 
                    starred 
                    where UID=%s and AID=%s''', [userID, aid])


# ==== ACCESS INFORMATION BASED ON USERS ====
# A-U-1
def getUserByUsername(conn, username):
    '''Returns user information, as a dictionary.
    '''
    curs = dbi.dictCursor(conn)
    curs.execute('''select UID, first_Name, last_Name, username
                    from user
                    where username=%s''', [username])
    return curs.fetchone()

# A-U-2
def getUserInfo(conn, UID):
    '''Returns user information, as a dictionary.
    '''
    curs = dbi.dictCursor(conn)
    curs.execute('''select first_Name, last_Name, username, footprint, photo
                    from user
                    where UID=%s''', [UID])
    return curs.fetchone()

# A-U-3
def getUsers(conn, searchTerm, sort="footprint"): 
    '''Returns the first name, last name, username,
    and footprint of all users that have a similar field
    to the search, as a list of dictionaries.

    sortTyp: 'asc' or 'desc'
    '''
    curs = dbi.dictCursor(conn)
    searchTerm = "%" + searchTerm + "%"
    curs.execute('''select first_Name, last_Name, footprint, username
                    from user
                    where first_Name like %s
                    or last_Name like %s
                    or username like %s''',
                    [searchTerm,searchTerm,searchTerm])
    return sorted(curs.fetchall(), key=lambda u: (u[sort], u['username']))

#TODO: (ALISSA) for above and below make them able to handle multiple sort options
    #ie: # of comp/star achis, count of specific comp achi, type? of most comp achis
    #these are statistics woo
        #type like electric car falls under transportation, no meat falls under foot etc
        #could be used for pie graphs... (low priority)

# A-U-4
def getAllUsers(conn, sort="footprint"):
    '''Returns the first name, last name, username,
    and footprint of all users, as a list of dictionaries.

    sortTyp: 'asc' or 'desc'
    '''
    curs = dbi.dictCursor(conn)
    curs.execute('''select first_Name, last_Name, footprint, username
                    from user''')

    return sorted(curs.fetchall(), key=lambda u: u[sort])

# A-U-5
def getCompAchieves(conn, UID):
    '''Returns the AID, title, description, and count of this user's
    completed achievements, as a list of dictionaries.
    '''
    curs = dbi.dictCursor(conn)
    #also need to do join for count here
    curs.execute('''select completed.AID,title,description,count,isRepeatable
                    from completed
                    join achievement
                    on achievement.AID=completed.AID
                    where UID=%s''', [UID])
    return curs.fetchall()

# A-U-6
def getStarAchieves(conn, UID):
    '''Returns the AID, title, and description of this user's
    starred achievements, as a list of dictionaries.
    '''
    curs = dbi.dictCursor(conn)
    curs.execute('''select starred.AID,title,description
                    from starred
                    join achievement
                    on achievement.AID=starred.AID
                    where UID=%s''', [UID])
    return curs.fetchall()

# A-U-7
def doesUserHaveCarbonData(conn, UID):
    '''returns the value of has_carbon_data for a given user.
    tells us whether they've filled out the carbon data form at least once'''
    curs = dbi.dictCursor(conn)
    curs.execute(''' select has_carbon_data from user where UID=%s''', [UID])
    result = curs.fetchone()
    return result['has_carbon_data']

# A-U-8
def getUserFootprint(conn, UID):
    '''given a user's UID, gets their current footprint data
    when we don't need to recalculate it'''
    curs = dbi.dictCursor(conn)
    curs.execute('''select uid, footprint from user where uid=%s''', [UID])
    return curs.fetchone()['footprint']

# A-U-9
def getUIDOnLogin(conn, username):
    #returns the user ID of the user with this username and password, or
    #return -1 if it's an invalid username/password combo
    curs = dbi.dictCursor(conn)
    curs.execute('''select UID,password from user 
                    where username = %s ''',
                    [username])
    res = curs.fetchone()
    if res:
        return res
    else:
        return -1

# A-U-11
def checkCorrectUser(conn,username,UID):
    '''Goes into the database to check if this username matches
    the userID's username of the person who is logged in.
    '''
    curs = dbi.dictCursor(conn)
    curs.execute('''select username from user where uid=%s''',[UID])
    currUsername = curs.fetchone()['username']
    # TODO: Can usernames be uppercased at all?

    return ((username == currUsername), currUsername)

# ==== ACCESS INFORMATION BASED ON USERS AND ACHIEVEMENTS ====
# A-B-1
def userAchieveExists(conn, UID, AID, tble="completed"):
    curs = dbi.dictCursor(conn)
    if tble == "completed":
        curs.execute('''select exists 
                            (select uid,aid from completed 
                                    where uid=%s and aid=%s) as exist''',
                     [UID,AID])

    elif tble == "starred":
        curs.execute('''select exists 
                            (select uid,aid from starred 
                                    where uid=%s and aid=%s) as exist''',
                     [UID,AID])
    
    else:
        errorStmt = "ERROR: table " + tble + " not recognized."
        print("*** " + errorStmt + " ***")
        return errorStmt
    
    return (curs.fetchone()['exist'] == 1)

# A-B-2
def getUserForAchievement(conn, UID, AID):
    '''Returns the first_Name, last_Name, username, and count
    for the specified user who has completed this achievement'''
    curs = dbi.dictCursor(conn)
    curs.execute('''select UID, first_Name, last_Name, username, count 
                    from completed inner join user using (UID)
                    where UID=%s and AID = %s''', [UID, AID])
    res = curs.fetchone()
    hasCount = True

    # means the user hasn't completed this achievement
    if res==None:
        res = getUser(conn, UID)
        hasCount = False

    return (res, hasCount)

# A-B-3
def getUserCompletedAchiev(conn, uid, aid):
    '''Returns UID, AID, count, timestamp from completed if the specified user has 
    completed the specified achievement'''
    curs = dbi.dictCursor(conn)
    curs.execute('''select * from completed where 
                    UID=%s and AID=%s''', [uid, aid])
    return curs.fetchone()

# ==== MODIFY DATABASE BASED ON USERS ====
# M-U-1
def updateUserInfo(conn, UID, flights, driving, lamb, beef, \
                    cheese, pork, turkey, chicken, laundry):
    '''Updates the carbon footprint info for a given user 
    (works for users who have no previously entered info 
    and for users who are changing old info). 
    Does not return anything.'''
    curs = dbi.dictCursor(conn)

    curs.execute('''delete from carbon where UID=%s''', [UID])

    curs.execute('''insert into carbon(uid,
                                       miles_flown, 
                                       miles_driven,
                                       servings_lamb,
                                       servings_beef,
                                       servings_cheese,
                                       servings_pork,
                                       servings_turkey,
                                       servings_chicken,
                                       laundry)
                    values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', 
                    [UID, flights, driving, lamb, beef, cheese, \
                        pork, turkey, chicken, laundry])
    
    curs.execute('''update user
                            set has_carbon_data=%s
                    where UID=%s''', [True, UID])

# M-U-2
def calculateUserFootprint(conn, UID):
    '''given a user's UID, get their info from the database and uses the
    carbon footprint calculator (calculator.py) to calculate and return 
    a total footprint'''
    #TODO: this works but the numbers seem to be slightly off. look into this more
    userData = getCarbonData(conn, UID)
    if debug:
        print('++ (databaseAccess.py) userData: ' + str(userData))
    total = calculator.plane_emissions(userData['miles_flown']) \
            + calculator.car_emissions(userData['miles_driven']) \
            + calculator.meat_emissions(userData['servings_lamb'], \
            userData['servings_beef'], userData['servings_cheese'], \
            userData['servings_pork'], userData['servings_turkey'], \
            userData['servings_chicken']) \
            + calculator.washer_emissions(userData['laundry']) \
            + calculator.dryer_emissions(userData['laundry'])
    
    curs = dbi.dictCursor(conn)
    #update footprint in user table
    curs.execute('''update user set footprint = %s 
                    where UID = %s''',
                [total, UID])
    
    return total

# M-U-3
def getCarbonData(conn, UID):
    '''given a UID, get the carbon data for that user'''
    curs = dbi.dictCursor(conn)
    curs.execute(''' select 
                        miles_flown,
                        miles_driven,
                        servings_lamb,
                        servings_beef,
                        servings_cheese,
                        servings_pork,
                        servings_turkey,
                        servings_chicken,
                        laundry
                    from carbon where UID = %s
                ''', [UID])
    return curs.fetchone()

# M-U-4
def setUIDOnSignup(conn, username, hashed_password, firstName, lastName):
    #puts the username, hashed password, salt, in the database
    #returns the uid the database created for this user
    #TODO: add in checking to make sure usernames are unique!! the logic here relies on this so it HAS to get done!
    curs = dbi.dictCursor(conn)
    #default for has_carbon_data is false so don't need to specify
    curs.execute('''insert into user (username, password, first_Name, last_Name) 
                    values (%s, %s, %s, %s)''',
                    [username, hashed_password, firstName, lastName])
    curs.execute('''select UID from user 
                    where username = %s 
                    and password = %s''', 
                    [username, hashed_password])
    return curs.fetchone()

# M-U-5
def updatePhoto(conn, UID, fileName):
    '''update the user's profile photo. returns true if filename! was changed
    useful for first photo change'''
    curs = dbi.dictCursor(conn)
    
    #will always be an update since we have to have the user before
    #they can change their user profile photo
    curs.execute('''update user set photo=%s where uid=%s''', [fileName,UID])
    curs.execute('''select ROW_COUNT()''')

    return (curs.fetchone()['ROW_COUNT()'] == 1)

# M-U-6
def deleteUser(conn, UID):
    '''deletes a user's information everywhere'''
    curs = dbi.dictCursor(conn)
    
    #delete the photo if it isn't earth.jpg
    curs.execute('''select photo from user where UID=%s''', [UID])
    f = curs.fetchone()['photo']
    if f != "earth.jpg":
        f = os.path.join('static/pictures/', f)
        os.remove(f)

    #remove from databases
    curs.execute('''delete from completed where UID=%s''', [UID])
    curs.execute('''delete from starred where UID=%s''', [UID])
    curs.execute('''delete from carbon where UID=%s''', [UID])
    curs.execute('''delete from user where UID=%s''', [UID])

# ==== MODIFY DATABASE BASED ON USERS AND ACHIEVEMENTS ====
# M-B-1
def insertCompleted(conn, uid, aid):
    '''inserts into the completed table 
    '''
    curs = dbi.dictCursor(conn)
    curs.execute('''insert into completed(UID, AID) values(%s,%s)''',
                    [uid, aid])
    return curs.fetchone()

# M-B-2
def deleteCompletedAchiev(conn, uid, aid):
    ''' deletes the entry in the completed table who's primary key is (uid, aid)
        essentially used to reset'''
    curs = dbi.dictCursor(conn)
    curs.execute('''delete from completed
                    where UID = %s and AID = %s''', [uid, aid])

# M-B-3
def updateCompletedCount(conn, UID, AID, count):
    ''' updates the count of the specific person and achievement to be count'''
    curs = dbi.dictCursor(conn)
    curs.execute('''update completed set count = %s 
                    where UID = %s and AID = %s ''', 
                        [count, UID, AID])

def getFunFact(conn, id):
    '''Given an id (which the route is in charge of randomly generating)
    return the associated fun fact & its source from our fun facts table'''
    curs = dbi.dictCursor(conn)
    curs.execute('''select fact_description,source from fact where id=%s''', [id])
    return curs.fetchone()

# ==========================================================
# This starts the ball rolling, *if* the file is run as a
# script, rather than just being imported.    

if __name__ == '__main__':
    print("*** WARNING: Should not run databaseAccess.py from the command line. ***")
        
