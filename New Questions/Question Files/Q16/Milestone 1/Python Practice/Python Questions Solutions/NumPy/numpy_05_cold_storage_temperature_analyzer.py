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
