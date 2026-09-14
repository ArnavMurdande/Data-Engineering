-- SQLBook: Code
-- Active: 1788025243381@@127.0.0.1@3306@customers_orders_db
--- Q1 Athlete DB

select e.event_name, a.athlete_name, r.finish_time, ROUND(
        avg(r.finish_time) over (
            partition by
                e.event_id
        ), 2
    ) as 'avg_event_time'
from
    results r
    join events e on e.event_id = r.event_id
    join athletes a on a.athlete_id = r.athlete_id
where
    r.status = 'Recorded'
order by e.event_name, r.finish_time, a.athlete_name;

------------------------------------------------------

-- SQLBook: Code
-- Active: 1788025243381@@127.0.0.1@3306@customers_orders_db
--- Q2 Customers: Days Between Customer Orders

select 
c.customer_name, 
o.order_id, 
DATE_FORMAT(o.order_date, '%Y-%m-%dT%H:%i:%s.000Z') as order_date, 
datediff(o.order_date,lag(o.order_date) over (partition by o.customer_id order by o.order_date, o.order_id)) as days_since_previous_order
from orders o
join customers c on 
c.customer_id = o.customer_id
order by c.customer_name, o.order_date, o.order_id;
-- SQLBook: Code
-- Active: 1788025243381@@127.0.0.1@3306@academic_lms
--- Q3 Academic LMS

select 
c.course_name,
avg(s.score) as 'avg_score'
from assignments a
join submissions s on
s.assignment_id = a.assignment_id
join courses c on
c.course_id = a.course_id
group by
c.course_id,
c.course_name
order by 
avg_score desc;

--- Q3 Academic LMS Alternative Approach

SELECT DISTINCT
c.course_name,
AVG(s.score) OVER(PARTITION BY c.course_id) AS avg_score
FROM courses c
JOIN assignments a ON c.course_id = a.course_id
JOIN submissions s ON a.assignment_id = s.assignment_id
ORDER BY 
avg_score DESC;
-- SQLBook: Code
-- Active: 1788025243381@@127.0.0.1@3306@delivery_tracking_db
--- Q4 Delivery_Tracking_DB

select
r.route_name,
d.driver_name,
o.delivery_time,
round(avg(o.delivery_time) over (partition by r.route_id),2) as 'avg_route_time'
from deliveries as o
join routes r on 
o.route_id = r.route_id
join drivers d on
d.driver_id = o.driver_id
where o.status = 'Completed'
order by  
r.route_name, 
o.delivery_time, 
d.driver_name;
-- SQLBook: Code
-- Active: 1788025243381@@127.0.0.1@3306@patient_appointments_db
--- Q5 Patient_Appointment_DB

SELECT 
p.patient_name,
a.appointment_id,
a.appointment_date,
datediff(a.appointment_date,lag(a.appointment_date) over( partition by p.patient_id order by a.appointment_date, a.appointment_id asc)) as 'days_since_previous_appointment'
FROM appointments a
join patients p ON
p.patient_id = a.patient_id
order by 
p.patient_name, 
a.appointment_date, 
a.appointment_id;
-- SQLBook: Code
-- Active: 1788025243381@@127.0.0.1@3306@hospital_db
--- Q6 Hospital_db

SELECT
department_name,
doctor_name,
total_revenue,
rank() over(partition by department_name order by data1.total_revenue desc) as revenue_rank
from
(select DISTINCT
d.department_name,
do.doctor_name,
sum(b.amount) over(partition by do.doctor_id)as 'total_revenue'
from appointments a
join bills b ON
b.appointment_id = a.appointment_id
join doctors do ON
do.doctor_id = a.doctor_id 
join departments d ON
d.dept_id = do.dept_id) as data1
order by 
department_name,
revenue_rank;
-- SQLBook: Code
-- Active: 1788025243381@@127.0.0.1@3306@movie_streaming
--- Q7 Movie_StreamingDB

select DISTINCT
m.movie_id,
m.title
from movies m
join watch_history w on 
w.movie_id = m.movie_id
where w.user_id in (
    select w1.user_id 
    from watch_history w1
    where w1.movie_id = '902'
);
-- SQLBook: Code
-- Active: 1788025243381@@127.0.0.1@3306@retail_store
--- Q8 Retail Store

select 
o.order_id,
c.name,
o.total_amount
from orders o
join customers c ON
c.customer_id = o.customer_id
where o.total_amount in (
    select 
    max(o1.total_amount)
    from orders o1
)

-- SQLBook: Code
-- Active: 1788025243381@@127.0.0.1@3306@university_core
--- Q9 University_Core

select 
s.student_id,
s.name,
c.course_id,
c.course_name,
e.grade,
d.department_name
from
enrollments e
join students s ON
s.student_id = e.student_id
join courses c on
c.course_id = e.course_id
join departments d ON
d.department_id = c.department_id   
order by 
s.student_id, 
c.course_id;


--- Q10 University_Core

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
