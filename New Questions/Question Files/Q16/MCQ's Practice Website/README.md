# 🚀 SQL & Data Engineering Exam Master • 200 High-Yield MCQs

An ultra-modern, interactive MCQ examination simulator, practice platform, and active recall revision suite built with **React**, **Vite**, and **Tailwind CSS**.

---

## 🌟 Key Features

### 1. 🎯 Practice & Learn Mode
- **200 High-Yield Questions** categorized across 13 core domains.
- **Enhanced Question Navigator**:
  - Direct jump to any question with real-time visual badges:
    - 🟢 **Emerald**: Correctly answered
    - 🔴 **Rose**: Incorrectly answered
    - 🔵 **Cyan / Ring**: Active / Current question
    - 🟡 **Amber Dot**: Starred / Bookmarked
  - Filter by Category, Text Search, Starred questions, or Missed questions.
- **Deep Technical Explanations**: Instant solution reveal with in-depth concept breakdown.
- **Keyboard Shortcuts**: `[1-4]` or `[A-D]` to select options, `[← / →]` for Previous/Next, `[S]` to Star, `[E]` for Explanation.

### 2. ⏱️ Timed Mock Exam Simulator
- **Configurable Presets**:
  - `15 Questions` (15 mins) — Quick Sprint
  - `25 Questions` (25 mins) — Standard Practice
  - `50 Questions` (50 mins) — Half Mock
  - `100 Questions` (1h 40m) — Comprehensive Assessment
  - `All 200 Questions` (3h 20m) — **Full Curriculum Mock**
- **Exam Features**:
  - Live ticking timer with color-coded alerts (< 5m pulse).
  - **Jump Palette** with filter tabs (`All`, `Unanswered`, `Flagged for Review`).
  - **Diagnostic Report**: Overall percentage, readiness rating, domain-by-domain mastery bars, and detailed question review filterable by missed or flagged.

### 3. ⚡ Active Recall Flashcards
- 3D interactive flip cards with question stem on front, verified solution and architectural explanation on back.
- Keyboard support (`[Space]` or `[Enter]` to flip, `[← / →]` to navigate).
- Shuffle random card mode.

### 4. 📑 High-Yield Blueprint Revision Sheet
- Condensed summaries of core architecture formulas, ACID properties, SCD Types, normal forms, and cloud data warehouse design patterns.

### 5. 🎨 Elevated Dark Mode & UI Aesthetics
- OLED-friendly deep slate background (`#020617`), ambient radial glow accents, glassmorphic card containers, and high-contrast typography.
- Seamless one-click Dark / Light mode toggle with persistent state in `localStorage`.

---

## 📚 Curriculum & Question Distribution (200 Questions)

| Domain / Category | Question Count | Topics Covered |
|---|---|---|
| **Handwritten Blueprint** | 15 | Query optimization, SARGability, B-Tree mechanics, Star vs Snowflake |
| **SQL DDL, DML & Constraints** | 17 | DDL/DML, Constraints, TRUNCATE vs DELETE, Data types, NULL logic |
| **Joins & Window Functions** | 31 | INNER/LEFT/FULL/CROSS/Anti-Joins, RANK, DENSE_RANK, ROW_NUMBER, LAG, LEAD, Framing |
| **Subqueries & Views** | 15 | Correlated subqueries, Scalar subqueries, CTEs, Materialized views, Updatable views |
| **Advanced SQL** | 8 | Recursive CTEs, Hierarchical queries, GROUP BY ROLLUP/CUBE |
| **TCL & Transactions** | 12 | ACID properties, Isolation levels, Dirty/Phantom reads, Deadlocks, Savepoints |
| **Data Warehousing & Dimensional Modeling** | 22 | Kimball vs Inmon, Fact types, Measure types, Conformed/Role-playing dimensions, OLAP |
| **Slowly Changing Dimensions (SCD)** | 12 | SCD Types 0, 1, 2, 3, 4, 6, Surrogate keys, Late arriving facts/dimensions |
| **Cloud & ETL/ELT** | 15 | Snowflake (Cloning, Time Travel, Micro-partitions), BigQuery, Redshift, Databricks Medallion, dbt, CDC |
| **OLTP vs OLAP & Normalization** | 10 | Workload traits, 1NF, 2NF, 3NF, BCNF, Denormalization, Row vs Column storage |
| **Python & Comp Fundamentals** | 23 | Computational knowledge, Memory references, Mutable/Immutable, Slicing, Generators, Big-O |
| **Indexing & Performance** | 10 | Clustered/Non-clustered, Covering index, Hash join, Bitmap index, Partition pruning |
| **Database Quality & Admin** | 10 | Profiling, Deduplication, COALESCE, NULLIF, Stored procedures, EXPLAIN plans |
| **Total** | **200 Questions** | Complete Exam Mastery |

---

## ⚡ Fast 1-Minute Local Setup

```bash
# 1. Navigate to the project directory
cd "MCQ's Practice Website"

# 2. Install dependencies
npm install

# 3. Start local development server
npm run dev

# 4. Build for production
npm run build
```

---

## 🌐 Instant Deployment Guide

### Option 1: Deploy to Vercel (Fastest • Zero Config)
1. Install Vercel CLI: `npm i -g vercel` (or visit [vercel.com](https://vercel.com)).
2. In the `MCQ's Practice Website` folder, run:
   ```bash
   vercel
   ```
3. Follow the 3-step prompt. Your site will be live on a global CDN in under 30 seconds!

### Option 2: Deploy to Netlify
1. Run `npm run build` to generate the `dist` folder.
2. Go to [app.netlify.com/drop](https://app.netlify.com/drop) and drag-and-drop the `dist` folder.
3. Your application is instantly deployed!

### Option 3: Automated GitHub Pages Deployment
A GitHub Actions workflow is already pre-configured in `.github/workflows/deploy.yml`.

1. Push this folder to your GitHub repository:
   ```bash
   git add "MCQ's Practice Website"
   git commit -m "Add MCQ Practice Website with 200 Questions"
   git push origin main
   ```
2. In your GitHub repository:
   - Go to **Settings** → **Pages**.
   - Under **Build and deployment** → **Source**, select **GitHub Actions**.
3. Every `git push` will now automatically build and publish the website to:
   `https://<your-username>.github.io/<repo-name>/`

---

## 📂 Project Structure

```
MCQ's Practice Website/
├── .github/
│   └── workflows/
│       └── deploy.yml        # Automated GitHub Pages CI/CD
├── dist/                     # Production build artifacts
├── public/                   # Static assets & icons
├── src/
│   ├── data/
│   │   ├── categories.js     # Filter categories
│   │   ├── cheatsheet.js     # Architecture cheat sheet data
│   │   └── questions.js      # All 200 verified questions
│   ├── App.jsx               # Main React application
│   ├── index.css             # Tailwind styling & dark mode glow effects
│   └── main.jsx              # Application bootstrap
├── index.html                # HTML entry point with modern typography
├── package.json              # Dependencies and scripts
├── postcss.config.js         # PostCSS configuration
├── tailwind.config.js        # Tailwind design system configuration
├── vite.config.js            # Vite build configuration with base relative paths
└── README.md                 # Documentation
```
