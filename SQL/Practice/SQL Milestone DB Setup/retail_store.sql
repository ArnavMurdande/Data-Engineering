CREATE DATABASE IF NOT EXISTS retail_store;

USE retail_store;

DROP TABLE IF EXISTS Order_Items;

DROP TABLE IF EXISTS Orders;

DROP TABLE IF EXISTS Products;

DROP TABLE IF EXISTS Customers;

CREATE TABLE Customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20)
);

CREATE TABLE Products (
    product_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE Orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE NOT NULL,
    total_amount DECIMAL(10, 2),
    FOREIGN KEY (customer_id) REFERENCES Customers (customer_id)
);

CREATE TABLE Order_Items (
    order_id INT,
    product_id INT,
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id) REFERENCES Orders (order_id),
    FOREIGN KEY (product_id) REFERENCES Products (product_id)
);

-- Insert Sample Data
INSERT INTO
    Customers
VALUES (
        201,
        'John Doe',
        'john@example.com',
        '1234567890'
    ),
    (
        202,
        'Jane Smith',
        'jane@example.com',
        '2345678901'
    ),
    (
        203,
        'Emily Davis',
        'emily@example.com',
        '3456789012'
    ),
    (
        204,
        'Mark Wilson',
        'mark@example.com',
        '4567890123'
    );

INSERT INTO
    Products
VALUES (
        301,
        'Laptop',
        'Electronics',
        1000.00
    ),
    (
        302,
        'Smartphone',
        'Electronics',
        600.00
    ),
    (
        303,
        'Office Chair',
        'Furniture',
        150.00
    ),
    (
        304,
        'Notebook Set',
        'Stationery',
        10.00
    );

INSERT INTO
    Orders
VALUES (
        401,
        201,
        '2023-08-01',
        1010.00
    ),
    (
        402,
        202,
        '2023-08-03',
        1600.00
    ),
    (403, 203, '2023-08-04', 20.00),
    (
        404,
        204,
        '2023-08-05',
        750.00
    );

INSERT INTO
    Order_Items
VALUES (401, 301, 1, 1000.00),
    (401, 304, 1, 10.00),
    (401, 303, 2, 150.00),
    (402, 301, 1, 1000.00),
    (402, 302, 1, 600.00),
    (402, 303, 1, 150.00),
    (403, 304, 2, 10.00),
    (403, 302, 1, 600.00),
    (403, 301, 1, 1000.00),
    (404, 303, 5, 150.00),
    (404, 304, 1, 10.00),
    (404, 302, 1, 600.00);