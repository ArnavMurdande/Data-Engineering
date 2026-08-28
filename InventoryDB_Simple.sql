/*
===============================================================================
InventoryDB - Simple Inventory Practice Database
Database engine: MySQL 8.0+

Supports Inventory questions from Q2, Q3 and Q4.
Contains database creation and sample data only.
No question statements or solution queries are included.
===============================================================================
*/

DROP DATABASE IF EXISTS InventoryDB;
CREATE DATABASE InventoryDB;
USE InventoryDB;

/* 1. SUPPLIERS */
CREATE TABLE Suppliers
(
    supplier_id INT PRIMARY KEY,
    supplier_name VARCHAR(100) NOT NULL UNIQUE
);

/* 2. PRODUCTS
   stock_quantity supports the basic low-stock question.
   supplier_id supports joining products with suppliers.
*/
CREATE TABLE Products
(
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL UNIQUE,
    category VARCHAR(50) NOT NULL,
    stock_quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    supplier_id INT NOT NULL,

    CONSTRAINT chk_product_stock
        CHECK (stock_quantity >= 0),

    CONSTRAINT chk_product_price
        CHECK (price >= 0),

    CONSTRAINT fk_product_supplier
        FOREIGN KEY (supplier_id)
        REFERENCES Suppliers(supplier_id)
);

/* 3. INVENTORY
   One row represents the inventory details of one product.
*/
CREATE TABLE Inventory
(
    inventory_id INT PRIMARY KEY,
    product_id INT NOT NULL UNIQUE,
    stock_quantity INT NOT NULL,
    reorder_level INT NOT NULL,

    CONSTRAINT chk_inventory_stock
        CHECK (stock_quantity >= 0),

    CONSTRAINT chk_reorder_level
        CHECK (reorder_level >= 0),

    CONSTRAINT fk_inventory_product
        FOREIGN KEY (product_id)
        REFERENCES Products(product_id)
);

/* 4. MONTHLY INVENTORY
   One row represents the closing inventory for one month.
*/
CREATE TABLE MonthlyInventory
(
    month_start DATE PRIMARY KEY,
    closing_stock INT NOT NULL,

    CONSTRAINT chk_closing_stock
        CHECK (closing_stock >= 0),

    CONSTRAINT chk_inventory_month_start
        CHECK (DAY(month_start) = 1)
);

/* SUPPLIER DATA */
INSERT INTO Suppliers
(supplier_id, supplier_name)
VALUES
(1, 'TechSupply'),
(2, 'Computer World'),
(3, 'OfficeHub'),
(4, 'Stationery Mart');

/* PRODUCT DATA
   Keyboard and USB Cable have fewer than 10 units for basic filtering practice.
*/
INSERT INTO Products
(product_id, product_name, category, stock_quantity, price, supplier_id)
VALUES
(101, 'Wireless Mouse', 'Electronics', 45,  799.00, 1),
(102, 'Keyboard',       'Electronics',  8, 1299.00, 2),
(103, 'Office Chair',   'Furniture',   25, 6500.00, 3),
(104, 'USB Cable',      'Electronics',  5,  299.00, 1),
(105, 'Notebook',       'Stationery',  60,  120.00, 4),
(106, 'Monitor',        'Electronics', 30, 18000.00, 1),
(107, 'USB Keyboard',   'Electronics', 12, 1500.00, 2);

/* INVENTORY DATA
   Wireless Mouse and USB Keyboard are below their reorder levels.
*/
INSERT INTO Inventory
(inventory_id, product_id, stock_quantity, reorder_level)
VALUES
(1, 101,  8, 20),
(2, 102, 18, 10),
(3, 103, 25, 10),
(4, 104, 20, 10),
(5, 105, 60, 20),
(6, 106, 30, 15),
(7, 107, 12, 25);

/* MONTHLY INVENTORY DATA */
INSERT INTO MonthlyInventory
(month_start, closing_stock)
VALUES
('2025-01-01', 5000),
('2025-02-01', 5400),
('2025-03-01', 5100),
('2025-04-01', 5750);
