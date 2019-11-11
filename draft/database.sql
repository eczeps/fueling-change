-- this file sets up the 'database' for the 'Fueling-Change App'
-- The database consists of tables: 

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
	Primary key (UID)
);

create table achievement(
	AID int auto_increment,
	title varchar(30),
	description varchar(50),
	isRepeatable int(1),
	isSelfReport int(1),
	Primary Key (AID)
);

create table userform(
	Primary key (UID),
	flights int,
	driving int,
	meat int,
	laundry int
	foreign key(UID) references user(UID)
        on update cascade
        on delete cascade
);

create table completed(
    UID int,
    AID int,
	Primary Key (UID, AID),
	timestamp datetime
	foreign key(UID) references user(UID)
        on update cascade
        on delete cascade
);

create table starred(
    UID int,
    AID int,
	Primary Key (UID, AID)
	foreign key(UID) references user(UID)
        on update cascade
        on delete cascade
);
