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
