from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify
                   )
import dbi

# ==========================================================
# The functions that do most of the work.

def getConn(db):
    '''Returns a database connection for that db'''
    dsn = dbi.read_cnf()
    conn = dbi.connect(dsn)
    conn.select_db(db)
    return conn

def getMovies(conn, title):
    '''Returns the tt, title, name of director of all movies
    that have a similar title to the search, as a list of
    dictionaries.
    '''
    curs = dbi.dictCursor(conn)
    title = "%" + title + "%"
    curs.execute('''select tt, title, name, `release`
                    from movie
                    left outer join person
                    on (director=nm)
                    where title like %s''', [title])
    return curs.fetchall()

def getAllMovies(conn):
    '''Returns the tt, title, name of director of all movies,
    as a list of dictionaries.
    '''
    curs = dbi.dictCursor(conn)
    curs.execute('''select tt, title, name, `release`
                    from movie
                    left outer join person
                    on (director=nm)''')
    return curs.fetchall()




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
        
