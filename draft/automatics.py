from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify
                   )
import dbi
import databaseAccess as dba
import sys,math
# the database to use:
currDB = dba.d

# ==========================================================
# The functions that do most of the work for automatic achiements.

def updateAutomaticAchieves(conn):
    '''Adds or removes the user's automatic achievements as we see fit.
    '''
    leadershipCheck=[12,13]
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
    
    if AID==12: #Top 10
        calc = 10.0
        dependentUpdate = 14 #for Once Upon A Time: Top 10
    elif AID==13: #Top 50
        calc = 2.0
        dependentUpdate = 15 #for Once Upon A Time: Top 50
    else:
        print("*** ERROR: AID " + str(AID) + " not recognized ***")
        exit #the function i think but it shouldn't happen!

    #possibly new current leaders
    curs.execute('''select uid 
                    from user 
                    where footprint <= (select max(footprint)/%s from user)''',
                 [calc])
    currLead = curs.fetchall()
    print("++ currentlyLeading:", currLead)

    #already current leaders
    curs.execute('''select uid from completed where aid=%s''', [AID])
    currLeadAlready = curs.fetchall()

    #all users
    curs.execute('''select uid,footprint from user''')
    allUsers = curs.fetchall()
    #TODO: how will we do deletions? will we store any data?
    
    for u in allUsers:
        #get counting
        curs.execute('''select count from completed where uid=%s and aid=%s''',
                     [u['uid'], dependentUpdate])
        existingCount = curs.fetchone()

        #for the first time the user is added to this achievement
        safeExistingCount = 0
        safe = False
        if (existingCount != None):
            safeExistingCount = existingCount['count']
            safe = True

        print("++ existingCount:", existingCount)

        isALeaderAlready = len(list(filter(lambda user: user['uid'] == u['uid'], currLeadAlready))) != 0
        isALeaderNow = len(list(filter(lambda user: user['uid'] == u['uid'], currLead))) != 0

        print('isALeaderAlready:', isALeaderAlready)
        print('isALeaderNow:', isALeaderNow)
        #check if the user was leading and no longer leading
        if (isALeaderAlready and not isALeaderNow):
            updatedCount = safeExistingCount + 1

            print("safe:", safe)
            if safe:
                dba.updateCompletedCount(conn, u['uid'], dependentUpdate, updatedCount)
            else:
                dba.insertCompleted(conn, u['uid'], dependentUpdate)

            dba.deleteCompletedAchiev(conn, u['uid'], AID)
                #elif next so this deletion is fine
        
        #check if the user is currently leading but wasn't before
        elif (isALeaderNow and not isALeaderAlready):
            dba.insertCompleted(conn, u['uid'], AID)
        
        else:
            print("++ no change to achievement " + str(AID) + " for user" + str(u['uid']))