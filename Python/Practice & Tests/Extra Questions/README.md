# 🐍 Python Extra Practice Questions

This directory contains additional Python practice questions covering **OOPs**, **Pandas**, and **NumPy** with complete problem statements and reference solutions.

---

## 📋 Questions Summary

| Category | File | Target Class | Key Methods & Concepts |
|---|---|---|---|
| **OOPs** | [`OOPS/oops_extra_01_library_inventory_system.py`](./OOPS/oops_extra_01_library_inventory_system.py) | `LibraryInventorySystem` | `add_book`, `update_book_quantity`, `get_book_stock`, `get_available_books` (explicit loop, `KeyError` handling) |
| **Pandas** | [`Pandas/pandas_extra_01_food_delivery_order_analyzer.py`](./Pandas/pandas_extra_01_food_delivery_order_analyzer.py) | `DeliveryTimeAnalyzer` | `create_delivery_log_df`, `create_restaurant_master_df`, `merge_restaurant_names`, `average_delivery_by_restaurant`, `filter_slow_deliveries`, `slowest_delivery_area` |
| **NumPy** | [`NumPy/numpy_extra_01_movie_rating_analyzer.py`](./NumPy/numpy_extra_01_movie_rating_analyzer.py) | `MovieRatingAnalyzer` | `create_rating_array`, `validate_ratings` (`np.any`), `compute_rating_summary`, `apply_bonus` (clip, round), `categorize_movies`, `format_ratings_with_grades` |

---

## 🧪 Automated Testing
All 3 classes are fully integrated into the test runner in `Python Practice/Python Practice Questions and Tests/test/test_runner.py` with **10 unit test cases each** (30 new test cases total).

To test any of your solutions:
1. Paste or write your class in `Python Milestone Practice.py`.
2. Run `Python Milestone Practice.py` to view automated evaluation results.
