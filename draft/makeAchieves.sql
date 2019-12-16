-- ONLY ADD ACHIEVEMENTS TO THE BOTTOM OF THIS FILE
-- ANYTHING ELSE WILL BREAK automatics.py

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
values ('Earthly Drying','Line-Dried the clothing',1,1);

insert into achievement(title,description,isRepeatable,isSelfReport)
values ('+1 Tree','Planted A Tree',1,1);

insert into achievement(title,description,isRepeatable,isSelfReport)
values ('Electric Cars Go VROOM!','Buy an electric car.',1,1);

insert into achievement(title,description,isSelfReport)
values ('Earth Powers','Upgraded to geothermal energy.',1);

insert into achievement(title,description,isRepeatable,isSelfReport)
values ('Solar Powers','Installed solar panels on home.',1,1);

insert into achievement(title,description,isRepeatable,isSelfReport)
values ('Wind Powers','Incorporated a wind turbine into home energy sources.',1,1);

insert into achievement(title,description)
values ('Leader!','Claim the number one spot of users based on carbon footprint.');

insert into achievement(title,description)
values ('Top 10!','Claim a spot in the top 10 percent of users based on carbon footprint.');

insert into achievement(title,description)
values ('Top 25!','Claim a spot in the top 25 percent of users based on carbon footprint.');

insert into achievement(title,description)
values ('Top 50!','Claim a spot in the top 50 percent of users based on carbon footprint.');

insert into achievement(title,description,isRepeatable)
values ('Once Upon a Time: Leader!','Has held a spot in the number one spot of users.',1);

insert into achievement(title,description,isRepeatable)
values ('Once Upon a Time: Top 10!','Has held a spot in the top 10 percent of users.',1);

insert into achievement(title,description,isRepeatable)
values ('Once Upon a Time: Top 25!','Has held a spot in the top 25 percent of users.',1);

insert into achievement(title,description,isRepeatable)
values ('Once Upon a Time: Top 50!','Has held a spot in the top 50 percent of users.',1);

insert into achievement(title,description)
values ("I've Been Around",'Obtained five unique achievements.');

insert into achievement(title,description)
values ("I'll Be Here All Night",'Obtained ten unique achievements.');

insert into achievement(title,description)
values ("I'm Here To Stay",'Obtained fifteen unique achievements.');

insert into achievement(title,description)
values ("I'll Be Here Forever",'Obtained all unique achievements at least once.');

insert into achievement(title,description)
values ("I'm Here Longer Than Forever",'Obtained all unique and repeatable achievements more than once.');

insert into achievement(title,description)
values ("Super Powered!",'Obtained all three (Earth, Wind, Solar) of the Power Achievements.');

insert into achievement(title,description,isRepeatable,isSelfReport)
values ('Biked','Biked to Work/School.',1,1);

insert into achievement(title,description,isRepeatable,isSelfReport)
values ('Bipedal','Walked to Work/School.',1,1);