# 🗄️ SQL Extra Practice Questions

This directory contains extra scenario-based SQL practice questions with full database setup scripts, sample data, and verified solutions.

---

## 📋 Questions Summary

| # | Question Title | Database | Tables Used | Key Concepts | Solution File |
|---|---|---|---|---|---|
| **1** | Most Popular Payment Method | `FOOD_DELIVERY_DB` | `Payments` | `COUNT(*)`, `GROUP BY`, `ORDER BY ... LIMIT 1` (No window functions) | [`01_most_popular_payment_method.sql`](./01_most_popular_payment_method.sql) |
| **2** | Fastest Score per Game | `GAMING_PLATFORM_DB` | `Games`, `Players`, `Scores` | `ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...)`, Joins, Filtering | [`02_fastest_score_per_game.sql`](./02_fastest_score_per_game.sql) |

---

## 🚀 How to Set Up & Run in MySQL

1. **Set Up Databases**:
   - Run [`DB Setup/FOOD_DELIVERY_DB.sql`](./DB%20Setup/FOOD_DELIVERY_DB.sql) to create `FOOD_DELIVERY_DB` and populate sample transactions.
   - Run [`DB Setup/GAMING_PLATFORM_DB.sql`](./DB%20Setup/GAMING_PLATFORM_DB.sql) to create `GAMING_PLATFORM_DB` and populate games, players, and match scores.

2. **Execute Solutions**:
   - Open [`01_most_popular_payment_method.sql`](./01_most_popular_payment_method.sql) or [`02_fastest_score_per_game.sql`](./02_fastest_score_per_game.sql) in your SQL client / VS Code SQLBook tab and click **Run**.
