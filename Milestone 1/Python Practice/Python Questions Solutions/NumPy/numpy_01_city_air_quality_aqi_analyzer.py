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
