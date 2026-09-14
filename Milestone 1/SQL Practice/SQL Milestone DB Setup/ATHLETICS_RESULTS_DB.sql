CREATE DATABASE IF NOT EXISTS ATHLETICS_RESULTS_DB;

USE ATHLETICS_RESULTS_DB;

DROP TABLE IF EXISTS Results;

DROP TABLE IF EXISTS Athletes;

DROP TABLE IF EXISTS Events;

CREATE TABLE Events (
    event_id INT PRIMARY KEY,
    event_name VARCHAR(100) NOT NULL
);

CREATE TABLE Athletes (
    athlete_id INT PRIMARY KEY,
    athlete_name VARCHAR(100) NOT NULL
);

CREATE TABLE Results (
    result_id INT PRIMARY KEY,
    event_id INT,
    athlete_id INT,
    finish_time DECIMAL(5, 2),
    status ENUM(
        'Recorded',
        'Disqualified',
        'DNS'
    ),
    FOREIGN KEY (event_id) REFERENCES Events (event_id),
    FOREIGN KEY (athlete_id) REFERENCES Athletes (athlete_id)
);

-- Insert Sample Data
INSERT INTO Events VALUES (1, '100m Sprint'), (2, '200m Sprint');

INSERT INTO
    Athletes
VALUES (1, 'Alice'),
    (2, 'Brian'),
    (3, 'Carlos'),
    (4, 'Diana');

INSERT INTO
    Results
VALUES (201, 1, 1, 11.20, 'Recorded'),
    (202, 1, 2, 10.95, 'Recorded'),
    (203, 1, 3, 12.10, 'Recorded'),
    (
        204,
        1,
        4,
        11.50,
        'Disqualified'
    ),
    (205, 2, 1, 22.50, 'Recorded'),
    (206, 2, 2, 21.80, 'Recorded'),
    (207, 2, 3, 21.80, 'Recorded'),
    (208, 2, 4, 23.10, 'DNS');