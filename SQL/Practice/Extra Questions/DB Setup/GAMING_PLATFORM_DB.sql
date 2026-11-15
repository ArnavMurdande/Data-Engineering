-- SQLBook: Code
-- ==============================================================================
-- Database: GAMING_PLATFORM_DB
-- Setup Script: Games, Players, Scores Tables
-- ==============================================================================

CREATE DATABASE IF NOT EXISTS GAMING_PLATFORM_DB;
USE GAMING_PLATFORM_DB;

DROP TABLE IF EXISTS Scores;
DROP TABLE IF EXISTS Players;
DROP TABLE IF EXISTS Games;

CREATE TABLE Games (
    game_id INT PRIMARY KEY,
    game_name VARCHAR(100) NOT NULL
);

CREATE TABLE Players (
    player_id INT PRIMARY KEY,
    player_name VARCHAR(100) NOT NULL
);

CREATE TABLE Scores (
    score_id INT PRIMARY KEY AUTO_INCREMENT,
    game_id INT NOT NULL,
    player_id INT NOT NULL,
    score INT NOT NULL,
    status ENUM('Recorded', 'Disqualified', 'Pending') NOT NULL,
    recorded_at DATETIME NOT NULL,
    FOREIGN KEY (game_id) REFERENCES Games(game_id),
    FOREIGN KEY (player_id) REFERENCES Players(player_id)
);

-- Insert Sample Data
INSERT INTO Games (game_id, game_name) VALUES
(1, 'Speed Racer'),
(2, 'Cyber Combat'),
(3, 'Pixel Puzzle');

INSERT INTO Players (player_id, player_name) VALUES
(101, 'Alex'),
(102, 'Blake'),
(103, 'Charlie'),
(104, 'David'),
(105, 'Emma');

INSERT INTO Scores (game_id, player_id, score, status, recorded_at) VALUES
-- Speed Racer
(1, 101, 950, 'Recorded', '2026-03-01 10:00:00'),
(1, 102, 980, 'Recorded', '2026-03-01 10:05:00'),
(1, 103, 950, 'Recorded', '2026-03-01 10:10:00'),
(1, 104, 870, 'Disqualified', '2026-03-01 10:15:00'),
(1, 105, 910, 'Recorded', '2026-03-01 10:20:00'),
(2, 101, 1500, 'Recorded', '2026-03-01 11:00:00'),
(2, 102, 1820, 'Recorded', '2026-03-01 11:10:00'),
(2, 103, 1820, 'Recorded', '2026-03-01 11:20:00'),
(2, 104, 1300, 'Pending', '2026-03-01 11:30:00'),
(3, 103, 450, 'Recorded', '2026-03-01 12:00:00'),
(3, 104, 520, 'Recorded', '2026-03-01 12:10:00'),
(3, 105, 520, 'Recorded', '2026-03-01 12:20:00');

