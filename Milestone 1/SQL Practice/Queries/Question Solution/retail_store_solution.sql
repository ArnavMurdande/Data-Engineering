-- ==============================================================================
-- Database: retail_store
-- Solution File: retail_store_solution.sql
-- ==============================================================================

USE retail_store;

-- ------------------------------------------------------------------------------
-- Question 1: Customer with the Highest Value Order
--
-- Problem Statement:
--   Management wants to know which customer placed the single highest-value order.
--   You need to find and return the customer’s name along with the order_id and
--   total_amount of that order.
--
-- Query Requirements:
--   Write a query that uses a single-row subquery to find order_id, customer_name,
--   and total_amount for the order with the maximum total_amount in the Orders table.
--
-- Required Output Columns:
--   order_id, customer_name, total_amount
-- ------------------------------------------------------------------------------

SELECT 
    o.order_id,
    c.name AS customer_name,
    o.total_amount
FROM Orders o
JOIN Customers c 
    ON o.customer_id = c.customer_id
WHERE o.total_amount = (
    SELECT MAX(total_amount) 
    FROM Orders
);
