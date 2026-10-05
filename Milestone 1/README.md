# 📚 Milestone 1 — Complete Preparation & Practice Hub

Comprehensive preparation material, practical questions, automated unit tests, relational schemas, and reference solutions for **L&T Milestone 1 (Python & SQL)**.

---

## 🗂️ Directory Overview

```
Milestone 1/
├── Milestone 1 Portion/              # Syllabus breakdown & exam planning roadmap
├── Milestone 1 Questions/            # Official question PDFs and Word documents
│   ├── Python/                       # Python problem sets, sample tests, and solutions
│   └── SQL/                          # SQL scenario-based problem docs & PDFs
├── Python Practice/                  # Python OOPs, Pandas, NumPy practice and automated tests
│   ├── Python Milestone Practice.py  # Interactive student practice workspace with auto-test runner hook
│   ├── Python Practice Material/     # Core learning materials & cheat sheets
│   ├── Python Practice Questions and Tests/
│   │   ├── Questions/                # Problem statements + solutions (OOPS, Pandas, NumPy)
│   │   └── test/test_runner.py       # Dynamic test runner (10 test cases per question, 200 total test assertions)
│   ├── Python Questions Solutions/   # Solution-only scripts categorized by domain
│   └── Extra Questions/              # Extra practice questions with complete solutions & test suites
│       ├── OOPS/                     # LibraryInventorySystem
│       ├── Pandas/                   # DeliveryTimeAnalyzer
│       └── NumPy/                    # MovieRatingAnalyzer
└── SQL Practice/                     # Relational databases, schemas, queries, and verified solutions
    ├── Queries/                      # Working scratch queries & reference solutions
    │   ├── Practice.sql              # Active practice script
    │   └── Question Solution/        # Tested solution files for all scenario-based questions
    ├── SQL Milestone DB Setup/       # Database creation & seed data scripts
    ├── SQL Practice Questions and Material/ # Curated problem lists and comprehensive reference guides
    └── Extra Questions/              # Extra scenario-based SQL questions & database setups
        ├── DB Setup/                 # FOOD_DELIVERY_DB and GAMING_PLATFORM_DB scripts
        ├── 01_most_popular_payment_method.sql
        └── 02_fastest_score_per_game.sql
```

---

## 🚀 Quick Start Guide

### 1. Python Practice & Automated Tests
1. Open `Python Practice/Python Milestone Practice.py`.
2. Implement your solutions in the designated functions/classes.
3. Run the file:
   ```bash
   python "Python Practice/Python Milestone Practice.py"
   ```
   *The dynamic test suite will automatically evaluate your implementations across 170 test assertions and report your score.*

### 2. SQL Practice & Database Schemas
1. Start your local MySQL server instance.
2. Run any schema setup script from `SQL Practice/SQL Milestone DB Setup/` to initialize databases and sample data.
3. Practice queries in `SQL Practice/Queries/Practice.sql` and verify against reference solutions in `SQL Practice/Queries/Question Solution/`.

---

## 🐍 Python Practice

### Topics & Question Breakdown
1. **OOPs (Object-Oriented Programming)**:
   - `oops_01_supply_chain_inventory`: In-memory stock tracker, replenishment, dispatch, exceptions.
   - `oops_02_employee_performance_tracker`: Employee ratings, dynamic promotion eligibility.
   - `oops_03_flight_reservation_system`: Seat booking, cancellation, and seat map checks.
   - `oops_04_hospital_bed_allocation`: Ward capacities, patient admissions, and discharge handling.
   - `oops_05_online_examination_system`: Score recording, percentiles, and passing thresholds.
   - `oops_06_museum_loan_registry`: Artifact loan state transitions and member lookups.

2. **Pandas (Data Cleaning & Aggregation)**:
   - `pandas_01_insurance_claim_processing`: Missing data cleaning, claim settlement categorization, branch summaries.
   - `pandas_02_e_commerce_order_processing`: Multi-item orders, revenue calculation, delivery status filtering.
   - `pandas_03_fitness_tracker`: Calorie expenditures, outlier handling, weekly activity metrics.
   - `pandas_04_fleet_vehicle_maintenance`: Service records, downtime analysis, overdue maintenance flags.
   - `pandas_05_hotel_reservation`: Booking trends, lead-time grouping, cancellation rate metrics.
   - `pandas_06_solar_maintenance_analyzer`: Panel efficiency, degradation trends, cleaning alerts.

3. **NumPy (Vectorized Analytics & Statistics)**:
   - `numpy_01_city_air_quality_aqi_analyzer`: Vectorized AQI computation, statistical bounds, category mapping.
   - `numpy_02_crop_yield_irrigation_analyzer`: Multi-zone yield matrices, irrigation efficiency scores.
   - `numpy_03_telecom_network_latency`: Latency percentiles, peak window detection, SLA threshold breaches.
   - `numpy_04_manufacturing_defect_rate`: Quality control arrays, consecutive defect run streaks.
   - `numpy_05_cold_storage_temperature_analyzer`: Temperature validation, thermal threshold alerts, streak scanning.

### 🧪 Automated Dynamic Test Runner
The test runner in `Python Practice/Python Practice Questions and Tests/test/test_runner.py`:
- Automatically scans your code in `Python Milestone Practice.py`.
- Runs **10 comprehensive test cases per question** (170 total test assertions).
- Tests edge cases, empty structures, custom exceptions (`ValueError`, `KeyError`), type validations, and numerical limits without hardcoding values.
- Outputs clean score summaries (e.g. `10/10 Passed`) whenever `Python Milestone Practice.py` is run.

---

## 🗄️ SQL Practice

### 9 Relational Databases & Schemas
All setup scripts are located in `SQL Practice/SQL Milestone DB Setup/`:
1. `ATHLETICS_RESULTS_DB.sql`: Athletes, events, and track finish times.
2. `CUSTOMERS_ORDERS_DB.sql`: Customers, orders, and order sequence dates.
3. `DELIVERY_TRACKING_DB.sql`: Routes, drivers, delivery durations, and completion statuses.
4. `PATIENT_APPOINTMENTS_DB.sql`: Patients, appointments, and fees.
5. `academic_lms.sql`: Instructors, courses, assignments, student submissions, and scores.
6. `hospital_db.sql`: Doctors, departments, appointments, and billing records.
7. `movie_streaming.sql`: Users, genres, movies, subscriptions, and watch history.
8. `retail_store.sql`: Customers, products, orders, and line-item purchases.
9. `university_core.sql`: Departments, students, courses, grades, and enrollments.

### Key Query Concepts Covered
- **Window Functions**: `AVG() OVER (PARTITION BY ...)`, `LAG() OVER (...)`, `LEAD()`, `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`.
- **Date Differences**: `DATEDIFF()` combined with lagged dates for customer order intervals.
- **Complex Joins & Aggregates**: Multi-table inner/left joins, `GROUP BY`, `HAVING`, and nested subqueries.
- **Filtering & Conditions**: Single-row subqueries (`MAX`), self-referencing lookups (`IN`), and status-based filtering (`ENUM`).

---

## 🌟 Extra Practice Questions (New)

### Python Extra Questions (`Python Practice/Extra Questions/`)
1. **OOPs**: `LibraryInventorySystem` — Dictionary-based stock tracking, restocking, quantity updates with `KeyError("Not found")`, and available book listings via explicit loops.
2. **Pandas**: `DeliveryTimeAnalyzer` — Multi-DataFrame left joins (`merge`), delivery log statistics, restaurant average delivery times, threshold filtering, and slowest delivery area extraction.
3. **NumPy**: `MovieRatingAnalyzer` — Integer array conversions, array-wide range validation (`np.any`), rating statistics, conditional bonus scaling with clipping, rating categorization, and grade mapping.

*All 3 Python extra questions are integrated into `test_runner.py` with **10 automated unit test cases each** (30 new assertions).*

### SQL Extra Questions (`SQL Practice/Extra Questions/`)
1. **Most Popular Payment Method** (`01_most_popular_payment_method.sql`):
   - Database: `FOOD_DELIVERY_DB` (Table: `Payments`)
   - Uses `COUNT(*)`, `GROUP BY`, and `ORDER BY ... LIMIT 1` without window functions to find the highest-frequency payment method with deterministic alphabetical tie-breaking.
2. **Fastest Score per Game** (`02_fastest_score_per_game.sql`):
   - Database: `GAMING_PLATFORM_DB` (Tables: `Games`, `Players`, `Scores`)
   - Uses `ROW_NUMBER() OVER (PARTITION BY s.game_id ORDER BY s.score DESC, p.player_name ASC)` for unique, deterministic ranking on recorded scores.
