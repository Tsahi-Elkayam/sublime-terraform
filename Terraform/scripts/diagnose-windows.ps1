# Windows Diagnostic Script for Terraform Sublime Text Plugin
# This script helps diagnose common issues on Windows

Write-Host "Terraform Sublime Text Plugin - Windows Diagnostics" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Collecting system information..." -ForegroundColor Yellow
Write-Host ""

# Function to check command
function Test-CommandVersion($cmd, $versionArg = "--version") {
    try {
        $result = & $cmd $versionArg 2>&1
        return @{
            Found = $true
            Version = ($result | Out-String).Trim()
            Path = (Get-Command $cmd).Path
        }
    } catch {
        return @{
            Found = $false
            Version = "Not found"
            Path = "N/A"
        }
    }
}

# 1. System Information
Write-Host "[System Information]" -ForegroundColor Green
Write-Host "Windows Version: $([System.Environment]::OSVersion.Version)" -ForegroundColor White
Write-Host "Architecture: $env:PROCESSOR_ARCHITECTURE" -ForegroundColor White
Write-Host "PowerShell: $($PSVersionTable.PSVersion)" -ForegroundColor White
Write-Host "User: $env:USERNAME" -ForegroundColor White
Write-Host "Computer: $env:COMPUTERNAME" -ForegroundColor White
Write-Host ""

# 2. Python Check
Write-Host "[Python Environment]" -ForegroundColor Green
$python = Test-CommandVersion "python"
if ($python.Found) {
    Write-Host "✓ Python: $($python.Version)" -ForegroundColor White
    Write-Host "  Path: $($python.Path)" -ForegroundColor Gray
    
    # Check pip
    $pip = Test-CommandVersion "pip"
    if ($pip.Found) {
        Write-Host "✓ Pip: $($pip.Version)" -ForegroundColor White
    } else {
        Write-Host "✗ Pip: Not found" -ForegroundColor Red
    }
    
    # Check virtual environment
    if ($env:VIRTUAL_ENV) {
        Write-Host "✓ Virtual Environment: $env:VIRTUAL_ENV" -ForegroundColor White
    } else {
        Write-Host "  Virtual Environment: Not active" -ForegroundColor Gray
    }
} else {
    Write-Host "✗ Python: Not found" -ForegroundColor Red
}
Write-Host ""

# 3. Terraform Check
Write-Host "[Terraform]" -ForegroundColor Green
$terraform = Test-CommandVersion "terraform" "version"
if ($terraform.Found) {
    Write-Host "✓ Terraform: $($terraform.Version)" -ForegroundColor White
    Write-Host "  Path: $($terraform.Path)" -ForegroundColor Gray
} else {
    Write-Host "✗ Terraform: Not found" -ForegroundColor Red
}
Write-Host ""

# 4. Git Check
Write-Host "[Git]" -ForegroundColor Green
$git = Test-CommandVersion "git"
if ($git.Found) {
    Write-Host "✓ Git: $($git.Version)" -ForegroundColor White
    Write-Host "  Path: $($git.Path)" -ForegroundColor Gray
} else {
    Write-Host "✗ Git: Not found" -ForegroundColor Red
}
Write-Host ""

# 5. Sublime Text Check
Write-Host "[Sublime Text]" -ForegroundColor Green
$sublimePaths = @(
    "${env:ProgramFiles}\Sublime Text\sublime_text.exe",
    "${env:ProgramFiles(x86)}\Sublime Text\sublime_text.exe",
    "${env:LocalAppData}\Programs\Sublime Text\sublime_text.exe",
    "$env:APPDATA\Sublime Text\sublime_text.exe"
)

$sublimeFound = $false
foreach ($path in $sublimePaths) {
    if (Test-Path $path) {
        Write-Host "✓ Sublime Text: Found" -ForegroundColor White
        Write-Host "  Path: $path" -ForegroundColor Gray
        $sublimeFound = $true
        break
    }
}
if (-not $sublimeFound) {
    Write-Host "✗ Sublime Text: Not found in standard locations" -ForegroundColor Red
}

# Check packages directory
$packagesDir = "$env:APPDATA\Sublime Text\Packages"
if (Test-Path $packagesDir) {
    Write-Host "✓ Packages Directory: $packagesDir" -ForegroundColor White
    
    # Check if plugin is installed
    $pluginPath = "$packagesDir\Terraform"
    if (Test-Path $pluginPath) {
        Write-Host "✓ Plugin Installed: Yes" -ForegroundColor White
        
        # Check if it's a symlink
        $item = Get-Item $pluginPath
        if ($item.LinkType -eq "SymbolicLink") {
            Write-Host "  Type: Symbolic Link" -ForegroundColor Gray
            Write-Host "  Target: $($item.Target)" -ForegroundColor Gray
        } else {
            Write-Host "  Type: Regular Directory" -ForegroundColor Gray
        }
    } else {
        Write-Host "✗ Plugin Installed: No" -ForegroundColor Red
    }
} else {
    Write-Host "✗ Packages Directory: Not found" -ForegroundColor Red
}

# Check LSP package
$lspPath = "$packagesDir\LSP"
if (Test-Path $lspPath) {
    Write-Host "✓ LSP Package: Installed" -ForegroundColor White
} else {
    Write-Host "✗ LSP Package: Not installed" -ForegroundColor Red
}
Write-Host ""

# 6. terraform-ls Check
Write-Host "[Terraform Language Server]" -ForegroundColor Green
$terraformLsPaths = @(
    ".\bin\terraform-ls.exe",
    ".\Terraform\bin\terraform-ls.exe",
    "$packagesDir\Terraform\bin\terraform-ls.exe"
)

$terraformLsFound = $false
foreach ($path in $terraformLsPaths) {
    if (Test-Path $path) {
        Write-Host "✓ terraform-ls: Found" -ForegroundColor White
        Write-Host "  Path: $((Resolve-Path $path).Path)" -ForegroundColor Gray
        
        # Check version
        try {
            $version = & $path version 2>&1
            Write-Host "  Version: $version" -ForegroundColor Gray
        } catch {
            Write-Host "  Version: Unable to determine" -ForegroundColor Gray
        }
        
        $terraformLsFound = $true
        break
    }
}

if (-not $terraformLsFound) {
    # Check in PATH
    $terraformLs = Test-CommandVersion "terraform-ls"
    if ($terraformLs.Found) {
        Write-Host "✓ terraform-ls: Found in PATH" -ForegroundColor White
        Write-Host "  Path: $($terraformLs.Path)" -ForegroundColor Gray
    } else {
        Write-Host "✗ terraform-ls: Not found" -ForegroundColor Red
    }
}
Write-Host ""

# 7. PATH Environment Variable
Write-Host "[PATH Environment]" -ForegroundColor Green
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
$systemPath = [Environment]::GetEnvironmentVariable("Path", "Machine")

Write-Host "User PATH entries:" -ForegroundColor White
$userPath.Split(';') | Where-Object { $_ -match "terraform|python|git" } | ForEach-Object {
    Write-Host "  $_" -ForegroundColor Gray
}

Write-Host "System PATH entries:" -ForegroundColor White
$systemPath.Split(';') | Where-Object { $_ -match "terraform|python|git" } | ForEach-Object {
    Write-Host "  $_" -ForegroundColor Gray
}
Write-Host ""

# 8. Test Dependencies
if (Test-Path ".\Terraform\requirements-test.txt") {
    Write-Host "[Test Dependencies]" -ForegroundColor Green
    Write-Host "Checking installed packages..." -ForegroundColor White
    
    $requiredPackages = @("pytest", "coverage", "mock", "flake8")
    foreach ($package in $requiredPackages) {
        try {
            $result = pip show $package 2>&1
            if ($LASTEXITCODE -eq 0) {
                $version = ($result | Select-String "Version:").ToString().Split()[1]
                Write-Host "✓ $package : $version" -ForegroundColor White
            } else {
                Write-Host "✗ $package : Not installed" -ForegroundColor Red
            }
        } catch {
            Write-Host "✗ $package : Check failed" -ForegroundColor Red
        }
    }
}
Write-Host ""

# 9. File Permissions
Write-Host "[File Permissions]" -ForegroundColor Green
if (Test-Path $pluginPath) {
    $acl = Get-Acl $pluginPath
    Write-Host "Plugin Directory Owner: $($acl.Owner)" -ForegroundColor White
    Write-Host "Current User Has Access: $(Test-Path $pluginPath -PathType Container)" -ForegroundColor White
}
Write-Host ""

# 10. Recommendations
Write-Host "[Recommendations]" -ForegroundColor Yellow
$issues = @()

if (-not $python.Found) {
    $issues += "Install Python 3.8+ from https://python.org"
}
if (-not $terraform.Found) {
    $issues += "Install Terraform from https://terraform.io/downloads"
}
if (-not $sublimeFound) {
    $issues += "Install Sublime Text 4 from https://sublimetext.com"
}
if (-not (Test-Path $pluginPath)) {
    $issues += "Install the plugin by running: .\scripts\windows-setup.ps1 -DevMode"
}
if (-not (Test-Path $lspPath)) {
    $issues += "Install LSP package in Sublime Text via Package Control"
}
if (-not $terraformLsFound) {
    $issues += "Download terraform-ls by running the setup script"
}

if ($issues.Count -gt 0) {
    Write-Host "Please address the following issues:" -ForegroundColor White
    $issues | ForEach-Object { Write-Host "  • $_" -ForegroundColor White }
} else {
    Write-Host "✓ Everything looks good!" -ForegroundColor Green
}

Write-Host ""
Write-Host "Diagnostics complete. Save this output if reporting issues." -ForegroundColor Cyan