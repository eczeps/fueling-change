from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify
                   )
import dbi
import databaseAccess as dba
import sys,math
# the database to use:
currDB = dba.d
debug = dba.debug
debugLong = dba.debugLong

# ==========================================================
# The functions that do most of the work for automatic achiements.

def updateAutomaticAchieves(conn):
    '''Adds or removes the user's automatic achievements as we see fit.
    '''
    leadershipCheck=[12,13,14,15]
    for i in leadershipCheck:
        updateLeaders(conn, i)


def updateLeaders(conn, AID): #AID is an int
    '''Adds or removes a particular leader related achievement.
    Right now there are only four that we care about
    (two are dependent on another two)
    '''
    curs = dbi.dictCursor(conn)

    #WHY? Python doesn't have regular switch statements
    #gotta use a dictionary or if/elif/else which is so gross :c

    calc = ""
    dependentUpdate = None
    
    if AID==12:
        dependentUpdate = 16 #for Once Upon A Time: Leader!
    elif AID==13: #Top 10
        calc = 10.0
        dependentUpdate = 17 #for Once Upon A Time: Top 10
    elif AID==14: #Top 25
        calc = 4.0
        dependentUpdate = 18 #for Once Upon A Time: Top 25
    elif AID==15: #Top 50
        calc = 2.0
        dependentUpdate = 19 #for Once Upon A Time: Top 50
    else:
        print("*** ERROR: AID " + str(AID) + " not recognized ***")
        exit #the function i think but it shouldn't happen!

    #possibly new current leaders
    if AID!=12:
        curs.execute('''select uid 
                        from user 
                        where footprint <= (select max(footprint)/%s from user)''',
                    [calc])
    else:
        curs.execute('''select uid 
                        from user 
                        where footprint = (select min(footprint) from user)''')
    currLead = curs.fetchall()
    if debug:
        print("++ (automatics.py) currentlyLeading:", currLead)

    #already current leaders
    curs.execute('''select uid from completed where aid=%s''', [AID])
    currLeadAlready = curs.fetchall()

    #all users
    curs.execute('''select footprint,uid,username from user order by footprint asc''')
    allUsers = curs.fetchall()
    #TODO: how will we do deletions? will we store any data?

    if debug:
        print("++ (automatics.py) allUsers:", allUsers)
    
    for u in allUsers:
        if debugLong:
            print('======')
            print("++++ (automatics.py) username:", u['username'])

        #get counting
        curs.execute('''select count from completed where uid=%s and aid=%s''',
                     [u['uid'], dependentUpdate])
        existingCount = curs.fetchone()

        #for the first time the user is added to this achievement
        safeExistingCount = 0
        if (existingCount != None):
            safeExistingCount = existingCount['count']

        if debugLong:
            print("++++ (automatics.py) existingCount:", existingCount)

        isALeaderAlready = len(list(filter(lambda user: user['uid'] == u['uid'], currLeadAlready))) != 0
        isALeaderNow = len(list(filter(lambda user: user['uid'] == u['uid'], currLead))) != 0

        if debugLong:
            print('++++ (automatics.py) isALeaderAlready:', isALeaderAlready)
            print('++++ (automatics.py) isALeaderNow:', isALeaderNow)

        #check if the user was leading and no longer leading
        if (isALeaderAlready and not isALeaderNow):
            updatedCount = safeExistingCount + 1

            if debugLong:
                print("++++ (automatics.py) safe:", (safeExistingCount != 0))

            if safeExistingCount != 0:
                dba.updateCompletedCount(conn, u['uid'], dependentUpdate, updatedCount)
            else:
                dba.insertCompleted(conn, u['uid'], dependentUpdate)

            dba.deleteCompletedAchiev(conn, u['uid'], AID)
                #elif next so this deletion is fine
        
        #check if the user is currently leading but wasn't before
        elif (isALeaderNow and not isALeaderAlready):
            dba.insertCompleted(conn, u['uid'], AID)
        
        else:
            if debugLong:
                print("++++ (automatics.py) no change to achievement " + str(AID) + " for " + u['username'])