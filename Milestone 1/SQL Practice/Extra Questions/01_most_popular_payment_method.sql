-- ==============================================================================
-- Question 1: Most Popular Payment Method (Table: Payments)
-- ==============================================================================
-- Problem Statement:
--   A food-delivery company maintains customer transaction records in the
--   Payments table. Each transaction is assigned a payment method such as
--   'UPI', 'Card', 'Cash', or 'Wallet'. You are asked to generate a report
--   that identifies the most frequently occurring payment method.
--
-- Requirements:
--   - For each payment method, calculate the total number of transactions
--     associated with it.
--   - Determine which method has the highest occurrence count.
--   - If multiple payment methods have the same highest count, sort by
--     transaction count in descending order and then by payment method in
--     ascending order, and return only the top method.
--   - Note: No Window function.
--
-- Required Output Columns:
--   payment_method, method_count
-- ==============================================================================

USE FOOD_DELIVERY_DB;

SELECT 
    payment_method, 
    COUNT(*) AS method_count
FROM Payments
GROUP BY 
    payment_method
ORDER BY 
    method_count DESC, 
    payment_method ASC
LIMIT 1;
