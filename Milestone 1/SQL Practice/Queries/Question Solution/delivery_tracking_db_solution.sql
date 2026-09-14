-- ==============================================================================
-- Database: DELIVERY_TRACKING_DB
-- Solution File: delivery_tracking_db_solution.sql
-- ==============================================================================

USE DELIVERY_TRACKING_DB;

-- ------------------------------------------------------------------------------
-- Question 7: Average Delivery Time by Route
--
-- Problem Statement:
--   Generate a report for every completed delivery showing the route name,
--   driver name, delivery time, and the average delivery time of all completed
--   deliveries within the same route.
--
-- Query Requirements:
--   Use AVG() as a window function with PARTITION BY route_id. Filter only
--   status = 'Completed'. Round the calculated average delivery time to 2
--   decimal places. Sort by route_name, delivery_time, driver_name.
--
-- Required Output Columns:
--   route_name, driver_name, delivery_time, avg_route_time
-- ------------------------------------------------------------------------------

SELECT 
    r.route_name,
    dr.driver_name,
    del.delivery_time,
    ROUND(
        AVG(del.delivery_time) OVER (PARTITION BY del.route_id), 
        2
    ) AS avg_route_time
FROM Deliveries del
JOIN Routes r 
    ON del.route_id = r.route_id
JOIN Drivers dr 
    ON del.driver_id = dr.driver_id
WHERE del.status = 'Completed'
ORDER BY 
    r.route_name, 
    del.delivery_time, 
    dr.driver_name;
