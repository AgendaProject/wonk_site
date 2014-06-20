create table wonks
(
	wonk_id integer primary key asc,
	name text,
	email text,
	phone text,
	bio text,
	web_url text,
	twitter_name text,
	blog_url text
);
create table wonk_topics
(
	wonk_id integer,
	topic text,
	reject_flag integer default (0)
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

update wonks set twitter_name = "@agendaproject" where wonk_id = 1001;
update wonks set twitter_name = "@morrispearl" where wonk_id = 1005;

update wonks set blog_url = "http://www.huffingtonpost.com/author/index.php?author=dean-baker" where wonk_id = 1011;
update wonks set blog_url = "http://www.huffingtonpost.com/author/index.php?author=jamie-rappaport-clark" where wonk_id = 1012;
update wonks set blog_url = "http://prospect.org/authors/125995/rss.xml" where wonk_id = 1013;


