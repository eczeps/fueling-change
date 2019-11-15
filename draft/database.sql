-- this file sets up the 'database' for the 'Fueling-Change App'
-- The database consists of tables: 

use atinney_db; -- change this when you are working please

drop table if exists userform;
drop table if exists completed;
drop table if exists starred;
drop table if exists user;
drop table if exists achievement;

Create table user(
	UID int auto_increment,
	first_Name varchar(30),
	last_Name varchar(30),
	footprint float,
	username varchar(30),
	password varchar(30),
	-- had to condense user and userform since can't have
	-- userform use UID as a primary key
	flights int,
	driving int,
	meat int,
	laundry int,
	Primary key (UID)
);

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

create table completed(
    UID int,
    AID int,
	Primary Key (UID, AID), --(UID, AID) won't always be unique: repeatable
	timestamp datetime,
	foreign key (UID) references user(UID)
        on update cascade
        on delete cascade
);

create table starred(
    UID int,
    AID int,
	Primary Key (UID, AID),
	foreign key (UID) references user(UID)
        on update cascade
        on delete cascade
);
