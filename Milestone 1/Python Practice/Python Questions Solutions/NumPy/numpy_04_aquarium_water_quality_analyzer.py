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
