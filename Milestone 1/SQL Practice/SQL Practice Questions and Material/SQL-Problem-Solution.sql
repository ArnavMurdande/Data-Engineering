# LTMB12 SQL Practice - Set 1
# Complete Solutions WITHOUT CTE

-- Database:
-- hospital_db

-- Tables:
-- patients
-- doctors
-- appointments
-- billing
-- treatments
-- medicines
-- prescriptions
-- appointment_audit

-- = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = EASY LEVEL = = = 

CREATE DATABASE HospitalDB;
USE HospitalDB;

-- 1. PATIENTS TABLE
CREATE TABLE patients (
    patient_id INT PRIMARY KEY,
    patient_name VARCHAR(100),
    gender VARCHAR(10),
    age INT,
    city VARCHAR(50)
);

INSERT INTO patients VALUES
(1, 'Rahul', 'Male', 35, 'Chennai'),
(2, 'Priya', 'Female', 28, 'Bangalore'),
(3, 'Arun', 'Male', 45, 'Hyderabad'),
(4, 'Sneha', 'Female', 31, 'Mumbai'),
(5, 'Kiran', 'Male', 50, 'Delhi'),
(6, 'Ramesh Kumar', 'Male', 42, 'Chennai'),
(7, 'Lakshmi Devi', 'Female', 36, 'Coimbatore'),
(8, 'Suresh Babu', 'Male', 29, 'Madurai'),
(9, 'Anitha Rao', 'Female', 55, 'Bangalore'),
(10, 'Vijay Sharma', 'Male', 61, 'Mumbai'),
(11, 'Deepa Nair', 'Female', 48, 'Kochi'),
(12, 'Karthik Raj', 'Male', 34, 'Chennai'),
(13, 'Meena Patel', 'Female', 40, 'Ahmedabad'),
(14, 'Rohit Singh', 'Male', 27, 'Delhi'),
(15, 'Pooja Gupta', 'Female', 31, 'Hyderabad'),
(16, 'Naveen Kumar', 'Male', 45, 'Pune'),
(17, 'Shalini Verma', 'Female', 52, 'Lucknow'),
(18, 'Ajay Das', 'Male', 38, 'Kolkata'),
(19, 'Neha Reddy', 'Female', 24, 'Hyderabad'),
(20, 'Manoj Jain', 'Male', 58, 'Jaipur');

-- 2. DOCTORS TABLE
CREATE TABLE doctors (
    doctor_id INT PRIMARY KEY,
    doctor_name VARCHAR(100),
    specialization VARCHAR(50),
    consultation_fee DECIMAL(10,2)
);

INSERT INTO doctors VALUES
(101, 'Dr. Kumar', 'Cardiology', 1000),
(102, 'Dr. Mehta', 'Neurology', 1500),
(103, 'Dr. Sharma', 'Orthopedics', 1200),
(104, 'Dr. Reddy', 'Dermatology', 800),
(105, 'Dr. Anjali lyer', 'Pediatrics', 900),
(106, 'Dr. Rajesh Gupta', 'ENT', 850),
(107, 'Dr. Vivek Menon', 'General Medicine', 700),
(108, 'Dr. Sunita Shah', 'Gynecology', 1300),
(109, 'Dr. Akash Verma', 'Cardiology', 1200),
(110, 'Dr. Harish Rao', 'Neurology', 1800),
(111, 'Dr. Kavitha Devi', 'Orthopedics', 1400),
(112, 'Dr. Prakash Nair', 'Pulmonology', 1100);

-- 3. APPOINTMENTS TABLE
CREATE TABLE appointments (
    appointment_id INT PRIMARY KEY,
    patient_id INT,
    doctor_id INT,
    appointment_date DATE,
    status VARCHAR(20),
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
);

INSERT INTO appointments VALUES
(1001, 1, 101, '2025-05-01', 'Completed'),
(1002, 2, 102, '2025-05-03', 'Completed'),
(1003, 3, 101, '2025-05-05', 'Pending'),
(1004, 4, 103, '2025-05-06', 'Completed'),
(1005, 5, 104, '2025-05-08', 'Cancelled'),
(1006, 6, 105, '2025-05-10', 'Completed'),
(1007, 7, 106, '2025-05-11', 'Completed'),
(1008, 8, 107, '2025-05-11', 'Completed'),
(1009, 9, 108, '2025-05-12', 'Pending'),
(1010, 10, 109, '2025-05-12', 'Completed'),
(1011, 11, 110, '2025-05-13', 'Completed'),
(1012, 12, 111, '2025-05-13', 'Completed'),
(1013, 13, 112, '2025-05-14', 'Cancelled'),
(1014, 14, 105, '2025-05-14', 'Completed'),
(1015, 15, 106, '2025-05-15', 'Completed'),
(1016, 16, 107, '2025-05-16', 'Pending'),
(1017, 17, 108, '2025-05-17', 'Completed'),
(1018, 18, 109, '2025-05-17', 'Completed'),
(1019, 19, 110, '2025-05-18', 'Completed'),
(1020, 20, 111, '2025-05-18', 'Pending'),
(1021, 1, 112, '2025-05-19', 'Completed'),
(1022, 2, 105, '2025-05-20', 'Completed'),
(1023, 3, 106, '2025-05-20', 'Completed'),
(1024, 4, 107, '2025-05-21', 'Completed'),
(1025, 5, 108, '2025-05-21', 'Cancelled');

-- 4. BILLING TABLE
CREATE TABLE billing (
    bill_id INT PRIMARY KEY,
    appointment_id INT,
    bill_amount DECIMAL(10,2),
    payment_status VARCHAR(20),
    FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id)
);

INSERT INTO billing VALUES
(1, 1001, 1000, 'Paid'),
(2, 1002, 1500, 'Paid'),
(3, 1003, 1000, 'Pending'),
(4, 1004, 1200, 'Paid'),
(5, 1005, 0, 'Cancelled'),
(6, 1006, 900, 'Paid'),
(7, 1007, 850, 'Paid'),
(8, 1008, 700, 'Paid'),
(9, 1009, 1300, 'Pending'),
(10, 1010, 1200, 'Paid'),
(11, 1011, 1800, 'Paid'),
(12, 1012, 1400, 'Paid'),
(13, 1013, 0, 'Cancelled'),
(14, 1014, 900, 'Paid'),
(15, 1015, 850, 'Paid'),
(16, 1016, 700, 'Pending'),
(17, 1017, 1300, 'Paid'),
(18, 1018, 1200, 'Paid'),
(19, 1019, 1800, 'Paid'),
(20, 1020, 1400, 'Pending'),
(21, 1021, 1100, 'Paid'),
(22, 1022, 900, 'Paid'),
(23, 1023, 850, 'Paid'),
(24, 1024, 700, 'Paid'),
(25, 1025, 0, 'Cancelled');

-- 5. TREATMENTS TABLE
CREATE TABLE treatments (
    treatment_id INT PRIMARY KEY,
    appointment_id INT,
    treatment_name VARCHAR(100),
    treatment_cost DECIMAL(10,2),
    FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id)
);

INSERT INTO treatments VALUES
(1, 1001, 'ECG', 500),
(2, 1002, 'Brain Scan', 2500),
(3, 1004, 'Knee X-Ray', 1200),
(4, 1006, 'Vaccination', 300),
(5, 1007, 'Ear Cleaning', 400),
(6, 1008, 'General Checkup', 250),
(7, 1010, 'ECG', 500),
(8, 1011, 'MRI Scan', 3500),
(9, 1012, 'Bone Scan', 1800),
(10, 1014, 'Vaccination', 300),
(11, 1015, 'ENT Checkup', 500),
(12, 1017, 'Pregnancy Scan', 2200),
(13, 1018, 'Stress Test', 900),
(14, 1019, 'Neurology Test', 4000),
(15, 1021, 'Pulmonary Function Test', 1600);

-- 6. MEDICINES TABLE
CREATE TABLE medicines (
    medicine_id INT PRIMARY KEY,
    medicine_name VARCHAR(100),
    medicine_price DECIMAL(10,2)
);

INSERT INTO medicines VALUES
(1, 'Paracetamol', 20),
(2, 'Amoxicillin', 120),
(3, 'Aspirin', 50),
(4, 'Metformin', 180),
(5, 'Atorvastatin', 250),
(6, 'Omeprazole', 90),
(7, 'Cetirizine', 40),
(8, 'Vitamin D', 150);

-- 7. PRESCRIPTIONS TABLE
CREATE TABLE prescriptions (
    prescription_id INT PRIMARY KEY,
    appointment_id INT,
    medicine_id INT,
    quantity INT,
    FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id),
    FOREIGN KEY (medicine_id) REFERENCES medicines(medicine_id)
);

INSERT INTO prescriptions VALUES
(1, 1001, 1, 10),
(2, 1001, 3, 5),
(3, 1002, 2, 7),
(4, 1004, 5, 15),
(5, 1006, 7, 10),
(6, 1007, 6, 5),
(7, 1008, 1, 10),
(8, 1010, 4, 20),
(9, 1011, 5, 30),
(10, 1012, 3, 15),
(11, 1014, 8, 10),
(12, 1015, 7, 5),
(13, 1017, 2, 10),
(14, 1018, 1, 20),
(15, 1019, 5, 15);

-- 8. APPOINTMENT AUDIT TABLE
CREATE TABLE appointment_audit (
    audit_id INT AUTO_INCREMENT PRIMARY KEY,
    appointment_id INT,
    action_type VARCHAR(50),
    action_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

------------------------------------------------------------
-- 1.
-- INNER JOIN Patients
-- with
--     completed appointments
--     and their doctors
------------------------------------------------------------

SELECT p.patient_name, d.doctor_name, a.appointment_date
FROM
    patients p
    INNER JOIN appointments a ON p.patient_id = a.patient_id
    INNER JOIN doctors d ON a.doctor_id = d.doctor_id
WHERE
    a.status = 'Completed';

------------------------------------------------------------
-- 2.
-- LEFT JOIN All appointments
-- with
--     billing information
------------------------------------------------------------

SELECT a.appointment_id, a.appointment_date, b.bill_amount
FROM appointments a
    LEFT JOIN billing b ON a.appointment_id = b.appointment_id;

-- ------------------------------------------------------------
-- 3. SIMPLE SUBQUERY Doctors charging more than average consultation fee
------------------------------------------------------------

SELECT
    doctor_id,
    doctor_name,
    consultation_fee
FROM doctors
WHERE
    consultation_fee > (
        SELECT AVG(consultation_fee)
        FROM doctors
    );

------------------------------------------------------------
-- 4.
-- JOIN + AGGREGATE Number of appointments handled by every doctor
------------------------------------------------------------

SELECT d.doctor_name, COUNT(a.appointment_id) AS total_appointments
FROM doctors d
    LEFT JOIN appointments a ON d.doctor_id = a.doctor_id
GROUP BY
    d.doctor_id,
    d.doctor_name;

------------------------------------------------------------
-- 5.
-- JOIN + AGGREGATE +
-- HAVING
--     Doctors who handled more than 2 appointments
------------------------------------------------------------

SELECT d.doctor_name, COUNT(a.appointment_id) AS total_appointments
FROM doctors d
    INNER JOIN appointments a ON d.doctor_id = a.doctor_id
GROUP BY
    d.doctor_id,
    d.doctor_name
HAVING
    COUNT(a.appointment_id) > 2;

-- = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = MEDIUM LEVEL = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

------------------------------------------------------------
-- 1.
-- JOIN + SUBQUERY Patients who consulted Cardiology doctors
------------------------------------------------------------

SELECT p.patient_name, d.doctor_name, a.appointment_date
FROM
    patients p
    INNER JOIN appointments a ON p.patient_id = a.patient_id
    INNER JOIN doctors d ON a.doctor_id = d.doctor_id
WHERE
    d.doctor_id IN (
        SELECT doctor_id
        FROM doctors
        WHERE
            specialization = 'Cardiology'
    );

------------------------------------------------------------
-- 2.
-- JOIN + AGGREGATE + SUBQUERY Doctors whose total revenue is greater than the average doctor revenue
------------------------------------------------------------

SELECT d.doctor_name, SUM(b.bill_amount) AS total_revenue
FROM
    doctors d
    INNER JOIN appointments a ON d.doctor_id = a.doctor_id
    INNER JOIN billing b ON a.appointment_id = b.appointment_id
GROUP BY
    d.doctor_id,
    d.doctor_name
HAVING
    SUM(b.bill_amount) > (
        SELECT AVG(doctor_revenue)
        FROM (
                SELECT a2.doctor_id, SUM(b2.bill_amount) AS doctor_revenue
                FROM appointments a2
                    INNER JOIN billing b2 ON a2.appointment_id = b2.appointment_id
                GROUP BY
                    a2.doctor_id
            ) AS revenue_table
    );

------------------------------------------------------------
-- 3. ROW_NUMBER Most recent appointment for every patient
------------------------------------------------------------

SELECT
    patient_name,
    appointment_date,
    doctor_name
FROM (
        SELECT p.patient_name, a.appointment_date, d.doctor_name, ROW_NUMBER() OVER (
                PARTITION BY
                    p.patient_id
                ORDER BY a.appointment_date DESC
            ) AS rn
        FROM
            patients p
            INNER JOIN appointments a ON p.patient_id = a.patient_id
            INNER JOIN doctors d ON a.doctor_id = d.doctor_id
    ) AS x
WHERE
    rn = 1;

------------------------------------------------------------
-- 4. RANK Rank doctors based on total billing revenue
------------------------------------------------------------

SELECT
    doctor_name,
    total_revenue,
    RANK() OVER (
        ORDER BY total_revenue DESC
    ) AS revenue_rank
FROM (
        SELECT d.doctor_id, d.doctor_name, SUM(b.bill_amount) AS total_revenue
        FROM
            doctors d
            INNER JOIN appointments a ON d.doctor_id = a.doctor_id
            INNER JOIN billing b ON a.appointment_id = b.appointment_id
        GROUP BY
            d.doctor_id, d.doctor_name
    ) AS x;

------------------------------------------------------------
-- 5. TOP REVENUE DOCTOR IN EACH SPECIALIZATION
------------------------------------------------------------

SELECT
    specialization,
    doctor_name,
    total_revenue
FROM (
        SELECT
            d.specialization, d.doctor_name, SUM(b.bill_amount) AS total_revenue, RANK() OVER (
                PARTITION BY
                    d.specialization
                ORDER BY SUM(b.bill_amount) DESC
            ) AS revenue_rank
        FROM
            doctors d
            INNER JOIN appointments a ON d.doctor_id = a.doctor_id
            INNER JOIN billing b ON a.appointment_id = b.appointment_id
        GROUP BY
            d.doctor_id, d.doctor_name, d.specialization
    ) AS x
WHERE
    revenue_rank = 1;

-- = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 20 SQL JOINS +
-- WINDOW
--     FUNCTION QUESTIONS = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

-- ------------------------------------------------------------
-- 1. LATEST APPOINTMENT FOR EVERY PATIENT
------------------------------------------------------------

SELECT
    patient_name,
    appointment_date,
    doctor_name
FROM (
        SELECT p.patient_name, a.appointment_date, d.doctor_name, ROW_NUMBER() OVER (
                PARTITION BY
                    p.patient_id
                ORDER BY a.appointment_date DESC
            ) AS rn
        FROM
            patients p
            INNER JOIN appointments a ON p.patient_id = a.patient_id
            INNER JOIN doctors d ON a.doctor_id = d.doctor_id
    ) AS x
WHERE
    rn = 1;

------------------------------------------------------------
-- 2. RANK DOCTORS BASED ON CONSULTATION FEES
------------------------------------------------------------

SELECT
    doctor_name,
    specialization,
    consultation_fee,
    RANK() OVER (
        ORDER BY consultation_fee DESC
    ) AS fee_rank
FROM doctors;

------------------------------------------------------------
-- 3. HIGHEST BILL GENERATED BY EACH PATIENT
------------------------------------------------------------

SELECT
    patient_name,
    bill_amount,
    appointment_date
FROM (
        SELECT p.patient_id, p.patient_name, b.bill_amount, a.appointment_date, ROW_NUMBER() OVER (
                PARTITION BY
                    p.patient_id
                ORDER BY b.bill_amount DESC
            ) AS rn
        FROM
            patients p
            INNER JOIN appointments a ON p.patient_id = a.patient_id
            INNER JOIN billing b ON a.appointment_id = b.appointment_id
    ) AS x
WHERE
    rn = 1;

------------------------------------------------------------
-- 4. RANK DOCTORS BY TOTAL REVENUE
------------------------------------------------------------

SELECT
    doctor_name,
    total_revenue,
    RANK() OVER (
        ORDER BY total_revenue DESC
    ) AS revenue_rank
FROM (
        SELECT d.doctor_id, d.doctor_name, SUM(b.bill_amount) AS total_revenue
        FROM
            doctors d
            INNER JOIN appointments a ON d.doctor_id = a.doctor_id
            INNER JOIN billing b ON a.appointment_id = b.appointment_id
        GROUP BY
            d.doctor_id, d.doctor_name
    ) AS x;

------------------------------------------------------------
-- 5. MOST EXPENSIVE TREATMENT HANDLED BY EACH DOCTOR
------------------------------------------------------------

SELECT
    doctor_name,
    treatment_name,
    treatment_cost
FROM (
        SELECT d.doctor_id, d.doctor_name, t.treatment_name, t.treatment_cost, ROW_NUMBER() OVER (
                PARTITION BY
                    d.doctor_id
                ORDER BY t.treatment_cost DESC
            ) AS rn
        FROM
            doctors d
            INNER JOIN appointments a ON d.doctor_id = a.doctor_id
            INNER JOIN treatments t ON a.appointment_id = t.appointment_id
    ) AS x
WHERE
    rn = 1;

------------------------------------------------------------
-- 6. APPOINTMENT NUMBERING FOR PATIENTS
------------------------------------------------------------

SELECT
    patient_name,
    appointment_date,
    ROW_NUMBER() OVER (
        PARTITION BY
            p.patient_id
        ORDER BY a.appointment_date
    ) AS visit_number
FROM patients p
    INNER JOIN appointments a ON p.patient_id = a.patient_id;

------------------------------------------------------------
-- 7. DENSE RANKING OF DOCTORS BY REVENUE
------------------------------------------------------------

SELECT
    doctor_name,
    total_revenue AS revenue,
    DENSE_RANK() OVER (
        ORDER BY total_revenue DESC
    ) AS dense_rank
FROM (
        SELECT d.doctor_id, d.doctor_name, SUM(b.bill_amount) AS total_revenue
        FROM
            doctors d
            INNER JOIN appointments a ON d.doctor_id = a.doctor_id
            INNER JOIN billing b ON a.appointment_id = b.appointment_id
        GROUP BY
            d.doctor_id, d.doctor_name
    ) AS x;

------------------------------------------------------------
-- 8. PREVIOUS APPOINTMENT DATE
------------------------------------------------------------

SELECT
    p.patient_name,
    a.appointment_date AS current_appointment_date,
    LAG(a.appointment_date) OVER (
        PARTITION BY
            p.patient_id
        ORDER BY a.appointment_date
    ) AS previous_appointment_date
FROM patients p
    INNER JOIN appointments a ON p.patient_id = a.patient_id;

------------------------------------------------------------
-- 9. NEXT APPOINTMENT DATE
------------------------------------------------------------

SELECT
    p.patient_name,
    a.appointment_date AS current_appointment_date,
    LEAD(a.appointment_date) OVER (
        PARTITION BY
            p.patient_id
        ORDER BY a.appointment_date
    ) AS next_appointment_date
FROM patients p
    INNER JOIN appointments a ON p.patient_id = a.patient_id;

------------------------------------------------------------
-- 10. HIGHEST REVENUE DOCTOR IN EACH SPECIALIZATION
------------------------------------------------------------

SELECT
    specialization,
    doctor_name,
    total_revenue
FROM (
        SELECT d.specialization, d.doctor_name, SUM(b.bill_amount) AS total_revenue, ROW_NUMBER() OVER (
                PARTITION BY
                    d.specialization
                ORDER BY SUM(b.bill_amount) DESC
            ) AS rn
        FROM
            doctors d
            INNER JOIN appointments a ON d.doctor_id = a.doctor_id
            INNER JOIN billing b ON a.appointment_id = b.appointment_id
        GROUP BY
            d.doctor_id, d.doctor_name, d.specialization
    ) AS x
WHERE
    rn = 1;

------------------------------------------------------------
-- 11. RANK PATIENTS BASED ON TOTAL HOSPITAL SPENDING
------------------------------------------------------------

SELECT
    patient_name,
    total_billing_amount,
    RANK() OVER (
        ORDER BY total_billing_amount DESC
    ) AS patient_rank
FROM (
        SELECT p.patient_id, p.patient_name, SUM(b.bill_amount) AS total_billing_amount
        FROM
            patients p
            INNER JOIN appointments a ON p.patient_id = a.patient_id
            INNER JOIN billing b ON a.appointment_id = b.appointment_id
        GROUP BY
            p.patient_id, p.patient_name
    ) AS x;

------------------------------------------------------------
-- 12. LATEST TREATMENT RECEIVED BY EACH PATIENT
------------------------------------------------------------

SELECT
    patient_name,
    treatment_name,
    appointment_date
FROM (
        SELECT p.patient_id, p.patient_name, t.treatment_name, a.appointment_date, ROW_NUMBER() OVER (
                PARTITION BY
                    p.patient_id
                ORDER BY a.appointment_date DESC
            ) AS rn
        FROM
            patients p
            INNER JOIN appointments a ON p.patient_id = a.patient_id
            INNER JOIN treatments t ON a.appointment_id = t.appointment_id
    ) AS x
WHERE
    rn = 1;

------------------------------------------------------------
-- 13. TOP 2 REVENUE - GENERATING DOCTORS
------------------------------------------------------------

SELECT
    doctor_name,
    total_revenue,
    revenue_rank
FROM (
        SELECT
            doctor_name, total_revenue, RANK() OVER (
                ORDER BY total_revenue DESC
            ) AS revenue_rank
        FROM (
                SELECT d.doctor_id, d.doctor_name, SUM(b.bill_amount) AS total_revenue
                FROM
                    doctors d
                    INNER JOIN appointments a ON d.doctor_id = a.doctor_id
                    INNER JOIN billing b ON a.appointment_id = b.appointment_id
                GROUP BY
                    d.doctor_id, d.doctor_name
            ) AS revenue
    ) AS ranked
WHERE
    revenue_rank <= 2;

------------------------------------------------------------
-- 14. RUNNING REVENUE GENERATED BY EACH DOCTOR
------------------------------------------------------------

SELECT d.doctor_name, a.appointment_date, b.bill_amount, SUM(b.bill_amount) OVER (
        PARTITION BY
            d.doctor_id
        ORDER BY a.appointment_date ROWS BETWEEN UNBOUNDED PRECEDING
            AND CURRENT ROW
    ) AS running_revenue
FROM
    doctors d
    INNER JOIN appointments a ON d.doctor_id = a.doctor_id
    INNER JOIN billing b ON a.appointment_id = b.appointment_id
ORDER BY d.doctor_name, a.appointment_date;

------------------------------------------------------------
-- 15. DIFFERENCE BETWEEN CURRENT AND PREVIOUS  BILL
------------------------------------------------------------

SELECT
    patient_name,
    appointment_date,
    current_bill,
    previous_bill,
    current_bill - previous_bill AS difference
FROM (
        SELECT
            p.patient_name, a.appointment_date, b.bill_amount AS current_bill, LAG(b.bill_amount) OVER (
                PARTITION BY
                    p.patient_id
                ORDER BY a.appointment_date
            ) AS previous_bill
        FROM
            patients p
            INNER JOIN appointments a ON p.patient_id = a.patient_id
            INNER JOIN billing b ON a.appointment_id = b.appointment_id
    ) AS x;

------------------------------------------------------------
-- 16. MOST FREQUENTLY VISITED DOCTOR FOR EACH PATIENT
------------------------------------------------------------

SELECT
    patient_name,
    doctor_name,
    total_visits
FROM (
        SELECT p.patient_id, p.patient_name, d.doctor_id, d.doctor_name, COUNT(*) AS total_visits, ROW_NUMBER() OVER (
                PARTITION BY
                    p.patient_id
                ORDER BY COUNT(*) DESC
            ) AS rn
        FROM
            patients p
            INNER JOIN appointments a ON p.patient_id = a.patient_id
            INNER JOIN doctors d ON a.doctor_id = d.doctor_id
        GROUP BY
            p.patient_id, p.patient_name, d.doctor_id, d.doctor_name
    ) AS x
WHERE
    rn = 1;

------------------------------------------------------------
-- 17. RANK TREATMENTS BY COST WITHIN EACH DOCTOR
------------------------------------------------------------

SELECT
    doctor_name,
    treatment_name,
    treatment_cost,
    RANK() OVER (
        PARTITION BY
            doctor_id
        ORDER BY treatment_cost DESC
    ) AS treatment_rank
FROM (
        SELECT d.doctor_id, d.doctor_name, t.treatment_name, t.treatment_cost
        FROM
            doctors d
            INNER JOIN appointments a ON d.doctor_id = a.doctor_id
            INNER JOIN treatments t ON a.appointment_id = t.appointment_id
    ) AS x;

------------------------------------------------------------
-- 18. FIRST APPOINTMENT OF EVERY PATIENT
------------------------------------------------------------

SELECT
    patient_name,
    appointment_date,
    doctor_name
FROM (
        SELECT p.patient_id, p.patient_name, a.appointment_date, d.doctor_name, ROW_NUMBER() OVER (
                PARTITION BY
                    p.patient_id
                ORDER BY a.appointment_date
            ) AS rn
        FROM
            patients p
            INNER JOIN appointments a ON p.patient_id = a.patient_id
            INNER JOIN doctors d ON a.doctor_id = d.doctor_id
    ) AS x
WHERE
    rn = 1;

------------------------------------------------------------
-- 19. DOCTOR REVENUE CONTRIBUTION PERCENTAGE
------------------------------------------------------------

SELECT
    doctor_name,
    total_revenue AS revenue_generated,
    ROUND(
        total_revenue * 100 / (
            SELECT SUM(bill_amount)
            FROM billing
        ),
        2
    ) AS revenue_contribution_percentage
FROM (
        SELECT d.doctor_id, d.doctor_name, SUM(b.bill_amount) AS total_revenue
        FROM
            doctors d
            INNER JOIN appointments a ON d.doctor_id = a.doctor_id
            INNER JOIN billing b ON a.appointment_id = b.appointment_id
        GROUP BY
            d.doctor_id, d.doctor_name
    ) AS x;

------------------------------------------------------------
-- 20. TOP 3 PATIENTS BY SPENDING IN EACH CITY
------------------------------------------------------------

SELECT
    city,
    patient_name,
    total_billing_amount,
    city_rank
FROM (
        SELECT
            city, patient_name, total_billing_amount, RANK() OVER (
                PARTITION BY
                    city
                ORDER BY total_billing_amount DESC
            ) AS city_rank
        FROM (
                SELECT p.patient_id, p.city, p.patient_name, SUM(b.bill_amount) AS total_billing_amount
                FROM
                    patients p
                    INNER JOIN appointments a ON p.patient_id = a.patient_id
                    INNER JOIN billing b ON a.appointment_id = b.appointment_id
                GROUP BY
                    p.patient_id, p.city, p.patient_name
            ) AS spending
    ) AS ranked
WHERE
    city_rank <= 3;
