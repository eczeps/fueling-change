#!/bin/bash
# Run this on your db if you want to test webpages and such

# Swaps the current database in databaseAccess.py:
# sed -i 's/d = ".*"/d = "'$1'"/' databaseAccess.py;

# WARNING: this deletes the databases and remakes them!
while true
do
    read -r -p 'This will reset all the databases. Continue? [yN] --> ' choice
    case "$choice" in
      n|N) echo "Operation aborted."; break;;
      y|Y) sed -i 's/d = ".*"/d = "'$1'"/' databaseAccess.py; mysql < database.sql $1; mysql < makeAchieves.sql $1; mysql < webpageTest.sql $1; echo "Success!"; break;;
      *) echo "Operation aborted."; break;;
    esac
done