import hashlib
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parent
LOG=ROOT/"test_report.log"
TEST=ROOT/"test_configurable_functions.py"
PROTECTED=[ROOT/"conftest.py",ROOT/"test_config.json",ROOT/"test_configurable_functions.py",ROOT/"test_runner.py",ROOT/"specification.md"]

def sha256(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for chunk in iter(lambda:f.read(65536),b""):
            h.update(chunk)
    return h.hexdigest()

def framework_fail(reason):
    with open(LOG,"a",encoding="utf-8") as f:
        f.write("Test Case 00 : framework_execution : FAIL | Expected = runnable untampered assessment with valid solution imports | Reason = "+reason.replace("\n"," ")+"\n")

def main():
    LOG.write_text("",encoding="utf-8")
    before={str(p):sha256(p) for p in PROTECTED if p.exists()}
    result=subprocess.run([sys.executable,"-m","pytest","-s","-q",TEST.name],cwd=str(ROOT))
    changed=[p.name for p in PROTECTED if p.exists() and str(p) in before and sha256(p)!=before[str(p)]]
    if changed:
        framework_fail("Protected assessment files were modified during execution: "+", ".join(changed))
        return 1
    if result.returncode!=0 and not LOG.read_text(encoding="utf-8").strip():
        framework_fail(f"pytest exited with code {result.returncode}; review syntax/import/collection output")
    return result.returncode

if __name__=="__main__":
    raise SystemExit(main())
