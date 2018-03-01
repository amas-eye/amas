drop table if exists metric;

create table metric(
	id integer primary key autoincrement,
	metric_name text not null,
	description text default null,
	tags text default null,
	last_update string default null
);
