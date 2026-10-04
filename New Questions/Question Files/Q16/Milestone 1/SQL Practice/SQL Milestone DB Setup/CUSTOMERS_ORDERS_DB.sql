CREATE DATABASE IF NOT EXISTS CUSTOMERS_ORDERS_DB;

USE CUSTOMERS_ORDERS_DB;

DROP TABLE IF EXISTS Orders;

DROP TABLE IF EXISTS Customers;

CREATE TABLE Customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL
);

CREATE TABLE Orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE NOT NULL,
    amount DECIMAL(10, 2),
    FOREIGN KEY (customer_id) REFERENCES Customers (customer_id)
);

-- Insert Sample Data: Option 1 (Matches PDF 'Expected Output' screenshot exactly)
INSERT INTO
    Customers
VALUES (1, 'Aditi'),
    (2, 'Bharat');

INSERT INTO
    Orders
VALUES (101, 1, '2025-11-07', 800.00),
    (102, 1, '2025-11-11', 1200.00),
    (105, 1, '2025-11-15', 950.00),
    (201, 2, '2025-11-14', 650.00);

-- Note: The question PDF (Page 6) also has an alternative 'Sample Data' table:
-- Customers: (1, 'Aarav'), (2, 'Diya'), (3, 'Kabir')
-- Orders:
-- (501, 1, '2025-08-02', 800.00), (506, 1, '2025-08-07', 1200.00), (514, 1, '2025-08-19', 950.00),
-- (602, 2, '2025-08-04', 650.00), (609, 2, '2025-08-13', 1050.00),
-- (701, 3, '2025-08-06', 1500.00), (708, 3, '2025-08-16', 1100.00)