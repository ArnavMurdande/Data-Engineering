"""
Instagram Reel Trend Engagement Analysis

Module-level Functions

Problem Statement:
Analyze daily Instagram reel view counts, compute metrics, and detect trend streaks.
A social media analytics team tracks Instagram Reel engagement trends for creators.
Each value represents the number of views received on a specific day.

Functions Required:
1. create_views_array(views_data: list) -> np.ndarray
   Convert list to NumPy array with dtype np.int64.
2. validate_views_array(views_array: np.ndarray) -> bool
   Return True if non-empty, numeric (np.issubdtype), and all values >= 0; otherwise False.
3. compute_view_metrics(views_array: np.ndarray) -> tuple
   Return tuple (total_views: int, average_views: float, maximum_views: int).
   Round average to 2 decimals.
4. categorize_trend_levels(views_array: np.ndarray) -> np.ndarray
   Map values:
   - < 3000: "Low Trend"
   - 3000 to 4999: "Moderate Trend"
   - >= 5000: "Viral Trend"
5. longest_growth_streak(views_array: np.ndarray) -> int
   Find the longest consecutive streak of days where views increased compared to the previous day.
   Return 0 for empty array, 1 for single value.
6. format_view_counts(views_array: np.ndarray) -> np.ndarray
   Format values with comma separators (e.g., "1,200").
"""

import numpy as np


def create_views_array(views_data: list) -> np.ndarray:
    return np.asarray(views_data, dtype=np.int64).reshape(-1)


def validate_views_array(views_array: np.ndarray) -> bool:
    if views_array.size == 0 or not np.issubdtype(views_array.dtype, np.number):
        return False
    return bool(np.all(views_array >= 0))


def compute_view_metrics(views_array: np.ndarray) -> tuple:
    total_views = int(np.sum(views_array))
    average_views = round(float(np.mean(views_array)), 2)
    maximum_views = int(np.max(views_array))
    return (total_views, average_views, maximum_views)


def categorize_trend_levels(views_array: np.ndarray) -> np.ndarray:
    conditions = [
        views_array < 3000,
        (views_array >= 3000) & (views_array <= 4999),
        views_array >= 5000,
    ]
    choices = [
        "Low Trend",
        "Moderate Trend",
        "Viral Trend",
    ]
    return np.select(conditions, choices, default="Unknown")


def longest_growth_streak(views_array: np.ndarray) -> int:
    n = len(views_array)
    if n == 0:
        return 0
    if n == 1:
        return 1

    current_streak = 1
    max_streak = 1
    for i in range(1, n):
        if views_array[i] > views_array[i - 1]:
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 1
    return max_streak


def format_view_counts(views_array: np.ndarray) -> np.ndarray:
    return np.array([f"{int(x):,}" for x in views_array])


if __name__ == "__main__":
    views = create_views_array([1200, 3500, 1800, 5200, 7600])
    print("Views Array:", views)
    print("Validate Views:", validate_views_array(views))
    print("Metrics:", compute_view_metrics(views))
    print("Trend Levels:", categorize_trend_levels(views))
    print("Longest Growth Streak:", longest_growth_streak(views))
    print("Formatted Counts:", format_view_counts(views))
