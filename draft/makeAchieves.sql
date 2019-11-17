use egarcia2_db;

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

