-- Creating achievements
insert into achievement(title,description)
values ('Joined Fueling Change!','Started their journey to lower carbon footprint');

insert into achievement(title,description,isRepeatable,isSelfReport)
values ('No Meat for a Week','Do not eat meat for seven days.',1,1); -- 1 is true, 0 is false

insert into achievement(title,description,isRepeatable,isSelfReport)
values ('Carpooled','Carpooled to Work/School.',1,1);

insert into achievement(title,description,isRepeatable,isSelfReport)
values ('Vegan','Became Vegan!',1,1);

insert into achievement(title,description,isRepeatable,isSelfReport)
values ('Vegetarian','Became Vegetarian',1,1);

insert into achievement(title,description,isRepeatable,isSelfReport)
values ('Earthly Drying','Line-Dried Clothing',1,1);

insert into achievement(title,description,isRepeatable,isSelfReport)
values ('+1 Tree','Planted A Tree',1,1);

insert into achievement(title,description,isSelfReport)
values ('Electric Car 1','Drive an electric car.',1); -- 0 is default

insert into achievement(title,description,isSelfReport)
values ('Electric Car 2','Buy an electric car.',1);

insert into achievement(title,description)
values ('Top 10','Claim a spot in the top 10 percent of users.');

insert into achievement(title,description)
values ('Top 50','Claim a spot in the top 50 percent of users.');

