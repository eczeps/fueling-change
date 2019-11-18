-- Run this on your db if you want to test webpages and such

use egarcia2_db;

-- Creating a user
insert into user(first_Name,last_Name,footprint,username,password,flights,driving,meat,laundry)
values ('alissa','tinney',4000.0,'atinney','abc',5,3,20,30);

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