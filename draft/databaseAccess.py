from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify
                   )
import dbi
currDB = 'eczepiel_db'
# change this when you want to work on your account
# we have to figure out later how to make a db that we all have access to

# ==========================================================
# The functions that do most of the work.

def getConn(db):
    '''Returns a database connection for that db'''
    dsn = dbi.read_cnf()
    conn = dbi.connect(dsn)
    conn.select_db(db)
    return conn

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
                    or description is like %s
                    or isRepeatable is like %s
                    or isSelfReport is like %s''',
                    [searchFor, searchFor, searchFor, searchFor])
    return curs.fetchall()

def getAllAchievements(conn):
    '''Returns the AID, title, description, isRepeatable, isSelfReport 
    of all achievements, as a list of dictionaries.
    '''
    curs = dbi.dictCursor(conn)
    curs.execute('''select AID, title, description, isRepeatable, isSelfReport
                    from achievement''')
    return curs.fetchall()

def getCompAchievements(conn, UID):
    '''Returns the AID, title, description, and count of this user's
    completed achievements, as a list of dictionaries.
    '''
    curs = dbi.dictCursor(conn)
    #also need to do join for count here
    curs.execute('''select AID
                    from completed
                    where UID=%s''', [UID])
    return curs.fetchall()
#for the one above and below need to do a join to get title
#and description but not in the mood to do that rn
def getStarAchievements(conn, UID):
    '''Returns the AID, title, and description of this user's
    starred achievements, as a list of dictionaries.
    '''
    curs = dbi.dictCursor(conn)
    curs.execute('''select AID
                    from starred
                    where UID=%s''', [UID])
    return curs.fetchall()

def getIsRepeatable(conn, AID):
    '''Returns whether or not this achievement is eligible
    for repetition. This is a Boolean return.
    '''
    curs = dbi.dictCursor(conn)
    curs.execute('''select isRepeatable from achievement where AID=%s''' [AID])
    
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
    curs.execute('''select isSelfReport from achievement where AID=%s''' [AID])
    
    #not checking for null cause if that happens it was our fault
    res = curs.fetchone()

    if res == 1: #in our world, 0 is false and 1 is true
        return True
    else:
        return False

def determineIsReportable(DB, AID, UID):
    '''Returns whether or not this achievement is reportable for
    the given user. This is a Boolean return.
    '''
    conn = getConn(DB)
    curs = dbi.dictCursor(conn)
    curs.execute('''select isSelfReport from completed
                    where UID=%s
                    and AID=%s''' [UID, AID])
    
    allOccurances = curs.fetchall()
    alreadyReported = allOccurances[len(allOccurances)-1]
    repeat = getIsRepeatable(conn, AID)
    report = getIsSelfReport(conn, AID)

    return (alreadyReported and repeat and report)

def getUser(conn, UID):
    '''Returns user information, as a dictionary.
    '''
    curs = dbi.dictCursor(conn)
    curs.execute('''select * from user
                    where UID=%s''', [UID])
    return curs.fetchone()

def updateUserInfo(conn, UID, flights, driving, lamb, beef, cheese, pork, turkey, chicken, laundry):
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
                            laundry=%s
                    where UID=%s''', [UID, flights, driving, lamb, beef, cheese, pork, turkey, chicken, laundry])



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
        
