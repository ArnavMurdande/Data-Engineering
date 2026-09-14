"""
Sensor Reading Analysis System

Class: SensorAnalyzer

Problem Statement:
Validate, summarize, reduce, and format float-based physical sensor readings.
A sensor network records physical measurements across devices.

Methods Required:
1. create_sensor_array(self, sensor_values: list) -> np.ndarray
   Convert list to NumPy float array.
2. validate_sensor_array(self, sensor_array: np.ndarray) -> bool
   Return True if array is non-empty and all values are strictly positive (> 0);
   otherwise False.
3. compute_sensor_statistics(self, sensor_array: np.ndarray) -> tuple
   Return tuple (total, average, maximum) with average rounded to 1 decimal place.
4. filter_extreme_readings(self, sensor_array: np.ndarray) -> np.ndarray
   Apply 10% reduction (multiply by 0.9) to all readings >= 50.0.
5. label_high_sensors(self, sensor_array: np.ndarray) -> np.ndarray
   Compare elements to array mean: return array with "High" if element > mean,
   else "Normal".
6. format_sensor_readings(self, sensor_array: np.ndarray) -> np.ndarray
   Format each element as string: f"{x:.2f} units".
"""

import numpy as np


class SensorAnalyzer:
    def __init__(self):
        pass

    def create_sensor_array(self, sensor_values: list) -> np.ndarray:
        return np.asarray(sensor_values, dtype=float).reshape(-1)

    def validate_sensor_array(self, sensor_array: np.ndarray) -> bool:
        if sensor_array.size == 0 or not np.issubdtype(sensor_array.dtype, np.number):
            return False
        return bool(np.all(sensor_array > 0))

    def compute_sensor_statistics(self, sensor_array: np.ndarray) -> tuple:
        total = float(np.sum(sensor_array))
        average = round(float(np.mean(sensor_array)), 1)
        maximum = float(np.max(sensor_array))
        return (total, average, maximum)

    def filter_extreme_readings(self, sensor_array: np.ndarray) -> np.ndarray:
        arr = sensor_array.astype(float).copy()
        mask = arr >= 50.0
        arr[mask] = arr[mask] * 0.9
        return arr

    def label_high_sensors(self, sensor_array: np.ndarray) -> np.ndarray:
        mean_val = np.mean(sensor_array)
        return np.where(sensor_array > mean_val, "High", "Normal")

    def format_sensor_readings(self, sensor_array: np.ndarray) -> np.ndarray:
        return np.array([f"{x:.2f} units" for x in sensor_array])


if __name__ == "__main__":
    analyzer = SensorAnalyzer()
    raw = [28.5, 415.0, 30.7, 92.1]
    arr = analyzer.create_sensor_array(raw)
    print("Sensor Array:", arr)
    print("Validate Array:", analyzer.validate_sensor_array(arr))
    print("Statistics:", analyzer.compute_sensor_statistics(arr))
    print("Filtered Extreme Readings:", analyzer.filter_extreme_readings(arr))
    print("Label High Sensors:", analyzer.label_high_sensors(arr))
    print("Format Readings:", analyzer.format_sensor_readings(arr))
