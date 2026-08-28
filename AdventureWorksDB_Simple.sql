/*
===============================================================================
AdventureWorksDB - Simple AdventureWorks-Style Practice Database
Database engine: MySQL 8.0+

Supports AdventureWorks questions from Q3 and Q4.
Contains database creation and sample data only.
No question statements or solution queries are included.
===============================================================================
*/

DROP DATABASE IF EXISTS AdventureWorksDB;
CREATE DATABASE AdventureWorksDB;
USE AdventureWorksDB;

/* 1. PRODUCT CATEGORIES */
CREATE TABLE ProductCategory
(
    ProductCategoryID INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL UNIQUE
);

/* 2. PRODUCT SUBCATEGORIES */
CREATE TABLE ProductSubcategory
(
    ProductSubcategoryID INT PRIMARY KEY,
    ProductCategoryID INT NOT NULL,
    Name VARCHAR(100) NOT NULL,

    CONSTRAINT fk_subcategory_category
        FOREIGN KEY (ProductCategoryID)
        REFERENCES ProductCategory(ProductCategoryID)
);

/* 3. PRODUCTS */
CREATE TABLE Product
(
    ProductID INT PRIMARY KEY,
    Name VARCHAR(150) NOT NULL,
    ProductNumber VARCHAR(50) NOT NULL UNIQUE,
    ProductSubcategoryID INT,

    CONSTRAINT fk_product_subcategory
        FOREIGN KEY (ProductSubcategoryID)
        REFERENCES ProductSubcategory(ProductSubcategoryID)
);

/* 4. SALES ORDER HEADER
   One row represents one sales order.
*/
CREATE TABLE SalesOrderHeader
(
    SalesOrderID INT PRIMARY KEY,
    OrderDate DATE NOT NULL,
    TotalDue DECIMAL(12,2) NOT NULL,

    CONSTRAINT chk_sales_total_due
        CHECK (TotalDue >= 0)
);

CREATE INDEX idx_sales_order_date
    ON SalesOrderHeader(OrderDate);

/* CATEGORY DATA */
INSERT INTO ProductCategory
(ProductCategoryID, Name)
VALUES
(1, 'Bikes'),
(2, 'Components'),
(3, 'Clothing'),
(4, 'Accessories');

/* SUBCATEGORY DATA */
INSERT INTO ProductSubcategory
(ProductSubcategoryID, ProductCategoryID, Name)
VALUES
(10, 1, 'Road Frames'),
(11, 1, 'Road Bikes'),
(12, 1, 'Mountain Bikes'),
(20, 2, 'Wheels'),
(21, 2, 'Brakes'),
(30, 3, 'Jerseys'),
(40, 4, 'Helmets');

/* PRODUCT DATA */
INSERT INTO Product
(ProductID, Name, ProductNumber, ProductSubcategoryID)
VALUES
(680, 'HL Road Frame - Black, 58', 'FR-R92B-58', 10),
(706, 'HL Road Frame - Red, 58',   'FR-R92R-58', 10),
(712, 'HL Road Tire',              'TI-R092',     11),
(713, 'Mountain Bike 200',         'BK-M200',     12),
(800, 'Road Wheel',                'WH-R100',     20),
(810, 'Disc Brake',                'BR-D100',     21),
(900, 'Cycling Jersey',            'CL-J100',     30),
(910, 'Sport Helmet',              'AC-H100',     40);

/* SALES DATA
   Multiple orders per month allow monthly SUM and LAG practice.
   Monthly totals are:
   January 2013  = 245000.00
   February 2013 = 271500.00
   March 2013    = 259800.00
   April 2013    = 298400.00
*/
INSERT INTO SalesOrderHeader
(SalesOrderID, OrderDate, TotalDue)
VALUES
(1001, '2013-01-05', 120000.00),
(1002, '2013-01-20', 125000.00),
(1003, '2013-02-08', 130000.00),
(1004, '2013-02-22', 141500.00),
(1005, '2013-03-04', 125000.00),
(1006, '2013-03-19', 134800.00),
(1007, '2013-04-06', 150000.00),
(1008, '2013-04-25', 148400.00);
