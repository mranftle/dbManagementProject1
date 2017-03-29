-- SQL Table Creation Statements
-- Project 1 Database

-- Tables
-- happiness, attack_outcomes, attack_victims, terrorist_attacks


-- uncomment DROP statements if script has already been run once
-- DROP TABLE terrorist_attacks;
-- DROP TABLE attack_outcomes;
-- DROP TABLE attack_victims;
-- DROP TABLE happiness;

-- create tables
CREATE TABlE attack_outcomes(
  eventid VARCHAR(32) NOT NULL,
  success INT,
  suicide INT,
  nkill INT,
  nwould INT,
  propvalue BIGINT,
  PRIMARY KEY(eventid)
);

CREATE TABLE attack_victims(
  eventid VARCHAR(32) NOT NULL,
  targtype1 VARCHAR(256),
  targsubtype1 VARCHAR(256),
  corp1 VARCHAR(256),
  target1 VARCHAR(512),
  natlty1 VARCHAR(64),
  PRIMARY KEY(eventid)
);


CREATE TABLE terrorist_attacks(
  eventid VARCHAR(32) NOT NULL,
  iyear INT,
  imonth INT,
  iday INT,
  country VARCHAR(64),
  region VARCHAR(64),
  city VARCHAR(128),
  gname VARCHAR(256),
  gsubname VARCHAR(256),
  claimed INT,
  nperps INT,
  weaptype1 VARCHAR(128),
  attacktype1 VARCHAR(128),
  motive VARCHAR(1024),
  PRIMARY KEY(eventid)
);

CREATE TABLE happiness(
  country VARCHAR(64) UNIQUE,
  region VARCHAR(64),
  hrank INT,
  hscore FLOAT,
  std_err FLOAT,
  economy FLOAT,
  family FLOAT,
  health FLOAT,
  freedom FLOAT,
  trust FLOAT,
  generosity FLOAT,
  dys_residual FLOAT
);

-- Data cleaned and .csv files generated in terrorist_data_parser.py
-- These commands were executed manually through the psql command line to insert the data into the db

--  \copy attacks_outcomes FROM '~/cse530/project1/data/outcomes.csv' DELIMITER E'\t' CSV HEADER;
--  \copy attacks_victims FROM '~/cse530/project1/data/victims.csv' DELIMITER E'\t' CSV HEADER;
--  \copy terrorist_attacks FROM '~/cse530/project1/data/attacks.csv' DELIMITER E'\t' CSV HEADER;
--  \copy happiness FROM '~/cse530/project1/data/happiness_2015.csv' DELIMITER ',' CSV HEADER;
