/**
 * Universal Test Runner for Learnlytica Assessment Pro
 * 
 * This script automatically detects the type of assessment (Python Script, Pytest, Shell, etc.)
 * and runs the appropriate command to generate test_report.log.
 */

const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

// Colors for console output
const COLORS = {
    reset: "\x1b[0m",
    green: "\x1b[32m",
    red: "\x1b[31m",
    yellow: "\x1b[33m",
    blue: "\x1b[34m",
    cyan: "\x1b[36m"
};

const WORKSPACE_DIR = process.cwd();
const REPORT_FILE = 'test_report.log';

function log(message, color = COLORS.reset) {
    console.log(`${color}${message}${COLORS.reset}`);
}

/**
 * Detect if a virtual environment exists and return the appropriate Python command
 */
function getPythonCommand() {
    const venvPath = path.join(WORKSPACE_DIR, '.venv');
    
    if (fs.existsSync(venvPath)) {
        const venvPython = process.platform === 'win32'
            ? path.join(venvPath, 'Scripts', 'python.exe')
            : path.join(venvPath, 'bin', 'python');
        
        if (fs.existsSync(venvPython)) {
            log(`🐍 Using virtual environment Python: ${venvPython}`, COLORS.cyan);
            return venvPython;
        }
    }
    
    // Fallback to system Python
    return 'python3';
}

function findFileRecursively(dir, filename) {
    try {
        const files = fs.readdirSync(dir);
        for (const file of files) {
            const fullPath = path.join(dir, file);
            const stat = fs.statSync(fullPath);
            
            if (stat.isDirectory() && file !== 'node_modules' && file !== '.git' && file !== '__pycache__') {
                const found = findFileRecursively(fullPath, filename);
                if (found) return found;
            } else if (file === filename) {
                return fullPath;
            }
        }
    } catch (e) {
        return null;
    }
    return null;
}

// Helper to find any file ending with _test_report.log
function findAnyReportFile(dir) {
    try {
        const files = fs.readdirSync(dir);
        for (const file of files) {
            const fullPath = path.join(dir, file);
            if (file.endsWith('_test_report.log') && file !== 'test_report.log') {
                return fullPath;
            }
        }
    } catch (e) {
        return null;
    }
    return null;
}

async function runCommand(command, args) {
    const currentDir = process.cwd();
    log(`\n🚀 Executing: ${command} ${args.join(' ')}`, COLORS.cyan);
    log(`📁 Working directory: ${currentDir}`, COLORS.blue);
    
    return new Promise((resolve, reject) => {
        console.log('[UniversalRunner] Spawning process:', command, args);
        console.log('[UniversalRunner] Current directory:', currentDir);
        
        // Use pipe for stdio to prevent test runners from waiting for user input
        // stdin is set to 'ignore' so any input() calls will immediately return EOF
        const proc = spawn(command, args, {
            cwd: currentDir,  // Use current directory (respects process.chdir() calls)
            shell: true,
            stdio: ['ignore', 'inherit', 'inherit'], // stdin: ignore, stdout: inherit, stderr: inherit
            env: {
                ...process.env,
                AUTOMATED_TEST: 'true',  // Signal to test runners that they're in automated mode
                NO_INTERACTIVE: 'true',
                CI: 'true'  // Many tools check for CI environment
            }
        });

        console.log('[UniversalRunner] Process spawned, PID:', proc.pid);

        proc.on('close', (code) => {
            console.log('[UniversalRunner] Process closed with code:', code);
            if (code === 0) {
                resolve();
            } else {
                // Don't reject, just resolve with code so we can check report file
                log(`⚠️ Command exited with code ${code}`, COLORS.yellow);
                resolve();
            }
        });

        proc.on('error', (err) => {
            console.error('[UniversalRunner] Process error:', err);
            log(`❌ Failed to start command: ${err.message}`, COLORS.red);
            reject(err);
        });

        // Add timeout warning (increased to 30s for network operations)
        const timeoutWarning = setTimeout(() => {
            console.warn('[UniversalRunner] ⚠️  Command has been running for 30+ seconds...');
        }, 30000);

        proc.on('close', () => {
            clearTimeout(timeoutWarning);
        });
    });
}

async function main() {
    console.log('[UniversalRunner] ========================================');
    console.log('[UniversalRunner] Starting universal test runner');
    console.log('[UniversalRunner] Workspace:', WORKSPACE_DIR);
    console.log('[UniversalRunner] Platform:', process.platform);
    console.log('[UniversalRunner] ========================================');
    
    log("🔍 Analyzing workspace for test configuration...", COLORS.blue);

    // 1. Detect Python command (venv or system)
    console.log('[UniversalRunner] Detecting Python command...');
    const pythonCmd = getPythonCommand();
    console.log('[UniversalRunner] Python command:', pythonCmd);

    // 2. Clean up old reports
    if (fs.existsSync(REPORT_FILE)) {
        try {
            fs.unlinkSync(REPORT_FILE);
            log("🧹 Cleaned up old test_report.log", COLORS.yellow);
        } catch (e) {}
    }

    // 3. Detect Test Runner Strategy
    console.log('[UniversalRunner] Detecting test runner strategy...');
    const testRunnerPy = findFileRecursively(WORKSPACE_DIR, 'test_runner.py');
    const runTestsSh = findFileRecursively(WORKSPACE_DIR, 'run_tests.sh');
    const pytestConfig = findFileRecursively(WORKSPACE_DIR, 'pytest.ini') || 
                        findFileRecursively(WORKSPACE_DIR, 'conftest.py') ||
                        findFileRecursively(WORKSPACE_DIR, 'test_config.json'); 

    console.log('[UniversalRunner] test_runner.py:', testRunnerPy || 'NOT FOUND');
    console.log('[UniversalRunner] run_tests.sh:', runTestsSh || 'NOT FOUND');
    console.log('[UniversalRunner] pytest config:', pytestConfig || 'NOT FOUND');

    let runnerDir = process.cwd();

    try {
        if (testRunnerPy) {
            log("✅ Detected Python Custom Runner (test_runner.py)", COLORS.green);
            runnerDir = path.dirname(testRunnerPy);
            console.log('[UniversalRunner] Changing directory to:', runnerDir);
            process.chdir(runnerDir);
            console.log('[UniversalRunner] Current directory is now:', process.cwd());
            await runCommand(pythonCmd, ['test_runner.py']);
        } 
        else if (runTestsSh) {
            log("✅ Detected Shell Runner (run_tests.sh)", COLORS.green);
            runnerDir = path.dirname(runTestsSh);
            process.chdir(runnerDir);
            if (process.platform !== 'win32') {
                await runCommand('chmod', ['+x', 'run_tests.sh']);
            }
            await runCommand('./run_tests.sh', []);
        } 
        else if (pytestConfig) {
            log("✅ Detected Pytest Configuration", COLORS.green);
            runnerDir = path.dirname(pytestConfig);
            process.chdir(runnerDir); 
            await runCommand(pythonCmd, ['-m', 'pytest']);
        }
        else {
            const testsDir = findFileRecursively(WORKSPACE_DIR, 'tests');
            const secretTestsDir = findFileRecursively(WORKSPACE_DIR, 'secret_tests');
            
            if (testsDir) {
                 log("⚠️ No explicit config found, but 'tests' dir exists. Trying generic pytest...", COLORS.yellow);
                 process.chdir(path.dirname(testsDir));
                 await runCommand(pythonCmd, ['-m', 'pytest']);
            } else if (secretTestsDir) {
                 log("⚠️ No explicit config found, but 'secret_tests' dir exists. Trying generic pytest...", COLORS.yellow);
                 process.chdir(path.dirname(secretTestsDir));
                 await runCommand(pythonCmd, ['-m', 'pytest']);
            } else {
                throw new Error("Could not detect any known test runner (test_runner.py, run_tests.sh, pytest config, or tests/secret_tests folder)");
            }
        }

        // 3. Verification & Normalization
        // Check for standard report first
        let reportPath = path.resolve(process.cwd(), 'test_report.log');
        
        if (!fs.existsSync(reportPath)) {
            // Check for non-standard reports (e.g. rds_test_report.log) in the runner dir
            const altReport = findAnyReportFile(runnerDir);
            if (altReport) {
                log(`⚠️ Found non-standard report: ${path.basename(altReport)}. Renaming to test_report.log`, COLORS.yellow);
                fs.copyFileSync(altReport, reportPath);
            }
        }
        
        if (fs.existsSync(reportPath)) {
            log(`\n✅ Success! generated: ${reportPath}`, COLORS.green);
            const content = fs.readFileSync(reportPath, 'utf8');
            const passCount = (content.match(/\[PASS\]/g) || []).length;
            const failCount = (content.match(/\[FAIL\]/g) || []).length;
            
            log(`📊 Summary: ${passCount} Passed, ${failCount} Failed`, COLORS.cyan);
        } else {
            log("\n❌ Error: Tests ran but 'test_report.log' was not generated.", COLORS.red);
            log("   Please ensure your solution code compiles and runs correctly.", COLORS.red);
        }

    } catch (e) {
        log(`\n💥 Critical Error: ${e.message}`, COLORS.red);
        process.exit(1);
    }
}

main();
