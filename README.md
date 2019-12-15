# fueling-change
CS304 final project

To set up the files for testing:
1. In bash, run the command: **./testingSetup.sh atinney_db**
2. However, replace **atinney_db** with your own database.
3. The script will prompt for the number of users:
    * If given 0 users, it will simply set up the achievements in makeAchieves.sql
    * If given 1 user, it will set up achievements in makeAchieves.sql and give the user the "Joined Fueling Change!" achievement.
    * If given 2 or more users, it will set up achievements in makeAchieves.sql, add selected achievements to user1 and user2, and give all users the "Joined Fueling Change!" achievement.