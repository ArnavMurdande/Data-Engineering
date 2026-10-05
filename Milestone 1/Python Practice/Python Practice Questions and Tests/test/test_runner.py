"""
Milestone Practice Test Suite & Runner
======================================
Automated evaluation tool for Python Milestone Practice questions.
Tests any solution written in 'Python Milestone Practice.py' against 10 comprehensive,
non-hardcoded test cases per problem type (OOPS, Pandas, NumPy).
"""

import inspect
import math
import os
import sys
import traceback
import numpy as np
import pandas as pd


# ==============================================================================
# TEST CASE RUNNER UTILITIES
# ==============================================================================

class TestCase:
    def __init__(self, tc_id: int, name: str, test_func):
        self.tc_id = tc_id
        self.name = name
        self.test_func = test_func

    def run(self, target_module):
        try:
            self.test_func(target_module)
            return True, None
        except AssertionError as ae:
            return False, f"Assertion Failed: {ae}"
        except Exception as e:
            tb = traceback.format_exc().splitlines()[-1]
            return False, f"Exception: {type(e).__name__}: {e} (at {tb})"


# ==============================================================================
# 1. OOPS TEST SUITES (10 Test Cases Each)
# ==============================================================================

def suite_oops_01_supply_chain(cls):
    tests = []

    def tc1(c):
        obj = c()
        assert hasattr(obj, "inv"), "Missing attribute 'inv'"
        assert isinstance(obj.inv, dict), "'inv' must be a dictionary"
        assert len(obj.inv) == 0, "'inv' should initially be empty"
    tests.append(TestCase(1, "Initial state verification (empty 'inv' dictionary)", tc1))

    def tc2(c):
        obj = c()
        res = obj.add_product("SKU_A", 15)
        assert obj.inv.get("SKU_A") == 15, f"Expected 15, got {obj.inv.get('SKU_A')}"
        assert res is obj.inv or res == {"SKU_A": 15}, "add_product must return updated inventory dictionary"
    tests.append(TestCase(2, "add_product creates new entry with exact quantity", tc2))

    def tc3(c):
        obj = c()
        obj.add_product("SKU_A", 10)
        obj.add_product("SKU_A", 25)
        assert obj.inv["SKU_A"] == 35, f"Expected 35 after restock, got {obj.inv['SKU_A']}"
    tests.append(TestCase(3, "add_product accumulates stock on existing product", tc3))

    def tc4(c):
        obj = c()
        obj.add_product("P1", 10)
        obj.add_product("P2", 20)
        obj.add_product("P3", 30)
        assert len(obj.inv) == 3 and obj.inv["P2"] == 20, "Multiple products should maintain distinct stock counts"
    tests.append(TestCase(4, "add_product handles multiple distinct products", tc4))

    def tc5(c):
        obj = c()
        obj.add_product("ITEM1", 50)
        res = obj.fulfill_order("ITEM1", 18)
        assert obj.inv["ITEM1"] == 32, f"Expected 32, got {obj.inv['ITEM1']}"
        assert res is obj.inv or res.get("ITEM1") == 32, "fulfill_order must return updated dictionary"
    tests.append(TestCase(5, "fulfill_order reduces existing stock correctly", tc5))

    def tc6(c):
        obj = c()
        obj.add_product("ITEM1", 20)
        obj.fulfill_order("ITEM1", 20)
        assert obj.inv["ITEM1"] == 0, f"Expected 0 stock after full depletion, got {obj.inv['ITEM1']}"
    tests.append(TestCase(6, "fulfill_order handles complete stock depletion to zero", tc6))

    def tc7(c):
        obj = c()
        obj.add_product("ITEM1", 10)
        raised = False
        try:
            obj.fulfill_order("ITEM1", 15)
        except ValueError as e:
            raised = True
            assert "insufficient stock" in str(e).lower(), f"Expected 'Insufficient Stock', got '{e}'"
        assert raised, "Expected ValueError when quantity exceeds available stock"
        assert obj.inv["ITEM1"] == 10, "Inventory must not be modified when order fails"
    tests.append(TestCase(7, "fulfill_order raises ValueError('Insufficient Stock') when quantity > stock", tc7))

    def tc8(c):
        obj = c()
        raised = False
        try:
            obj.fulfill_order("NON_EXISTENT", 5)
        except ValueError:
            raised = True
        assert raised, "Expected ValueError when product does not exist in inventory"
    tests.append(TestCase(8, "fulfill_order raises ValueError for unknown product ID", tc8))

    def tc9(c):
        obj = c()
        obj.add_product("RET_1", 20)
        obj.fulfill_order("RET_1", 10)
        res = obj.restock_return("RET_1", 5)
        assert obj.inv["RET_1"] == 15, f"Expected 15, got {obj.inv['RET_1']}"
        assert res is obj.inv or res.get("RET_1") == 15, "restock_return must return updated dictionary"
    tests.append(TestCase(9, "restock_return increases stock on existing product", tc9))

    def tc10(c):
        obj = c()
        obj.add_product("P_IN_STOCK", 12)
        obj.add_product("P_ZERO", 5)
        obj.fulfill_order("P_ZERO", 5)
        obj.restock_return("P_NEW_RET", 7)
        available = obj.list_available_products()
        assert isinstance(available, list), "list_available_products must return a list"
        assert "P_IN_STOCK" in available and "P_NEW_RET" in available, "Products with stock > 0 must be in list"
        assert "P_ZERO" not in available, "Products with 0 units must not be included in available list"
    tests.append(TestCase(10, "list_available_products returns only product IDs where stock > 0", tc10))

    return "Supply Chain Inventory Tracker (Class: SupplyChainInventory)", tests


def suite_oops_02_event_registration(c):
    tests = []

    def tc1(cls):
        obj = cls()
        assert hasattr(obj, "events") and isinstance(obj.events, dict) and len(obj.events) == 0, \
            "Must initialize empty self.events dictionary"
    tests.append(TestCase(1, "Initial state verification (empty self.events)", tc1))

    def tc2(cls):
        obj = cls()
        res = obj.register_participant("Keynote", 120)
        assert obj.events.get("Keynote") == 120, "Should add new event with participant count"
        assert res is obj.events or res.get("Keynote") == 120, "Must return updated events dictionary"
    tests.append(TestCase(2, "register_participant adds new event", tc2))

    def tc3(cls):
        obj = cls()
        obj.register_participant("Workshop", 30)
        obj.register_participant("Workshop", 25)
        assert obj.events["Workshop"] == 55, "Should increment participant count on existing event"
    tests.append(TestCase(3, "register_participant increments existing event count", tc3))

    def tc4(cls):
        obj = cls()
        obj.register_participant("Panel", 50)
        res = obj.cancel_participant("Panel", 15)
        assert obj.events["Panel"] == 35, "Should subtract canceled count"
        assert res is obj.events or res.get("Panel") == 35, "Must return updated dictionary"
    tests.append(TestCase(4, "cancel_participant reduces count on valid cancellation", tc4))

    def tc5(cls):
        obj = cls()
        obj.register_participant("Panel", 40)
        obj.cancel_participant("Panel", 40)
        assert obj.events["Panel"] == 0, "Should allow canceling down to 0"
    tests.append(TestCase(5, "cancel_participant handles cancellation down to zero", tc5))

    def tc6(cls):
        obj = cls()
        obj.register_participant("Hackathon", 20)
        raised = False
        try:
            obj.cancel_participant("Hackathon", 25)
        except ValueError as e:
            raised = True
            assert "cannot cancel more participants" in str(e).lower(), f"Unexpected error message: {e}"
        assert raised, "Expected ValueError when cancellation exceeds registration"
    tests.append(TestCase(6, "cancel_participant raises ValueError when count to cancel > registered", tc6))

    def tc7(cls):
        obj = cls()
        raised = False
        try:
            obj.cancel_participant("NonExistent", 5)
        except ValueError:
            raised = True
        assert raised, "Expected ValueError when canceling from non-existent event"
    tests.append(TestCase(7, "cancel_participant raises ValueError for unknown event", tc7))

    def tc8(cls):
        obj = cls()
        obj.register_participant("OldRoom", 45)
        obj.register_participant("NewRoom", 15)
        res = obj.reschedule_event("OldRoom", "NewRoom")
        assert "OldRoom" not in obj.events, "Old event must be deleted"
        assert obj.events["NewRoom"] == 60, "Participants must be transferred to existing new event"
        assert res is obj.events or res.get("NewRoom") == 60, "Must return updated dictionary"
    tests.append(TestCase(8, "reschedule_event transfers to existing event and removes old event", tc8))

    def tc9(cls):
        obj = cls()
        obj.register_participant("SeminarA", 70)
        res = obj.reschedule_event("SeminarA", "SeminarB")
        assert "SeminarA" not in obj.events and obj.events.get("SeminarB") == 70, \
            "Should create new event with transferred count"
        res_non = obj.reschedule_event("NonExistent", "SeminarB")
        assert res_non is obj.events, "Should return existing dictionary if old_event_id not found"
    tests.append(TestCase(9, "reschedule_event handles new event creation and non-existent old ID", tc9))

    def tc10(cls):
        obj = cls()
        obj.register_participant("Event1", 10)
        obj.register_participant("Event2", 5)
        obj.cancel_participant("Event2", 5)
        active = obj.get_active_events()
        assert isinstance(active, list), "get_active_events must return a list"
        assert "Event1" in active and "Event2" not in active, "Must only return events with participant count > 0"
    tests.append(TestCase(10, "get_active_events filters events with count > 0", tc10))

    return "Event Registration Tracker (Class: EventRegistrationTracker)", tests


def suite_oops_03_traffic_control(c):
    tests = []

    def tc1(cls):
        obj = cls()
        assert hasattr(obj, "traffic_data") and isinstance(obj.traffic_data, dict) and len(obj.traffic_data) == 0, \
            "traffic_data must be initialized as an empty dictionary"
    tests.append(TestCase(1, "Initial state verification (empty self.traffic_data)", tc1))

    def tc2(cls):
        obj = cls()
        res = obj.add_intersection("Main & 1st", 45)
        assert obj.traffic_data.get("Main & 1st") == 45, "Should record intersection and count"
        assert res is obj.traffic_data or res.get("Main & 1st") == 45, "Must return updated dictionary"
    tests.append(TestCase(2, "add_intersection registers intersection and vehicle count", tc2))

    def tc3(cls):
        obj = cls()
        obj.add_intersection("Main & 1st", 45)
        res = obj.update_vehicle_count("Main & 1st", 90)
        assert obj.traffic_data["Main & 1st"] == 90, "Should update count"
        assert res is obj.traffic_data or res.get("Main & 1st") == 90, "Must return updated dictionary"
    tests.append(TestCase(3, "update_vehicle_count updates count for existing intersection", tc3))

    def tc4(cls):
        obj = cls()
        res = obj.update_vehicle_count("Unknown & 2nd", 50)
        assert res == "Error: Intersection not found", f"Expected error string, got {res}"
    tests.append(TestCase(4, "update_vehicle_count returns error string when intersection not found", tc4))

    def tc5(cls):
        obj = cls()
        obj.add_intersection("Loc1", 85)
        obj.add_intersection("Loc2", 30)
        obj.add_intersection("Loc3", 50)
        congested = obj.get_congested_intersections(40)
        assert isinstance(congested, dict), "Must return a dictionary"
        assert "Loc1" in congested and "Loc3" in congested and "Loc2" not in congested, \
            "Must filter intersections with count > threshold"
    tests.append(TestCase(5, "get_congested_intersections filters count strictly > threshold", tc5))

    def tc6(cls):
        obj = cls()
        obj.add_intersection("LocExact", 50)
        congested = obj.get_congested_intersections(50)
        assert "LocExact" not in congested, "Equality with threshold must not be included"
    tests.append(TestCase(6, "get_congested_intersections threshold boundary check (strict inequality)", tc6))

    def tc7(cls):
        obj = cls()
        obj.add_intersection("HighCongestion", 81)
        signals = obj.adjust_traffic_signals()
        assert signals.get("HighCongestion") == "Long Green", "Count > 80 must receive 'Long Green'"
    tests.append(TestCase(7, "adjust_traffic_signals assigns 'Long Green' for count > 80", tc7))

    def tc8(cls):
        obj = cls()
        obj.add_intersection("MidLow", 40)
        obj.add_intersection("MidHigh", 80)
        signals = obj.adjust_traffic_signals()
        assert signals.get("MidLow") == "Normal Green" and signals.get("MidHigh") == "Normal Green", \
            "Counts between 40 and 80 inclusive must receive 'Normal Green'"
    tests.append(TestCase(8, "adjust_traffic_signals assigns 'Normal Green' for 40 <= count <= 80", tc8))

    def tc9(cls):
        obj = cls()
        obj.add_intersection("LowTraffic", 39)
        obj.add_intersection("ZeroTraffic", 0)
        signals = obj.adjust_traffic_signals()
        assert signals.get("LowTraffic") == "Short Green" and signals.get("ZeroTraffic") == "Short Green", \
            "Counts < 40 must receive 'Short Green'"
    tests.append(TestCase(9, "adjust_traffic_signals assigns 'Short Green' for count < 40", tc9))

    def tc10(cls):
        obj = cls()
        obj.add_intersection("A", 100)
        obj.add_intersection("B", 60)
        obj.add_intersection("C", 10)
        signals = obj.adjust_traffic_signals()
        assert signals == {"A": "Long Green", "B": "Normal Green", "C": "Short Green"}, \
            f"Expected mapped signals for all, got {signals}"
    tests.append(TestCase(10, "adjust_traffic_signals correctly maps full range of intersections", tc10))

    return "Smart City Traffic Control System (Class: TrafficControlSystem)", tests


def suite_oops_04_chess_tournament(c):
    tests = []

    def tc1(cls):
        obj = cls()
        res = obj.add_player("P101", "Arjun", 1850)
        assert "P101" in res or "P101" in getattr(obj, "players", {}), "Player must be added"
        details = obj.get_player_details("P101")
        assert details == {"name": "Arjun", "rating": 1850, "status": "Active"}, \
            f"Expected full player dictionary, got {details}"
    tests.append(TestCase(1, "add_player registers new player with name, rating, status='Active'", tc1))

    def tc2(cls):
        obj = cls()
        obj.add_player("P101", "Arjun", 1850)
        raised = False
        try:
            obj.add_player("P101", "Duplicate", 1900)
        except ValueError as e:
            raised = True
            assert "already exists" in str(e).lower(), f"Unexpected message: {e}"
        assert raised, "Expected ValueError when adding duplicate player ID"
    tests.append(TestCase(2, "add_player raises ValueError('Player already exists') for duplicates", tc2))

    def tc3(cls):
        obj = cls()
        obj.add_player("P102", "Priya", 1750)
        res = obj.update_rating("P102", 1820)
        details = obj.get_player_details("P102")
        assert details["rating"] == 1820, f"Expected rating 1820, got {details['rating']}"
        assert res is not None, "update_rating should return updated dictionary"
    tests.append(TestCase(3, "update_rating updates rating for existing player", tc3))

    def tc4(cls):
        obj = cls()
        obj.add_player("P103", "Rohan", 1900)
        obj.update_rating("P103", 1950)
        details = obj.get_player_details("P103")
        assert details["name"] == "Rohan" and details["status"] == "Active", \
            "update_rating must preserve name and status"
    tests.append(TestCase(4, "update_rating preserves player name and status", tc4))

    def tc5(cls):
        obj = cls()
        raised = False
        try:
            obj.update_rating("UNKNOWN", 2000)
        except KeyError as e:
            raised = True
            assert "player not found" in str(e).lower(), f"Unexpected message: {e}"
        assert raised, "Expected KeyError when updating non-existent player"
    tests.append(TestCase(5, "update_rating raises KeyError('Player not found') for unknown player", tc5))

    def tc6(cls):
        obj = cls()
        obj.add_player("P104", "Deepa", 1600)
        details = obj.get_player_details("P104")
        assert details["name"] == "Deepa" and details["rating"] == 1600, "Details must match registered player"
    tests.append(TestCase(6, "get_player_details retrieves correct player record", tc6))

    def tc7(cls):
        obj = cls()
        raised = False
        try:
            obj.get_player_details("P999")
        except KeyError as e:
            raised = True
            assert "player not found" in str(e).lower(), f"Unexpected message: {e}"
        assert raised, "Expected KeyError for unknown player ID in get_player_details"
    tests.append(TestCase(7, "get_player_details raises KeyError('Player not found')", tc7))

    def tc8(cls):
        obj = cls()
        obj.add_player("P1", "A", 2000)
        obj.add_player("P2", "B", 1500)
        obj.add_player("P3", "C", 1850)
        qual = obj.qualified_players(1800)
        assert isinstance(qual, list), "qualified_players must return a list"
        assert "P1" in qual and "P3" in qual and "P2" not in qual, "Must include only players with rating >= min_rating"
    tests.append(TestCase(8, "qualified_players filters players by minimum rating", tc8))

    def tc9(cls):
        obj = cls()
        obj.add_player("P_Exact", "Exact", 1800)
        qual = obj.qualified_players(1800)
        assert "P_Exact" in qual, "Rating exactly equal to minimum_rating must qualify (boundary check)"
    tests.append(TestCase(9, "qualified_players includes boundary match (rating == minimum_rating)", tc9))

    def tc10(cls):
        obj = cls()
        obj.add_player("P_Low", "Low", 1400)
        qual = obj.qualified_players(1900)
        assert qual == [], "Should return empty list when no players qualify"
    tests.append(TestCase(10, "qualified_players returns empty list when none qualify", tc10))

    return "Chess Tournament Player Management System (Class: ChessTournamentSystem)", tests


def suite_oops_05_library_loan(c):
    tests = []

    def tc1(cls):
        obj = cls()
        assert hasattr(obj, "loans") and isinstance(obj.loans, dict) and len(obj.loans) == 0, \
            "loans must be initialized as empty dict"
    tests.append(TestCase(1, "Initial state verification (empty self.loans)", tc1))

    def tc2(cls):
        obj = cls()
        res = obj.register_loan("L101", "Python Guide", "Alice")
        details = obj.loans.get("L101")
        assert details == {"book_title": "Python Guide", "member_name": "Alice", "status": "On Loan"}, \
            f"Expected loan structure, got {details}"
        assert res is obj.loans or res.get("L101") == details, "Must return updated loans dictionary"
    tests.append(TestCase(2, "register_loan creates record with book_title, member_name, status='On Loan'", tc2))

    def tc3(cls):
        obj = cls()
        obj.register_loan("L101", "Python Guide", "Alice")
        raised = False
        try:
            obj.register_loan("L101", "Duplicate Book", "Bob")
        except ValueError as e:
            raised = True
            assert "already registered" in str(e).lower(), f"Unexpected message: {e}"
        assert raised, "Expected ValueError when loan_id is already registered"
    tests.append(TestCase(3, "register_loan raises ValueError('Loan already registered') on duplicate", tc3))

    def tc4(cls):
        obj = cls()
        obj.register_loan("L102", "Clean Code", "Bob")
        res = obj.change_member("L102", "Charlie")
        assert obj.loans["L102"]["member_name"] == "Charlie", "Member name must be updated"
        assert res is obj.loans or res.get("L102")["member_name"] == "Charlie", "Must return updated loans dictionary"
    tests.append(TestCase(4, "change_member updates member_name on existing loan", tc4))

    def tc5(cls):
        obj = cls()
        obj.register_loan("L103", "Data Science", "Alice")
        obj.change_member("L103", "David")
        details = obj.loans["L103"]
        assert details["book_title"] == "Data Science" and details["status"] == "On Loan", \
            "book_title and status must be preserved"
    tests.append(TestCase(5, "change_member preserves book_title and status='On Loan'", tc5))

    def tc6(cls):
        obj = cls()
        raised = False
        try:
            obj.change_member("UNKNOWN", "Eve")
        except KeyError as e:
            raised = True
            assert "loan not found" in str(e).lower(), f"Unexpected message: {e}"
        assert raised, "Expected KeyError when changing member of non-existent loan"
    tests.append(TestCase(6, "change_member raises KeyError('Loan not found') for unknown loan ID", tc6))

    def tc7(cls):
        obj = cls()
        obj.register_loan("L104", "Algorithms", "Frank")
        details = obj.get_loan_details("L104")
        assert details["book_title"] == "Algorithms" and details["member_name"] == "Frank", "Details must match"
    tests.append(TestCase(7, "get_loan_details returns stored details dictionary", tc7))

    def tc8(cls):
        obj = cls()
        raised = False
        try:
            obj.get_loan_details("L999")
        except KeyError:
            raised = True
        assert raised, "Expected KeyError for unknown loan ID in get_loan_details"
    tests.append(TestCase(8, "get_loan_details raises KeyError('Loan not found')", tc8))

    def tc9(cls):
        obj = cls()
        obj.register_loan("L1", "B1", "Alice")
        obj.register_loan("L2", "B2", "Bob")
        obj.register_loan("L3", "B3", "Alice")
        loans = obj.loans_by_member("Alice")
        assert isinstance(loans, list), "loans_by_member must return a list"
        assert loans == ["L1", "L3"], f"Expected ['L1', 'L3'], got {loans}"
    tests.append(TestCase(9, "loans_by_member returns list of loans preserving insertion order", tc9))

    def tc10(cls):
        obj = cls()
        obj.register_loan("L1", "B1", "Alice")
        assert obj.loans_by_member("alice") == [], "Member matching must be case-sensitive"
        assert obj.loans_by_member("Nobody") == [], "Non-borrowing member should return empty list"
    tests.append(TestCase(10, "loans_by_member enforces case sensitivity and empty return", tc10))

    return "Library Book Loan Registry (Class: LibraryLoanRegistry)", tests


def suite_oops_06_museum_loan(c):
    tests = []

    def tc1(cls):
        obj = cls()
        assert hasattr(obj, "loans") and isinstance(obj.loans, dict) and len(obj.loans) == 0, \
            "loans must be initialized as empty dict"
    tests.append(TestCase(1, "Initial state verification (empty self.loans)", tc1))

    def tc2(cls):
        obj = cls()
        res = obj.register_loan("M201", "Vase", "Gallery A")
        expected = {"artifact_name": "Vase", "destination": "Gallery A", "status": "On Loan"}
        assert obj.loans.get("M201") == expected, f"Expected {expected}, got {obj.loans.get('M201')}"
        assert res is obj.loans or res.get("M201") == expected, "Must return updated dictionary"
    tests.append(TestCase(2, "register_loan stores artifact_name, destination, status='On Loan'", tc2))

    def tc3(cls):
        obj = cls()
        obj.register_loan("M201", "Vase", "Gallery A")
        raised = False
        try:
            obj.register_loan("M201", "Different", "Gallery B")
        except ValueError as e:
            raised = True
            assert "already registered" in str(e).lower(), f"Unexpected message: {e}"
        assert raised, "Expected ValueError on duplicate loan_id"
    tests.append(TestCase(3, "register_loan raises ValueError('Loan already registered') for duplicate", tc3))

    def tc4(cls):
        obj = cls()
        obj.register_loan("M202", "Painting", "Gallery B")
        res = obj.change_destination("M202", "National Hall")
        assert obj.loans["M202"]["destination"] == "National Hall", "Destination must be updated"
        assert res is obj.loans or res.get("M202")["destination"] == "National Hall", "Must return updated dictionary"
    tests.append(TestCase(4, "change_destination updates destination field on existing loan", tc4))

    def tc5(cls):
        obj = cls()
        obj.register_loan("M203", "Sculpture", "City Museum")
        obj.change_destination("M203", "State Museum")
        details = obj.loans["M203"]
        assert details["artifact_name"] == "Sculpture" and details["status"] == "On Loan", \
            "artifact_name and status must be preserved"
    tests.append(TestCase(5, "change_destination preserves artifact_name and status='On Loan'", tc5))

    def tc6(cls):
        obj = cls()
        raised = False
        try:
            obj.change_destination("UNKNOWN", "New Dest")
        except KeyError as e:
            raised = True
            assert "loan not found" in str(e).lower(), f"Unexpected message: {e}"
        assert raised, "Expected KeyError when destination changed on unknown loan"
    tests.append(TestCase(6, "change_destination raises KeyError('Loan not found')", tc6))

    def tc7(cls):
        obj = cls()
        obj.register_loan("M204", "Fossil", "Natural History")
        details = obj.get_loan_details("M204")
        assert details["artifact_name"] == "Fossil" and details["destination"] == "Natural History", \
            "Details must match registered artifact"
    tests.append(TestCase(7, "get_loan_details returns stored details dictionary", tc7))

    def tc8(cls):
        obj = cls()
        raised = False
        try:
            obj.get_loan_details("NONEXISTENT")
        except KeyError:
            raised = True
        assert raised, "Expected KeyError for non-existent loan in get_loan_details"
    tests.append(TestCase(8, "get_loan_details raises KeyError('Loan not found')", tc8))

    def tc9(cls):
        obj = cls()
        obj.register_loan("A1", "Art1", "City Hall")
        obj.register_loan("A2", "Art2", "Metro")
        obj.register_loan("A3", "Art3", "City Hall")
        loans = obj.loans_by_destination("City Hall")
        assert isinstance(loans, list), "loans_by_destination must return a list"
        assert loans == ["A1", "A3"], f"Expected ['A1', 'A3'], got {loans}"
    tests.append(TestCase(9, "loans_by_destination returns matching loan IDs in insertion order", tc9))

    def tc10(cls):
        obj = cls()
        obj.register_loan("A1", "Art1", "City Hall")
        assert obj.loans_by_destination("city hall") == [], "Destination check must be case-sensitive"
        assert obj.loans_by_destination("Nowhere") == [], "Empty list when destination not found"
    tests.append(TestCase(10, "loans_by_destination is case-sensitive and handles zero matches", tc10))

    return "Museum Artifact Loan Registry (Class: MuseumLoanRegistry)", tests


# ==============================================================================
# 2. PANDAS TEST SUITES (10 Test Cases Each)
# ==============================================================================

def suite_pandas_01_claim_analyzer(cls):
    tests = []

    def tc1(c):
        obj = c()
        df = obj.create_claims_df([[101, "Health", 5000.0, "Approved", "2024-01-01"]])
        assert isinstance(df, pd.DataFrame), "create_claims_df must return a DataFrame"
        assert list(df.columns) == ["CustomerID", "Category", "Amount", "Status", "Date"], \
            f"Columns mismatch: {list(df.columns)}"
    tests.append(TestCase(1, "create_claims_df builds DataFrame with exact required schema", tc1))

    def tc2(c):
        obj = c()
        data = [
            [1, "Auto", 1000.0, "Approved", "2024-01-01"],
            [2, "Auto", 2000.0, "Approved", "2024-01-02"],
            [3, "Health", 3000.0, "Rejected", "2024-01-01"],
            [4, "Health", 4000.0, "Approved", "2024-01-02"],
        ]
        df = obj.create_claims_df(data)
        rate = obj.approval_rate_by_category(df)
        auto_rate = rate[rate["Category"] == "Auto"]["Approval Rate"].iloc[0]
        health_rate = rate[rate["Category"] == "Health"]["Approval Rate"].iloc[0]
        assert auto_rate == 100.0, f"Expected 100.0% for Auto, got {auto_rate}"
        assert health_rate == 50.0, f"Expected 50.0% for Health, got {health_rate}"
    tests.append(TestCase(2, "approval_rate_by_category computes accurate percentage rates", tc2))

    def tc3(c):
        obj = c()
        df = obj.create_claims_df([[1, "Home", 500.0, "Rejected", "2024-01-01"]])
        rate = obj.approval_rate_by_category(df)
        assert list(rate.columns) == ["Category", "Approval Rate"], f"Columns mismatch: {list(rate.columns)}"
        val = rate["Approval Rate"].iloc[0]
        assert val == 0.0, f"Expected 0.0% for all-rejected category, got {val}"
    tests.append(TestCase(3, "approval_rate_by_category handles 0% approval rate and schema", tc3))

    def tc4(c):
        obj = c()
        data = [[1, "Life", 10000.0, "Approved", "2024-01-01"], [2, "Life", 50000.0, "Approved", "2024-01-02"]]
        df = obj.create_claims_df(data)
        flagged = obj.add_flag_high_amount(df, 20000.0)
        assert "IsHighValue" in flagged.columns, "Missing 'IsHighValue' column"
        assert bool(flagged["IsHighValue"].iloc[0]) is False and bool(flagged["IsHighValue"].iloc[1]) is True, \
            "High value boolean flag mismatch"
    tests.append(TestCase(4, "add_flag_high_amount appends boolean IsHighValue column", tc4))

    def tc5(c):
        obj = c()
        df = obj.create_claims_df([[1, "Auto", 25000.0, "Approved", "2024-01-01"]])
        flagged = obj.add_flag_high_amount(df, 25000.0)
        assert bool(flagged["IsHighValue"].iloc[0]) is False, \
            "Equality with threshold should evaluate to False (strict > threshold)"
    tests.append(TestCase(5, "add_flag_high_amount boundary check (Amount == threshold is False)", tc5))

    def tc6(c):
        obj = c()
        data = [
            [1, "Health", 5000.0, "Pending", "2024-01-01"],
            [2, "Health", 15000.0, "Approved", "2024-01-02"],
            [3, "Auto", 12000.0, "Pending", "2024-01-03"],
        ]
        df = obj.create_claims_df(data)
        top = obj.get_top_pending_claims(df, 1)
        assert len(top) == 1 and top["Status"].iloc[0] == "Pending", "Must filter only Pending status"
        assert top["Amount"].iloc[0] == 12000.0, "Must be sorted descending by Amount"
    tests.append(TestCase(6, "get_top_pending_claims filters Pending claims and sorts descending", tc6))

    def tc7(c):
        obj = c()
        data = [
            [1, "A", 100.0, "Pending", "2024-01-01"],
            [2, "B", 300.0, "Pending", "2024-01-02"],
            [3, "C", 200.0, "Pending", "2024-01-03"],
        ]
        df = obj.create_claims_df(data)
        top = obj.get_top_pending_claims(df, 2)
        assert len(top) == 2, "Must return exactly top n rows"
        amounts = list(top["Amount"])
        assert amounts == [300.0, 200.0], f"Expected [300.0, 200.0], got {amounts}"
    tests.append(TestCase(7, "get_top_pending_claims respects limit parameter n", tc7))

    def tc8(c):
        obj = c()
        data = [
            [1, "Health", 1000.0, "Approved", "2024-01-01"],
            [2, "Health", 3000.0, "Approved", "2024-01-02"],
            [3, "Auto", 2000.0, "Pending", "2024-01-03"],
        ]
        df = obj.create_claims_df(data)
        summary = obj.claim_summary_by_status(df)
        assert set(summary.columns) == {"Status", "sum", "min", "max", "avg"}, \
            f"Expected ['Status', 'sum', 'min', 'max', 'avg'], got {list(summary.columns)}"
    tests.append(TestCase(8, "claim_summary_by_status output has columns Status, sum, min, max, avg", tc8))

    def tc9(c):
        obj = c()
        data = [
            [1, "Health", 1000.0, "Approved", "2024-01-01"],
            [2, "Health", 3000.0, "Approved", "2024-01-02"],
        ]
        df = obj.create_claims_df(data)
        summary = obj.claim_summary_by_status(df)
        row = summary[summary["Status"] == "Approved"].iloc[0]
        assert row["sum"] == 4000.0 and row["min"] == 1000.0 and row["max"] == 3000.0 and row["avg"] == 2000.0, \
            f"Aggregated statistics mismatch: {row.to_dict()}"
    tests.append(TestCase(9, "claim_summary_by_status calculates exact math for sum, min, max, avg", tc9))

    def tc10(c):
        obj = c()
        data = [[1, "Health", 1000.0, "Approved", "2024-01-01"]]
        df = obj.create_claims_df(data)
        _ = obj.add_flag_high_amount(df, 500.0)
        assert "IsHighValue" not in df.columns, "Methods should not mutate original DataFrame in place"
    tests.append(TestCase(10, "Methods operate non-destructively on DataFrame copies", tc10))

    return "Insurance Claim Processing (Class: ClaimAnalyzer)", tests


def suite_pandas_02_solar_farm(cls):
    tests = []

    def tc1(c):
        obj = c()
        df = obj.create_production_df([["T1", "2025-08-01", 500.0, 5.4, 30]])
        assert list(df.columns) == ["TurbineID", "Date", "Energy", "WindSpeed", "OutageMinutes"], \
            f"Columns mismatch: {list(df.columns)}"
    tests.append(TestCase(1, "create_production_df builds schema with 5 required columns", tc1))

    def tc2(c):
        obj = c()
        data = [
            ["T1", "2025-08-01", 500.0, 5.0, 0],
            ["T2", "2025-08-01", 800.0, 4.0, 0],
            ["T1", "2025-08-02", 700.0, 6.0, 0],
        ]
        df = obj.create_production_df(data)
        total = obj.total_energy_per_turbine(df)
        assert "TurbineID" in total.columns and "TotalEnergy" in total.columns, "Must have TurbineID and TotalEnergy"
        t1_val = total[total["TurbineID"] == "T1"]["TotalEnergy"].iloc[0]
        assert t1_val == 1200.0, f"Expected 1200.0 for T1, got {t1_val}"
    tests.append(TestCase(2, "total_energy_per_turbine aggregates energy and renames to TotalEnergy", tc2))

    def tc3(c):
        obj = c()
        df = obj.create_production_df([["T1", "2025-08-01", 1440.0, 5.0, 0]])
        res = obj.add_energy_per_min(df)
        assert "EnergyPerMin" in res.columns, "Must contain EnergyPerMin"
        # 1440 minutes in day, 0 outage => 1440 / 1440 = 1.0
        assert math.isclose(res["EnergyPerMin"].iloc[0], 1.0, abs_tol=0.01)
    tests.append(TestCase(3, "add_energy_per_min computes Energy / (1440 - OutageMinutes)", tc3))

    def tc4(c):
        obj = c()
        df = obj.create_production_df([["T1", "2025-08-01", 720.0, 5.0, 720]])
        res = obj.add_energy_per_min(df)
        # ActiveMinutes = 1440 - 720 = 720 => 720 / 720 = 1.0
        assert math.isclose(res["EnergyPerMin"].iloc[0], 1.0, abs_tol=0.01)
    tests.append(TestCase(4, "add_energy_per_min correctly factors OutageMinutes into uptime", tc4))

    def tc5(c):
        obj = c()
        data = [
            ["T1", "2025-08-01", 100.0, 7.5, 0],
            ["T2", "2025-08-01", 100.0, 7.0, 0],
        ]
        df = obj.create_production_df(data)
        res = obj.categorize_wind_band(df)
        assert list(res["WindBand"]) == ["High", "High"], "WindSpeed >= 7 must be 'High'"
    tests.append(TestCase(5, "categorize_wind_band maps WindSpeed >= 7 to 'High'", tc5))

    def tc6(c):
        obj = c()
        data = [
            ["T1", "2025-08-01", 100.0, 3.0, 0],
            ["T2", "2025-08-01", 100.0, 6.9, 0],
        ]
        df = obj.create_production_df(data)
        res = obj.categorize_wind_band(df)
        assert list(res["WindBand"]) == ["Moderate", "Moderate"], "3 <= WindSpeed < 7 must be 'Moderate'"
    tests.append(TestCase(6, "categorize_wind_band maps 3 <= WindSpeed < 7 to 'Moderate'", tc6))

    def tc7(c):
        obj = c()
        data = [["T1", "2025-08-01", 100.0, 2.9, 0], ["T2", "2025-08-01", 100.0, 0.0, 0]]
        df = obj.create_production_df(data)
        res = obj.categorize_wind_band(df)
        assert list(res["WindBand"]) == ["Low", "Low"], "WindSpeed < 3 must be 'Low'"
    tests.append(TestCase(7, "categorize_wind_band maps WindSpeed < 3 to 'Low'", tc7))

    def tc8(c):
        obj = c()
        data = [
            ["T1", "2025-08-01", 100.0, 5.0, 15],
            ["T2", "2025-08-01", 200.0, 5.0, 45],
            ["T3", "2025-08-01", 300.0, 5.0, 60],
        ]
        df = obj.create_production_df(data)
        filtered = obj.frequent_outage_rows(df, 30)
        assert len(filtered) == 2 and list(filtered["TurbineID"]) == ["T2", "T3"], \
            "Must return rows where OutageMinutes > 30"
    tests.append(TestCase(8, "frequent_outage_rows filters OutageMinutes strictly > n", tc8))

    def tc9(c):
        obj = c()
        data = [
            ["T1", "2025-08-01", 500.0, 5.0, 10],
            ["T2", "2025-08-01", None, 5.0, 10],
            ["T3", "2025-08-01", 800.0, 5.0, 10],
        ]
        df = obj.create_production_df(data)
        cleaned = obj.clean_and_top_days(df)
        assert len(cleaned) == 2 and "T2" not in list(cleaned["TurbineID"]), "Must drop NaN rows"
    tests.append(TestCase(9, "clean_and_top_days removes rows with null values", tc9))

    def tc10(c):
        obj = c()
        data = [
            ["T1", "2025-08-01", 300.0, 5.0, 0],
            ["T2", "2025-08-01", 900.0, 5.0, 0],
            ["T3", "2025-08-01", 600.0, 5.0, 0],
        ]
        df = obj.create_production_df(data)
        sorted_df = obj.clean_and_top_days(df)
        assert list(sorted_df["Energy"]) == [900.0, 600.0, 300.0], "Must be sorted descending by Energy"
    tests.append(TestCase(10, "clean_and_top_days sorts results descending by Energy", tc10))

    return "Solar Farm Production Analyzer (Class: SolarFarmAnalyzer)", tests


def suite_pandas_03_marketplace_returns(cls):
    tests = []

    def tc1(c):
        obj = c()
        o = obj.create_orders_df([[1, "S1", "Toys", "2024-07-01", 500.0]])
        assert list(o.columns) == ["OrderID", "SellerID", "Category", "OrderDate", "OrderAmount"]
    tests.append(TestCase(1, "create_orders_df creates schema: OrderID, SellerID, Category, OrderDate, OrderAmount", tc1))

    def tc2(c):
        obj = c()
        r = obj.create_returns_df([[1, "2024-07-05", 500.0, "Defective"]])
        assert list(r.columns) == ["OrderID", "ReturnDate", "RefundAmount", "Reason"]
    tests.append(TestCase(2, "create_returns_df creates schema: OrderID, ReturnDate, RefundAmount, Reason", tc2))

    def tc3(c):
        obj = c()
        o = obj.create_orders_df([[1, "S1", "Toys", "2024-07-01", 500.0], [2, "S2", "Books", "2024-07-02", 300.0]])
        r = obj.create_returns_df([[1, "2024-07-05", 500.0, "Defective"]])
        merged = obj.merge_orders_returns(o, r)
        assert len(merged) == 2, "Merge must retain all orders (left join)"
        assert pd.notna(merged.loc[merged["OrderID"] == 1, "RefundAmount"].values[0])
        assert pd.isna(merged.loc[merged["OrderID"] == 2, "RefundAmount"].values[0])
    tests.append(TestCase(3, "merge_orders_returns joins orders with returns on OrderID", tc3))

    def tc4(c):
        obj = c()
        o = obj.create_orders_df([
            [1, "S1", "Tech", "2024-07-01", 1000.0],
            [2, "S1", "Tech", "2024-07-02", 1000.0],
            [3, "S2", "Books", "2024-07-03", 200.0],
        ])
        r = obj.create_returns_df([[1, "2024-07-05", 1000.0, "Defective"]])
        merged = obj.merge_orders_returns(o, r)
        rates = obj.category_refund_rate(merged)
        tech_rate = rates[rates["Category"] == "Tech"]["RefundRate"].iloc[0]
        books_rate = rates[rates["Category"] == "Books"]["RefundRate"].iloc[0]
        assert tech_rate == 50.0, f"Expected 50% refund rate for Tech, got {tech_rate}"
        assert books_rate == 0.0, f"Expected 0% refund rate for Books, got {books_rate}"
    tests.append(TestCase(4, "category_refund_rate computes correct percentage RefundRate", tc4))

    def tc5(c):
        obj = c()
        o = obj.create_orders_df([[1, "S1", "Toys", "2024-07-01", 100.0]])
        r = obj.create_returns_df([])
        merged = obj.merge_orders_returns(o, r)
        rates = obj.category_refund_rate(merged)
        assert list(rates.columns) == ["Category", "Orders", "ReturnedOrders", "RefundRate"], \
            f"Columns mismatch: {list(rates.columns)}"
    tests.append(TestCase(5, "category_refund_rate produces exact required column names", tc5))

    def tc6(c):
        obj = c()
        o = obj.create_orders_df([
            [1, "S1", "Zebra", "2024-07-01", 100.0],
            [2, "S1", "Apple", "2024-07-02", 100.0],
        ])
        r = obj.create_returns_df([])
        merged = obj.merge_orders_returns(o, r)
        rates = obj.category_refund_rate(merged)
        assert list(rates["Category"]) == ["Apple", "Zebra"], "Output must be sorted by Category ascending"
    tests.append(TestCase(6, "category_refund_rate sorts by Category ascending", tc6))

    def tc7(c):
        obj = c()
        o = obj.create_orders_df([
            [1, "S1", "A", "2024-07-01", 100.0],
            [2, "S1", "A", "2024-07-02", 100.0],
            [3, "S2", "A", "2024-07-03", 100.0],
        ])
        r = obj.create_returns_df([
            [1, "2024-07-05", 100.0, "Defective"],
            [2, "2024-07-06", 100.0, "Wrong Item"],
            [3, "2024-07-07", 100.0, "Damaged"],
        ])
        merged = obj.merge_orders_returns(o, r)
        high = obj.high_return_sellers(merged, 1)
        assert len(high) == 1 and high["SellerID"].iloc[0] == "S1" and high["ReturnCount"].iloc[0] == 2, \
            "Should identify sellers with ReturnCount > n"
    tests.append(TestCase(7, "high_return_sellers identifies sellers exceeding return threshold n", tc7))

    def tc8(c):
        obj = c()
        o = obj.create_orders_df([[1, "S1", "A", "2024-07-01", 100.0]])
        r = obj.create_returns_df([[1, "2024-07-05", 100.0, "Broken"]])
        merged = obj.merge_orders_returns(o, r)
        high = obj.high_return_sellers(merged, 1)
        assert len(high) == 0, "Strict > comparison must exclude equality with threshold"
    tests.append(TestCase(8, "high_return_sellers strict inequality boundary check", tc8))

    def tc9(c):
        obj = c()
        raw = [
            [1, "2024-07-05", 500.0, "Defective"],
            [2, "2024-07-06", 500.0, None],
            [3, "2024-07-07", 0.0, "No Reason"],
            [4, "2024-07-08", -10.0, "Invalid Amount"],
        ]
        r = obj.create_returns_df(raw)
        cleaned = obj.clean_returns_data(r)
        assert len(cleaned) == 1 and cleaned["OrderID"].iloc[0] == 1, \
            "Must drop null reasons and refund amounts <= 0"
    tests.append(TestCase(9, "clean_returns_data drops null reasons and non-positive refund amounts", tc9))

    def tc10(c):
        obj = c()
        r = obj.create_returns_df([[10, "2024-07-05", 250.0, "Wrong Size"]])
        cleaned = obj.clean_returns_data(r)
        assert cleaned.index[0] == 0, "Cleaned DataFrame must reset index with drop=True"
    tests.append(TestCase(10, "clean_returns_data returns zero-based indexed copy", tc10))

    return "Marketplace Returns and Refund Analysis (Class: ReturnsAnalyzer)", tests


def suite_pandas_04_ev_charging(cls):
    tests = []

    def tc1(c):
        obj = c()
        raw = [[501, "ST01", "Bengaluru", "2025-02-01", 42.5, 75, "Paid"]]
        df = obj.create_sessions_df(raw)
        assert list(df.columns) == ["SessionID", "StationID", "City", "ChargingDate", "EnergyKWh", "DurationMinutes", "PaymentStatus"]
        assert isinstance(df["ChargingDate"].iloc[0], str), "ChargingDate must be preserved as string"
    tests.append(TestCase(1, "create_sessions_df creates 7 columns with string ChargingDate", tc1))

    def tc2(c):
        obj = c()
        raw = [
            [1, "ST1", "CityA", "2025-01-01", 30.0, 45, "Paid"],
            [None, "ST1", "CityA", "2025-01-01", 30.0, 45, "Paid"],
            [2, None, "CityA", "2025-01-01", 30.0, 45, "Paid"],
            [3, "ST1", None, "2025-01-01", 30.0, 45, "Paid"],
            [4, "ST1", "CityA", "2025-01-01", 30.0, 45, None],
        ]
        df = obj.create_sessions_df(raw)
        cleaned = obj.clean_sessions_data(df)
        assert len(cleaned) == 1 and cleaned["SessionID"].iloc[0] == 1, "Must drop rows with null key columns"
    tests.append(TestCase(2, "clean_sessions_data drops rows with null identifiers or status", tc2))

    def tc3(c):
        obj = c()
        raw = [
            [1, "ST1", "CityA", "2025-01-01", 0.0, 30, "Paid"],
            [2, "ST1", "CityA", "2025-01-01", 10.0, 0, "Paid"],
            [3, "ST1", "CityA", "2025-01-01", 20.0, 30, "UnknownStatus"],
            [4, "ST1", "CityA", "2025-01-01", 25.0, 40, "Pending"],
            [5, "ST1", "CityA", "2025-01-01", 30.0, 50, "Failed"],
        ]
        df = obj.create_sessions_df(raw)
        cleaned = obj.clean_sessions_data(df)
        assert len(cleaned) == 2 and set(cleaned["PaymentStatus"]) == {"Pending", "Failed"}, \
            "Must keep Energy > 0, Duration > 0, and PaymentStatus in Paid/Pending/Failed"
    tests.append(TestCase(3, "clean_sessions_data validates numeric positivity and allowed statuses", tc3))

    def tc4(c):
        obj = c()
        df = obj.create_sessions_df([
            [1, "ST1", "CityA", "2025-01-01", 10.0, 100, "Paid"],
            [2, "ST1", "CityA", "2025-01-01", 10.0, 60, "Paid"],
        ])
        flagged = obj.add_long_session_flag(df, 90)
        assert "IsLongSession" in flagged.columns
        assert list(flagged["IsLongSession"]) == [1, 0]
    tests.append(TestCase(4, "add_long_session_flag creates binary 1/0 indicator", tc4))

    def tc5(c):
        obj = c()
        df = obj.create_sessions_df([[1, "ST1", "CityA", "2025-01-01", 10.0, 90, "Paid"]])
        flagged = obj.add_long_session_flag(df, 90)
        assert flagged["IsLongSession"].iloc[0] == 0, "Duration equal to threshold must produce 0"
    tests.append(TestCase(5, "add_long_session_flag threshold boundary equality evaluates to 0", tc5))

    def tc6(c):
        obj = c()
        raw = [
            [1, "ST01", "CityA", "2025-01-01", 40.0, 60, "Paid"],
            [2, "ST01", "CityA", "2025-01-02", 60.0, 90, "Paid"],
        ]
        df = obj.create_sessions_df(raw)
        util = obj.station_utilization_summary(df)
        assert list(util.columns) == ["StationID", "SessionCount", "TotalEnergyKWh", "AverageDuration"]
        row = util.iloc[0]
        assert row["SessionCount"] == 2 and row["TotalEnergyKWh"] == 100.0 and row["AverageDuration"] == 75.0
    tests.append(TestCase(6, "station_utilization_summary computes count, sum, and mean duration", tc6))

    def tc7(c):
        obj = c()
        df = obj.create_sessions_df([
            [1, "ST1", "CityA", "2025-01-01", 50.0, 70, "Paid"],
            [2, "ST1", "CityA", "2025-01-01", 60.0, 80, "Paid"],
            [3, "ST2", "CityA", "2025-01-01", 30.0, 40, "Paid"],
        ] )
        high = obj.high_energy_stations(df, 100.0)
        assert len(high) == 1 and high["StationID"].iloc[0] == "ST1"
        assert high["TotalEnergyKWh"].iloc[0] == 110.0
    tests.append(TestCase(7, "high_energy_stations aggregates and filters TotalEnergyKWh > threshold", tc7))

    def tc8(c):
        obj = c()
        df = obj.create_sessions_df([[1, "ST1", "CityA", "2025-01-01", 100.0, 60, "Paid"]])
        high = obj.high_energy_stations(df, 100.0)
        assert len(high) == 0, "Strict > comparison must exclude boundary match"
    tests.append(TestCase(8, "high_energy_stations strict inequality boundary check", tc8))

    def tc9(c):
        obj = c()
        raw = [
            [1, "ST1", "CityA", "2025-01-01", 10.0, 30, "Paid"],
            [2, "ST1", "CityA", "2025-01-01", 20.0, 40, "Pending"],
            [3, "ST2", "CityB", "2025-01-01", 15.0, 35, "Paid"],
        ]
        df = obj.create_sessions_df(raw)
        rev = obj.city_revenue_summary(df)
        assert "City" in rev.columns and "Revenue" in rev.columns
        # CityA Paid: 10 * 18 = 180 (Pending excluded)
        # CityB Paid: 15 * 18 = 270
        a_rev = rev[rev["City"] == "CityA"]["Revenue"].iloc[0]
        assert a_rev == 180.0, f"Expected 180.0 for CityA, got {a_rev}"
    tests.append(TestCase(9, "city_revenue_summary calculates Revenue = EnergyKWh * 18 for Paid sessions only", tc9))

    def tc10(c):
        obj = c()
        raw = [[1, "ST1", "CityA", "2025-01-01", 10.0, 30, "Paid"]]
        df = obj.create_sessions_df(raw)
        rev = obj.city_revenue_summary(df)
        assert rev.index[0] == 0, "Revenue summary must return zero-based indexed DataFrame"
    tests.append(TestCase(10, "city_revenue_summary returns zero-based index", tc10))

    return "Electric Vehicle Charging Station Analysis (Class: EVChargingAnalyzer)", tests


def suite_pandas_05_hospital_equipment(cls):
    tests = []

    def tc1(c):
        obj = c()
        raw = [["S1", "EQ1", "Cardio", "2025-01-01", 100.0, 2.5, "Completed"]]
        df = obj.create_services_df(raw)
        assert list(df.columns) == ["ServiceID", "EquipmentID", "Department", "ServiceDate", "UsageHours", "DowntimeHours", "ServiceStatus"]
    tests.append(TestCase(1, "create_services_df creates DataFrame with 7 required columns", tc1))

    def tc2(c):
        obj = c()
        raw = [
            ["S1", "EQ1", "Cardio", "2025-01-01", 100.0, 2.0, "Completed"],
            ["S2", "EQ1", "Cardio", "2025-01-01", None, 2.0, "Completed"],
            ["S3", "EQ1", "Cardio", "2025-01-01", 0.0, 2.0, "Completed"],
            ["S4", "EQ1", "Cardio", "2025-01-01", 50.0, -1.0, "Completed"],
            ["S5", "EQ1", "Cardio", "2025-01-01", 50.0, 1.0, "Cancelled"],
        ]
        df = obj.create_services_df(raw)
        cleaned = obj.clean_service_data(df)
        assert len(cleaned) == 1 and cleaned["ServiceID"].iloc[0] == "S1"
    tests.append(TestCase(2, "clean_service_data drops nulls, Usage<=0, Downtime<0, and invalid statuses", tc2))

    def tc3(c):
        obj = c()
        raw = [
            ["S1", "EQ1", "Cardio", "2025-01-01", 10.0, 0.0, "Scheduled"],
            ["S2", "EQ2", "Cardio", "2025-01-01", 20.0, 1.0, "Completed"],
        ]
        df = obj.create_services_df(raw)
        cleaned = obj.clean_service_data(df)
        assert len(cleaned) == 2 and set(cleaned["ServiceStatus"]) == {"Scheduled", "Completed"}, \
            "Both Scheduled and Completed with Downtime>=0 are valid"
    tests.append(TestCase(3, "clean_service_data allows DowntimeHours == 0 and Scheduled status", tc3))

    def tc4(c):
        obj = c()
        df = obj.create_services_df([
            ["S1", "EQ1", "Cardio", "2025-01-01", 10.0, 5.0, "Completed"],
            ["S2", "EQ1", "Cardio", "2025-01-01", 10.0, 2.0, "Completed"],
        ])
        res = obj.add_attention_flag(df, 3.0)
        assert "NeedsAttention" in res.columns
        assert list(res["NeedsAttention"]) == [1, 0]
    tests.append(TestCase(4, "add_attention_flag creates NeedsAttention binary flag", tc4))

    def tc5(c):
        obj = c()
        df = obj.create_services_df([["S1", "EQ1", "Cardio", "2025-01-01", 10.0, 4.0, "Completed"]])
        res = obj.add_attention_flag(df, 4.0)
        assert res["NeedsAttention"].iloc[0] == 0, "Equality with downtime_threshold must be 0"
    tests.append(TestCase(5, "add_attention_flag boundary check (Downtime == threshold produces 0)", tc5))

    def tc6(c):
        obj = c()
        raw = [
            ["S1", "EQ01", "A", "2025-01-01", 50.0, 2.0, "Completed"],
            ["S2", "EQ01", "A", "2025-01-02", 70.0, 3.5, "Completed"],
        ]
        df = obj.create_services_df(raw)
        summary = obj.equipment_performance_summary(df)
        assert list(summary.columns) == ["EquipmentID", "ServiceCount", "TotalUsageHours", "AverageDowntime"]
        row = summary.iloc[0]
        assert row["ServiceCount"] == 2 and row["TotalUsageHours"] == 120.0 and row["AverageDowntime"] == 2.75
    tests.append(TestCase(6, "equipment_performance_summary computes count, sum, and 2-decimal average", tc6))

    def tc7(c):
        obj = c()
        raw = [
            ["S1", "EQ02", "A", "2025-01-01", 10.0, 1.0, "Completed"],
            ["S2", "EQ01", "A", "2025-01-01", 10.0, 1.0, "Completed"],
        ]
        df = obj.create_services_df(raw)
        summary = obj.equipment_performance_summary(df)
        assert list(summary["EquipmentID"]) == ["EQ01", "EQ02"], "Must sort ascending by EquipmentID"
    tests.append(TestCase(7, "equipment_performance_summary sorts ascending by EquipmentID", tc7))

    def tc8(c):
        obj = c()
        raw = [
            ["S1", "EQ1", "A", "2025-01-01", 40.0, 1.0, "Completed"],
            ["S2", "EQ2", "A", "2025-01-01", 150.0, 1.0, "Completed"],
        ]
        df = obj.create_services_df(raw)
        low = obj.low_usage_equipment(df, 100.0)
        assert len(low) == 1 and low["EquipmentID"].iloc[0] == "EQ1" and low["TotalUsageHours"].iloc[0] == 40.0
    tests.append(TestCase(8, "low_usage_equipment filters TotalUsageHours strictly < threshold", tc8))

    def tc9(c):
        obj = c()
        raw = [
            ["S1", "E1", "Cardio", "2025-01-01", 10.0, 2.0, "Completed"],
            ["S2", "E1", "Cardio", "2025-01-01", 10.0, 4.0, "Scheduled"],
            ["S3", "E2", "Radiology", "2025-01-01", 10.0, 3.0, "Completed"],
        ]
        df = obj.create_services_df(raw)
        cost = obj.departmental_service_cost(df)
        assert list(cost.columns) == ["Department", "ServiceCost"]
        # Cardio: 2.0 * 300 = 600 (Scheduled excluded)
        # Radiology: 3.0 * 300 = 900
        cardio_cost = cost[cost["Department"] == "Cardio"]["ServiceCost"].iloc[0]
        assert cardio_cost == 600.0, f"Expected 600.0 for Cardio, got {cardio_cost}"
    tests.append(TestCase(9, "departmental_service_cost calculates DowntimeHours * 300 for Completed services", tc9))

    def tc10(c):
        obj = c()
        raw = [
            ["S1", "E1", "Surgery", "2025-01-01", 10.0, 2.0, "Completed"],
            ["S2", "E2", "Anesthesia", "2025-01-01", 10.0, 1.0, "Completed"],
        ]
        df = obj.create_services_df(raw)
        cost = obj.departmental_service_cost(df)
        assert list(cost["Department"]) == ["Anesthesia", "Surgery"], "Must sort by Department ascending"
    tests.append(TestCase(10, "departmental_service_cost sorts by Department ascending", tc10))

    return "Hospital Equipment Service Analyzer (Class: HospitalEquipmentAnalyzer)", tests


def suite_pandas_06_solar_maintenance(cls):
    tests = []

    def tc1(c):
        obj = c()
        raw = [["INS1", "S1", "North", "2025-01-01", 120.0, 3.0, "Completed"]]
        df = obj.create_inspections_df(raw)
        assert list(df.columns) == ["InspectionID", "SiteID", "Region", "InspectionDate", "OutputMWh", "DowntimeHours", "MaintenanceStatus"]
    tests.append(TestCase(1, "create_inspections_df builds schema with 7 exact columns", tc1))

    def tc2(c):
        obj = c()
        raw = [
            ["I1", "S1", "R1", "2025-01-01", 100.0, 2.0, "Completed"],
            ["I2", "S1", "R1", "2025-01-01", None, 2.0, "Completed"],
            ["I3", "S1", "R1", "2025-01-01", -5.0, 2.0, "Completed"],
            ["I4", "S1", "R1", "2025-01-01", 100.0, -1.0, "Completed"],
            ["I5", "S1", "R1", "2025-01-01", 100.0, 2.0, "Pending"],
        ]
        df = obj.create_inspections_df(raw)
        cleaned = obj.clean_inspection_data(df)
        assert len(cleaned) == 1 and cleaned["InspectionID"].iloc[0] == "I1"
    tests.append(TestCase(2, "clean_inspection_data drops nulls, Output<=0, Downtime<0, and invalid status", tc2))

    def tc3(c):
        obj = c()
        raw = [["I1", "S1", "R1", "2025-01-01", 50.0, 0.0, "Scheduled"]]
        df = obj.create_inspections_df(raw)
        cleaned = obj.clean_inspection_data(df)
        assert len(cleaned) == 1 and cleaned["MaintenanceStatus"].iloc[0] == "Scheduled", \
            "Scheduled with DowntimeHours == 0 must be retained"
    tests.append(TestCase(3, "clean_inspection_data retains DowntimeHours == 0 and Scheduled status", tc3))

    def tc4(c):
        obj = c()
        df = obj.create_inspections_df([
            ["I1", "S1", "R1", "2025-01-01", 50.0, 5.0, "Completed"],
            ["I2", "S1", "R1", "2025-01-01", 50.0, 2.0, "Completed"],
        ])
        flagged = obj.add_attention_flag(df, 3.0)
        assert "NeedsAttention" in flagged.columns
        assert list(flagged["NeedsAttention"]) == [1, 0]
    tests.append(TestCase(4, "add_attention_flag creates NeedsAttention binary flag", tc4))

    def tc5(c):
        obj = c()
        df = obj.create_inspections_df([["I1", "S1", "R1", "2025-01-01", 50.0, 4.0, "Completed"]])
        flagged = obj.add_attention_flag(df, 4.0)
        assert flagged["NeedsAttention"].iloc[0] == 0, "Downtime equal to threshold must evaluate to 0"
    tests.append(TestCase(5, "add_attention_flag boundary check (Downtime == threshold produces 0)", tc5))

    def tc6(c):
        obj = c()
        raw = [
            ["I1", "S1", "R1", "2025-01-01", 100.0, 2.0, "Completed"],
            ["I2", "S1", "R1", "2025-01-02", 150.0, 3.5, "Completed"],
        ]
        df = obj.create_inspections_df(raw)
        summary = obj.site_performance_summary(df)
        assert list(summary.columns) == ["SiteID", "InspectionCount", "TotalOutputMWh", "AverageDowntime"]
        row = summary.iloc[0]
        assert row["InspectionCount"] == 2 and row["TotalOutputMWh"] == 250.0 and row["AverageDowntime"] == 2.75
    tests.append(TestCase(6, "site_performance_summary computes count, sum, and 2-decimal average", tc6))

    def tc7(c):
        obj = c()
        raw = [
            ["I1", "SiteB", "R1", "2025-01-01", 100.0, 1.0, "Completed"],
            ["I2", "SiteA", "R1", "2025-01-01", 100.0, 1.0, "Completed"],
        ]
        df = obj.create_inspections_df(raw)
        summary = obj.site_performance_summary(df)
        assert list(summary["SiteID"]) == ["SiteA", "SiteB"], "Must be sorted by SiteID ascending"
    tests.append(TestCase(7, "site_performance_summary sorts by SiteID ascending", tc7))

    def tc8(c):
        obj = c()
        raw = [
            ["I1", "Site1", "R1", "2025-01-01", 80.0, 1.0, "Completed"],
            ["I2", "Site2", "R1", "2025-01-01", 250.0, 1.0, "Completed"],
        ]
        df = obj.create_inspections_df(raw)
        low = obj.low_output_sites(df, 100.0)
        assert len(low) == 1 and low["SiteID"].iloc[0] == "Site1" and low["TotalOutputMWh"].iloc[0] == 80.0
    tests.append(TestCase(8, "low_output_sites filters TotalOutputMWh strictly < threshold", tc8))

    def tc9(c):
        obj = c()
        raw = [
            ["I1", "S1", "West", "2025-01-01", 50.0, 4.0, "Completed"],
            ["I2", "S1", "West", "2025-01-01", 50.0, 2.0, "Scheduled"],
            ["I3", "S2", "East", "2025-01-01", 50.0, 3.0, "Completed"],
        ]
        df = obj.create_inspections_df(raw)
        cost = obj.regional_maintenance_cost(df)
        assert list(cost.columns) == ["Region", "MaintenanceCost"]
        # West: 4.0 * 250 = 1000 (Scheduled excluded)
        # East: 3.0 * 250 = 750
        west_cost = cost[cost["Region"] == "West"]["MaintenanceCost"].iloc[0]
        assert west_cost == 1000.0, f"Expected 1000.0 for West, got {west_cost}"
    tests.append(TestCase(9, "regional_maintenance_cost calculates DowntimeHours * 250 for Completed only", tc9))

    def tc10(c):
        obj = c()
        raw = [
            ["I1", "S1", "North", "2025-01-01", 50.0, 2.0, "Completed"],
            ["I2", "S2", "Central", "2025-01-01", 50.0, 2.0, "Completed"],
        ]
        df = obj.create_inspections_df(raw)
        cost = obj.regional_maintenance_cost(df)
        assert list(cost["Region"]) == ["Central", "North"], "Must sort by Region ascending"
    tests.append(TestCase(10, "regional_maintenance_cost sorts by Region ascending", tc10))

    return "Solar Farm Maintenance Analysis (Class: SolarMaintenanceAnalyzer)", tests


# ==============================================================================
# 3. NUMPY TEST SUITES (10 Test Cases Each)
# ==============================================================================

def suite_numpy_01_city_aqi(m):
    tests = []

    def tc1(mod):
        arr = mod.create_aqi_array([50, 75, 120])
        assert isinstance(arr, np.ndarray), "Must return a NumPy ndarray"
        assert arr.dtype == np.int64, f"Expected dtype int64, got {arr.dtype}"
    tests.append(TestCase(1, "create_aqi_array creates 1D array with dtype int64", tc1))

    def tc2(mod):
        arr = mod.create_aqi_array([0, 50, 100])
        assert mod.validate_aqi_array(arr) is True, "Array with values 0..100 must validate as True"
    tests.append(TestCase(2, "validate_aqi_array returns True for values in [0, 100]", tc2))

    def tc3(mod):
        arr = mod.create_aqi_array([])
        assert mod.validate_aqi_array(arr) is False, "Empty array must return False"
    tests.append(TestCase(3, "validate_aqi_array returns False for empty array", tc3))

    def tc4(mod):
        arr = mod.create_aqi_array([25, 101])
        assert mod.validate_aqi_array(arr) is False, "Array with value > 100 must return False"
        arr_neg = mod.create_aqi_array([-1, 50])
        assert mod.validate_aqi_array(arr_neg) is False, "Array with negative value must return False"
    tests.append(TestCase(4, "validate_aqi_array rejects out-of-range values (<0 or >100)", tc4))

    def tc5(mod):
        arr = np.array(["a", "b", "c"])
        res = mod.validate_aqi_array(arr)
        assert res is False, "Non-numeric array must return False without raising exceptions"
    tests.append(TestCase(5, "validate_aqi_array returns False for non-numeric arrays safely", tc5))

    def tc6(mod):
        arr = mod.create_aqi_array([50, 100, 150])
        stats = mod.compute_aqi_stats(arr)
        assert isinstance(stats, tuple) and len(stats) == 4, "Must return 4-tuple (mean, std, max, min)"
        mean_val, std_val, max_val, min_val = stats
        assert math.isclose(mean_val, 100.0, abs_tol=0.01)
        assert max_val == 150.0 and min_val == 50.0
    tests.append(TestCase(6, "compute_aqi_stats calculates accurate mean, std, max, min", tc6))

    def tc7(mod):
        arr = mod.create_aqi_array([25, 75, 125])
        cats = list(mod.categorize_aqi(arr))
        assert cats == ["Good", "Moderate", "USG"], f"Expected ['Good', 'Moderate', 'USG'], got {cats}"
    tests.append(TestCase(7, "categorize_aqi maps 0-50 Good, 51-100 Moderate, 101-150 USG", tc7))

    def tc8(mod):
        arr = mod.create_aqi_array([175, 250, 400])
        cats = list(mod.categorize_aqi(arr))
        assert cats == ["Unhealthy", "Very Unhealthy", "Hazardous"], f"Expected ['Unhealthy', 'Very Unhealthy', 'Hazardous'], got {cats}"
    tests.append(TestCase(8, "categorize_aqi maps 151-200 Unhealthy, 201-300 Very Unhealthy, 301-500 Hazardous", tc8))

    def tc9(mod):
        arr = mod.create_aqi_array([100, 160, 170, 180, 120, 165])
        streak = mod.longest_unhealthy_streak(arr)
        assert streak == 3, f"Expected streak of 3, got {streak}"
    tests.append(TestCase(9, "longest_unhealthy_streak tracks consecutive days where AQI >= 151", tc9))

    def tc10(mod):
        arr = mod.create_aqi_array([50, 80, 120])
        streak = mod.longest_unhealthy_streak(arr)
        assert streak == 0, "Zero unhealthy days should return streak of 0"
    tests.append(TestCase(10, "longest_unhealthy_streak returns 0 when no days qualify", tc10))

    return "City Air Quality AQI Analyzer (Module Functions)", tests


def suite_numpy_02_sensor_analyzer(cls):
    tests = []

    def tc1(c):
        obj = c()
        arr = obj.create_sensor_array([12.5, 30.0, 45.2])
        assert isinstance(arr, np.ndarray), "create_sensor_array must return a NumPy array"
        assert np.issubdtype(arr.dtype, np.floating), f"Expected float dtype, got {arr.dtype}"
    tests.append(TestCase(1, "create_sensor_array creates float NumPy array", tc1))

    def tc2(c):
        obj = c()
        arr = obj.create_sensor_array([10.0, 25.5, 80.0])
        assert obj.validate_sensor_array(arr) is True, "All positive values should validate True"
    tests.append(TestCase(2, "validate_sensor_array returns True when all values are > 0", tc2))

    def tc3(c):
        obj = c()
        arr_zero = obj.create_sensor_array([10.0, 0.0, 20.0])
        assert obj.validate_sensor_array(arr_zero) is False, "Zero value must return False"
        arr_neg = obj.create_sensor_array([10.0, -5.0, 20.0])
        assert obj.validate_sensor_array(arr_neg) is False, "Negative value must return False"
    tests.append(TestCase(3, "validate_sensor_array rejects non-positive readings (<= 0)", tc3))

    def tc4(c):
        obj = c()
        arr_empty = obj.create_sensor_array([])
        assert obj.validate_sensor_array(arr_empty) is False, "Empty array must return False"
    tests.append(TestCase(4, "validate_sensor_array rejects empty array", tc4))

    def tc5(c):
        obj = c()
        arr = obj.create_sensor_array([20.0, 40.0, 60.0])
        stats = obj.compute_sensor_statistics(arr)
        assert isinstance(stats, tuple) and len(stats) == 3, "Must return 3-tuple (total, average, maximum)"
        tot, avg, mx = stats
        assert math.isclose(tot, 120.0, abs_tol=0.01)
        assert math.isclose(avg, 40.0, abs_tol=0.1)
        assert math.isclose(mx, 60.0, abs_tol=0.01)
    tests.append(TestCase(5, "compute_sensor_statistics calculates total, 1-decimal average, max", tc5))

    def tc6(c):
        obj = c()
        arr = obj.create_sensor_array([60.0, 100.0])
        reduced = obj.filter_extreme_readings(arr)
        assert math.isclose(reduced[0], 54.0, abs_tol=0.01), f"Expected 54.0, got {reduced[0]}"
        assert math.isclose(reduced[1], 90.0, abs_tol=0.01), f"Expected 90.0, got {reduced[1]}"
    tests.append(TestCase(6, "filter_extreme_readings applies 10% reduction to readings >= 50.0", tc6))

    def tc7(c):
        obj = c()
        arr = obj.create_sensor_array([49.9, 50.0])
        reduced = obj.filter_extreme_readings(arr)
        assert math.isclose(reduced[0], 49.9, abs_tol=0.01), "< 50.0 should not be changed"
        assert math.isclose(reduced[1], 45.0, abs_tol=0.01), "== 50.0 boundary must be reduced"
    tests.append(TestCase(7, "filter_extreme_readings boundary test (50.0 reduced, 49.9 unchanged)", tc7))

    def tc8(c):
        obj = c()
        arr = obj.create_sensor_array([10.0, 50.0, 30.0])  # mean = 30.0
        labels = list(obj.label_high_sensors(arr))
        assert labels == ["Normal", "High", "Normal"], f"Expected ['Normal', 'High', 'Normal'], got {labels}"
    tests.append(TestCase(8, "label_high_sensors tags elements > mean as 'High' and others as 'Normal'", tc8))

    def tc9(c):
        obj = c()
        arr = obj.create_sensor_array([20.0, 20.0, 20.0])  # mean = 20.0
        labels = list(obj.label_high_sensors(arr))
        assert labels == ["Normal", "Normal", "Normal"], "Equality with mean must produce 'Normal'"
    tests.append(TestCase(9, "label_high_sensors boundary equality evaluates to 'Normal'", tc9))

    def tc10(c):
        obj = c()
        arr = obj.create_sensor_array([55.0, 66.5])
        formatted = list(obj.format_sensor_readings(arr))
        assert formatted == ["55.00 units", "66.50 units"], f"Expected ['55.00 units', '66.50 units'], got {formatted}"
    tests.append(TestCase(10, "format_sensor_readings formats as f'{x:.2f} units'", tc10))

    return "Sensor Reading Analysis System (Class: SensorAnalyzer)", tests


def suite_numpy_03_instagram_reels(m):
    tests = []

    def tc1(mod):
        arr = mod.create_views_array([1000, 2000, 3000])
        assert isinstance(arr, np.ndarray) and arr.dtype == np.int64, "Must return int64 NumPy array"
    tests.append(TestCase(1, "create_views_array creates int64 NumPy array", tc1))

    def tc2(mod):
        arr = mod.create_views_array([1200, 3500, 0])
        assert mod.validate_views_array(arr) is True, "Non-negative numeric array should validate True"
    tests.append(TestCase(2, "validate_views_array returns True for non-negative values", tc2))

    def tc3(mod):
        arr_neg = mod.create_views_array([100, -200, 300])
        assert mod.validate_views_array(arr_neg) is False, "Negative values must return False"
        arr_empty = mod.create_views_array([])
        assert mod.validate_views_array(arr_empty) is False, "Empty array must return False"
    tests.append(TestCase(3, "validate_views_array rejects negative values and empty arrays", tc3))

    def tc4(mod):
        arr = np.array(["a", "b"])
        assert mod.validate_views_array(arr) is False, "Non-numeric array must return False"
    tests.append(TestCase(4, "validate_views_array rejects non-numeric arrays safely", tc4))

    def tc5(mod):
        arr = mod.create_views_array([1200, 3500, 1800, 5200, 7600])
        metrics = mod.compute_view_metrics(arr)
        assert isinstance(metrics, tuple) and len(metrics) == 3, "Must return 3-tuple"
        total, avg, mx = metrics
        assert total == 19300 and math.isclose(avg, 3860.0, abs_tol=0.01) and mx == 7600
        assert isinstance(total, (int, np.integer)) and isinstance(mx, (int, np.integer))
    tests.append(TestCase(5, "compute_view_metrics returns (total_views, avg_views, max_views) with ints and rounded avg", tc5))

    def tc6(mod):
        arr = mod.create_views_array([2999, 100])
        cats = list(mod.categorize_trend_levels(arr))
        assert cats == ["Low Trend", "Low Trend"], "Views < 3000 must be 'Low Trend'"
    tests.append(TestCase(6, "categorize_trend_levels maps < 3000 to 'Low Trend'", tc6))

    def tc7(mod):
        arr = mod.create_views_array([3000, 4999])
        cats = list(mod.categorize_trend_levels(arr))
        assert cats == ["Moderate Trend", "Moderate Trend"], "3000 to 4999 must be 'Moderate Trend'"
    tests.append(TestCase(7, "categorize_trend_levels maps 3000..4999 to 'Moderate Trend'", tc7))

    def tc8(mod):
        arr = mod.create_views_array([5000, 10000])
        cats = list(mod.categorize_trend_levels(arr))
        assert cats == ["Viral Trend", "Viral Trend"], ">= 5000 must be 'Viral Trend'"
    tests.append(TestCase(8, "categorize_trend_levels maps >= 5000 to 'Viral Trend'", tc8))

    def tc9(mod):
        empty_arr = mod.create_views_array([])
        single_arr = mod.create_views_array([500])
        assert mod.longest_growth_streak(empty_arr) == 0, "Empty array streak must be 0"
        assert mod.longest_growth_streak(single_arr) == 1, "Single element streak must be 1"
    tests.append(TestCase(9, "longest_growth_streak handles empty (0) and single (1) day arrays", tc9))

    def tc10(mod):
        arr1 = mod.create_views_array([1200, 3500, 1800, 5200, 7600])
        streak1 = mod.longest_growth_streak(arr1)
        assert streak1 == 3, f"Expected streak of 3 (1800->5200->7600), got {streak1}"
        formatted = list(mod.format_view_counts(mod.create_views_array([1200, 35000, 1800000])))
        assert formatted == ["1,200", "35,000", "1,800,000"], f"Expected commas, got {formatted}"
    tests.append(TestCase(10, "longest_growth_streak detects multi-day streak and format_view_counts adds commas", tc10))

    return "Instagram Reel Trend Engagement Analysis (Module Functions)", tests


def suite_numpy_04_aquarium_temp(m):
    tests = []

    def tc1(mod):
        arr = mod.create_water_temperature_array([15.5, 20.0, 28.5])
        assert isinstance(arr, np.ndarray) and arr.dtype == np.float64, "Must return float64 NumPy array"
    tests.append(TestCase(1, "create_water_temperature_array creates 1D float64 array", tc1))

    def tc2(mod):
        arr = mod.create_water_temperature_array([12.0, 20.0, 30.0])
        assert mod.validate_water_temperature_array(arr) is True, "Values between 12.0 and 30.0 must validate True"
    tests.append(TestCase(2, "validate_water_temperature_array returns True for [12.0, 30.0]", tc2))

    def tc3(mod):
        arr_low = mod.create_water_temperature_array([11.9, 20.0])
        assert mod.validate_water_temperature_array(arr_low) is False, "< 12.0 must return False"
        arr_high = mod.create_water_temperature_array([20.0, 30.1])
        assert mod.validate_water_temperature_array(arr_high) is False, "> 30.0 must return False"
    tests.append(TestCase(3, "validate_water_temperature_array rejects out-of-range temperatures", tc3))

    def tc4(mod):
        arr_empty = mod.create_water_temperature_array([])
        assert mod.validate_water_temperature_array(arr_empty) is False, "Empty array must return False"
        arr_str = np.array(["warm", "cold"])
        assert mod.validate_water_temperature_array(arr_str) is False, "Non-numeric array must return False safely"
    tests.append(TestCase(4, "validate_water_temperature_array rejects empty and non-numeric arrays safely", tc4))

    def tc5(mod):
        arr = mod.create_water_temperature_array([16.0, 20.0, 24.0])
        stats = mod.compute_water_temperature_stats(arr)
        assert isinstance(stats, tuple) and len(stats) == 4, "Must return 4-tuple"
        mean_v, std_v, max_v, min_v = stats
        assert math.isclose(mean_v, 20.0, abs_tol=0.01)
        assert max_v == 24.0 and min_v == 16.0
    tests.append(TestCase(5, "compute_water_temperature_stats calculates mean, std, max, min", tc5))

    def tc6(mod):
        arr = mod.create_water_temperature_array([12.0, 15.0, 18.0])
        cats = list(mod.categorize_water_temperatures(arr))
        assert cats == ["Cold", "Cold", "Cold"], "12.0 <= val <= 18.0 must be 'Cold'"
    tests.append(TestCase(6, "categorize_water_temperatures maps 12.0 <= val <= 18.0 to 'Cold'", tc6))

    def tc7(mod):
        arr = mod.create_water_temperature_array([18.1, 22.0, 26.0])
        cats = list(mod.categorize_water_temperatures(arr))
        assert cats == ["Optimal", "Optimal", "Optimal"], "18.0 < val <= 26.0 must be 'Optimal'"
    tests.append(TestCase(7, "categorize_water_temperatures maps 18.0 < val <= 26.0 to 'Optimal'", tc7))

    def tc8(mod):
        arr = mod.create_water_temperature_array([26.1, 28.0, 30.0])
        cats = list(mod.categorize_water_temperatures(arr))
        assert cats == ["Warm", "Warm", "Warm"], "26.0 < val <= 30.0 must be 'Warm'"
    tests.append(TestCase(8, "categorize_water_temperatures maps 26.0 < val <= 30.0 to 'Warm'", tc8))

    def tc9(mod):
        arr = mod.create_water_temperature_array([10.0, 35.0])
        cats = list(mod.categorize_water_temperatures(arr))
        assert cats == ["Invalid", "Invalid"], "Out-of-range temperatures must be 'Invalid'"
    tests.append(TestCase(9, "categorize_water_temperatures maps out-of-range readings to 'Invalid'", tc9))

    def tc10(mod):
        arr = mod.create_water_temperature_array([20.0, 27.0, 28.5, 29.0, 15.0, 28.0])
        streak = mod.longest_warm_streak(arr)
        assert streak == 3, f"Expected streak of 3 (27.0, 28.5, 29.0), got {streak}"
        arr_none = mod.create_water_temperature_array([15.0, 20.0])
        assert mod.longest_warm_streak(arr_none) == 0, "No warm days should return 0"
    tests.append(TestCase(10, "longest_warm_streak counts consecutive warm readings (26 < val <= 30)", tc10))

    return "Aquarium Water Quality Analyzer (Module Functions)", tests


def suite_numpy_05_cold_storage(m):
    tests = []

    def tc1(mod):
        arr = mod.create_temperature_array([-22.0, -18.5, 4.0])
        assert isinstance(arr, np.ndarray) and arr.dtype == np.float64, "Must return float64 NumPy array"
        assert list(arr) == [-22.0, -18.5, 4.0], "Must preserve input order"
    tests.append(TestCase(1, "create_temperature_array creates float64 array preserving order", tc1))

    def tc2(mod):
        arr = mod.create_temperature_array([-30.0, 0.0, 10.0])
        assert mod.validate_temperature_array(arr) is True, "-30.0 to 10.0 inclusive must validate True"
    tests.append(TestCase(2, "validate_temperature_array returns True for [-30.0, 10.0]", tc2))

    def tc3(mod):
        arr_low = mod.create_temperature_array([-30.1, 0.0])
        assert mod.validate_temperature_array(arr_low) is False, "< -30.0 must return False"
        arr_high = mod.create_temperature_array([0.0, 10.1])
        assert mod.validate_temperature_array(arr_high) is False, "> 10.0 must return False"
    tests.append(TestCase(3, "validate_temperature_array rejects out-of-range temperatures", tc3))

    def tc4(mod):
        arr_empty = mod.create_temperature_array([])
        assert mod.validate_temperature_array(arr_empty) is False, "Empty array must return False"
        arr_str = np.array(["freeze", "cold"])
        assert mod.validate_temperature_array(arr_str) is False, "Non-numeric array must return False safely"
    tests.append(TestCase(4, "validate_temperature_array rejects empty and non-numeric arrays safely", tc4))

    def tc5(mod):
        arr = mod.create_temperature_array([-20.0, -10.0, 0.0])
        stats = mod.compute_temperature_stats(arr)
        assert isinstance(stats, tuple) and len(stats) == 4, "Must return 4-tuple"
        mean_v, std_v, max_v, min_v = stats
        assert math.isclose(mean_v, -10.0, abs_tol=0.01)
        assert math.isclose(std_v, 8.16, abs_tol=0.02)
        assert max_v == 0.0 and min_v == -20.0
    tests.append(TestCase(5, "compute_temperature_stats computes population statistics rounded to 2 decimals", tc5))

    def tc6(mod):
        arr = mod.create_temperature_array([-30.0, -25.0, -18.0])
        cats = list(mod.categorize_temperatures(arr))
        assert cats == ["Frozen", "Frozen", "Frozen"], "-30.0 <= val <= -18.0 must be 'Frozen'"
    tests.append(TestCase(6, "categorize_temperatures maps -30.0 <= val <= -18.0 to 'Frozen'", tc6))

    def tc7(mod):
        arr = mod.create_temperature_array([-17.9, 0.0, 5.0])
        cats = list(mod.categorize_temperatures(arr))
        assert cats == ["Chilled", "Chilled", "Chilled"], "-18.0 < val <= 5.0 must be 'Chilled'"
    tests.append(TestCase(7, "categorize_temperatures maps -18.0 < val <= 5.0 to 'Chilled'", tc7))

    def tc8(mod):
        arr = mod.create_temperature_array([5.1, 8.0, 10.0])
        cats = list(mod.categorize_temperatures(arr))
        assert cats == ["Warning", "Warning", "Warning"], "5.0 < val <= 10.0 must be 'Warning'"
    tests.append(TestCase(8, "categorize_temperatures maps 5.0 < val <= 10.0 to 'Warning'", tc8))

    def tc9(mod):
        arr = mod.create_temperature_array([-35.0, 12.0])
        cats = list(mod.categorize_temperatures(arr))
        assert cats == ["Invalid", "Invalid"], "Temperatures below -30 or above 10 must be 'Invalid'"
    tests.append(TestCase(9, "categorize_temperatures maps out-of-range temperatures to 'Invalid'", tc9))

    def tc10(mod):
        arr = mod.create_temperature_array([2.0, 6.0, 7.5, 9.0, 0.0, 8.0])
        streak = mod.longest_warning_streak(arr)
        assert streak == 3, f"Expected streak of 3 (6.0, 7.5, 9.0), got {streak}"
        arr_none = mod.create_temperature_array([-10.0, 2.0])
        assert mod.longest_warning_streak(arr_none) == 0, "No warning readings must return 0"
    tests.append(TestCase(10, "longest_warning_streak counts consecutive warning readings (5 < val <= 10)", tc10))

    return "Cold-Storage Temperature Analyzer (Module Functions)", tests


# ==============================================================================
# 4. EXTRA QUESTIONS TEST SUITES (10 Test Cases Each)
# ==============================================================================

def suite_oops_extra_01_library_inventory(cls):
    tests = []

    def tc1(c):
        obj = c()
        assert hasattr(obj, "books") or hasattr(obj, "inv") or hasattr(obj, "inventory"), "Missing dictionary attribute for books"
        book_dict = getattr(obj, "books", getattr(obj, "inv", getattr(obj, "inventory", None)))
        assert isinstance(book_dict, dict), "Books container must be a dictionary"
        assert len(book_dict) == 0, "Books container should initially be empty"
    tests.append(TestCase(1, "Initial state verification (empty books dictionary)", tc1))

    def tc2(c):
        obj = c()
        res = obj.add_book("Book A", 5)
        stock = obj.get_book_stock("Book A")
        assert stock == 5, f"Expected 5, got {stock}"
        assert isinstance(res, dict) and res.get("Book A") == 5, "add_book must return updated dictionary"
    tests.append(TestCase(2, "add_book creates a new book entry", tc2))

    def tc3(c):
        obj = c()
        obj.add_book("Book A", 5)
        res = obj.add_book("Book A", 3)
        assert obj.get_book_stock("Book A") == 8, f"Expected 8, got {obj.get_book_stock('Book A')}"
        assert res.get("Book A") == 8, "add_book must return updated dictionary with accumulated count"
    tests.append(TestCase(3, "add_book accumulates stock on existing book", tc3))

    def tc4(c):
        obj = c()
        obj.add_book("Clean Code", 4)
        obj.add_book("Design Patterns", 6)
        obj.add_book("Refactoring", 2)
        assert obj.get_book_stock("Clean Code") == 4
        assert obj.get_book_stock("Design Patterns") == 6
        assert obj.get_book_stock("Refactoring") == 2
    tests.append(TestCase(4, "add_book manages multiple distinct books independently", tc4))

    def tc5(c):
        obj = c()
        obj.add_book("Python Basics", 10)
        res = obj.update_book_quantity("Python Basics", 25)
        assert obj.get_book_stock("Python Basics") == 25, f"Expected 25, got {obj.get_book_stock('Python Basics')}"
        assert isinstance(res, dict) and res.get("Python Basics") == 25, "update_book_quantity must return updated dictionary"
    tests.append(TestCase(5, "update_book_quantity modifies existing quantity", tc5))

    def tc6(c):
        obj = c()
        obj.add_book("Out of Print Book", 10)
        obj.update_book_quantity("Out of Print Book", 0)
        assert obj.get_book_stock("Out of Print Book") == 0, "Quantity can be updated to 0"
    tests.append(TestCase(6, "update_book_quantity handles setting quantity to 0", tc6))

    def tc7(c):
        obj = c()
        raised = False
        try:
            obj.update_book_quantity("Nonexistent Book", 5)
        except KeyError as e:
            raised = True
            assert "not found" in str(e).lower(), f"Expected 'Not found', got '{e}'"
        assert raised, "Expected KeyError('Not found') when updating missing book"
    tests.append(TestCase(7, "update_book_quantity raises KeyError('Not found') for non-existent book", tc7))

    def tc8(c):
        obj = c()
        obj.add_book("Algorithms", 12)
        stock = obj.get_book_stock("Algorithms")
        assert stock == 12, f"Expected 12, got {stock}"
    tests.append(TestCase(8, "get_book_stock retrieves exact available quantity", tc8))

    def tc9(c):
        obj = c()
        raised = False
        try:
            obj.get_book_stock("Missing Book")
        except KeyError as e:
            raised = True
            assert "not found" in str(e).lower(), f"Expected 'Not found', got '{e}'"
        assert raised, "Expected KeyError('Not found') when fetching missing book"
    tests.append(TestCase(9, "get_book_stock raises KeyError('Not found') for non-existent book", tc9))

    def tc10(c):
        obj = c()
        obj.add_book("Available 1", 5)
        obj.add_book("Zero Stock", 0)
        obj.add_book("Available 2", 8)
        available = obj.get_available_books()
        assert isinstance(available, list), "get_available_books must return a list"
        assert sorted(available) == ["Available 1", "Available 2"], f"Expected ['Available 1', 'Available 2'], got {available}"
        empty_obj = c()
        assert empty_obj.get_available_books() == [], "Empty inventory must return empty list"
    tests.append(TestCase(10, "get_available_books returns list of books with stock > 0", tc10))

    return "Library Inventory Management System (Class: LibraryInventorySystem)", tests


def suite_pandas_extra_01_delivery_time(cls):
    tests = []

    def tc1(c):
        obj = c()
        data = [[1, "R101", "Zone A", 30], [2, "R102", "Zone B", 45]]
        df = obj.create_delivery_log_df(data)
        assert isinstance(df, pd.DataFrame), "Must return a DataFrame"
        assert list(df.columns) == ["OrderID", "RestaurantCode", "Area", "DeliveryTime"], f"Columns mismatch: {df.columns}"
        assert len(df) == 2, f"Expected 2 rows, got {len(df)}"
    tests.append(TestCase(1, "create_delivery_log_df builds DataFrame with correct columns", tc1))

    def tc2(c):
        obj = c()
        master = [["R101", "Burger Hub"], ["R102", "Taco Town"]]
        df = obj.create_restaurant_master_df(master)
        assert isinstance(df, pd.DataFrame), "Must return a DataFrame"
        assert list(df.columns) == ["RestaurantCode", "RestaurantName"], f"Columns mismatch: {df.columns}"
        assert len(df) == 2, f"Expected 2 rows, got {len(df)}"
    tests.append(TestCase(2, "create_restaurant_master_df builds DataFrame with correct columns", tc2))

    def tc3(c):
        obj = c()
        log = [[1, "R1", "North", 25], [2, "R2", "South", 35]]
        master = [["R1", "Pasta Palace"], ["R2", "Curry Corner"]]
        df_log = obj.create_delivery_log_df(log)
        df_master = obj.create_restaurant_master_df(master)
        merged = obj.merge_restaurant_names(df_log, df_master)
        assert "RestaurantName" in merged.columns, "Merged df must contain 'RestaurantName'"
        assert len(merged) == 2, "All delivery log rows must be preserved"
        names = merged.set_index("RestaurantCode")["RestaurantName"].to_dict()
        assert names["R1"] == "Pasta Palace" and names["R2"] == "Curry Corner"
    tests.append(TestCase(3, "merge_restaurant_names joins delivery log with restaurant master", tc3))

    def tc4(c):
        obj = c()
        log = [[1, "R1", "North", 25], [2, "R99", "Unknown", 40]]
        master = [["R1", "Pasta Palace"]]
        df_log = obj.create_delivery_log_df(log)
        df_master = obj.create_restaurant_master_df(master)
        merged = obj.merge_restaurant_names(df_log, df_master)
        assert len(merged) == 2, "Left join must preserve unmapped orders"
        unmapped_name = merged.loc[merged["RestaurantCode"] == "R99", "RestaurantName"].iloc[0]
        assert pd.isna(unmapped_name), "Unmapped restaurant code must have NaN for RestaurantName"
    tests.append(TestCase(4, "merge_restaurant_names preserves unmapped orders via left join", tc4))

    def tc5(c):
        obj = c()
        log = [
            [1, "R1", "A", 20],
            [2, "R1", "B", 40],
            [3, "R2", "A", 30],
            [4, "R2", "B", 50],
        ]
        master = [["R1", "ResA"], ["R2", "ResB"]]
        df_log = obj.create_delivery_log_df(log)
        df_master = obj.create_restaurant_master_df(master)
        merged = obj.merge_restaurant_names(df_log, df_master)
        avg_df = obj.average_delivery_by_restaurant(merged)
        avg_dict = avg_df.set_index("RestaurantName")["Average Delivery"].to_dict()
        assert math.isclose(avg_dict["ResA"], 30.0, rel_tol=1e-3), f"Expected 30.0 for ResA, got {avg_dict.get('ResA')}"
        assert math.isclose(avg_dict["ResB"], 40.0, rel_tol=1e-3), f"Expected 40.0 for ResB, got {avg_dict.get('ResB')}"
    tests.append(TestCase(5, "average_delivery_by_restaurant computes exact mean delivery times", tc5))

    def tc6(c):
        obj = c()
        log = [[1, "R1", "A", 25]]
        master = [["R1", "ResA"]]
        df_log = obj.create_delivery_log_df(log)
        df_master = obj.create_restaurant_master_df(master)
        merged = obj.merge_restaurant_names(df_log, df_master)
        avg_df = obj.average_delivery_by_restaurant(merged)
        assert "Average Delivery" in avg_df.columns, "Column must be renamed to 'Average Delivery'"
        assert "RestaurantName" in avg_df.columns, "Index must be reset so 'RestaurantName' is a column"
    tests.append(TestCase(6, "average_delivery_by_restaurant resets index and renames column", tc6))

    def tc7(c):
        obj = c()
        log = [
            [1, "R1", "A", 15],
            [2, "R1", "B", 35],
            [3, "R2", "C", 45],
            [4, "R2", "D", 20],
        ]
        df_log = obj.create_delivery_log_df(log)
        slow = obj.filter_slow_deliveries(df_log, 30)
        assert len(slow) == 2, f"Expected 2 slow deliveries, got {len(slow)}"
        assert set(slow["OrderID"].tolist()) == {2, 3}, "Must contain orders with DeliveryTime > 30"
    tests.append(TestCase(7, "filter_slow_deliveries filters rows strictly exceeding threshold", tc7))

    def tc8(c):
        obj = c()
        log = [[1, "R1", "A", 20], [2, "R2", "B", 25]]
        df_log = obj.create_delivery_log_df(log)
        slow = obj.filter_slow_deliveries(df_log, 50)
        assert isinstance(slow, pd.DataFrame) and len(slow) == 0, "Threshold above all values must return empty DataFrame"
    tests.append(TestCase(8, "filter_slow_deliveries returns empty DataFrame when none exceed threshold", tc8))

    def tc9(c):
        obj = c()
        log = [
            [1, "R1", "Downtown", 60],
            [2, "R2", "Downtown", 40],
            [3, "R1", "Suburbs", 25],
            [4, "R2", "Suburbs", 35],
            [5, "R3", "Uptown", 20],
        ]
        df_log = obj.create_delivery_log_df(log)
        slowest = obj.slowest_delivery_area(df_log)
        assert slowest["Area"].iloc[0] == "Downtown", f"Expected 'Downtown', got {slowest['Area'].iloc[0]}"
        assert math.isclose(slowest["DeliveryTime"].iloc[0], 50.0, rel_tol=1e-3)
    tests.append(TestCase(9, "slowest_delivery_area identifies area with highest average delivery time", tc9))

    def tc10(c):
        obj = c()
        log = [
            [1, "R1", "North", 30],
            [2, "R2", "South", 50],
        ]
        df_log = obj.create_delivery_log_df(log)
        slowest = obj.slowest_delivery_area(df_log)
        assert isinstance(slowest, pd.DataFrame), "Must return a DataFrame"
        assert len(slowest) == 1, f"Expected 1 row, got {len(slowest)}"
        assert slowest.index[0] == 0, "Index must be reset with drop=True starting at 0"
    tests.append(TestCase(10, "slowest_delivery_area returns single-row DataFrame with reset index", tc10))

    return "Food Delivery Order Analyzer (Class: DeliveryTimeAnalyzer)", tests


def suite_numpy_extra_01_movie_rating(cls):
    tests = []

    def tc1(c):
        obj = c()
        arr = obj.create_rating_array([85, 90, 75])
        assert isinstance(arr, np.ndarray), "Must return a NumPy ndarray"
        assert np.issubdtype(arr.dtype, np.integer), f"Array must have integer dtype, got {arr.dtype}"
        assert list(arr) == [85, 90, 75]
    tests.append(TestCase(1, "create_rating_array creates integer NumPy array from list", tc1))

    def tc2(c):
        obj = c()
        arr = np.array([0, 50, 85, 100])
        assert obj.validate_ratings(arr) is True, "Array with elements in [0, 100] must be valid"
    tests.append(TestCase(2, "validate_ratings returns True for ratings within [0, 100]", tc2))

    def tc3(c):
        obj = c()
        arr_empty = np.array([])
        assert obj.validate_ratings(arr_empty) is False, "Empty array must be invalid (False)"
    tests.append(TestCase(3, "validate_ratings returns False for empty array", tc3))

    def tc4(c):
        obj = c()
        arr_low = np.array([-1, 50, 80])
        arr_high = np.array([50, 80, 101])
        assert obj.validate_ratings(arr_low) is False, "Rating < 0 must be invalid (False)"
        assert obj.validate_ratings(arr_high) is False, "Rating > 100 must be invalid (False)"
    tests.append(TestCase(4, "validate_ratings returns False for out-of-bound ratings (<0 or >100)", tc4))

    def tc5(c):
        obj = c()
        arr = np.array([80, 90, 75])
        total, avg, max_val = obj.compute_rating_summary(arr)
        assert total == 245, f"Expected total 245, got {total}"
        assert math.isclose(avg, 81.7, abs_tol=0.05), f"Expected avg 81.7, got {avg}"
        assert max_val == 90, f"Expected max 90, got {max_val}"
    tests.append(TestCase(5, "compute_rating_summary computes total, rounded average, and maximum", tc5))

    def tc6(c):
        obj = c()
        arr = np.array([92])
        total, avg, max_val = obj.compute_rating_summary(arr)
        assert total == 92 and math.isclose(avg, 92.0, abs_tol=0.01) and max_val == 92
    tests.append(TestCase(6, "compute_rating_summary works correctly for single-element array", tc6))

    def tc7(c):
        obj = c()
        arr = np.array([80, 85, 90])
        bonus = obj.apply_bonus(arr)
        assert math.isclose(bonus[0], 80.0, abs_tol=0.1)
        assert math.isclose(bonus[1], 85.0, abs_tol=0.1)
        assert math.isclose(bonus[2], 94.5, abs_tol=0.1), f"Expected 94.5, got {bonus[2]}"
    tests.append(TestCase(7, "apply_bonus increases ratings > 85 by 5% and leaves <= 85 unchanged", tc7))

    def tc8(c):
        obj = c()
        arr = np.array([98, 100])
        bonus = obj.apply_bonus(arr)
        assert math.isclose(bonus[0], 100.0, abs_tol=0.01), f"Expected 100.0, got {bonus[0]}"
        assert math.isclose(bonus[1], 100.0, abs_tol=0.01), f"Expected 100.0, got {bonus[1]}"
    tests.append(TestCase(8, "apply_bonus clips ratings to maximum of 100.0", tc8))

    def tc9(c):
        obj = c()
        arr = np.array([95, 90, 85, 80, 79, 60])
        cats = list(obj.categorize_movies(arr))
        expected = ["Excellent", "Excellent", "Good", "Good", "Needs Improvement", "Needs Improvement"]
        assert cats == expected, f"Expected {expected}, got {cats}"
    tests.append(TestCase(9, "categorize_movies maps thresholds to 'Excellent', 'Good', 'Needs Improvement'", tc9))

    def tc10(c):
        obj = c()
        arr = np.array([95, 84, 73, 55])
        grades = list(obj.format_ratings_with_grades(arr))
        expected = ["A", "B", "C", "D"]
        assert grades == expected, f"Expected {expected}, got {grades}"
    tests.append(TestCase(10, "format_ratings_with_grades maps ratings to 'A', 'B', 'C', 'D' via loop", tc10))

    return "Movie Rating Analyzer (Class: MovieRatingAnalyzer)", tests


# ==============================================================================
# DISPATCHER & DETECTOR
# ==============================================================================

def detect_and_build_suites(target):
    """
    Inspects a module or dictionary of globals to detect which questions are implemented.
    Returns a list of (suite_name, test_cases_list, target_object).
    """
    suites = []

    # Check for OOPS Classes
    if hasattr(target, "SupplyChainInventory") and inspect.isclass(target.SupplyChainInventory):
        name, tests = suite_oops_01_supply_chain(target.SupplyChainInventory)
        suites.append((name, tests, target.SupplyChainInventory))

    if hasattr(target, "EventRegistrationTracker") and inspect.isclass(target.EventRegistrationTracker):
        name, tests = suite_oops_02_event_registration(target.EventRegistrationTracker)
        suites.append((name, tests, target.EventRegistrationTracker))

    if hasattr(target, "TrafficControlSystem") and inspect.isclass(target.TrafficControlSystem):
        name, tests = suite_oops_03_traffic_control(target.TrafficControlSystem)
        suites.append((name, tests, target.TrafficControlSystem))

    if hasattr(target, "ChessTournamentSystem") and inspect.isclass(target.ChessTournamentSystem):
        name, tests = suite_oops_04_chess_tournament(target.ChessTournamentSystem)
        suites.append((name, tests, target.ChessTournamentSystem))

    if hasattr(target, "LibraryLoanRegistry") and inspect.isclass(target.LibraryLoanRegistry):
        name, tests = suite_oops_05_library_loan(target.LibraryLoanRegistry)
        suites.append((name, tests, target.LibraryLoanRegistry))

    if hasattr(target, "MuseumLoanRegistry") and inspect.isclass(target.MuseumLoanRegistry):
        name, tests = suite_oops_06_museum_loan(target.MuseumLoanRegistry)
        suites.append((name, tests, target.MuseumLoanRegistry))

    # Check for Pandas Classes
    if hasattr(target, "ClaimAnalyzer") and inspect.isclass(target.ClaimAnalyzer):
        name, tests = suite_pandas_01_claim_analyzer(target.ClaimAnalyzer)
        suites.append((name, tests, target.ClaimAnalyzer))

    if hasattr(target, "SolarFarmAnalyzer") and inspect.isclass(target.SolarFarmAnalyzer):
        name, tests = suite_pandas_02_solar_farm(target.SolarFarmAnalyzer)
        suites.append((name, tests, target.SolarFarmAnalyzer))

    if hasattr(target, "ReturnsAnalyzer") and inspect.isclass(target.ReturnsAnalyzer):
        name, tests = suite_pandas_03_marketplace_returns(target.ReturnsAnalyzer)
        suites.append((name, tests, target.ReturnsAnalyzer))

    if hasattr(target, "EVChargingAnalyzer") and inspect.isclass(target.EVChargingAnalyzer):
        name, tests = suite_pandas_04_ev_charging(target.EVChargingAnalyzer)
        suites.append((name, tests, target.EVChargingAnalyzer))

    if hasattr(target, "HospitalEquipmentAnalyzer") and inspect.isclass(target.HospitalEquipmentAnalyzer):
        name, tests = suite_pandas_05_hospital_equipment(target.HospitalEquipmentAnalyzer)
        suites.append((name, tests, target.HospitalEquipmentAnalyzer))

    if hasattr(target, "SolarMaintenanceAnalyzer") and inspect.isclass(target.SolarMaintenanceAnalyzer):
        name, tests = suite_pandas_06_solar_maintenance(target.SolarMaintenanceAnalyzer)
        suites.append((name, tests, target.SolarMaintenanceAnalyzer))

    # Check for NumPy Classes or Module Functions
    if hasattr(target, "SensorAnalyzer") and inspect.isclass(target.SensorAnalyzer):
        name, tests = suite_numpy_02_sensor_analyzer(target.SensorAnalyzer)
        suites.append((name, tests, target.SensorAnalyzer))

    # Distinct module-level functions
    if hasattr(target, "create_aqi_array") or hasattr(target, "longest_unhealthy_streak"):
        name, tests = suite_numpy_01_city_aqi(target)
        suites.append((name, tests, target))

    if hasattr(target, "create_views_array") or hasattr(target, "longest_growth_streak"):
        name, tests = suite_numpy_03_instagram_reels(target)
        suites.append((name, tests, target))

    if hasattr(target, "create_water_temperature_array") or hasattr(target, "longest_warm_streak"):
        name, tests = suite_numpy_04_aquarium_temp(target)
        suites.append((name, tests, target))

    if hasattr(target, "create_temperature_array") or hasattr(target, "longest_warning_streak"):
        name, tests = suite_numpy_05_cold_storage(target)
        suites.append((name, tests, target))

    # Check for Extra Questions Classes
    if hasattr(target, "LibraryInventorySystem") and inspect.isclass(target.LibraryInventorySystem):
        name, tests = suite_oops_extra_01_library_inventory(target.LibraryInventorySystem)
        suites.append((name, tests, target.LibraryInventorySystem))

    if hasattr(target, "DeliveryTimeAnalyzer") and inspect.isclass(target.DeliveryTimeAnalyzer):
        name, tests = suite_pandas_extra_01_delivery_time(target.DeliveryTimeAnalyzer)
        suites.append((name, tests, target.DeliveryTimeAnalyzer))

    if hasattr(target, "MovieRatingAnalyzer") and inspect.isclass(target.MovieRatingAnalyzer):
        name, tests = suite_numpy_extra_01_movie_rating(target.MovieRatingAnalyzer)
        suites.append((name, tests, target.MovieRatingAnalyzer))

    return suites


def run_tests_for_file(file_path: str):
    """
    Executes tests against the python file at file_path.
    """
    print("=" * 80)
    print(f"RUNNING TEST EVALUATION FOR: {os.path.basename(file_path)}")
    print(f"Target Path: {os.path.abspath(file_path)}")
    print("=" * 80)

    if not os.path.exists(file_path):
        print(f"[ERROR] File not found: {file_path}")
        return False

    with open(file_path, "r", encoding="utf-8") as f:
        code_content = f.read().strip()

    if not code_content:
        print("\n[INFO] 'Python Milestone Practice.py' is currently empty!")
        print("Please write or paste your solution for any question into the file and run again.")
        print("Supported Questions: All 6 OOPS, 6 Pandas, and 5 NumPy milestone problems.")
        return False

    # Execute target in isolated namespace
    namespace = {
        "__name__": "__practice_eval__",
        "__file__": os.path.abspath(file_path),
    }

    try:
        exec(compile(code_content, file_path, "exec"), namespace)
    except Exception as e:
        print(f"\n[SYNTAX / EXECUTION ERROR] Failed to load {file_path}:")
        traceback.print_exc()
        return False

    class TargetProxy:
        pass

    target_obj = TargetProxy()
    for k, v in namespace.items():
        setattr(target_obj, k, v)

    suites = detect_and_build_suites(target_obj)

    if not suites:
        print("\n[INFO] No recognized Milestone classes or functions found in file.")
        print("Supported implementations:")
        print("  - OOPS: SupplyChainInventory, EventRegistrationTracker, TrafficControlSystem,")
        print("          ChessTournamentSystem, LibraryLoanRegistry, MuseumLoanRegistry")
        print("  - Pandas: ClaimAnalyzer, SolarFarmAnalyzer, ReturnsAnalyzer,")
        print("            EVChargingAnalyzer, HospitalEquipmentAnalyzer, SolarMaintenanceAnalyzer")
        print("  - NumPy: City AQI functions, SensorAnalyzer, Instagram Reels functions,")
        print("           Aquarium Water Quality functions, Cold-Storage functions")
        return False

    total_passed = 0
    total_cases = 0

    for suite_name, test_cases, test_target in suites:
        print(f"\nEvaluating: {suite_name}")
        print("-" * 80)
        passed_count = 0
        total_suite_cases = len(test_cases)

        for tc in test_cases:
            passed, err = tc.run(test_target)
            if passed:
                passed_count += 1
                print(f"  [PASS] TC {tc.tc_id:02d}: {tc.name}")
            else:
                print(f"  [FAIL] TC {tc.tc_id:02d}: {tc.name}")
                print(f"         Reason: {err}")

        pct = (passed_count / total_suite_cases) * 100.0
        print("-" * 80)
        print(f"Result for {suite_name}:")
        print(f"  Passed: {passed_count} / {total_suite_cases} Test Cases ({pct:.1f}%)")
        print("=" * 80)

        total_passed += passed_count
        total_cases += total_suite_cases

    return total_passed == total_cases


if __name__ == "__main__":
    # If a specific file is supplied as command-line argument, test that
    if len(sys.argv) > 1:
        target_path = sys.argv[1]
    else:
        # Check standard locations for Python Milestone Practice.py
        candidate1 = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "Python Questions Solutions", "Python Milestone Practice.py")
        )
        candidate2 = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "Python Milestone Practice.py")
        )
        if os.path.exists(candidate1) and os.path.getsize(candidate1) > 0:
            target_path = candidate1
        elif os.path.exists(candidate2) and os.path.getsize(candidate2) > 0:
            target_path = candidate2
        elif os.path.exists(candidate1):
            target_path = candidate1
        else:
            target_path = candidate2

    run_tests_for_file(target_path)
