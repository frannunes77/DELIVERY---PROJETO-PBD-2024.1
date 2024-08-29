create table if not exists Usuario(
	id serial primary key,
	username varchar(255) not null,
	password varchar(255) not null
);
insert into Usuario(username, password) 
values ('fran_nunes', '123');

select * from Usuario;