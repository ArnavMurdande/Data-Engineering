# ⚡ Data Engineering & SQL Master Hub

🔗 **Live Website:** [https://arnavmurdande.github.io/Data-Engineering/](https://arnavmurdande.github.io/Data-Engineering/)

[![GitHub Pages](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-success?style=for-the-badge&logo=github)](https://arnavmurdande.github.io/Data-Engineering/)
[![React](https://img.shields.io/badge/React-18-blue?style=for-the-badge&logo=react)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-6-purple?style=for-the-badge&logo=vite)](https://vitejs.dev/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind-3.4-38bdf8?style=for-the-badge&logo=tailwindcss)](https://tailwindcss.com/)
[![Python](https://img.shields.io/badge/Python-3.12+-3776ab?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479a1?style=for-the-badge&logo=mysql&logoColor=white)](https://mysql.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](./LICENSE)

A structured, production-grade repository containing interactive exam preparation tools, relational database schemas, dynamic Python unit-testing suites, and practice question patterns for **SQL, Kimball Dimensional Modeling, Cloud Data Warehouses, Python (OOPs, Pandas, NumPy), and Data Engineering Assessments**.

---

## 📂 Repository Architecture

```
Data-Engineering/
├── 🚀 MCQ's Practice Website/          # Full-stack Interactive Exam & Practice Web Application
│   ├── src/                            # React 18 Application Source Code
│   │   ├── data/                       # Curated Technical Learning Content
│   │   │   ├── questions.js            # 200 High-Yield MCQs with In-Depth Technical Explanations
│   │   │   ├── categories.js           # 13 Domain Categories (SQL, Warehousing, Modeling, etc.)
│   │   │   └── cheatsheet.js           # Architecture Cheat Sheets & SQL Formula Summaries
│   │   ├── App.jsx                     # Core UI with Dark/Light Modes, Exam Simulator & Filters
│   │   ├── index.css                   # Custom Scrollbars, Glassmorphic & Glow Styles
│   │   └── main.jsx                    # Application Entry Point
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
│
├── 📚 Milestone 1/                      # Complete L&T Milestone 1 Exam Preparation Suite
│   ├── Python Practice/                # Python OOPs, Pandas, NumPy Practice & Automated Evaluator
│   │   ├── Python Milestone Practice.py# Interactive student workspace with auto-test runner hook
│   │   ├── Python Practice Material/   # Foundational syntax guides and reference notes
│   │   ├── Python Practice Questions and Tests/
│   │   │   ├── Questions/              # 17 Questions with Problem Statements & Solutions
│   │   │   │   ├── OOPS/               # 6 Object-Oriented Design Scenarios
│   │   │   │   ├── Pandas/             # 6 Data Cleaning, Grouping & Aggregation Problems
│   │   │   │   └── NumPy/              # 5 Vectorized Analytics & Statistical Array Problems
│   │   │   └── test/test_runner.py     # Dynamic Evaluator (10 test cases/question, 170 test assertions)
│   │   └── Python Questions Solutions/ # Modular solution-only scripts organized by domain
│   │
│   ├── SQL Practice/                   # 9 Relational Databases, DDL/DML Schemas & Query Solutions
│   │   ├── Queries/
│   │   │   ├── Practice.sql            # Active SQL query development and testing scratchpad
│   │   │   └── Question Solution/      # 9 Verified reference solutions for 10 exam scenarios
│   │   ├── SQL Milestone DB Setup/     # DDL & DML initialization scripts for all 9 databases
│   │   └── SQL Practice Questions and Material/ # Curated problem statements & reference materials
│   │
│   ├── Milestone 1 Questions/          # Official Assessment PDFs and Reference Word Documents
│   ├── Milestone 1 Portion/            # Syllabus breakdown & exam planning roadmap
│   └── README.md                       # Comprehensive Milestone 1 documentation & index
│
├── ⚙️ .github/workflows/deploy.yml      # Automated CI/CD Pipeline for GitHub Pages Deployment
└── 📄 LICENSE                          # MIT License
```

---

## 🌟 Interactive MCQ's Practice Website

An interactive exam simulator and revision web application built with **React 18**, **Vite**, and **TailwindCSS**, hosted directly on GitHub Pages.

### Core Features
1. **200 High-Yield Technical MCQs**:
   - **Advanced SQL**: Joins (Inner, Outer, Self, Cross), Window Functions (`ROW_NUMBER`, `RANK`, `DENSE_RANK`, `LEAD`, `LAG`), Subqueries, CTEs, Aggregations, Grouping Sets, and ACID Transactions.
   - **Data Warehousing & Dimensional Modeling**: Kimball Star/Snowflake schemas, Fact vs Dimension tables, Conformed Dimensions, Slowly Changing Dimensions (SCD Types 0–6), and Grain definition.
   - **Modern Cloud Data Platforms**: Architecture concepts across Snowflake (virtual warehouses, clustering), BigQuery, AWS Redshift, and Databricks Medallion architecture (Bronze, Silver, Gold).
   - **Database Internals & Optimization**: Normalization (1NF through BCNF), Indexing (B-Trees, Hash), Partitions, Execution Plans, and Sharding.
2. **Interactive Study Modes**:
   - 🎯 **Practice & Learn**: Immediate answer validation with granular explanations, starred/missed question filters, and category badges.
   - ⏱️ **Exam Simulator**: Timed assessment mode with ticking timer, question jump palette, question flagging, and configurable attempt counts (15, 25, 50, 100, or all 200 Qs).
   - ⚡ **Active Recall Flashcards**: 3D flip card animations with keyboard shortcut support (`[SPACE]`, `[←/→]`).
   - 📋 **High-Yield Cheat Sheet**: Quick formula, syntax, and architecture pattern review.
3. **Themes & UX**:
   - OLED Dark Mode & High-Contrast Light Mode with local storage persistence.
   - Visual question status matrix (`Correct`, `Wrong`, `Active`, `Starred`).

### Running Locally
```bash
# 1. Clone repository
git clone https://github.com/ArnavMurdande/Data-Engineering.git

# 2. Navigate to the website directory
cd "Data-Engineering/MCQ's Practice Website"

# 3. Install dependencies
npm install

# 4. Start Vite development server
npm run dev
```

---

## 📚 Milestone 1 Preparation Suite

The [`Milestone 1`](./Milestone%201) folder contains comprehensive, end-to-end practice materials for the **L&T Milestone 1 Assessment**:

### 1. Python Practice & Dynamic Test Runner
- **17 Coding Problems** across three essential domains:
  - **OOPs (6 Questions)**: In-memory state tracking, custom validation exceptions (`ValueError`, `KeyError`), seat reservations, inventory dispatches, and bed allocation systems.
  - **Pandas (6 Questions)**: Insurance claims cleaning, e-commerce revenue aggregation, vehicle downtime flags, hotel cancellations, and panel degradation tracking.
  - **NumPy (5 Questions)**: Vectorized air quality indexing, crop yield matrices, network latency percentiles, and streak-scanning algorithms.
- **Dynamic Evaluation Engine (`test_runner.py`)**:
  - Automatically hooks into `Python Milestone Practice.py`.
  - Runs **10 rigorous test cases per question** (170 unit test assertions total).
  - Validates edge cases, empty structures, type correctness, and error conditions without hardcoding.

### 2. SQL Practice & Database Schemas
- **9 Independent Relational Databases** with clean DDL table definitions and DML seed datasets:
  - `ATHLETICS_RESULTS_DB` (Track events, athlete performances)
  - `CUSTOMERS_ORDERS_DB` (Customer purchase history & sequence intervals)
  - `DELIVERY_TRACKING_DB` (Routes, drivers, and delivery completion times)
  - `PATIENT_APPOINTMENTS_DB` (Clinical schedules and appointments)
  - `academic_lms` (Courses, instructors, assignments, and student grades)
  - `hospital_db` (Doctor departments, appointments, and billing revenue)
  - `movie_streaming` (Users, genres, subscription plans, and watch history)
  - `retail_store` (Orders, line-items, products, and customers)
  - `university_core` (Departments, students, enrollments, and course records)
- **10 Scenario-Based Solutions**:
  - Verified implementations for window averages (`AVG() OVER (PARTITION BY ...)`), lagged date differences (`DATEDIFF + LAG`), dense ranking (`DENSE_RANK()`), single-row subqueries, and co-viewed item lookups.

---

## 🌐 Continuous Deployment (GitHub Pages)

The repository includes an automated GitHub Actions workflow (`.github/workflows/deploy.yml`) that automatically builds and deploys the `MCQ's Practice Website` whenever changes are pushed to `main`.

Live site: [https://arnavmurdande.github.io/Data-Engineering/](https://arnavmurdande.github.io/Data-Engineering/)

---

## 📄 License

This repository is open source and licensed under the [MIT License](./LICENSE).
