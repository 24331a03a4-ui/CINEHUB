-- OTT PLATFORM DATABASE
-- ============================================

DROP DATABASE IF EXISTS ott_platform;

CREATE DATABASE ott_platform;
USE ott_platform;

-- ============================================
-- 1. OTT PLATFORMS
-- ============================================

CREATE TABLE platforms (
platform_id INT AUTO_INCREMENT PRIMARY KEY,
platform_name VARCHAR(50) NOT NULL UNIQUE
);

INSERT INTO platforms (platform_name)
VALUES
('Netflix'),
('Amazon Prime'),
('JioHotstar');

-- ============================================
-- 2. GENRES
-- ============================================

CREATE TABLE genres (
genre_id INT AUTO_INCREMENT PRIMARY KEY,
genre_name VARCHAR(50) NOT NULL UNIQUE
);

INSERT INTO genres (genre_name)
VALUES
('Action'),
('Adventure'),
('Comedy'),
('Drama'),
('Romance'),
('Thriller'),
('Horror'),
('Science Fiction'),
('Fantasy'),
('Crime'),
('Documentary'),
('Animation'),
('Mystery'),
('Historical'),
('Biography'),
('Sports');

-- ============================================
-- 3. MOVIES
-- ============================================

CREATE TABLE movies (
movie_id INT AUTO_INCREMENT PRIMARY KEY,
platform_id INT NOT NULL,
genre_id INT,
genre_name VARCHAR(50),
title VARCHAR(150) NOT NULL,
description TEXT,
release_year YEAR,
duration_minutes INT,
language VARCHAR(50),
rating DECIMAL(3,1),


FOREIGN KEY (platform_id)
    REFERENCES platforms(platform_id)
    ON DELETE CASCADE,

FOREIGN KEY (genre_id)
    REFERENCES genres(genre_id)
    ON DELETE SET NULL


);

-- ============================================
-- 4. SERIES
-- ============================================

CREATE TABLE series (
series_id INT AUTO_INCREMENT PRIMARY KEY,
platform_id INT NOT NULL,
genre_id INT,
genre_name VARCHAR(50),
title VARCHAR(150) NOT NULL,
description TEXT,
release_year YEAR,
seasons INT,
language VARCHAR(50),
rating DECIMAL(3,1),


FOREIGN KEY (platform_id)
    REFERENCES platforms(platform_id)
    ON DELETE CASCADE,

FOREIGN KEY (genre_id)
    REFERENCES genres(genre_id)
    ON DELETE SET NULL


);

-- ============================================
-- 5. DOCUMENTARIES
-- ============================================

CREATE TABLE documentaries (
documentary_id INT AUTO_INCREMENT PRIMARY KEY,
platform_id INT NOT NULL,
genre_id INT,
genre_name VARCHAR(50),
title VARCHAR(150) NOT NULL,
description TEXT,
release_year YEAR,
duration_minutes INT,
language VARCHAR(50),
rating DECIMAL(3,1),

FOREIGN KEY (platform_id)
    REFERENCES platforms(platform_id)
    ON DELETE CASCADE,

FOREIGN KEY (genre_id)
    REFERENCES genres(genre_id)
    ON DELETE SET NULL

);

-- ============================================
-- 6. MOVIE - GENRE
-- MANY-TO-MANY RELATIONSHIP
-- ============================================

CREATE TABLE movie_genres (
movie_id INT NOT NULL,
genre_id INT NOT NULL,

PRIMARY KEY (movie_id, genre_id),

FOREIGN KEY (movie_id)
    REFERENCES movies(movie_id)
    ON DELETE CASCADE,

FOREIGN KEY (genre_id)
    REFERENCES genres(genre_id)
    ON DELETE CASCADE

);

-- ============================================
-- 7. SERIES - GENRE
-- MANY-TO-MANY RELATIONSHIP
-- ============================================

CREATE TABLE series_genres (
series_id INT NOT NULL,
genre_id INT NOT NULL,

PRIMARY KEY (series_id, genre_id),

FOREIGN KEY (series_id)
    REFERENCES series(series_id)
    ON DELETE CASCADE,

FOREIGN KEY (genre_id)
    REFERENCES genres(genre_id)
    ON DELETE CASCADE
);

-- ============================================
-- 8. DOCUMENTARY - GENRE
-- MANY-TO-MANY RELATIONSHIP
-- ============================================

CREATE TABLE documentary_genres (
documentary_id INT NOT NULL,
genre_id INT NOT NULL,

PRIMARY KEY (documentary_id, genre_id),

FOREIGN KEY (documentary_id)
    REFERENCES documentaries(documentary_id)
    ON DELETE CASCADE,

FOREIGN KEY (genre_id)
    REFERENCES genres(genre_id)
    ON DELETE CASCADE

);

-- ============================================
-- INSERT MOVIES
-- ============================================

INSERT INTO movies
(platform_id, genre_id, genre_name, title, description, release_year, duration_minutes, language, rating)
VALUES
(1, 1, 'Action', 'Extraction',
'An action thriller movie', 2020, 116, 'English', 7.0),

(1, 1, 'Action', 'Red Notice',
'An action comedy movie', 2021, 118, 'English', 6.3),

(2, 8, 'Science Fiction', 'The Tomorrow War',
'A science fiction action movie', 2021, 140, 'English', 6.5),

(2, 4, 'Drama', 'Sound of Metal',
'A drama movie about a musician', 2019, 120, 'English', 7.7),

(3, 9, 'Fantasy', 'Brahmastra',
'A fantasy adventure movie', 2022, 167, 'Hindi', 5.5),

(3, 3, 'Comedy', 'JugJugg Jeeyo',
'A family comedy drama', 2022, 148, 'Hindi', 6.1);

-- ============================================
-- INSERT SERIES
-- ============================================

INSERT INTO series
(platform_id, genre_id, genre_name, title, description, release_year, seasons, language, rating)
VALUES
(1, 8, 'Science Fiction', 'Stranger Things',
'A science fiction mystery series', 2016, 4, 'English', 8.7),

(1, 10, 'Crime', 'Money Heist',
'A crime thriller series', 2017, 5, 'Spanish', 8.2),

(2, 1, 'Action', 'The Boys',
'A superhero action series', 2019, 4, 'English', 8.7),

(2, 1, 'Action', 'The Family Man',
'An Indian action thriller series', 2019, 2, 'Hindi', 8.7),

(3, 6, 'Thriller', 'Special Ops',
'An Indian spy thriller series', 2020, 2, 'Hindi', 8.5),

(3, 10, 'Crime', 'Criminal Justice',
'A crime drama series', 2018, 3, 'Hindi', 8.1);

-- ============================================
-- INSERT DOCUMENTARIES
-- ============================================

INSERT INTO documentaries
(platform_id, genre_id, genre_name, title, description, release_year, duration_minutes, language, rating)
VALUES
(1, 11, 'Documentary', 'Our Planet',
'A nature documentary', 2019, 480, 'English', 9.3),

(1, 11, 'Documentary', 'The Social Dilemma',
'A documentary about social media', 2020, 94, 'English', 7.6),

(2, 16, 'Sports', 'All or Nothing',
'A sports documentary series', 2016, 360, 'English', 8.7),

(2, 16, 'Sports', 'The Test',
'A cricket documentary', 2020, 300, 'English', 8.7),

(3, 11, 'Documentary', 'Indian Space Dreams',
'A documentary about space exploration', 2022, 110, 'Hindi', 8.0),

(3, 11, 'Documentary', 'Wild India',
'A documentary about Indian wildlife', 2021, 90, 'Hindi', 8.5);

-- ============================================
-- INSERT MOVIE GENRES
-- ============================================

INSERT INTO movie_genres (movie_id, genre_id)
VALUES
(1, 1),
(1, 6),

(2, 1),
(2, 3),

(3, 1),
(3, 8),

(4, 4),

(5, 9),
(5, 2),

(6, 3),
(6, 4);

-- ============================================
-- INSERT SERIES GENRES
-- ============================================

INSERT INTO series_genres (series_id, genre_id)
VALUES
(1, 8),
(1, 13),

(2, 10),
(2, 6),

(3, 1),
(3, 4),

(4, 1),
(4, 10),
(4, 6),

(5, 6),
(5, 10),

(6, 4),
(6, 10);

-- ============================================
-- INSERT DOCUMENTARY GENRES
-- ============================================

INSERT INTO documentary_genres (documentary_id, genre_id)
VALUES
(1, 11),
(1, 2),

(2, 11),
(2, 4),

(3, 16),
(3, 11),

(4, 16),
(4, 11),

(5, 11),
(5, 8),

(6, 11),
(6, 14);

-- ============================================
-- VIEW ALL TABLES
-- ============================================

SELECT * FROM platforms;
SELECT * FROM genres;
SELECT * FROM movies;
SELECT * FROM series;
SELECT * FROM documentaries;
SELECT * FROM movie_genres;
SELECT * FROM series_genres;
SELECT * FROM documentary_genres;

-- ============================================
-- MOVIE DETAILS WITH PLATFORM AND GENRE
-- ============================================

SELECT
m.movie_id,
m.title,
p.platform_name,
m.genre_id,
m.genre_name,
m.release_year,
m.rating
FROM movies m
JOIN platforms p
ON m.platform_id = p.platform_id;

-- ============================================
-- SERIES DETAILS WITH PLATFORM AND GENRE
-- ============================================

SELECT
s.series_id,
s.title,
p.platform_name,
s.genre_id,
s.genre_name,
s.release_year,
s.seasons,
s.rating
FROM series s
JOIN platforms p
ON s.platform_id = p.platform_id;

-- ============================================
-- DOCUMENTARY DETAILS WITH PLATFORM AND GENRE
-- ============================================

SELECT
d.documentary_id,
d.title,
p.platform_name,
d.genre_id,
d.genre_name,
d.release_year,
d.rating
FROM documentaries d
JOIN platforms p
ON d.platform_id = p.platform_id;

ALTER TABLE movies
ADD COLUMN content_url VARCHAR(500);

ALTER TABLE series
ADD COLUMN content_url VARCHAR(500);

ALTER TABLE documentaries 
ADD COLUMN content_url VARCHAR(500);

UPDATE movies
SET content_url = 'https://www.netflix.com/in/title/80230399'
WHERE movie_id = 1;

UPDATE movies
SET content_url = 'https://www.netflix.com/in/title/81161626'
WHERE movie_id = 2;

UPDATE movies
SET content_url = 'https://www.primevideo.com/detail/0L8V88NU7CFYRKM857QDN2O5B4'
WHERE movie_id = 3;