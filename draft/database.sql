-- this file sets up the 'database' for the 'Fueling-Change App'
-- The database consists of tables: 
drop table if exists completed;
drop table if exists starred;
drop table if exists carbon;
drop table if exists user;
drop table if exists achievement;
drop table if exists fact;

/* User table will hold all of the user's information
Used to calculate the user's carbon footprint, as well as personal info */
Create table user(
	UID int auto_increment,
	first_Name varchar(30),
	last_Name varchar(30),
	username varchar(30),
	password char(60),
	footprint float,
	has_carbon_data boolean not null DEFAULT false,
	Primary key (UID)
);

/* Carbon table will hold all of the user's carbon data
Used to calculate the user's carbon footprint, as well as personal info */
Create table carbon(
	UID int,
	foreign key (UID) references user(UID)
        on update cascade
        on delete cascade,
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

/* achievement table stores information
about all possible achievements a user can earn */
create table achievement(
	AID int auto_increment,
	title varchar(30),
	description varchar(100),
	isRepeatable boolean not null default 0,
	isSelfReport boolean not null default 0,
	-- boolean in mysql is tinyint(1)
	-- 0 is false
	Primary Key (AID)
);

/* achievement table will hold userIDs and achievement IDs as key value
pairs to indicate which users have completed what. the counter indicates
how many time a user has completed the achievement */
create table completed(
    UID int,
    AID int,
	Primary Key (UID, AID),
	count int not null default 1,
	ts timestamp DEFAULT CURRENT_TIMESTAMP
		on update CURRENT_TIMESTAMP,
	foreign key (UID) references user(UID)
        on update cascade
        on delete cascade
);

/* similar to the completed table, the starred table userIDs
and achievement IDs as key value pairs to indicate which users
certain users have starred certain achievements */
create table starred(
    UID int,
    AID int,
	Primary Key (UID, AID),
	foreign key (UID) references user(UID)
        on update cascade
        on delete cascade
);

/* table to store our rotating fun facts that'll be randomly
displayed on the homepage */
create table fact(
	id int auto_increment,
	fact_description varchar(500),
	source varchar(140),
	primary key (id)
)