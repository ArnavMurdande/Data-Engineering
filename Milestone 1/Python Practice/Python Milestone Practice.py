"""
Python Milestone Practice
=========================
Write or paste your practice solution code below for any of the Milestone questions:
- OOPS: SupplyChainInventory, EventRegistrationTracker, TrafficControlSystem,
        ChessTournamentSystem, LibraryLoanRegistry, MuseumLoanRegistry
- Pandas: ClaimAnalyzer, SolarFarmAnalyzer, ReturnsAnalyzer,
          EVChargingAnalyzer, HospitalEquipmentAnalyzer, SolarMaintenanceAnalyzer
- NumPy: City AQI functions, SensorAnalyzer, Instagram Reels functions,
         Aquarium Water Quality functions, Cold-Storage functions

Whenever you run this file (python "Python Milestone Practice.py" or Run in VS Code),
it will automatically run against 10 rigorous test cases and show you your score!
"""

import numpy as np
import pandas as pd


# ------------------------------------------------------------------------------
# WRITE YOUR CODE BELOW THIS LINE
# ------------------------------------------------------------------------------

import numpy as np

def create_aqi_array(values: list) -> np.ndarray:
    # aqi_array = np.asarray(values, dtype=np.int64).reshape(-1)
    # return aqi_array
    return np.asarray(values, dtype=np.int64).reshape(-1)  # .reshape(row, columns) shapes array into rows and columns and -1 automatically decides it *** #

def validate_aqi_array(arr: np.ndarray) -> bool:
    if arr.size == 0 or not np.issubdtype(arr.dtype, np.number):
        return False
    return bool(np.all((arr >=0) & (arr <= 100)))

def compute_aqi_stats(arr: np.ndarray) -> tuple:
    mean = round(float(np.mean(arr)),2) 
    std_dev = round(float(np.std(arr)),2) 
    max = round(float(np.max(arr)),2) 
    min = round(float(np.min(arr)),2) 

    return(mean, std_dev, max, min)

def categorize_aqi(arr: np.ndarray) -> np.ndarray:
    category = [
        (arr >= 0) & (arr <= 50),
        (arr >= 51) & (arr <= 100),
        (arr >= 101) & (arr <= 150),
        (arr >= 151) & (arr <= 200),
        (arr >= 201) & (arr <= 300),
        (arr >= 301) & (arr <=500),
    ]

    choices = [
        "Good",
        "Moderate",
        "USG",
        "Unhealthy",
        "Very Unhealthy",
        "Hazardous",
    ]

    return np.select(category, choices, default= "Invalid")

def longest_unhealthy_streak(arr: np.ndarray) -> int:
    max_streak = 0
    current_streak = 0

    for val in arr:
        if val >= 151:
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else: 
            current_streak = 0

    return max_streak


# ------------------------------------------------------------------------------
# AUTOMATIC TEST RUNNER HOOK (Do not modify below)
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    import importlib.util
    import os

    current_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(current_dir, "Python Practice Questions and Tests", "test", "test_runner.py"),
        os.path.join(current_dir, "..", "Python Practice Questions and Tests", "test", "test_runner.py"),
    ]
    runner_path = next((os.path.abspath(p) for p in candidates if os.path.exists(p)), None)

    if runner_path and os.path.exists(runner_path):
        spec = importlib.util.spec_from_file_location("test_runner", runner_path)
        if spec and spec.loader:
            test_runner = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(test_runner)
            test_runner.run_tests_for_file(__file__)
        else:
            print(f"Error: Unable to load test runner from {runner_path}")
    else:
        print("Error: Could not locate 'test_runner.py' in 'Python Practice Questions and Tests/test'.")
