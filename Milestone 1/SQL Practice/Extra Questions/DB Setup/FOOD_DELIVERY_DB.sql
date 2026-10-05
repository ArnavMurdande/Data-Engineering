-- ==============================================================================
-- Database: FOOD_DELIVERY_DB
-- Setup Script: Payments Table
-- ==============================================================================

CREATE DATABASE IF NOT EXISTS FOOD_DELIVERY_DB;
USE FOOD_DELIVERY_DB;

DROP TABLE IF EXISTS Payments;

CREATE TABLE Payments (
    payment_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    customer_id INT NOT NULL,
    payment_method ENUM('UPI', 'Card', 'Cash', 'Wallet') NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    payment_date DATETIME NOT NULL
);

-- Insert Sample Data
INSERT INTO Payments (order_id, customer_id, payment_method, amount, payment_date) VALUES
(1001, 201, 'UPI', 350.00, '2026-03-01 12:15:00'),
(1002, 202, 'Card', 520.00, '2026-03-01 12:20:00'),
(1003, 203, 'UPI', 210.00, '2026-03-01 12:35:00'),
(1004, 204, 'Wallet', 150.00, '2026-03-01 13:00:00'),
(1005, 205, 'UPI', 680.00, '2026-03-01 13:15:00'),
(1006, 206, 'Card', 490.00, '2026-03-01 13:30:00'),
(1007, 207, 'Cash', 120.00, '2026-03-01 13:45:00'),
(1008, 208, 'UPI', 890.00, '2026-03-01 14:00:00'),
(1009, 209, 'Card', 310.00, '2026-03-01 14:10:00'),
(1010, 210, 'Wallet', 250.00, '2026-03-01 14:25:00');
