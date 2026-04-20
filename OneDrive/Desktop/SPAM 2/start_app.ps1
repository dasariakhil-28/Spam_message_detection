# ============================================================
# SPAM DETECTION SYSTEM - START SCRIPT
# Run this script to start the server and open in browser
# ============================================================

Write-Host "=================================================="
Write-Host "🚀 SPAM DETECTION SYSTEM STARTUP"
Write-Host "=================================================="
Write-Host ""

# Get the script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommandPath
Set-Location $scriptDir

Write-Host "📁 Project Directory: $scriptDir"
Write-Host ""

# Check if virtual environment exists
if (Test-Path ".\.venv\Scripts\python.exe") {
    Write-Host "✅ Virtual environment found"
} else {
    Write-Host "❌ Virtual environment not found!"
    Write-Host "Please run: python -m venv .venv"
    exit
}

Write-Host ""
Write-Host "🔧 Activating virtual environment..."

# Activate virtual environment
& ".\.venv\Scripts\Activate.ps1"

Write-Host "✅ Virtual environment activated"
Write-Host ""

# Check if model exists
if (Test-Path ".\spam_model.pkl") {
    Write-Host "✅ ML Model found (spam_model.pkl)"
} else {
    Write-Host "⚠️  Warning: Model file not found"
    Write-Host "   Run: python train_model.py"
}

Write-Host ""
Write-Host "=================================================="
Write-Host "🌐 Starting Flask Server"
Write-Host "=================================================="
Write-Host ""
Write-Host "📱 Website will be available at: http://localhost:5000"
Write-Host "🔌 API Endpoint: http://localhost:5000/api"
Write-Host ""
Write-Host "Press Ctrl+C to stop the server"
Write-Host "=================================================="
Write-Host ""

# Start Flask app
$pythonExe = ".\.venv\Scripts\python.exe"

# Start server in background and capture the process
$flaskProcess = Start-Process -FilePath $pythonExe -ArgumentList "app.py" -PassThru -NoNewWindow

# Wait a bit for server to start
Write-Host "⏳ Waiting for server to start..."
Start-Sleep -Seconds 3

# Check if server is running
$healthCheck = $null
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000/api/health" -UseBasicParsing -ErrorAction SilentlyContinue -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Server is running!"
        Write-Host ""
        Write-Host "🌐 Opening browser..."
        
        # Open the website in default browser
        Start-Process "http://localhost:5000"
        
        Write-Host "✅ Browser opened!"
        Write-Host ""
        Write-Host "=================================================="
        Write-Host "✨ SPAM DETECTION SYSTEM IS READY!"
        Write-Host "=================================================="
        Write-Host ""
        Write-Host "The server will continue running..."
        Write-Host "Keep this window open while using the application."
        Write-Host ""
        Write-Host "Press Ctrl+C in this window to stop."
        
        # Wait for process to complete
        $flaskProcess | Wait-Process
    }
} catch {
    Write-Host "❌ Server failed to start"
    Write-Host "Error: $_"
    exit 1
}
