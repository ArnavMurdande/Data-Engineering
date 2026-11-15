CREATE DATABASE IF NOT EXISTS DELIVERY_TRACKING_DB;

USE DELIVERY_TRACKING_DB;

DROP TABLE IF EXISTS Deliveries;

DROP TABLE IF EXISTS Drivers;

DROP TABLE IF EXISTS Routes;

CREATE TABLE Routes (
    route_id INT PRIMARY KEY,
    route_name VARCHAR(100) NOT NULL
);

CREATE TABLE Drivers (
    driver_id INT PRIMARY KEY,
    driver_name VARCHAR(100) NOT NULL
);

CREATE TABLE Deliveries (
    delivery_id INT PRIMARY KEY,
    route_id INT,
    driver_id INT,
    delivery_time DECIMAL(6, 2),
    status ENUM(
        'Completed',
        'Delayed',
        'Cancelled'
    ),
    FOREIGN KEY (route_id) REFERENCES Routes (route_id),
    FOREIGN KEY (driver_id) REFERENCES Drivers (driver_id)
);

-- Insert Sample Data
INSERT INTO Routes VALUES (1, 'Route A'), (2, 'Route B');

INSERT INTO
    Drivers
VALUES (1, 'Driver 1'),
    (2, 'Driver 2'),
    (3, 'Driver 3'),
    (4, 'Driver 4');

INSERT INTO
    Deliveries
VALUES (301, 1, 1, 42.50, 'Completed'),
    (302, 1, 2, 39.00, 'Completed'),
    (303, 1, 3, 46.00, 'Completed'),
    (304, 1, 4, 55.00, 'Delayed'),
    (305, 2, 1, 61.00, 'Completed'),
    (306, 2, 2, 58.50, 'Completed'),
    (307, 2, 3, 63.50, 'Completed'),
    (308, 2, 4, 70.00, 'Cancelled');