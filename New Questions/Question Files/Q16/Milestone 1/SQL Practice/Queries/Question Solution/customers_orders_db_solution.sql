-- ==============================================================================
-- Database: CUSTOMERS_ORDERS_DB
-- Solution File: customers_orders_db_solution.sql
-- ==============================================================================

USE CUSTOMERS_ORDERS_DB;

-- ------------------------------------------------------------------------------
-- Question 10: Days Between Customer Orders
--
-- Problem Statement:
--   For each order placed by a customer, calculate the number of days that
--   have passed since the customer's immediately previous order.
--
-- Query Requirements:
--   Process orders separately for each customer using customer_id.
--   Use LAG() to retrieve the immediately previous order_date ordered by
--   order_date, order_id. Calculate the number of days between current and
--   previous date. The first order should produce NULL.
--   Sort by customer_name, order_date, order_id.
--
-- Required Output Columns:
--   customer_name, order_id, order_date, days_since_previous_order
-- ------------------------------------------------------------------------------

SELECT 
    c.customer_name,
    o.order_id,
    o.order_date,
    DATEDIFF(
        o.order_date,
        LAG(o.order_date) OVER (
            PARTITION BY o.customer_id 
            ORDER BY o.order_date, o.order_id
        )
    ) AS days_since_previous_order
FROM Orders o
JOIN Customers c 
    ON o.customer_id = c.customer_id
ORDER BY 
    c.customer_name, 
    o.order_date, 
    o.order_id;

-- Note on Expected Output vs Sample Data:
-- In MS1-SQL (1).pdf:
-- 1. If run on the "Sample Data" table (Aarav, Diya, Kabir), the day differences are (NULL, 5, 12) for Aarav,
--    (NULL, 9) for Diya, and (NULL, 10) for Kabir.
-- 2. If run on the "Expected Output" screenshot dataset (Aditi, Bharat), the day differences are
--    (NULL, 4, 4) for Aditi and (NULL) for Bharat.
-- If your assessment requires ISO date formatting, wrap o.order_date with:
-- DATE_FORMAT(o.order_date, '%Y-%m-%dT%H:%i:%s.000Z') AS order_date
