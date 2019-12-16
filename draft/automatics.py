from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify
                   )
import dbi
import databaseAccess as dba
import sys,math
import functools as fts
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
    
    updateAchiLeads(conn)

def updateAchiLeads(conn): #AID is an int
    '''Adds or removes a particular achievement count
    related achievement. There are six that we care about.
    [20,21,22,23,24,25]
    '''
    curs = dbi.dictCursor(conn)

    #all users
    curs.execute('''select uid from user''')
    allUsers = curs.fetchall()
    
    #count repeatable achis
    curs.execute('''select count(*) from achievement where isRepeatable=1''')
    totalRepCount = curs.fetchone()['count(*)']

    for u in allUsers:
        UID = u['uid']

        # the number of achievements that user has completed
        curs.execute('''select count(*) from completed where uid=%s''', [UID])
        achiCount = curs.fetchone()['count(*)']

        #{AID: minCount}
        toCheck = [{'AID': 20, 'minCount': 5}, #I've Been Around
                   {'AID': 21, 'minCount': 10}, #I'll Be Here All Night
                   {'AID': 22, 'minCount': 15}] #I'm Here To Stay

        for p in toCheck:
            checkCounts(conn, UID, p['AID'], achiCount, p['minCount'])
            #(conn, UID, AID, totalCount, count)
        
        # the number of repeatable achievements that user has completed
        curs.execute('''select count(*) from completed 
                        join achievement on achievement.AID=completed.AID 
                        where UID=%s and isRepeatable=1''', [u['uid']])
        usrRepCount = curs.fetchone()['count(*)']

        #I'll Be Here Forever & I'm Here Longer Than Forever
        checkMaximums(conn, UID, usrRepCount, totalRepCount)
        
        checkHighPower(conn, UID) #Super Powered!

def checkCounts(conn, UID, AID, totalCount, count):
    if totalCount >= count:
        if not dba.userAchieveExists(conn, UID, AID):
            dba.insertCompleted(conn, UID, AID)
    else:
        dba.deleteCompletedAchiev(conn, UID, AID)

def checkMaximums(conn, UID, usrRepCount, totalRepCount):
    if usrRepCount==totalRepCount: #I'm Here Forever
        dba.insertCompleted(conn, UID, 23)

        curs.execute('''select count,aid from completed 
                    join achievement on achievement.AID=completed.AID 
                    where UID=%s and isRepeatable=1''', [UID])
        reps = curs.fetchall()

        #I'm Here Longer Than Forever
        isLargeCounts = list(map(lambda x: x['count']>=2, reps))
        doubleOnReps = fts.reduce(lambda x,y: (x and y), isLargeCounts)
        if doubleOnReps:
            dba.insertCompleted(conn, UID, 24)
        else:
            dba.deleteCompletedAchiev(conn, UID, 24)
    else:
        dba.deleteCompletedAchiev(conn, UID, 23)

def checkHighPower(conn, UID):
    '''Adds or removes achievement 25.
    '''
    curs = dbi.dictCursor(conn)
    curs.execute('''select count(*) from completed
                    where uid=%s and (aid=9 or aid=10 or aid=11)''',
                [UID])
    total = curs.fetchone()['count(*)']

    if (total==3):
        dba.insertCompleted(conn, UID, 25)
    else:
        #make sure to remove if it is there
        #eg: they added and then removed
        dba.deleteCompletedAchiev(conn, UID, 25)
        
    return (total==3)

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
    
    if AID==12: #Leader!
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
    #TODO: how will we do deletions? will we store any data after?

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