import dbi, databaseAccess
import sys

'''Sets up automatic users that cannot be logged into.
'''

if __name__ == '__main__':
    conn = databaseAccess.getConn(sys.argv[1])
    
    curs = dbi.dictCursor(conn)

    howMany = int(sys.argv[2]) + 1

    for i in range(1,howMany):
        uName = "user" + str(i)
        footP = i * 1000.0

        curs.execute('''insert into user(first_Name,last_Name,username,footprint)
                        values('Jane','Doe',%s,%s)''', [uName,footP])
        
        curs.execute('''insert into completed(UID,AID)
                        values(%s,1)''', [i])
    

    

    