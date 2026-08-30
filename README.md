# ⚡ Data Engineering & SQL Master Hub

[![GitHub Pages](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-success?style=for-the-badge&logo=github)](https://arnavmurdande.github.io/Data-Engineering-/)
[![React](https://img.shields.io/badge/React-18-blue?style=for-the-badge&logo=react)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-6-purple?style=for-the-badge&logo=vite)](https://vitejs.dev/)
[![TailwindCSS](https://img.shields.io/badge/Tailwind-3.4-38bdf8?style=for-the-badge&logo=tailwindcss)](https://tailwindcss.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](./LICENSE)

A structured repository containing interactive exam preparation tools, relational & analytical database schemas, and practice question patterns for **SQL, Kimball Dimensional Modeling, Cloud Data Warehouses, and Data Engineering Interviews**.

---

## 📂 Repository Architecture

```
Data-Engineering-/
├── 🚀 MCQ's Practice Website/     # Full-stack Interactive Exam & Practice Web App
│   ├── src/
│   │   ├── data/
│   │   │   ├── questions.js       # 200 High-Yield MCQs with Technical Solutions
│   │   │   ├── categories.js      # 13 Domain Categories
│   │   │   └── cheatsheet.js      # Architecture & SQL Formula Cheat Sheets
│   │   ├── App.jsx                # Modern UI with Dark/Light Modes, Filters, Simulator
│   │   └── index.css              # Custom Scrollbars, Glassmorphic & Glow Styles
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
│
├── 🗄️ Mock DB Setup/              # Production-grade SQL Schema Dumps & Seed Scripts
│   ├── AdventureWorksDB_Simple.sql
│   ├── InventoryDB_Simple.sql
│   ├── SmartDB.sql
│   └── StudentDB_Simple.sql
│
├── 📑 Mock Practice Questions/    # Curated Question Pattern Papers (PDFs)
│   ├── Q1_Pattern.pdf
│   ├── Q2-Pattern.pdf
│   ├── Q3_pattern.pdf
│   └── Q4-Pattern.pdf
│
└── ⚙️ .github/workflows/deploy.yml # Automated CI/CD for GitHub Pages Deployment
```

---

## 🌟 Features of MCQ's Practice Website

1. **200 High-Yield MCQs**:
   - Covers SQL (Joins, Window Functions, Subqueries, CTEs, Aggregations, Transactions).
   - Data Warehousing (Kimball Star/Snowflake schemas, Fact vs Dimension, SCD 0–6).
   - Modern Cloud Engines (Snowflake, BigQuery, AWS Redshift, Databricks Medallion architecture).
   - Normalization (1NF, 2NF, 3NF, BCNF) and Performance Optimization (Execution Plans, B-Trees, Partitions).
2. **Interactive Modes**:
   - 🎯 **Practice & Learn**: Instant validation, deep technical explanations, starred/missed filters, and custom category selector with count badges.
   - ⏱️ **Exam Simulator**: Real exam conditions with ticking timer, question jump palette, review flagging, and option to attempt **All 200 Questions (3h 20m)** or presets (15, 25, 50, 100 Qs).
   - ⚡ **Active Recall Flashcards**: 3D flip card animations with keyboard shortcuts (`[SPACE]`, `[←/→]`).
   - 📋 **High-Yield Cheat Sheet**: Quick formula and architecture design pattern revision.
3. **Themes & Navigation**:
   - True OLED Dark Mode & High-Contrast Light Mode with persistent state.
   - Real-time status indicator palette (`Correct`, `Wrong`, `Active`, `Starred`).
   - Full keyboard navigation support.

---

## 🚀 Running Locally

```bash
# 1. Clone the repository
git clone https://github.com/ArnavMurdande/Data-Engineering-.git

# 2. Navigate to the website directory
cd "Data-Engineering-/MCQ's Practice Website"

# 3. Install dependencies
npm install

# 4. Start Vite development server
npm run dev
```

---

## 🌐 Live Deployment (GitHub Pages)

The repository includes an automated GitHub Actions workflow (`.github/workflows/deploy.yml`).

To enable GitHub Pages:
1. Go to your repository **Settings** on GitHub.
2. Under the **Code and automation** section in the left sidebar, click **Pages**.
3. Under **Build and deployment > Source**, select **GitHub Actions**.
4. Every push to `main` will automatically build and deploy the app to:
   `https://arnavmurdande.github.io/Data-Engineering/`

---

## 📄 License
This project is open source and available under the [MIT License](./LICENSE).
