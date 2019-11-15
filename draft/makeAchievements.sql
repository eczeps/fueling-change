-- Some starter achievements.
-- Run this on your db if you want to test webpages and such

use atinney_db;

-- Creating a user
insert into user(first_Name,last_Name,footprint,username,password,flights,driving,meat,laundry)
values ('alissa','tinney',4000.0,'atinney','abc',5,3,20,30);

-- Creating achievements
insert into achievement(title,description,isRepeatable,isSelfReport)
values ('No Meat for a Week','Do not eat meat for seven days.',1,1); -- 1 is true, 0 is false

insert into achievement(title,description,isSelfReport)
values ('Electric Car 1','Drive an electric car.',1); -- 0 is default

insert into achievement(title,description,isSelfReport)
values ('Electric Car 2','Buy an electric car.',1);

insert into achievement(title,description)
values ('Top 10','Claim a spot in the top 10 percent of users.');

insert into achievement(title,description)
values ('Top 50','Claim a spot in the top 50 percent of users.');

-- Inserting into completed
insert into completed(UID,AID)
values(1,1);

insert into completed(UID,AID)
values(1,2);

-- Inserting into starred
insert into starred(UID,AID)
values(1,3);

insert into starred(UID,AID)
values(1,4);

insert into starred(UID,AID)
values(1,5);

-- Showing results
select * from user;
select * from achievement;
select * from completed;
select * from starred;