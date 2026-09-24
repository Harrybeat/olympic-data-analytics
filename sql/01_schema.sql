-- PostgreSQL Schema für Olympic Data Analytics

CREATE TYPE medal_enum AS ENUM ('Gold', 'Silver', 'Bronze', 'No Medal');
CREATE TYPE sex_enum AS ENUM ('M', 'F');

CREATE TABLE Athletes (
    athlete_id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    sex sex_enum
);

CREATE TABLE NOC_Regions (
    noc VARCHAR(5) PRIMARY KEY,
    region_name VARCHAR(255)
);

CREATE TABLE Events (
    event_id INT PRIMARY KEY,
    sport VARCHAR(100),
    event_name VARCHAR(255)
);

CREATE TABLE Athlete_Events (
    participation_id INT PRIMARY KEY,
    athlete_id INT REFERENCES Athletes (athlete_id),
    event_id INT REFERENCES Events (event_id),
    noc VARCHAR(5) REFERENCES NOC_Regions (noc),
    year INT,
    age FLOAT,
    height_cm FLOAT,
    weight_kg FLOAT,
    medal medal_enum
);