-- SQLBook: Code
-- Active: 1788025243381@@127.0.0.1@3306@athletics_results_db
---Repractice Q1

select 
e.event_name,
a.athlete_name,
r.finish_time,
ROUND(avg(r.finish_time) over(partition by e.event_id),2) as 'avg_event_time'
from results r
join athletes a on 
a.athlete_id = r.athlete_id
join events e on
e.event_id = r.event_id
where r.status = 'Recorded'
order by 
e.event_name,
r.finish_time,
a.athlete_name;
-- SQLBook: Code
-- Active: 1788025243381@@127.0.0.1@3306@customers_orders_db
--- Repractice Q2

select 
c.customer_name,
o.order_id,
DATE_FORMAT(o.order_date,'%Y-%m-%dT%H:%i:%s.000z') as order_date,
DATEDIFF(o.order_date,lag(o.order_date)over(partition by c.customer_id order by o.order_date)) as 'days_since_previous_order'
from orders o
join customers c on 
c.customer_id = o.customer_id;
-- SQLBook: Code
-- Active: 1788025243381@@127.0.0.1@3306@delivery_tracking_db
--- Repractice Q3

select 
r.route_name,
d.driver_name,
di.delivery_time,
round(avg(di.delivery_time) over(partition by r.route_id),2) as 'avg_route_time' 
from deliveries di
join drivers d on
d.driver_id = di.driver_id
join routes r on 
r.route_id = di.route_id
where di.status = 'Completed'
order by 
r.route_name,
di.delivery_time,
d.driver_name;
-- SQLBook: Code
-- Active: 1788025243381@@127.0.0.1@3306@patient_appointments_db
--- Repractice Q4 

select 
p.patient_name,
a.appointment_id,
date_format(a.appointment_date,'%Y-%m-%dT%H:%i:%s.000z') as 'appointment_date',
datediff(a.appointment_date,lag(a.appointment_date) over(partition by p.patient_id order by a.appointment_date)) as 'days_since_previous_appointment'
from appointments a
join patients p on 
p.patient_id = a.patient_id
order by 
p.patient_name, 
a.appointment_date, 
a.appointment_id;



-- SQLBook: Code
-- Active: 1788025243381@@127.0.0.1@3306@retail_store
--- Repractice Q5

SELECT
o.order_id,
c.name,
o.total_amount
from orders o
join customers c ON
c.customer_id = o.customer_id
where o.total_amount = (
    select max(o1.total_amount)
    from orders o1
)

-- SQLBook: Code
-- Active: 1788025243381@@127.0.0.1@3306@university_core
--- Repractice Q6 University

select 
s.student_id,
s.name,
c.course_id,
c.course_name,
e.grade,
d.department_name
from enrollments e 
join students s on 
s.student_id = e.student_id
join courses c on 
c.course_id = e.course_id
join departments d on
d.department_id =  s.department_id
order by
s.name;


--- Repractice Q7 University


select
s.student_id,
s.name,
count(e.course_id) as 'course_count',
rank() over(order by count(e.course_id) desc),
dense_rank() over (order by count(e.course_id) desc)
from enrollments e 
join students s on 
s.student_id = e.student_id
group by 
s.student_id,
s.name;
-- SQLBook: Code
-- Active: 1788025243381@@127.0.0.1@3306@movie_streaming
--- Repractice Q8

select 
m.movie_id,
m.title 
from movies m 
join watch_history w on
w.movie_id = m.movie_id
where w.user_id in (
    select w1.user_id 
    from watch_history w1
    where movie_id = '902'
)
group by m.movie_id;

-- SQLBook: Code
-- Active: 1788025243381@@127.0.0.1@3306@hospital_db
--- Repractice Q9 Hospital DB

    SELECT
    department_name,
    doctor_name,
    total_revenue,
    rank() over(PARTITION BY department_name order by data1.total_revenue desc) as 'revenue_rank'
    from
    (select DISTINCT
    d.department_name,
    do.doctor_name,
    sum(b.amount) over(partition by do.doctor_id) as 'total_revenue'
    from appointments a
    join bills b ON
    b.appointment_id = a.appointment_id
    join doctors do ON
    do.doctor_id = a.doctor_id 
    join departments d ON
    d.dept_id = do.dept_id
    ) as data1
    order by 
    department_name,
    revenue_rank;

-- SQLBook: Code
-- Active: 1788025243381@@127.0.0.1@3306@academic_lms
--- Repractice Q10

select DISTINCT
c.course_name,
avg(s.score) over (partition by c.course_id) as 'avg_score'
from submissions s
join assignments a on 
a.assignment_id = s.assignment_id
join courses c on
c.course_id = a.course_id
order by 
avg_score desc;