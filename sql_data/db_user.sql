CREATE DATABASE USERS;
USE USERS;

CREATE TABLE user(
   username varchar(100) not null,
   email varchar(100) not null,
   password varchar(100) not null,
   PRIMARY KEY(username), UNIQUE(email)
);


insert into user(username,email,password)
values("Me" , "Ani@Secure.com" , "$argon2id$v=19$m=16,t=2,p=1$VXc5eWZNR1phb1JLN0hGcQ$VqDcMJuxpPLxba7FEwWRjg");

CREATE TABLE clients(
   name varchar(100) not null,
   email varchar(100) not null,
   phone varchar(30) not null,
   PRIMARY KEY(email), UNIQUE(phone)
);

insert into clients(name,email,phone)
values("ita" , "i@walla.com" , "0500000000");

CREATE TABLE userpass(
   id int not null AUTO_INCREMENT,
   uname varchar(100) not null,
   passwordtemp varchar(100) not null,
   passwordsecond varchar(100) not null,
   passwordthird varchar(100) not null, 
   PRIMARY KEY(id), FOREIGN KEY(uname) REFERENCES user(username), UNIQUE(uname)
);

insert into userpass(uname, passwordtemp, passwordsecond, passwordthird)
values("Me","$argon2id$v=19$m=16,t=2,p=1$VXc5eWZNR1phb1JLN0hGcQ$VqDcMJuxpPLxba7FEwWRjg","$argon2id$v=19$m=16,t=2,p=1$VXc5eWZNR1phb1JLN0hGcQ$VqDcMJuxpPLxba7FEwWRjg","$argon2id$v=19$m=16,t=2,p=1$VXc5eWZNR1phb1JLN0hGcQ$VqDcMJuxpPLxba7FEwWRjg");