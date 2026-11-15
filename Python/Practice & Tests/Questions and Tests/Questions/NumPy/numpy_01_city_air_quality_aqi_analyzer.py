"""
City Air Quality AQI Analyzer

Module-level Functions

Problem Statement:
Load, validate, summarize, categorize, and streak-analyze AQI readings (0-500).
A city logs daily AQI values. Build utilities to analyze air quality trends.

Functions Required:
1. create_aqi_array(values: list) -> np.ndarray
   Convert list to 1D NumPy array with dtype int64.
2. validate_aqi_array(arr: np.ndarray) -> bool
   Return True if array is non-empty, numeric, and all values are between 0 and 100 inclusive;
   otherwise False.
3. compute_aqi_stats(arr: np.ndarray) -> tuple
   Calculate mean, standard deviation, max, and min rounded to 2 decimal places.
   Return (mean, std, max, min).
4. categorize_aqi(arr: np.ndarray) -> np.ndarray
   Categorize values:
   - 0-50: "Good"
   - 51-100: "Moderate"
   - 101-150: "USG"
   - 151-200: "Unhealthy"
   - 201-300: "Very Unhealthy"
   - 301-500: "Hazardous"
5. longest_unhealthy_streak(arr: np.ndarray) -> int
   Find the longest sequence of consecutive days where AQI >= 151.
"""

import numpy as np


def create_aqi_array(values: list) -> np.ndarray:
    return np.asarray(values, dtype=np.int64).reshape(-1)


def validate_aqi_array(arr: np.ndarray) -> bool:
    if arr.size == 0 or not np.issubdtype(arr.dtype, np.number):
        return False
    return bool(np.all((arr >= 0) & (arr <= 100)))


def compute_aqi_stats(arr: np.ndarray) -> tuple:
    mean_val = round(float(np.mean(arr)), 2)
    std_val = round(float(np.std(arr)), 2)
    max_val = round(float(np.max(arr)), 2)
    min_val = round(float(np.min(arr)), 2)
    return (mean_val, std_val, max_val, min_val)


def categorize_aqi(arr: np.ndarray) -> np.ndarray:
    conditions = [
        (arr >= 0) & (arr <= 50),
        (arr >= 51) & (arr <= 100),
        (arr >= 101) & (arr <= 150),
        (arr >= 151) & (arr <= 200),
        (arr >= 201) & (arr <= 300),
        (arr >= 301) & (arr <= 500),
    ]
    choices = [
        "Good",
        "Moderate",
        "USG",
        "Unhealthy",
        "Very Unhealthy",
        "Hazardous",
    ]
    return np.select(conditions, choices, default="Invalid")


def longest_unhealthy_streak(arr: np.ndarray) -> int:
    current_streak = 0
    max_streak = 0
    for val in arr:
        if val >= 151:
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 0
    return max_streak


if __name__ == "__main__":
    readings = [32, 95, 172, 180, 155, 325]
    arr = create_aqi_array(readings)
    print("AQI Array:", arr)
    print("Validate (0-100):", validate_aqi_array(arr))
    valid_sub = create_aqi_array([45, 60, 80])
    print("Validate valid_sub:", validate_aqi_array(valid_sub))
    print("Stats:", compute_aqi_stats(arr))
    print("Categories:", categorize_aqi(arr))
    print("Longest Unhealthy Streak:", longest_unhealthy_streak(arr))
