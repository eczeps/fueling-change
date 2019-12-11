from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify
                   )
import dbi
import calculator as calculator
import sys,math
# the database to use:
d = "egarcia2_db"
# script testingSetup.sh replaces this like so:
# $ ./testingSetup.sh atinney_db

# ==========================================================
# The functions that do most of the work.

def getConn(db):
    '''Returns a database connection for that db'''
    # dsn = dbi.read_cnf('../../.my.team_cnf') # for group db
    dsn = dbi.read_cnf() #for own db
    conn = dbi.connect(dsn)
    conn.select_db(db)
    return conn

def getAchieveInfo(conn, AID):
    '''Returns the title, description, isRepeatable, isSelfReport of given AID'''
    curs = dbi.dictCursor(conn)
    curs.execute('''select title, description, isRepeatable, isSelfReport
                    from achievement
                    where AID = %s''', [AID])
    return curs.fetchone()

def getAchievePeople(conn, AID):
    '''Returns the UID, first_Name, last_Name, username, and count
    for people who have completed this achievement'''
    curs = dbi.dictCursor(conn)
    curs.execute('''select UID, first_Name, last_Name, username, count 
                    from completed inner join user using (UID) 
                    where AID = %s''', [AID])
    return curs.fetchall()

def getUsers(conn, searchTerm):
    '''Returns the UID, first name, last name, and username
    of all users that have a similar field to the search,
    as a list of dictionaries.
    '''
    curs = dbi.dictCursor(conn)
    searchTerm = "%" + searchTerm + "%"
    curs.execute('''select UID, first_Name, last_Name, username
                    from user
                    where first_Name like %s
                    or last_Name like %s
                    or username like %s''',
                    [searchTerm,searchTerm,searchTerm])
    return curs.fetchall()

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

def getAllAchievements(conn):
    '''Returns the AID, title, description, isRepeatable, isSelfReport 
    of all achievements, as a list of dictionaries.
    '''
    curs = dbi.dictCursor(conn)
    curs.execute('''select AID, title, description, isRepeatable, isSelfReport
                    from achievement''')
    return curs.fetchall()

def insertCompleted(conn, uid, aid):
    '''inserts into the completed table 
    '''
    curs = dbi.dictCursor(conn)
    #still buggy

    #returns 1 if row exists
    # rowExists=curs.execute('''select exists(select * 
    #                                 from completed 
    #                                 where UID=%s and AID=%s)''',
    #                           [uid, aid])
    # isRepeatable = getIsRepeatable(conn, aid)
    # isSelfReport = getIsSelfReport(conn, aid)

    # if rowExists==1:
    #     if isRepeatable:
    #         print("if statement")
    #         currCount = curs.execute('''select count 
    #                                 from completed 
    #                                 where UID=%s and AID=%s)''',
    #                              [uid, aid])
    #         updatedCount = currCount + 1

    #         curs.execute('''update completed set count=%s where UID=%s and AID=%s''',
    #                 [updatedCount, uid, aid])
    # else:
    #     print("else statement")
    curs.execute('''insert into completed(UID, AID) values(%s,%s)''',
                    [uid, aid])
    return curs.fetchone()

def getCompAchievements(conn, UID):
    '''Returns the AID, title, description, and count of this user's
    completed achievements, as a list of dictionaries.
    '''
    curs = dbi.dictCursor(conn)
    #also need to do join for count here
    curs.execute('''select completed.AID,title,description,count
                    from completed
                    join achievement
                    on achievement.AID=completed.AID
                    where UID=%s''', [UID])
    return curs.fetchall()

def getStarredAchieves(conn, UID):
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

def getIsRepeatable(conn, AID):
    '''Returns whether or not this achievement is eligible
    for repetition. This is a Boolean return.
    '''
    curs = dbi.dictCursor(conn)
    curs.execute('''select isRepeatable from achievement where AID=%s''', [AID])
    
    #not checking for null cause if that happens it was our fault
    res = curs.fetchone()

    if res == 1: #in our world, 0 is false and 1 is true
        return True
    else:
        return False

def getIsSelfReport(conn, AID):
    '''Returns whether or not this achievement is eligible
    for self report. This is a Boolean return.
    '''
    curs = dbi.dictCursor(conn)
    curs.execute('''select isSelfReport from achievement where AID=%s''', [AID])
    
    #not checking for null cause if that happens it was our fault
    res = curs.fetchone()

    if res == 1: #in our world, 0 is false and 1 is true
        return True
    else:
        return False


def getReportedAchieves(conn, UID):
    '''Returns a simple list of AIDs for all completed user achievements
    that says if the achievement is currently reportable by the user.
    '''
    curs = dbi.dictCursor(conn)
    curs.execute('''select AID from completed
                    where UID=%s''', [UID])

    return list(map(lambda x: x['AID'], curs.fetchall()))

def getUserByUsername(conn, username):
    '''Returns user information, as a dictionary.
    '''
    curs = dbi.dictCursor(conn)
    curs.execute('''select UID, first_Name, last_Name, username
                    from user
                    where username=%s''', [username])
    return curs.fetchone()

def getUser(conn, UID):
    '''Returns user information, as a dictionary.
    '''
    curs = dbi.dictCursor(conn)
    curs.execute('''select first_Name, last_Name, username
                    from user
                    where UID=%s''', [UID])
    return curs.fetchone()

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

def updateUserInfo(conn, UID, flights, driving, lamb, beef, \
                    cheese, pork, turkey, chicken, laundry):
    '''Updates the carbon footprint info for a given user 
    (works for users who have no previously entered info 
    and for users who are changing old info). 
    Does not return anything.'''
    curs = dbi.dictCursor(conn)
    curs.execute('''update user 
                            set miles_flown=%s, 
                            miles_driven=%s,
                            servings_lamb=%s,
                            servings_beef=%s,
                            servings_cheese=%s,
                            servings_pork=%s,
                            servings_turkey=%s,
                            servings_chicken=%s,
                            laundry=%s,
                            has_carbon_data=%s
                    where UID=%s''', [flights, driving, \
                    lamb, beef, cheese, pork, turkey, chicken, laundry, True, UID])


def doesUserHaveCarbonData(conn, UID):
    curs = dbi.dictCursor(conn)
    curs.execute(''' select has_carbon_data from user where UID=%s''', [UID])
    return curs.fetchone()['has_carbon_data']


def calculateUserFootprint(conn, UID):
    '''given a user's UID, get their info from the database and uses the
    carbon footprint calculator (calculator.py) to calculate and return 
    a total footprint'''
    #TODO: this works but the numbers seem to be slightly off. look into this more
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
                    from user where UID = %s
                ''', [UID])
    userData = curs.fetchone()
    print('userData in databaseaccess: ' + str(userData))
    total = calculator.plane_emissions(userData['miles_flown']) \
            + calculator.car_emissions(userData['miles_driven']) \
            + calculator.meat_emissions(userData['servings_lamb'], \
            userData['servings_beef'], userData['servings_cheese'], \
            userData['servings_pork'], userData['servings_turkey'], \
            userData['servings_chicken']) \
            + calculator.washer_emissions(userData['laundry']) \
            + calculator.dryer_emissions(userData['laundry'])
    return total


def getUIDOnLogin(conn, username):
    #returns the user ID of the user with this username and password, or
    #return -1 if it's an invalid username/password combo
    curs = dbi.dictCursor(conn)
    curs.execute('''select UID,password from user 
                    where username = %s ''',
                    [username])
    result = curs.fetchone()
    if result:
        return result
    else:
        return -1


def setUIDOnSignup(conn, username, hashed_password, firstName, lastName):
    #puts the username, hashed password, salt, in the database
    #returns the uid the database created for this user
    #TODO: add in checking to make sure usernames are unique!! the logic here relies on this so it HAS to get done!
    curs = dbi.dictCursor(conn)
    curs.execute('''insert into user (username, password, first_Name, last_Name, has_carbon_data) 
                    values (%s, %s, %s, %s, false)''',
                    [username, hashed_password, firstName, lastName])
    curs.execute('''select UID from user 
                    where username = %s 
                    and password = %s''', 
                    [username, hashed_password])
    return curs.fetchone()

#TODO: delete this once logins & signups are working
def getSaltByUsername(conn, username):
    #returns the salt associated with the given username
    #this is called when someone is logging in and we're checking their password
    curs = dbi.dictCursor(conn)
    curs.execute('''select salt from user where username = %s''', [username])
    return curs.fetchone()


def prettyRound(number):
    return math.floor(round(number,0))

# ==========================================================
# This starts the ball rolling, *if* the file is run as a
# script, rather than just being imported.    

if __name__ == '__main__':
    conn = getConn('wmdb')
    pl = getPeople(conn)
    for person in pl:
        print('{name} born on {date}'
              .format(name=person['name'],
                      date=person['birthdate']))
        
