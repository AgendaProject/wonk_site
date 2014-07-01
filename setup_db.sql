drop table if exists wonks;
create table wonks
(
	wonk_id integer,
	name text,
	email text,
	phone text,
	bio text,
	web_url text,
	twitter_name text,
	blog_url text
);
drop table if exists wonk_topics;
create table wonk_topics
(
	wonk_id integer,
	topic text,
	reject_flag integer
);

drop table if exists wonk_news_items;
create table wonk_news_items
(
	wonk_id integer,
	title text,
	news_date date,
	news_type text,
	news_teaser text,
	news_url text
);
	

-- test data

insert into wonks (wonk_id, name) values (1001,"Erica");
insert into wonks (wonk_id, name) values (1002,"Hanna");
insert into wonks (wonk_id, name) values (1003,"Cathryn");
insert into wonks (wonk_id, name) values (1004,"Mary");
insert into wonks (wonk_id, name) values (1005,"Morris");

insert into wonks (wonk_id, name) values (1011, "Dean Baker");
insert into wonks (wonk_id, name) values (1012, "Jamie Rappaport Clark");
insert into wonks (wonk_id, name) values (101, "Robert Kuttner");



insert into wonk_topics (wonk_id, topic) values (1001,"min.*wage");
insert into wonk_topics (wonk_id, topic) values (1001,"Wonk");
insert into wonk_topics (wonk_id, topic) values (1002,"min.*wage");
insert into wonk_topics (wonk_id, topic) values (1003,"min.*wage");
insert into wonk_topics (wonk_id, topic) values (1004,"min.*wage");
insert into wonk_topics (wonk_id, topic) values (1005,"min.*wage");
insert into wonk_topics (wonk_id, topic) values (1005,"Wonk");
insert into wonk_topics (wonk_id, topic) values (1001,"tax");
insert into wonk_topics (wonk_id, topic) values (1002,"tax");
insert into wonk_topics (wonk_id, topic) values (1003,"tax");

insert into wonk_topics (wonk_id, topic) values (1011,"tax");
insert into wonk_topics (wonk_id, topic) values (1012,"tax");

insert into wonk_topics (wonk_id, topic) values (1003,"Alaska");
insert into wonk_topics (wonk_id, topic) values (1003,"Mississippi");

update wonks set twitter_name = "@agendaproject" where wonk_id = 1001;
update wonks set twitter_name = "@morrispearl" where wonk_id = 1005;

update wonks set blog_url = "http://www.huffingtonpost.com/author/index.php?author=dean-baker" where wonk_id = 1011;
update wonks set blog_url = "http://www.huffingtonpost.com/author/index.php?author=jamie-rappaport-clark" where wonk_id = 1012;
update wonks set blog_url = "http://prospect.org/authors/125995/rss.xml" where wonk_id = 1013;

update wonks set bio = "Ms. Payne is a graduate of Duke, and earned here MBA and Wharton" where wonk_id = 1001;
update wonks set bio = "Ms. DeSimone was graduated from New York University in 2014" where wonk_id = 1003;



