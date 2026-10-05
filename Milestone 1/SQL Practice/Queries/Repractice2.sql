-- SQLBook: Code
-- Active: 1788025243381@@127.0.0.1@3306@academic_lms
--- Q1

select DISTINCT
c.course_name,
avg(s.score) over(partition by c.course_id) as 'avg_score'
from  submissions s
join assignments a on 
a.assignment_id = s.assignment_id
join courses c on
c.course_id = a.course_id
order by avg_score desc;

-- SQLBook: Code
-- Active: 1788025243381@@127.0.0.1@3306@athletics_results_db
---Q2
select 
e.event_name,
a.athlete_name,
r.finish_time,
round(avg(r.finish_time) over(partition by e.event_id) ,2)as 'avg_event_time'
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
--- Q3

SELECT
c.customer_name,
o.order_id,
o.order_date,
DATEDIFF(o.order_date, lag(o.order_date) over(PARTITION BY c.customer_id order by o.order_date, o.order_id))
from orders o
join customers c on
c.customer_id = o.customer_id
order by 
c.customer_name ,
o.order_date ,
o.order_id;
-- SQLBook: Code
-- Active: 1788025243381@@127.0.0.1@3306@delivery_tracking_db
--- Q4

select 
r.route_name,
d.driver_name,
di.delivery_time,
avg(di.delivery_time) over(partition by r.route_id)
from deliveries di
join drivers d ON
d.driver_id = di.driver_id
join routes r ON
r.route_id = di.route_id
where di.status = 'Completed'
-- SQLBook: Code
-- Active: 1788025243381@@127.0.0.1@3306@food_delivery_db
--- Q5

select 
p.payment_method,
count(p.payment_method) as 'method_count'
from payments p 
group by p.payment_method
order by 
method_count desc,
p.payment_method asc
limit 1;

-- SQLBook: Code
-- Active: 1788025243381@@127.0.0.1@3306@gaming_platform_db
--- Q6

select 
g.game_name,
p.player_name,
s.score,
row_number() over(partition by g.game_id order by s.score desc) as 'rank_in_game'
from scores s
join games g on 
g.game_id = s.game_id
join players p on 
p.player_id = s.player_id
where s.status = 'Recorded'

-- SQLBook: Code
-- Active: 1788025243381@@127.0.0.1@3306@hospital_db
--- Q7 

select 
department_name,
doctor_name,
total_revenue,
rank() over(PARTITION BY department_name order by data1.total_revenue desc) as 'revenue_rank'
from
(select
d.department_name,
do.doctor_name,
sum(b.amount) as 'total_revenue'
from appointments a 
join doctors do on
do.doctor_id = a.doctor_id
join departments d on 
d.dept_id = do.dept_id
join bills b on 
b.appointment_id = a.appointment_id
group by 
do.doctor_id) as data1
order by
data1.department_name asc,
data1.total_revenue desc; 

-- SQLBook: Code
-- Active: 1788025243381@@127.0.0.1@3306@movie_streaming
--- Q8
select DISTINCT
m.movie_id,
m.title
from movies m 
join watch_history w ON
w.movie_id = m.movie_id
where w.user_id in (select w1.user_id from watch_history w1 where movie_id = '902')

-- SQLBook: Code
-- Active: 1788025243381@@127.0.0.1@3306@patient_appointments_db
--- Q9

SELECT
p.patient_name,
a.appointment_id,
a.appointment_date,
datediff(a.appointment_date, lag(a.appointment_date) over(partition by p.patient_id order by appointment_date asc, a.appointment_id asc)) as 'days_since_previous_appointment'
from appointments a 
join patients p on 
p.patient_id = a.patient_id
order by 
p.patient_name, 
a.appointment_date, 
a.appointment_id;
-- SQLBook: Code
-- Active: 1788025243381@@127.0.0.1@3306@retail_store
--- Q10

SELECT  
o.order_id,
c.name,
o.total_amount 
from orders o 
join customers c ON
c.customer_id = o.customer_id
where o.total_amount in (select max(o1.total_amount) from orders o1) 

-- SQLBook: Code
-- Active: 1788025243381@@127.0.0.1@3306@university_core
--- Q11 AND Q12


---Q11
SELECT
s.student_id,
s.name,
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


--- Q12

SELECT 
s.student_id,
s.name,
count(e.course_id) as 'course_count',
rank() over(order by count(e.course_id) desc) as 'rank_by_enrollments',
DENSE_RANK() over(order by count(e.course_id) desc) as 'dense_rank_by_enrollments'
from enrollments e
join students s on
s.student_id = e.student_id
group by 
s.student_id,
s.name
