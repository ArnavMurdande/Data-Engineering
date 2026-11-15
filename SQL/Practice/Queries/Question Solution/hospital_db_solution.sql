-- ==============================================================================
-- Database: HOSPITAL_DB
-- Solution File: hospital_db_solution.sql
-- ==============================================================================

USE HOSPITAL_DB;

-- ------------------------------------------------------------------------------
-- Question 4: Highest-Revenue Doctor per Department
--
-- Problem Statement:
--   A hospital administration system tracks appointments and billing for doctors
--   across multiple departments. Generate a report showing the top-earning
--   doctors within each department based on total billed amount.
--
-- Query Requirements:
--   For every doctor, compute the department name, doctor name, total revenue
--   (sum of all bill amounts), and rank within department. Use RANK()
--   (not ROW_NUMBER) ordered by total revenue descending so ties share the
--   same rank.
--
-- Required Output Columns:
--   department_name, doctor_name, total_revenue, revenue_rank
-- ------------------------------------------------------------------------------

SELECT 
    dept.department_name,
    doc.doctor_name,
    SUM(b.amount) AS total_revenue,
    RANK() OVER (
        PARTITION BY dept.dept_id 
        ORDER BY SUM(b.amount) DESC
    ) AS revenue_rank
FROM Doctors doc
JOIN Departments dept 
    ON doc.dept_id = dept.dept_id
JOIN Appointments a 
    ON doc.doctor_id = a.doctor_id
JOIN Bills b 
    ON a.appointment_id = b.appointment_id
GROUP BY 
    dept.dept_id, 
    dept.department_name, 
    doc.doctor_id, 
    doc.doctor_name
ORDER BY 
    dept.department_name, 
    revenue_rank;
