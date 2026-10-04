import hashlib
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
REPORT = os.path.join(ROOT, "test_report.log")
PROTECTED = ["conftest.py", "test_config.json", "test_configurable_functions.py", "test_runner.py", "specification.md"]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


before = {name: sha256(os.path.join(ROOT, name)) for name in PROTECTED}
cmd = [sys.executable, "-m", "pytest", "-q", "-s", "test_configurable_functions.py"]
proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
output = (proc.stdout or "") + (proc.stderr or "")
print(output, end="")
after = {name: sha256(os.path.join(ROOT, name)) for name in PROTECTED}
tampered = [name for name in PROTECTED if before[name] != after[name]]
with open(REPORT, "w", encoding="utf-8") as f:
    f.write(output)
    f.write("\nFramework Tamper Check : " + ("FAIL - " + ", ".join(tampered) if tampered else "PASS") + "\n")
raise SystemExit(1 if proc.returncode != 0 or tampered else 0)
