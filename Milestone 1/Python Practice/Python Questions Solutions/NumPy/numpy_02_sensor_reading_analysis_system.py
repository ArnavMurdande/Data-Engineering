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
