create database tennis;
use tennis;

-- Categories
CREATE TABLE categories (
    category_id VARCHAR(50) PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL
);

-- Competitions
CREATE TABLE competitions (
    competition_id VARCHAR(50) PRIMARY KEY,
    competition_name VARCHAR(100) NOT NULL,
    parent_id VARCHAR(50),
    type VARCHAR(20),
    gender VARCHAR(10),
    category_id VARCHAR(50),
    FOREIGN KEY (category_id) REFERENCES Categories(category_id)
);

-- Complexes
CREATE TABLE complexes (
    complex_id VARCHAR(50) PRIMARY KEY,
    complex_name VARCHAR(100) NOT NULL
);

-- Venues
CREATE TABLE venues (
    venue_id VARCHAR(50) PRIMARY KEY,
    venue_name VARCHAR(100),
    city_name VARCHAR(100),
    country_name VARCHAR(100),
    country_code CHAR(3),
    timezone VARCHAR(100),
    complex_id VARCHAR(50),
    FOREIGN KEY (complex_id) REFERENCES Complexes(complex_id)
);

-- Competitors
CREATE TABLE competitors (
    competitor_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100),
    country VARCHAR(100),
    country_code CHAR(3),
    abbreviation VARCHAR(10)
);

-- Rankings
CREATE TABLE competitor_Rankings (
    rank_id INT AUTO_INCREMENT PRIMARY KEY,
    ranking INT,
    movement INT,
    points INT,
    competitions_played INT,
    competitor_id VARCHAR(50),
    FOREIGN KEY (competitor_id) REFERENCES Competitors(competitor_id)
);



