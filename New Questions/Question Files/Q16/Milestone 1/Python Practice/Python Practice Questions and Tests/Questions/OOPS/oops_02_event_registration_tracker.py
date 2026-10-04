"""
Event Registration Tracker

Class: EventRegistrationTracker

Problem Statement:
Design an Event Registration Tracker for a conference management system tracking
registered participant counts per event. Each event entry has:
- Key: event_id (String, unique)
- Value: Number of registered participants (Integer)

State Initialization:
def __init__(self):
    self.events = {}

Methods Required:
1. register_participant(self, event_id: str, count: int) -> dict
   If event exists, increase count; otherwise add event. Return updated dictionary.
2. cancel_participant(self, event_id: str, count: int) -> dict
   If event does not exist or registered count < count to cancel,
   raise ValueError("Cannot cancel more participants than registered").
   Otherwise subtract count. Return updated dictionary.
3. reschedule_event(self, old_event_id: str, new_event_id: str) -> dict
   If old_event_id not found in events dictionary, return existing dictionary.
   Transfer count to new_event_id (add if exists, else assign) and delete old_event_id.
   Return updated dictionary.
4. get_active_events(self) -> list
   Return list of event IDs where participant count > 0.
"""


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


if __name__ == "__main__":
    tracker = EventRegistrationTracker()
    print("Register Gaming (10):", tracker.register_participant("Gaming", 10))
    print("Register Trekking (20):", tracker.register_participant("Trekking", 20))
    print("Cancel Gaming (5):", tracker.cancel_participant("Gaming", 5))
    print("Reschedule Gaming to Esports:", tracker.reschedule_event("Gaming", "Esports"))
    print("Active Events:", tracker.get_active_events())
