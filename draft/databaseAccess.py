from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify
                   )
import dbi
currDB = 'atinney_db'
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
    curs.execute('''select UID,first_Name,last_Name,footprint,
                    flights,driving,meat,laundry from user
                    where UID=%s''', [UID])
    return curs.fetchone()



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
        
