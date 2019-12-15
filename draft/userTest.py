import dbi, databaseAccess
import sys
from random import randint

'''Sets up automatic users that cannot be logged into.
'''

if __name__ == '__main__':
    conn = databaseAccess.getConn(sys.argv[1])
    
    curs = dbi.dictCursor(conn)

    howMany = int(sys.argv[2]) + 1

    for i in range(1,howMany):
        uName = "user" + str(randint(0,1000))
        footP = i * 206 #this is about 1000 when the only thing there is for driving
        print("footP:", footP)
        pWord="$2b$12$x7Gi0W4r4UkBAJvpWyX65eOWsvMbgTITesVT9e.QfjS33Q7iJonfS"

        curs.execute('''insert into user(first_Name,last_Name,username,password)
                        values('Jane','Doe',%s,%s)''',
                        [uName,pWord])
        
        databaseAccess.updateUserInfo(conn,i,0,footP,0,0,0,0,0,0,0)
        databaseAccess.calculateUserFootprint(conn,i)
        
        curs.execute('''insert into completed(UID,AID)
                        values(%s,1)''', [i])
    

    

    