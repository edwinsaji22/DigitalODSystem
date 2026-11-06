# ==============================================================================
# Digital Leave / On-Duty (OD) Application System
# Automated Build & Tomcat Deployment Script (PowerShell)
# ==============================================================================

[CmdletBinding()]
param(
    [Parameter(Mandatory = $false, Position = 0)]
    [string]$TomcatPath
)

$ErrorActionPreference = "Stop"
$WorkspaceRoot = $PSScriptRoot

Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host " DIGITAL OD SYSTEM - BUILD & TOMCAT DEPLOYMENT SCRIPT" -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Cyan

# ------------------------------------------------------------------------------
# STEP 1: Locate Apache Tomcat Installation Directory
# ------------------------------------------------------------------------------
if (-not $TomcatPath) {
    if ($env:CATALINA_HOME -and (Test-Path $env:CATALINA_HOME)) {
        $TomcatPath = $env:CATALINA_HOME
    } elseif ($env:TOMCAT_HOME -and (Test-Path $env:TOMCAT_HOME)) {
        $TomcatPath = $env:TOMCAT_HOME
    } else {
        # Check standard default installation paths
        $CommonPaths = @(
            "C:\Program Files\Apache Software Foundation\Tomcat 9.0",
            "C:\Program Files\Apache Software Foundation\Tomcat 8.5",
            "C:\apache-tomcat-9.0.*",
            "C:\apache-tomcat-9*",
            "C:\apache-tomcat*",
            "D:\apache-tomcat*"
        )
        foreach ($pattern in $CommonPaths) {
            $found = Get-ChildItem -Path $pattern -Directory -ErrorAction SilentlyContinue | Select-Object -First 1
            if ($found) {
                $TomcatPath = $found.FullName
                break
            }
        }
    }
}

if (-not $TomcatPath -or -not (Test-Path $TomcatPath)) {
    Write-Host "`n[!] Apache Tomcat installation directory not detected automatically." -ForegroundColor Yellow
    $TomcatPath = Read-Host "Please enter your Tomcat root folder path (e.g. C:\apache-tomcat-9.0.80)"
    if (-not $TomcatPath -or -not (Test-Path $TomcatPath)) {
        Write-Error "Invalid Tomcat path provided. Deployment aborted."
        exit 1
    }
}

Write-Host "[+] Target Apache Tomcat Path : $TomcatPath" -ForegroundColor Green

# ------------------------------------------------------------------------------
# STEP 2: Compile All Java Classes into WEB-INF/classes
# ------------------------------------------------------------------------------
Write-Host "`n[*] Compiling Java source files..." -ForegroundColor Cyan

$ClassesDir = Join-Path $WorkspaceRoot "WEB-INF\classes"
if (-not (Test-Path $ClassesDir)) {
    New-Item -ItemType Directory -Path $ClassesDir -Force | Out-Null
}

$LibJars = Join-Path $WorkspaceRoot "WEB-INF\lib\*"
$Classpath = ".;$WorkspaceRoot;$LibJars"

$JavaFiles = Get-ChildItem -Path $WorkspaceRoot -Recurse -Filter "*.java" | Select-Object -ExpandProperty FullName

try {
    & javac -encoding UTF-8 -cp $Classpath -d $ClassesDir $JavaFiles
    Write-Host "[+] Compilation successful! Classes placed into WEB-INF/classes" -ForegroundColor Green
} catch {
    Write-Error "Java compilation failed. Please verify JDK installation and classpath."
    exit 1
}

# ------------------------------------------------------------------------------
# STEP 3: Deploy Application to Tomcat webapps/DigitalODSystem
# ------------------------------------------------------------------------------
$TargetAppDir = Join-Path $TomcatPath "webapps\DigitalODSystem"

Write-Host "`n[*] Deploying to: $TargetAppDir" -ForegroundColor Cyan

if (-not (Test-Path $TargetAppDir)) {
    New-Item -ItemType Directory -Path $TargetAppDir -Force | Out-Null
}

# Items to deploy
$DeployItems = @(
    "login.html",
    "index.html",
    "student_dashboard.jsp",
    "staff_dashboard.jsp",
    "hod_dashboard.jsp",
    "od_criteria.jsp",
    "dashboard.jsp",
    "student_dashboard.html",
    "staff_dashboard.html",
    "hod_dashboard.html",
    "css",
    "WEB-INF"
)

foreach ($item in $DeployItems) {
    $src = Join-Path $WorkspaceRoot $item
    if (Test-Path $src) {
        Copy-Item -Path $src -Destination $TargetAppDir -Recurse -Force
        Write-Host "    -> Copied $item" -ForegroundColor Gray
    }
}

Write-Host "`n=====================================================================" -ForegroundColor Green
Write-Host " [SUCCESS] DEPLOYMENT COMPLETE!" -ForegroundColor Green
Write-Host "=====================================================================" -ForegroundColor Green
Write-Host "`nNext Steps to run the system:"
Write-Host "1. MySQL Database Setup (if not already done):" -ForegroundColor Yellow
Write-Host "   mysql -u root -p < `"$WorkspaceRoot\schema.sql`"" -ForegroundColor White
Write-Host "`n2. Start Apache Tomcat Server:" -ForegroundColor Yellow
Write-Host "   `"$TomcatPath\bin\startup.bat`"" -ForegroundColor White
Write-Host "`n3. Open Web Browser and access the application:" -ForegroundColor Yellow
Write-Host "   http://localhost:8080/DigitalODSystem/login.html" -ForegroundColor Cyan
Write-Host "`nDefault Test Logins:" -ForegroundColor White
Write-Host "   - Student: username: studentjohn | password: pass123" -ForegroundColor White
Write-Host "   - Staff:   username: staffjacob  | password: jacob1234" -ForegroundColor White
Write-Host "   - HOD:     username: hodsmith    | password: hod1234" -ForegroundColor White
Write-Host "=====================================================================`n"
