"""
Smart City Traffic Control System

Class: TrafficControlSystem

Problem Statement:
A Traffic Control System monitors vehicle counts across intersections and adjusts signal timings.
Each intersection entry has:
- Key: Intersection Name (String)
- Value: Vehicle Count (Integer)

State Initialization:
def __init__(self):
    self.traffic_data = {}

Methods Required:
1. add_intersection(self, intersection: str, vehicle_count: int) -> dict
   Insert intersection and vehicle count into traffic data dictionary. Return updated dictionary.
2. update_vehicle_count(self, intersection: str, new_count: int) -> dict | str
   If intersection not found, return "Error: Intersection not found".
   Otherwise update vehicle count and return updated dictionary.
3. get_congested_intersections(self, congestion_threshold: int) -> dict
   Return dictionary of intersections where vehicle count > congestion_threshold.
4. adjust_traffic_signals(self) -> dict
   Return dictionary mapping intersection to signal timing:
   - count > 80: "Long Green"
   - 40 <= count <= 80: "Normal Green"
   - count < 40: "Short Green"
"""


class TrafficControlSystem:
    def __init__(self):
        self.traffic_data = {}

    def add_intersection(self, intersection: str, vehicle_count: int) -> dict:
        self.traffic_data[intersection] = vehicle_count
        return self.traffic_data

    def update_vehicle_count(self, intersection: str, new_count: int) -> dict | str:
        if intersection not in self.traffic_data:
            return "Error: Intersection not found"
        self.traffic_data[intersection] = new_count
        return self.traffic_data

    def get_congested_intersections(self, congestion_threshold: int) -> dict:
        return {
            intersection: count
            for intersection, count in self.traffic_data.items()
            if count > congestion_threshold
        }

    def adjust_traffic_signals(self) -> dict:
        signals = {}
        for intersection, count in self.traffic_data.items():
            if count > 80:
                signals[intersection] = "Long Green"
            elif 40 <= count <= 80:
                signals[intersection] = "Normal Green"
            else:
                signals[intersection] = "Short Green"
        return signals


if __name__ == "__main__":
    tcs = TrafficControlSystem()
    print("Add 5th Ave:", tcs.add_intersection("5th Avenue & Main St", 20))
    print("Add Broadway:", tcs.add_intersection("Broadway & 1st St", 50))
    print("Add Central:", tcs.add_intersection("Central Square", 85))
    print("Update 5th Ave:", tcs.update_vehicle_count("5th Avenue & Main St", 35))
    print("Congested (>30):", tcs.get_congested_intersections(30))
    print("Signals:", tcs.adjust_traffic_signals())
