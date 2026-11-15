# SQL Practice Questions — Database Reference Guide

A master catalog of all practice questions, problem statements, requirements, and reference queries grouped by database in alphabetical / navigator order.

---

## 📑 Database Navigator Index

1. [academic_lms](#1-academic_lms)
2. [athletics_results_db](#2-athletics_results_db)
3. [customers_orders_db](#3-customers_orders_db)
4. [delivery_tracking_db](#4-delivery_tracking_db)
5. [food_delivery_db](#5-food_delivery_db)
6. [gaming_platform_db](#6-gaming_platform_db)
7. [hospital_db](#7-hospital_db)
8. [movie_streaming](#8-movie_streaming)
9. [mysql (System Database)](#9-mysql-system-database)
10. [patient_appointments_db](#10-patient_appointments_db)
11. [retail_store](#11-retail_store)
12. [university_core](#12-university_core)

---

## 1. academic_lms

### Overview

- **Database**: `academic_lms`
- **Tables Involved**: `Courses`, `Assignments`, `Submissions`
- **Solution File**: `SQL Practice/Queries/Question Solution/academic_lms_solution.sql`

### Question: Calculate Average Assignment Score per Course

#### Problem Statement

Calculate the average assignment score per course across all recorded submissions.

#### Requirements

- Join `Courses`, `Assignments`, and `Submissions` tables.
- Group the data by `course_id` and `course_name`.
- Calculate the average score for each course using `AVG(s.score)`.
- Order the result by `avg_score` in descending order.

#### Required Output Columns

`course_name`, `avg_score`

#### Reference Solution

```sql
USE academic_lms;

SELECT 
    c.course_name,
    AVG(s.score) AS avg_score
FROM Courses c
JOIN Assignments a 
    ON c.course_id = a.course_id
JOIN Submissions s 
    ON a.assignment_id = s.assignment_id
GROUP BY 
    c.course_id, 
    c.course_name
ORDER BY 
    avg_score DESC;
```

---

## 2. athletics_results_db

### Overview

- **Database**: `ATHLETICS_RESULTS_DB`
- **Tables Involved**: `Events`, `Athletes`, `Results`
- **Solution File**: `SQL Practice/Queries/Question Solution/athletics_results_db_solution.sql`

### Question: Event Average Finish Time

#### Problem Statement

Generate a report that, for every recorded track performance, displays the event name, athlete name, finish time in seconds, and the average finish time of all recorded performances within the same event.

#### Requirements

- Use the `AVG()` window function partitioned by `r.event_id` to compute the event average.
- Filter only performances where `status = 'Recorded'` (exclude `Disqualified` or `DNS`).
- Round the computed average to 2 decimal places using `ROUND(..., 2)`.
- Sort the results by `event_name`, `finish_time`, and `athlete_name`.

#### Required Output Columns

`event_name`, `athlete_name`, `finish_time`, `avg_event_time`

#### Reference Solution

```sql
USE ATHLETICS_RESULTS_DB;

SELECT 
    e.event_name,
    a.athlete_name,
    r.finish_time,
    ROUND(
        AVG(r.finish_time) OVER (PARTITION BY r.event_id), 
        2
    ) AS avg_event_time
FROM Results r
JOIN Events e 
    ON r.event_id = e.event_id
JOIN Athletes a 
    ON r.athlete_id = a.athlete_id
WHERE r.status = 'Recorded'
ORDER BY 
    e.event_name, 
    r.finish_time, 
    a.athlete_name;
```

---

## 3. customers_orders_db

### Overview

- **Database**: `CUSTOMERS_ORDERS_DB`
- **Tables Involved**: `Customers`, `Orders`
- **Solution File**: `SQL Practice/Queries/Question Solution/customers_orders_db_solution.sql`

### Question: Days Between Customer Orders

#### Problem Statement

For each order placed by a customer, calculate the number of days that have passed since the customer's immediately previous order.

#### Requirements

- Process orders separately for each customer using `customer_id`.
- Use the `LAG()` window function to retrieve the immediately preceding `order_date`, partitioned by `customer_id` and ordered by `order_date, order_id`.
- Compute the elapsed days using `DATEDIFF()`.
- The first order for any customer will naturally return `NULL`.
- Sort the output by `customer_name`, `order_date`, and `order_id`.

#### Required Output Columns

`customer_name`, `order_id`, `order_date`, `days_since_previous_order`

#### Reference Solution

```sql
USE CUSTOMERS_ORDERS_DB;

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
```

*(Note: If ISO formatting is required by your assessment platform, format `order_date` using `DATE_FORMAT(o.order_date, '%Y-%m-%dT%H:%i:%s.000Z')`.)*

---

## 4. delivery_tracking_db

### Overview

- **Database**: `DELIVERY_TRACKING_DB`
- **Tables Involved**: `Routes`, `Drivers`, `Deliveries`
- **Solution File**: `SQL Practice/Queries/Question Solution/delivery_tracking_db_solution.sql`

### Question: Average Delivery Time by Route

#### Problem Statement

Generate a report for every completed delivery showing the route name, driver name, delivery time, and the average delivery time of all completed deliveries within the same route.

#### Requirements

- Use the `AVG()` window function with `PARTITION BY del.route_id`.
- Filter strictly for completed deliveries where `status = 'Completed'`.
- Round the computed average route time to 2 decimal places (`ROUND(..., 2)`).
- Sort the results by `route_name`, `delivery_time`, and `driver_name`.

#### Required Output Columns

`route_name`, `driver_name`, `delivery_time`, `avg_route_time`

#### Reference Solution

```sql
USE DELIVERY_TRACKING_DB;

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
```

---

## 5. food_delivery_db

### Overview

- **Database**: `FOOD_DELIVERY_DB`
- **Tables Involved**: `Payments`
- **Solution File**: `SQL Practice/Extra Questions/01_most_popular_payment_method.sql`

### Question: Most Popular Payment Method

#### Problem Statement

A food-delivery company maintains customer transaction records in the `Payments` table. Each transaction is assigned a payment method such as `'UPI'`, `'Card'`, `'Cash'`, or `'Wallet'`. Generate a report that identifies the single most frequently occurring payment method.

#### Requirements

- For each payment method, calculate the total number of transactions associated with it.
- Determine which method has the highest occurrence count.
- If multiple payment methods share the same highest count, sort by transaction count in descending order and then by payment method in ascending alphabetical order, and return only the top method.
- **Constraint**: Do not use window functions (`LIMIT 1` with `GROUP BY` and `ORDER BY`).

#### Required Output Columns

`payment_method`, `method_count`

#### Reference Solution

```sql
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
```

---

## 6. gaming_platform_db

### Overview

- **Database**: `GAMING_PLATFORM_DB`
- **Tables Involved**: `Games`, `Players`, `Scores`
- **Solution File**: `SQL Practice/Extra Questions/02_fastest_score_per_game.sql`

### Question: Fastest Score / Rank per Game

#### Problem Statement

An online gaming platform maintains match performance data for multiple games. Each game has multiple players participating, and each player's score is stored in the `Scores` table. Generate a report that, for every valid recorded score, displays the game name, player name, score, and rank within that game based on score (highest = rank 1).

#### Requirements

- Only include scores where `status = 'Recorded'` (exclude `Disqualified` and `Pending`).
- Use `ROW_NUMBER()` (not `RANK()`), ensuring every performance receives a unique rank within the game.
- Partition by `game_id` and order by `score DESC`, `player_name ASC` to break ties deterministically.
- Order the final report by `game_name ASC` and `rank_in_game ASC`.

#### Required Output Columns

`game_name`, `player_name`, `score`, `rank_in_game`

#### Reference Solution

```sql
USE GAMING_PLATFORM_DB;

SELECT 
    g.game_name,
    p.player_name,
    s.score,
    ROW_NUMBER() OVER (
        PARTITION BY s.game_id 
        ORDER BY s.score DESC, p.player_name ASC
    ) AS rank_in_game
FROM Scores s
JOIN Games g 
    ON s.game_id = g.game_id
JOIN Players p 
    ON s.player_id = p.player_id
WHERE s.status = 'Recorded'
ORDER BY 
    g.game_name ASC, 
    rank_in_game ASC;
```

---

## 7. hospital_db

### Overview

- **Database**: `HOSPITAL_DB`
- **Tables Involved**: `Departments`, `Doctors`, `Appointments`, `Bills`
- **Solution File**: `SQL Practice/Queries/Question Solution/hospital_db_solution.sql`

### Question: Highest-Revenue Doctor per Department

#### Problem Statement

A hospital administration system tracks appointments and billing for doctors across multiple departments. Generate a report showing the doctors ranked within each department based on total billed revenue.

#### Requirements

- For every doctor, compute the department name, doctor name, total billed revenue (`SUM(b.amount)`), and their rank within the department.
- Use `RANK()` (not `ROW_NUMBER()`) partitioned by `dept_id` ordered by total revenue descending so ties share the same rank.
- Sort the result by `department_name` and `revenue_rank`.

#### Required Output Columns

`department_name`, `doctor_name`, `total_revenue`, `revenue_rank`

#### Reference Solution

```sql
USE HOSPITAL_DB;

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
```

---

## 8. movie_streaming

### Overview

- **Database**: `movie_streaming`
- **Tables Involved**: `Movies`, `Watch_History`
- **Solution File**: `SQL Practice/Queries/Question Solution/movie_streaming_solution.sql`

### Question: Movies Watched by Viewers of 'Life of Pi'

#### Problem Statement

List all distinct movies that have been watched by any user who has watched the movie `'Life of Pi'`.

#### Requirements

- Retrieve `movie_id` and `title`.
- Eliminate duplicates using `DISTINCT`.
- Use a subquery to find all `user_id`s who have watched `'Life of Pi'`.
- Filter outer watch history records to those users.
- Sort the result by `movie_id`.

#### Required Output Columns

`movie_id`, `title`

#### Reference Solution

```sql
USE movie_streaming;

SELECT DISTINCT
    m.movie_id,
    m.title
FROM Movies m
JOIN Watch_History wh 
    ON m.movie_id = wh.movie_id
WHERE wh.user_id IN (
    SELECT wh_sub.user_id
    FROM Watch_History wh_sub
    JOIN Movies m_sub 
        ON wh_sub.movie_id = m_sub.movie_id
    WHERE m_sub.title = 'Life of Pi'
)
ORDER BY 
    m.movie_id;
```

---

## 9. mysql (System Database)

### Overview

- **Database**: `mysql`
- **Description**: Built-in MySQL System Catalog & Data Dictionary.
- **Note**: This database contains server metadata, user account privileges, character sets, and time zone information. It does not host candidate practice problems.

---

## 10. patient_appointments_db

### Overview

- **Database**: `PATIENT_APPOINTMENTS_DB`
- **Tables Involved**: `Patients`, `Appointments`
- **Solution File**: `SQL Practice/Queries/Question Solution/patient_appointments_db_solution.sql`

### Question: Days Between Patient Appointments

#### Problem Statement

For each appointment, calculate the number of days that have passed since the patient's immediately previous appointment.

#### Requirements

- Partition appointments separately for each patient using `patient_id`.
- Use `LAG()` over `appointment_date` ordered by `appointment_date, appointment_id`.
- Calculate the difference in days using `DATEDIFF()`.
- The first appointment for each patient will have `days_since_previous_appointment` as `NULL`.
- Sort results by `patient_name`, `appointment_date`, and `appointment_id`.

#### Required Output Columns

`patient_name`, `appointment_id`, `appointment_date`, `days_since_previous_appointment`

#### Reference Solution

```sql
USE PATIENT_APPOINTMENTS_DB;

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
```

---

## 11. retail_store

### Overview

- **Database**: `retail_store`
- **Tables Involved**: `Customers`, `Orders`
- **Solution File**: `SQL Practice/Queries/Question Solution/retail_store_solution.sql`

### Question: Customer with the Highest Value Order

#### Problem Statement

Management wants to identify which customer placed the single highest-value order. Find and return the customer's name along with the `order_id` and `total_amount` of that order.

#### Requirements

- Use a single-row subquery to locate the maximum `total_amount` in the `Orders` table (`WHERE o.total_amount = (SELECT MAX(total_amount) FROM Orders)`).
- Join `Orders` with `Customers` on `customer_id`.

#### Required Output Columns

`order_id`, `customer_name`, `total_amount`

#### Reference Solution

```sql
USE retail_store;

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
```

---

## 12. university_core

### Overview

- **Database**: `university_core`
- **Tables Involved**: `Students`, `Courses`, `Enrollments`, `Departments`
- **Solution File**: `SQL Practice/Queries/Question Solution/university_core_solution.sql`

---

### Question A: Student Enrollments with Grades and Department Names

#### Problem Statement

Generate a report listing every student along with the courses they are enrolled in, the grades they have received, and the departments offering those courses.

#### Requirements

- Join `Students`, `Enrollments`, `Courses`, and `Departments`.
- Select `student_id`, student name, `course_id`, course name, `grade`, and department name.
- Sort by `student_id` and `course_id`.

#### Required Output Columns

`student_id`, `student_name`, `course_id`, `course_name`, `grade`, `department_name`

#### Reference Solution

```sql
USE university_core;

SELECT 
    s.student_id,
    s.name AS student_name,
    c.course_id,
    c.course_name,
    e.grade,
    d.department_name
FROM Enrollments e
JOIN Students s 
    ON e.student_id = s.student_id
JOIN Courses c 
    ON e.course_id = c.course_id
JOIN Departments d 
    ON c.department_id = d.department_id
ORDER BY 
    s.student_id, 
    c.course_id;
```

---

### Question B: Students Ranked by Course Enrollments

#### Problem Statement

Rank students based on the total number of courses in which they are enrolled.

#### Requirements

- Count the total course enrollments per student using `LEFT JOIN` on `Enrollments` so students with zero enrollments are retained.
- Compute both `RANK()` and `DENSE_RANK()` based on course count in descending order.
- Sort the final result by `rank_by_enrollments` and `student_id`.

#### Required Output Columns

`student_id`, `name`, `course_count`, `rank_by_enrollments`, `dense_rank_by_enrollments`

#### Reference Solution

```sql
USE university_core;

SELECT 
    s.student_id,
    s.name,
    COUNT(e.course_id) AS course_count,
    RANK() OVER (
        ORDER BY COUNT(e.course_id) DESC
    ) AS rank_by_enrollments,
    DENSE_RANK() OVER (
        ORDER BY COUNT(e.course_id) DESC
    ) AS dense_rank_by_enrollments
FROM Students s
LEFT JOIN Enrollments e 
    ON s.student_id = e.student_id
GROUP BY 
    s.student_id, 
    s.name
ORDER BY 
    rank_by_enrollments, 
    s.student_id;
```
