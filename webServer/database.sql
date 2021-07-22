create database drashti ;

create table login(
    username VARCHAR(20) PRIMARY KEY,
    password VARCHAR(64) NOT NULL
);

insert into login values('deepak','joshi');

create table notification(
    email VARCHAR(100) PRIMARY KEY
) ;

insert into notification values('test@email.com');

CREATE TABLE nodes(
    name VARCHAR(20),
    ip VARCHAR(16) PRIMARY KEY,
    description VARCHAR(200),
    server VARCHAR(1) DEFAULT '0',
    status VARCHAR(1) DEFAULT '0'
);

ALTER TABLE nodes ADD rtt VARCHAR(10) DEFAULT 'I' ;

CREATE TABLE logs(
    username VARCHAR(20),
    ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
