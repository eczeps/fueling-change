#!/bin/bash
# Run this on your db if you want to test webpages and such

# Swaps the current database in databaseAccess.py:
# sed -i 's/d = ".*"/d = "'$1'"/' databaseAccess.py;

# WARNING: this deletes the databases and remakes them!
while true
do
    read -r -p 'This will reset all the databases. Continue? [yN] --> ' choice
    case "$choice" in
      n|N) echo "Operation aborted."; exit;;
      y|Y) sed -i 's/d = ".*"/d = "'$1'"/' databaseAccess.py; mysql < database.sql $1; echo "Successfully reset database!"; break;;
      *) echo "Operation aborted."; exit;;
    esac
done


#add automatic, unloginable users with incrementing footprints
while true
do
    read -r -p 'Please give a number for automatic users. --> ' choice
    if [[ "$choice" =~ ^0+ ]]
    then
      python testUsers.py $1 $(($choice))
      mysql < makeAchieves.sql $1
      echo "No users inserted."
      exit
    elif [[ "$choice" =~ ^1$ ]]
    then
      python testUsers.py $1 $(($choice))
      mysql < makeAchieves.sql $1
      echo "Successfully created $choice users!"
      exit
    elif [[ "$choice" =~ ^[1-9]+[0-9]+$ ]]
    then
      python testUsers.py $1 $(($choice))
      mysql < makeAchieves.sql $1
      mysql < webpageTest.sql $1
      echo "Successfully created $choice users!"
      echo "Selected achievements have been added to user1 and user2."
      exit
    else
      mysql < makeAchieves.sql $1
      echo "You did not give an integer."
      echo "No users inserted."
      exit
    fi
done




if ! [[ "$yournumber" =~ ^[0-9]+$ ]] ; 
 then exec >&2; echo "error: Not a number"; exit 1
fi