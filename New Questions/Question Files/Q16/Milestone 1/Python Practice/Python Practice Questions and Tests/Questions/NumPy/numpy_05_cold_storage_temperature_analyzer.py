"""
Cold-Storage Temperature Analyzer

Module-level Functions

Problem Statement:
Inspect and summarize cold-room storage temperatures in degrees Celsius.
A food distribution centre records cold-room temperatures. Implement five independent
NumPy functions that create, validate, summarize, categorize, and scan those readings.

Functions Required:
1. create_temperature_array(values: list) -> np.ndarray
   Convert values to 1D NumPy array with dtype np.float64. Preserve input order.
2. validate_temperature_array(arr: np.ndarray) -> bool
   Return True if array is non-empty, numeric dtype, and all values are between
   -30.0 and 10.0 inclusive; otherwise False without raising exceptions.
3. compute_temperature_stats(arr: np.ndarray) -> tuple
   Compute mean, population standard deviation (ddof=0), max, and min rounded to 2 decimal places.
   Return tuple of Python floats: (mean, standard_deviation, maximum, minimum).
4. categorize_temperatures(arr: np.ndarray) -> np.ndarray
   Bin values:
   - -30.0 <= val <= -18.0: "Frozen"
   - -18.0 < val <= 5.0: "Chilled"
   - 5.0 < val <= 10.0: "Warning"
   - below -30.0 or above 10.0: "Invalid"
5. longest_warning_streak(arr: np.ndarray) -> int
   Return greatest number of consecutive readings satisfying 5.0 < val <= 10.0.
   Any other value, including an invalid value, breaks the current streak.
   Return 0 if none exist.
"""

import numpy as np


def create_temperature_array(values: list) -> np.ndarray:
    return np.asarray(values, dtype=np.float64).reshape(-1)


def validate_temperature_array(arr: np.ndarray) -> bool:
    if arr.size == 0 or not np.issubdtype(arr.dtype, np.number):
        return False
    return bool(np.all((arr >= -30.0) & (arr <= 10.0)))


def compute_temperature_stats(arr: np.ndarray) -> tuple:
    mean_val = round(float(np.mean(arr)), 2)
    std_val = round(float(np.std(arr)), 2)
    max_val = round(float(np.max(arr)), 2)
    min_val = round(float(np.min(arr)), 2)
    return (mean_val, std_val, max_val, min_val)


def categorize_temperatures(arr: np.ndarray) -> np.ndarray:
    conditions = [
        (arr >= -30.0) & (arr <= -18.0),
        (arr > -18.0) & (arr <= 5.0),
        (arr > 5.0) & (arr <= 10.0),
    ]
    choices = ["Frozen", "Chilled", "Warning"]
    return np.select(conditions, choices, default="Invalid")


def longest_warning_streak(arr: np.ndarray) -> int:
    current_streak = 0
    max_streak = 0
    for value in arr:
        if 5.0 < value <= 10.0:
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 0
    return max_streak


if __name__ == "__main__":
    temps = [-22.0, -18.5, 4.0, 6.5, 8.0, 9.5, -5.0]
    arr = create_temperature_array(temps)
    print("Temp Array:", arr)
    print("Validate Array:", validate_temperature_array(arr))
    print("Stats:", compute_temperature_stats(arr))
    print("Categorize:", categorize_temperatures(arr))
    print("Longest Warning Streak:", longest_warning_streak(arr))
