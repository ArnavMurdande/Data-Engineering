# 🚀 Databricks Milestone 2 Exam Master • 200 High-Yield MCQs

An ultra-modern, interactive MCQ examination simulator, practice platform, and active recall revision suite built with **React**, **Vite**, and **Tailwind CSS**.

---

## 🌟 Key Features

### 1. 🎯 Practice & Learn Mode
- **200 High-Yield Questions** categorized across 11 core Databricks & Big Data engineering domains.
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
- Condensed summaries of core architecture formulas, HDFS mechanics, Spark cluster deployment, RDD lifecycle, Catalyst Optimizer, and Java/Scala fundamentals.

### 5. 🎨 Elevated Dark Mode & UI Aesthetics
- OLED-friendly deep slate background (`#020617`), ambient radial glow accents, glassmorphic card containers, and high-contrast typography.
- Seamless one-click Dark / Light mode toggle with persistent state in `localStorage`.

---

## 📚 Curriculum & Question Distribution (200 Questions)

| Domain / Category | Question Count | Topics Covered |
|---|---|---|
| **Big Data & Hadoop Architecture** | 15 | 4Vs of Big Data, HDFS NameNode/DataNode mechanics, Block replication, YARN ResourceManager & NodeManager |
| **Spark Cluster Architecture** | 15 | Driver & Executors, Client vs Cluster deploy modes, Cluster Managers (YARN/K8s/Standalone), Spark UI |
| **Spark Core & RDDs** | 25 | RDD Lineage, Lazy Transformations vs Eager Actions, Narrow vs Wide dependencies, Shuffle, Storage levels |
| **Spark SQL & DataFrames** | 25 | DataFrames API, Schemas, StructType/StructField, CSV/Parquet/JSON ingestion, Built-in SQL functions, Aggregations |
| **Catalyst, Plans & Optimization** | 20 | 4-Phase Catalyst Pipeline, Physical Plans, Cost-Based Optimizer (CBO), Broadcast Hash Joins, Data skew mitigation |
| **Structured Streaming & Kafka** | 25 | Micro-batch vs Continuous processing, Output Modes (Append/Complete/Update), Watermarking, Checkpoint offsets |
| **Java Fundamentals & Collections** | 20 | JVM Heap vs Stack, Generational Garbage Collection, ArrayList vs LinkedList, HashMap vs ConcurrentHashMap |
| **Java OOPs & SOLID Principles** | 20 | Encapsulation, Polymorphism (Overriding vs Overloading), Abstract classes vs Interfaces, 5 SOLID principles |
| **Java Streams & File I/O** | 15 | Java 8 Streams API (filter, map, flatMap, collect), Try-With-Resources, File I/O, java.time immutability |
| **Java Concurrency & JDBC** | 10 | Thread lifecycle, synchronized vs ReentrantLock, volatile variables, JDBC Transactions (ACID, rollback, savepoint) |
| **Scala & Functional Programming** | 10 | Immutability (val vs var), Pattern matching, Case classes, Option/Some/None, Try/Success/Failure, Pure functions |
| **Total** | **200 Questions** | Complete Milestone 2 Mastery |

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
