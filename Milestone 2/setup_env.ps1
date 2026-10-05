# ==============================================================================
# PySpark Office Laptop One-Click Setup Script (PowerShell)
# ==============================================================================

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Setting up Milestone 2 PySpark Environment (Windows)     " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Verify Python
$pythonCmd = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $pythonCmd) {
    Write-Host "[ERROR] Python is not installed or not in PATH." -ForegroundColor Red
    Write-Host "Please install Python 3.10-3.12 from python.org and check 'Add Python to PATH'." -ForegroundColor Yellow
    Exit 1
}
Write-Host "[OK] Found Python: $pythonCmd" -ForegroundColor Green

# 2. Check Java (Spark Requirement)
$javaCmd = (Get-Command java -ErrorAction SilentlyContinue).Source
if (-not $javaCmd -and -not $env:JAVA_HOME) {
    Write-Host "[NOTE] Java is not detected in PATH or JAVA_HOME." -ForegroundColor Yellow
    Write-Host "PySpark requires Java (JDK 11 or 17 recommended)." -ForegroundColor Yellow
} else {
    Write-Host "[OK] Java detected." -ForegroundColor Green
}

# 3. Create Virtualenv
$setupDir = Join-Path $PSScriptRoot "PySpark Setup"
$venvDir = Join-Path $setupDir ".venv"
if (-not (Test-Path $venvDir)) {
    Write-Host "Creating virtual environment at $venvDir..." -ForegroundColor Cyan
    & python -m venv $venvDir
} else {
    Write-Host "[OK] Virtual environment already exists." -ForegroundColor Green
}

# 4. Install Dependencies
$venvPython = Join-Path $venvDir "Scripts\python.exe"
Write-Host "Installing dependencies from requirements.txt..." -ForegroundColor Cyan
& $venvPython -m pip install --upgrade pip
& $venvPython -m pip install -r (Join-Path $setupDir "requirements.txt")

# 5. Download Hadoop WinUtils & MySQL connector
Write-Host "Downloading Hadoop winutils & connector..." -ForegroundColor Cyan
& $venvPython (Join-Path $setupDir "download_assets.py")

Write-Host ""
Write-Host "==========================================================" -ForegroundColor Green
Write-Host " Environment Setup Complete!                             " -ForegroundColor Green
Write-Host " To practice, open 'Milestone 2/PySpark Practice/solution.py'" -ForegroundColor Green
Write-Host " and click 'Run Python File' in VS Code!" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
