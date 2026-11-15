-- ==============================================================================
-- Database: PATIENT_APPOINTMENTS_DB
-- Solution File: patient_appointments_db_solution.sql
-- ==============================================================================

USE PATIENT_APPOINTMENTS_DB;

-- ------------------------------------------------------------------------------
-- Question 8: Days Between Patient Appointments
--
-- Problem Statement:
--   For each appointment, calculate the number of days that have passed since
--   the patient's immediately previous appointment.
--
-- Query Requirements:
--   Partition appointments separately for each patient using patient_id.
--   Use LAG() to retrieve the previous appointment_date ordered by
--   appointment_date, appointment_id. Calculate the days difference between
--   current and previous date. For the first appointment,
--   days_since_previous_appointment should be NULL.
--   Sort by patient_name, appointment_date, appointment_id.
--
-- Required Output Columns:
--   patient_name, appointment_id, appointment_date, days_since_previous_appointment
-- ------------------------------------------------------------------------------

SELECT 
    p.patient_name,
    a.appointment_id,
    a.appointment_date,
    DATEDIFF(
        a.appointment_date,
        LAG(a.appointment_date) OVER (
            PARTITION BY a.patient_id 
            ORDER BY a.appointment_date, a.appointment_id
        )
    ) AS days_since_previous_appointment
FROM Appointments a
JOIN Patients p 
    ON a.patient_id = p.patient_id
ORDER BY 
    p.patient_name, 
    a.appointment_date, 
    a.appointment_id;
