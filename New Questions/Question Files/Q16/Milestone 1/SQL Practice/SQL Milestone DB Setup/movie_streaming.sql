CREATE DATABASE IF NOT EXISTS movie_streaming;

USE movie_streaming;

DROP TABLE IF EXISTS Subscriptions;

DROP TABLE IF EXISTS Watch_History;

DROP TABLE IF EXISTS Movies;

DROP TABLE IF EXISTS Genres;

DROP TABLE IF EXISTS Users;

CREATE TABLE Users (
    user_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    signup_date DATE NOT NULL
);

CREATE TABLE Genres (
    genre_id INT PRIMARY KEY,
    genre_name VARCHAR(50) NOT NULL
);

CREATE TABLE Movies (
    movie_id INT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    release_year INT,
    genre_id INT,
    FOREIGN KEY (genre_id) REFERENCES Genres (genre_id)
);

CREATE TABLE Watch_History (
    user_id INT,
    movie_id INT,
    watch_date DATE NOT NULL,
    PRIMARY KEY (user_id, movie_id, watch_date),
    FOREIGN KEY (user_id) REFERENCES Users (user_id),
    FOREIGN KEY (movie_id) REFERENCES Movies (movie_id)
);

CREATE TABLE Subscriptions (
    subscription_id INT PRIMARY KEY,
    user_id INT,
    plan VARCHAR(50) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users (user_id)
);

-- Insert Sample Data
INSERT INTO
    Users
VALUES (
        801,
        'Alice Moore',
        'alice@stream.com',
        '2023-01-15'
    ),
    (
        802,
        'Bob Green',
        'bob@stream.com',
        '2023-02-10'
    ),
    (
        803,
        'Carol White',
        'carol@stream.com',
        '2023-03-20'
    ),
    (
        804,
        'Dave Black',
        'dave@stream.com',
        '2023-04-05'
    );

INSERT INTO
    Genres
VALUES (1, 'Drama'),
    (2, 'Action'),
    (3, 'Comedy'),
    (4, 'Documentary');

INSERT INTO
    Movies
VALUES (
        901,
        'The Great Escape',
        1963,
        2
    ),
    (902, 'Life of Pi', 2012, 4),
    (
        903,
        'The Office (Series)',
        2005,
        3
    ),
    (904, 'Hamlet', 1996, 1);

INSERT INTO
    Watch_History
VALUES (801, 901, '2023-08-01'),
    (801, 902, '2023-08-02'),
    (802, 903, '2023-08-03'),
    (802, 904, '2023-08-04'),
    (803, 901, '2023-08-05'),
    (803, 902, '2023-08-06'),
    (804, 903, '2023-08-07'),
    (804, 904, '2023-08-08'),
    (801, 903, '2023-08-09'),
    (802, 902, '2023-08-10'),
    (803, 904, '2023-08-11'),
    (804, 901, '2023-08-12');

INSERT INTO
    Subscriptions
VALUES (
        1001,
        801,
        'Premium',
        19.99,
        '2023-08-01',
        '2023-08-31'
    ),
    (
        1002,
        802,
        'Basic',
        9.99,
        '2023-08-01',
        '2023-08-31'
    ),
    (
        1003,
        803,
        'Premium',
        19.99,
        '2023-08-01',
        '2023-08-31'
    ),
    (
        1004,
        804,
        'Standard',
        14.99,
        '2023-08-01',
        '2023-08-31'
    );