class EventRegistrationTracker:
    def __init__(self):
        self.events = {}

    def register_participant(self, event_id: str, count: int) -> dict:
        if event_id in self.events:
            self.events[event_id] += count
        else:
            self.events[event_id] = count
        return self.events

    def cancel_participant(self, event_id: str, count: int) -> dict:
        if event_id not in self.events or self.events[event_id] < count:
            raise ValueError("Cannot cancel more participants than registered")
        self.events[event_id] -= count
        return self.events

    def reschedule_event(self, old_event_id: str, new_event_id: str) -> dict:
        if old_event_id not in self.events:
            return self.events
        count = self.events[old_event_id]
        if new_event_id in self.events:
            self.events[new_event_id] += count
        else:
            self.events[new_event_id] = count
        del self.events[old_event_id]
        return self.events

    def get_active_events(self) -> list:
        return [event_id for event_id, count in self.events.items() if count > 0]
