create database drashti ;

create table login(
    username VARCHAR(20) PRIMARY KEY,
    password VARCHAR(64) NOT NULL
);

insert into login values('deepak','joshi');