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
