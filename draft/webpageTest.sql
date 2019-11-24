-- Creating a user
insert into user(first_Name,last_Name,footprint,username,password,
                miles_flown,miles_driven,servings_lamb,servings_beef,
                servings_cheese,servings_pork,servings_chicken,
                servings_turkey,laundry)
values ('alissa','tinney',4000.0,'atinney','abc',5,3,20,30,2,4,50,30,5);

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
-- select * from user;
-- select * from achievement;
-- select * from completed;
-- select * from starred;