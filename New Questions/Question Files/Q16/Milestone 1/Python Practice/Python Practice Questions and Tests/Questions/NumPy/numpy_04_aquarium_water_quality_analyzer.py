"""
Aquarium Water Quality Analyzer

Module-level Functions

Problem Statement:
Analyze aquarium water temperature readings in degrees Celsius.
A marine facility records water temperature to ensure aquatic life thrives.

Functions Required:
1. create_water_temperature_array(values: list) -> np.ndarray
   Convert list to 1D NumPy array with dtype np.float64.
2. validate_water_temperature_array(arr: np.ndarray) -> bool
   Return True if array is non-empty, numeric dtype, and all values are 12.0 to 30.0 inclusive;
   otherwise False without raising exceptions.
3. compute_water_temperature_stats(arr: np.ndarray) -> tuple
   Calculate mean, population standard deviation (ddof=0), max, and min rounded to 2 decimal places.
   Return tuple of Python floats: (mean, std, max, min).
4. categorize_water_temperatures(arr: np.ndarray) -> np.ndarray
   Bin values:
   - 12.0 <= val <= 18.0: "Cold"
   - 18.0 < val <= 26.0: "Optimal"
   - 26.0 < val <= 30.0: "Warm"
   - out of range: "Invalid"
5. longest_warm_streak(arr: np.ndarray) -> int
   Return greatest number of consecutive readings satisfying 26.0 < val <= 30.0.
   Return 0 if none exist.
"""

import numpy as np


def create_water_temperature_array(values: list) -> np.ndarray:
    return np.asarray(values, dtype=np.float64).reshape(-1)


def validate_water_temperature_array(arr: np.ndarray) -> bool:
    if arr.size == 0 or not np.issubdtype(arr.dtype, np.number):
        return False
    return bool(np.all((arr >= 12.0) & (arr <= 30.0)))


def compute_water_temperature_stats(arr: np.ndarray) -> tuple:
    mean_val = round(float(np.mean(arr)), 2)
    std_val = round(float(np.std(arr)), 2)
    max_val = round(float(np.max(arr)), 2)
    min_val = round(float(np.min(arr)), 2)
    return (mean_val, std_val, max_val, min_val)


def categorize_water_temperatures(arr: np.ndarray) -> np.ndarray:
    conditions = [
        (arr >= 12.0) & (arr <= 18.0),
        (arr > 18.0) & (arr <= 26.0),
        (arr > 26.0) & (arr <= 30.0),
    ]
    choices = ["Cold", "Optimal", "Warm"]
    return np.select(conditions, choices, default="Invalid")


def longest_warm_streak(arr: np.ndarray) -> int:
    current_streak = 0
    longest = 0
    for value in arr:
        if 26.0 < value <= 30.0:
            current_streak += 1
            longest = max(longest, current_streak)
        else:
            current_streak = 0
    return longest


if __name__ == "__main__":
    temps = [15.5, 22.0, 24.5, 27.5, 28.0, 29.1, 16.0]
    arr = create_water_temperature_array(temps)
    print("Water Temp Array:", arr)
    print("Validate Array:", validate_water_temperature_array(arr))
    print("Stats:", compute_water_temperature_stats(arr))
    print("Categorize:", categorize_water_temperatures(arr))
    print("Longest Warm Streak:", longest_warm_streak(arr))
