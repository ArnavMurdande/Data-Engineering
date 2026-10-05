"""
PySpark Practice Questions - Unified Tester Engine
===================================================
A single tester file that merges testing functionality across all 10 assessment questions:
  1. Q401: Retail Commerce Operations
  2. Q402: Telecom Usage Intelligence
  3. Aircraft Maintenance Compliance Analytics
  4. Film Production Crew Payment Analytics
  5. Museum Artifact Catalog Insights
  6. Precision Agriculture Field Inspection
  7. Insurance Claims & Policy Insights
  8. Telecom Recharge Insights
  9. Q777: Clinic Appointment Wait-Time Analytics
 10. Q1000: SmartCity Mobility Mega Assessment

All test suites are centralized in the `Tests/` directory, datasets in `data/`,
and low-level designs in `LLD/`.
"""

import os
import sys
import time
import subprocess
from typing import Dict, List, Optional, Tuple

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TESTS_DIR = os.path.join(ROOT_DIR, "Tests")
QUESTIONS_DIR = os.path.join(ROOT_DIR, "Questions")
NEW_QUESTIONS_DIR = os.path.join(ROOT_DIR, "New Questions")
PYTHON_EXE = sys.executable
# Auto-detect virtual environment python if current python interpreter lacks pyspark
try:
    import pyspark
except ImportError:
    candidate_venv_py = os.path.join(os.path.dirname(ROOT_DIR), "PySpark Setup", ".venv", "Scripts", "python.exe")
    if os.path.exists(candidate_venv_py):
        PYTHON_EXE = candidate_venv_py

# Question registry: key -> (id, title, test_file, question_dir, total_tests, aliases)
QUESTION_REGISTRY = {
    "Q401": {
        "id": "Q401",
        "title": "Retail Commerce Operations",
        "test_file": os.path.join(TESTS_DIR, "test_Q401.py"),
        "dir": os.path.join(QUESTIONS_DIR, "Retail_Commerce_Operations"),
        "expected_tests": 20,
        "aliases": ["401", "q401", "retail", "commerce", "retail_commerce_operations"],
    },
    "Q402": {
        "id": "Q402",
        "title": "Telecom Usage Intelligence",
        "test_file": os.path.join(TESTS_DIR, "test_Q402.py"),
        "dir": os.path.join(QUESTIONS_DIR, "Telecom_Usage_Intelligence"),
        "expected_tests": 20,
        "aliases": ["402", "q402", "telecom", "usage", "telecom_usage_intelligence"],
    },
    "AIRCRAFT": {
        "id": "AIRCRAFT",
        "title": "Aircraft Maintenance Compliance Analytics",
        "test_file": os.path.join(TESTS_DIR, "test_Aircraft_Maintenance.py"),
        "dir": os.path.join(QUESTIONS_DIR, "Aircraft_Maintenance_Compliance_Analytics"),
        "expected_tests": 6,
        "aliases": ["aircraft", "maintenance", "aircraft_maintenance", "med1", "aircraft_maintenance_compliance_analytics"],
    },
    "FILM": {
        "id": "FILM",
        "title": "Film Production Crew Payment Analytics",
        "test_file": os.path.join(TESTS_DIR, "test_Film_Crew_Payment.py"),
        "dir": os.path.join(QUESTIONS_DIR, "Film_Production_Crew_Payment_Analytics"),
        "expected_tests": 6,
        "aliases": ["film", "crew", "film_crew", "payments", "med2", "film_production_crew_payment_analytics"],
    },
    "MUSEUM": {
        "id": "MUSEUM",
        "title": "Museum Artifact Catalog Insights",
        "test_file": os.path.join(TESTS_DIR, "test_Museum_Artifact.py"),
        "dir": os.path.join(QUESTIONS_DIR, "Museum_Artifact_Catalog_Insights"),
        "expected_tests": 6,
        "aliases": ["museum", "artifact", "artifacts", "easy2", "museum_artifact_catalog_insights"],
    },
    "AGRICULTURE": {
        "id": "AGRICULTURE",
        "title": "Precision Agriculture Field Inspection",
        "test_file": os.path.join(TESTS_DIR, "test_Precision_Agriculture.py"),
        "dir": os.path.join(QUESTIONS_DIR, "Precision_Agriculture_Field_Inspection"),
        "expected_tests": 6,
        "aliases": ["agriculture", "precision", "field_inspections", "agri", "easy1", "precision_agriculture_field_inspection"],
    },
    "INSURANCE": {
        "id": "INSURANCE",
        "title": "Insurance Claims & Policy Insights",
        "test_file": os.path.join(TESTS_DIR, "test_Insurance_Claims.py"),
        "dir": os.path.join(QUESTIONS_DIR, "Insurance_Claims_Policy_Insights"),
        "expected_tests": 6,
        "aliases": ["insurance", "claims", "insurance_claims", "policies", "insurance_claims_policy_insights"],
    },
    "TELECOM_RECHARGE": {
        "id": "TELECOM_RECHARGE",
        "title": "Telecom Recharge Insights",
        "test_file": os.path.join(TESTS_DIR, "test_Telecom_Recharge.py"),
        "dir": os.path.join(QUESTIONS_DIR, "Telecom_Recharge_Insights"),
        "expected_tests": 6,
        "aliases": ["recharge", "telecom_recharge", "recharges", "telecom_recharge_insights"],
    },
    "Q777": {
        "id": "Q777",
        "title": "Clinic Appointment Wait-Time Analytics",
        "test_file": os.path.join(TESTS_DIR, "test_Q777.py"),
        "dir": os.path.join(QUESTIONS_DIR, "Clinic_Appointment_Wait_Time_Analytics"),
        "expected_tests": 9,
        "aliases": ["777", "q777", "clinic", "wait", "appointment", "clinic_appointment_wait_time_analytics"],
    },
    "Q1000": {
        "id": "Q1000",
        "title": "SmartCity Mobility Mega Assessment",
        "test_file": os.path.join(TESTS_DIR, "test_Q1000.py"),
        "dir": os.path.join(QUESTIONS_DIR, "SmartCity_Mobility_Mega_Assessment"),
        "expected_tests": 40,
        "aliases": ["1000", "q1000", "smartcity", "mobility", "mega", "smartcity_mobility_mega_assessment"],
    },
    "Q16": {
        "id": "Q16",
        "title": "Digital Banking KYC Risk Insights",
        "test_file": os.path.join(TESTS_DIR, "test_Q16.py"),
        "dir": os.path.join(NEW_QUESTIONS_DIR, "Q16"),
        "expected_tests": 6,
        "aliases": ["16", "q16", "kyc", "kyc_customers", "digital_banking"],
    },
    "Q17": {
        "id": "Q17",
        "title": "Emergency Triage Wait-Time Insights",
        "test_file": os.path.join(TESTS_DIR, "test_Q17.py"),
        "dir": os.path.join(NEW_QUESTIONS_DIR, "Q17"),
        "expected_tests": 6,
        "aliases": ["17", "q17", "triage", "emergency", "wait_time"],
    },
    "Q18": {
        "id": "Q18",
        "title": "Vaccine Batch Stability Insights",
        "test_file": os.path.join(TESTS_DIR, "test_Q18.py"),
        "dir": os.path.join(NEW_QUESTIONS_DIR, "Q18"),
        "expected_tests": 6,
        "aliases": ["18", "q18", "vaccine", "vaccine_batches", "stability"],
    },
    "Q19": {
        "id": "Q19",
        "title": "Music Streaming Release Insights",
        "test_file": os.path.join(TESTS_DIR, "test_Q19.py"),
        "dir": os.path.join(NEW_QUESTIONS_DIR, "Q19"),
        "expected_tests": 6,
        "aliases": ["19", "q19", "music", "music_tracks", "streaming"],
    },
    "Q24": {
        "id": "Q24",
        "title": "Merchant Settlement Risk Analytics",
        "test_file": os.path.join(TESTS_DIR, "test_Q24.py"),
        "dir": os.path.join(NEW_QUESTIONS_DIR, "Q24"),
        "expected_tests": 6,
        "aliases": ["24", "q24", "settlement", "settlements", "merchants"],
    },
    "Q25": {
        "id": "Q25",
        "title": "Remote Patient Monitoring Alert Analytics",
        "test_file": os.path.join(TESTS_DIR, "test_Q25.py"),
        "dir": os.path.join(NEW_QUESTIONS_DIR, "Q25"),
        "expected_tests": 6,
        "aliases": ["25", "q25", "monitoring", "patients", "observations", "alert"],
    },
    "Q26": {
        "id": "Q26",
        "title": "Bioreactor Run Performance Analytics",
        "test_file": os.path.join(TESTS_DIR, "test_Q26.py"),
        "dir": os.path.join(NEW_QUESTIONS_DIR, "Q26"),
        "expected_tests": 6,
        "aliases": ["26", "q26", "bioreactor", "reactors", "bioreactor_runs"],
    },
    "Q27": {
        "id": "Q27",
        "title": "Streaming Ad Campaign Performance Analytics",
        "test_file": os.path.join(TESTS_DIR, "test_Q27.py"),
        "dir": os.path.join(NEW_QUESTIONS_DIR, "Q27"),
        "expected_tests": 6,
        "aliases": ["27", "q27", "ad", "impressions", "campaigns", "ad_impressions"],
    },
}

# Terminal formatting
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def detect_question_from_source(
    source_path: Optional[str] = None,
    source_code: Optional[str] = None
) -> Tuple[Optional[str], List[str], Dict[str, int]]:
    """
    Parses user source code via AST and identifies the best matching assessment question
    based on functions defined in solutions/.
    """
    import ast

    if source_code is None:
        if source_path is None or not os.path.exists(source_path):
            default_path = os.path.join(os.path.dirname(ROOT_DIR), "PySpark Practice", "solution.py")
            if os.path.exists(default_path):
                source_path = default_path
            else:
                return None, [], {}
        try:
            with open(source_path, "r", encoding="utf-8", errors="replace") as f:
                source_code = f.read()
        except Exception:
            return None, [], {}

    try:
        tree = ast.parse(source_code)
    except Exception:
        return None, [], {}

    # Find functions defined at top level, excluding internal/boilerplate
    user_funcs = {
        node.name for node in tree.body
        if isinstance(node, ast.FunctionDef)
        and not node.name.startswith("_")
        and node.name not in ["main", "run_tests", "execute_question_tests", "print_banner", "print_scorecard"]
    }

    if not user_funcs:
        return None, [], {}

    # Build reference function dictionary
    sol_dir = os.path.join(ROOT_DIR, "solutions")
    ref_map = {
        "Q401": "solution_Q401.py",
        "Q402": "solution_Q402.py",
        "Q777": "solution_Q777.py",
        "Q1000": "solution_Q1000.py",
        "AIRCRAFT": "solution_Aircraft_Maintenance.py",
        "FILM": "solution_Film_Crew_Payment.py",
        "MUSEUM": "solution_Museum_Artifact.py",
        "AGRICULTURE": "solution_Precision_Agriculture.py",
        "INSURANCE": "solution_Insurance_Claims.py",
        "TELECOM_RECHARGE": "solution_Telecom_Recharge.py",
        "Q16": "solution_Q16.py",
        "Q17": "solution_Q17.py",
        "Q18": "solution_Q18.py",
        "Q19": "solution_Q19.py",
        "Q24": "solution_Q24.py",
        "Q25": "solution_Q25.py",
        "Q26": "solution_Q26.py",
        "Q27": "solution_Q27.py",
    }

    question_funcs = {}
    func_occurrences = {}
    for qkey, fname in ref_map.items():
        p = os.path.join(sol_dir, fname)
        if not os.path.exists(p):
            continue
        try:
            with open(p, "r", encoding="utf-8", errors="replace") as f:
                rtree = ast.parse(f.read())
            qf = {n.name for n in rtree.body if isinstance(n, ast.FunctionDef) and not n.name.startswith("_")}
            question_funcs[qkey] = qf
            for fn in qf:
                func_occurrences[fn] = func_occurrences.get(fn, 0) + 1
        except Exception:
            pass

    # Score each question
    scores = {}
    matches = {}
    for qkey, qf in question_funcs.items():
        overlap = user_funcs.intersection(qf)
        if overlap:
            score = sum(3 if func_occurrences.get(fn, 0) == 1 else 1 for fn in overlap)
            # Bonus points for question-specific keywords in source
            bonus_keywords = {
                "Q401": ["commerce", "retail", "gross_amount", "discount_rate"],
                "Q402": ["telecom_usage", "roaming", "data_usage", "call_duration"],
                "Q777": ["appointment", "doctor", "wait_time", "patient"],
                "Q1000": ["trip", "mobility", "smartcity", "vehicle"],
                "AIRCRAFT": ["aircraft", "maintenance", "part_cost"],
                "FILM": ["crew", "payment", "production", "hourly_rate"],
                "MUSEUM": ["artifact", "gallery", "acquisition"],
                "AGRICULTURE": ["field", "moisture", "crop", "inspection"],
                "INSURANCE": ["claim", "policy", "claim_amount"],
                "TELECOM_RECHARGE": ["recharge", "payment_mode", "topup"],
                "Q16": ["kyc", "customer", "onboarding_date", "risk_score"],
                "Q17": ["triage", "arrival_time", "doctor_start_time", "priority"],
                "Q18": ["vaccine", "potency", "expiry_date", "manufacture_date"],
                "Q19": ["track", "genre", "stream_count", "artist"],
                "Q24": ["settlement", "merchant", "gross_amount", "fee_amount"],
                "Q25": ["observation", "systolic", "heart_rate", "care_team"],
                "Q26": ["bioreactor", "reactor", "process_type", "yield_pct"],
                "Q27": ["impression", "campaign", "ad_length", "watch_pct"],
            }
            code_lower = source_code.lower()
            for kw in bonus_keywords.get(qkey, []):
                if kw in code_lower:
                    score += 1
            scores[qkey] = score
            matches[qkey] = sorted(list(overlap))

    if not scores:
        return None, [], {}

    best_q = max(scores.keys(), key=lambda k: scores[k])
    return best_q, matches.get(best_q, []), scores


def resolve_question_key(target: str, source_path: Optional[str] = None) -> Optional[str]:
    target_clean = target.strip().lower()
    if target_clean in ["all", "everything", "*"]:
        return "ALL"
    if target_clean in ["auto", "detect", "automatic"]:
        detected_key, matched_funcs, _ = detect_question_from_source(source_path)
        if detected_key:
            print(f"{CYAN}[AUTO-DETECT]{RESET} Detected Question: {BOLD}{detected_key}{RESET} ({QUESTION_REGISTRY[detected_key]['title']})")
            print(f"              Matched Functions: {matched_funcs}")
            return detected_key
        else:
            print(f"{YELLOW}[AUTO-DETECT]{RESET} No matching functions detected. Defaulting to Q401.")
            return "Q401"
    for key, data in QUESTION_REGISTRY.items():
        if target_clean == key.lower() or target_clean in [a.lower() for a in data["aliases"]]:
            return key
    return None


def execute_question_tests(qkey: str, custom_solution_module=None) -> Dict:
    """Executes the test suite for a specific question from Tests/."""
    qinfo = QUESTION_REGISTRY[qkey]
    qtitle = qinfo["title"]
    test_file = qinfo["test_file"]
    qdir = qinfo["dir"]

    # Clear previous test_report.log in Tests
    log_file = os.path.join(TESTS_DIR, "test_report.log")
    if os.path.exists(log_file):
        try:
            os.remove(log_file)
        except Exception:
            pass

    t0 = time.time()
    sub_env = os.environ.copy()
    sub_env["TARGET_QUESTION"] = qkey

    stdout_file = os.path.join(TESTS_DIR, "pytest_stdout.tmp")
    stderr_file = os.path.join(TESTS_DIR, "pytest_stderr.tmp")

    with open(stdout_file, "w", encoding="utf-8") as out_f, open(stderr_file, "w", encoding="utf-8") as err_f:
        proc = subprocess.Popen(
            [PYTHON_EXE, "-m", "pytest", test_file, "-q", "--disable-warnings"],
            cwd=TESTS_DIR,
            env=sub_env,
            stdout=out_f,
            stderr=err_f,
        )

        seen_lines = set()
        while proc.poll() is None:
            if os.path.exists(log_file):
                try:
                    with open(log_file, "r", encoding="utf-8", errors="replace") as f:
                        for line in f:
                            line_s = line.strip()
                            if line_s and line_s not in seen_lines:
                                seen_lines.add(line_s)
                                if ": PASS" in line_s or "[PASS]" in line_s:
                                    print(f"\n    {GREEN}✔{RESET} {line_s}", end="", flush=True)
                                elif ": FAIL" in line_s or "[FAIL]" in line_s:
                                    print(f"\n    {RED}✘{RESET} {line_s}", end="", flush=True)
                except Exception:
                    pass
            time.sleep(0.2)

    duration = time.time() - t0

    # Read captured stdout and stderr
    stdout = ""
    stderr = ""
    try:
        with open(stdout_file, "r", encoding="utf-8", errors="replace") as f:
            stdout = f.read()
        os.remove(stdout_file)
    except Exception:
        pass
    try:
        with open(stderr_file, "r", encoding="utf-8", errors="replace") as f:
            stderr = f.read()
        os.remove(stderr_file)
    except Exception:
        pass

    # Parse test_report.log if written
    log_text = ""
    if os.path.exists(log_file):
        try:
            with open(log_file, "r", encoding="utf-8", errors="replace") as f:
                log_text = f.read()
        except Exception:
            pass

    combined_output = log_text + "\n" + stdout
    lines = combined_output.splitlines()
    passed_cases = []
    failed_cases = []

    i = 0
    while i < len(lines):
        line_clean = lines[i].strip()
        if "[PASS]" in line_clean or " : PASS" in line_clean:
            if line_clean not in passed_cases:
                passed_cases.append(line_clean)
        elif "[FAIL]" in line_clean or " : FAIL" in line_clean:
            msg = line_clean
            j = i + 1
            while j < len(lines) and not ("[FAIL]" in lines[j] or "[PASS]" in lines[j] or ": PASS" in lines[j] or ": FAIL" in lines[j] or lines[j].strip().startswith("===")):
                if lines[j].strip().startswith("Reason"):
                    msg += f"\n         -> {lines[j].strip()}"
                    break
                j += 1
            if msg not in failed_cases:
                failed_cases.append(msg)
        i += 1

    total_expected = qinfo["expected_tests"]
    passed_count = len(passed_cases)

    # Fallback to pytest summary if log was quiet
    if passed_count == 0 and "passed" in stdout:
        import re
        m = re.search(r'(\d+)\s+passed', stdout)
        if m:
            passed_count = int(m.group(1))
            passed_cases = [f"[PASS] PyTest Passed {i+1}" for i in range(passed_count)]

    passed = (passed_count == total_expected and len(failed_cases) == 0)

    return {
        "id": qkey,
        "title": qtitle,
        "expected": total_expected,
        "passed_count": passed_count,
        "failed_count": len(failed_cases),
        "passed": passed,
        "duration": duration,
        "passed_cases": passed_cases,
        "failed_cases": failed_cases,
        "stderr": stderr,
        "stdout": stdout,
    }


def print_banner(target: str, mode: str = "TEST"):
    print("=" * 72)
    print("         PySpark Practice - Unified Solution Tester")
    print("=" * 72)
    print(f"Target Question : {target}")
    print(f"Execution Mode  : {mode}")
    print(f"Python Binary   : {PYTHON_EXE}")
    print()


def print_scorecard(results: List[Dict]):
    print("\n" + "=" * 70)
    print("                PYSPARK PRACTICE QUESTIONS SCORECARD")
    print("=" * 70)
    print(f"{'#':<4}{'Question / Domain':<38}{'Tests':<11}{'Time':<9}{'Status'}")
    print("-" * 70)

    total_passed = 0
    total_expected = 0
    total_time = 0.0

    for idx, r in enumerate(results, 1):
        total_passed += r["passed_count"]
        total_expected += r["expected"]
        total_time += r["duration"]

        status_str = f"{GREEN}PASSED{RESET}" if r["passed"] else f"{RED}FAILED{RESET}"
        tests_str = f"{r['passed_count']}/{r['expected']}"
        time_str = f"{r['duration']:.1f}s"
        title_trunc = r["title"][:36]

        print(f"{idx:<4}{title_trunc:<38}{tests_str:<11}{time_str:<9}{status_str}")

    pct = (total_passed / total_expected * 100.0) if total_expected > 0 else 0.0
    print("-" * 70)
    print(f"Total Score: {total_passed}/{total_expected} Tests Passed ({pct:.1f}%) | Total Time: {total_time:.1f}s")

    if total_passed == total_expected and total_expected > 0:
        print(f"{GREEN}>>> ALL ASSESSMENTS PASSED WITH 100% SUCCESS! EXCELLENT WORK! <<<{RESET}")
    else:
        print(f"{YELLOW}[!] Some test cases require attention. Review failed cases above.{RESET}")
    print("=" * 70 + "\n")


def run_tests(target: str = "ALL", custom_solution_module=None, source_path: Optional[str] = None):
    """
    Main entry point for testing assessment solutions.
    target: "AUTO", "ALL", or specific question key/alias (e.g., "Q401", "Q777", "AIRCRAFT")
    """
    if source_path is None and custom_solution_module is not None:
        source_path = getattr(custom_solution_module, "__file__", None)
    resolved_key = resolve_question_key(target, source_path=source_path)
    if not resolved_key:
        print(f"\n{RED}Unknown question target: '{target}'{RESET}")
        print("Available options:")
        print("  ALL")
        for k, v in QUESTION_REGISTRY.items():
            print(f"  {k} ({v['title']})")
        return

    print(f"\n=== Starting PySpark Test Run (Target: {target}) ===\n")

    targets_to_run = (
        list(QUESTION_REGISTRY.keys())
        if resolved_key == "ALL"
        else [resolved_key]
    )

    results = []
    for qkey in targets_to_run:
        qinfo = QUESTION_REGISTRY[qkey]
        print(f"[{qkey}] {qinfo['title']} ...", end=" ", flush=True)

        res = execute_question_tests(qkey, custom_solution_module)
        results.append(res)

        status_tag = f"{GREEN}PASS{RESET}" if res["passed"] else f"{RED}FAIL{RESET}"
        print(f"\r[{qkey}] {qinfo['title']}")
        print(f"  Status: {status_tag} | Tests: {res['passed_count']}/{res['expected']} | Duration: {res['duration']:.2f}s")

        if res["passed_cases"]:
            print("  --- Passed Test Cases ---")
            for c in res["passed_cases"]:
                print(f"  {c}")

        if res["failed_cases"]:
            print(f"  {RED}--- Failures / Issues ---{RESET}")
            for f in res["failed_cases"]:
                print(f"  {RED}{f}{RESET}")

        print()

    print_scorecard(results)
    return results


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "ALL"
    print_banner(target)
    run_tests(target)
