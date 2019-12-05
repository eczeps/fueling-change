-- this file sets up the 'database' for the 'Fueling-Change App'
-- The database consists of tables: 
drop table if exists completed;
drop table if exists starred;
drop table if exists user;
drop table if exists achievement;

/* User table will hold all of the user's information
Used to calculate the user's carbon footprint, as well as personal info */
Create table user(
	UID int auto_increment,
	first_Name varchar(30),
	last_Name varchar(30),
	footprint float,
	username varchar(30),
	password varchar(30),
	-- had to condense user and userform since can't have
	-- userform use UID as a primary key
	miles_flown int,
	miles_driven int,
	servings_lamb int,
	servings_beef int,
	servings_cheese int,
	servings_pork int,
	servings_turkey int,
	servings_chicken int,
	laundry int,
	Primary key (UID)
);

<<<<<<< HEAD
-- achievement table stores info about all possible achievements a user can earn 
=======
/* achievement table stores information
about all possible achievements a user can earn */
>>>>>>> 062098ea773d1833917b2df6cb1e97b25ba8d4d2
create table achievement(
	AID int auto_increment,
	title varchar(30),
	description varchar(50),
	isRepeatable boolean not null default 0,
	isSelfReport boolean not null default 0,
	-- boolean in mysql is tinyint(1)
	-- 0 is false
	Primary Key (AID)
);

<<<<<<< HEAD
/* completed table will hold userIDs and achievement IDs as key value pairs to 
indicate which users have completed what; the counter indicates how many 
times a user has completed the achievement */
=======
/* achievement table will hold userIDs and achievement IDs as key value
pairs to indicate which users have completed what. the counter indicates
how many time a user has completed the achievement */
>>>>>>> 062098ea773d1833917b2df6cb1e97b25ba8d4d2
create table completed(
    UID int,
    AID int,
	Primary Key (UID, AID),
	count int not null default 0,
	ts timestamp DEFAULT CURRENT_TIMESTAMP
		on update CURRENT_TIMESTAMP,
	foreign key (UID) references user(UID)
        on update cascade
        on delete cascade
);
<<<<<<< HEAD
/* similar to the achievements table, the starred table uses userIDs
and achievementIDs as key value pairs to indicate
=======

/* similar to the completed table, the starred table userIDs
and achievement IDs as key value pairs to indicate which users
>>>>>>> 062098ea773d1833917b2df6cb1e97b25ba8d4d2
certain users have starred certain achievements */
create table starred(
    UID int,
    AID int,
	Primary Key (UID, AID),
	foreign key (UID) references user(UID)
        on update cascade
        on delete cascade
);
