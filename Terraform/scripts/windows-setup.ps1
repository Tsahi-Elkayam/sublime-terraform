# Terraform Sublime Text Plugin - Windows Setup Script
# Run this script to set up the development environment on Windows

param(
    [switch]$SkipDependencies,
    [switch]$DevMode,
    [switch]$Force
)

$ErrorActionPreference = "Stop"

Write-Host "Terraform Sublime Text Plugin - Windows Setup" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

if (-not $isAdmin) {
    Write-Warning "Some operations may require administrator privileges"
}

# Function to test command availability
function Test-Command($cmdname) {
    return [bool](Get-Command -Name $cmdname -ErrorAction SilentlyContinue)
}

# Function to add to PATH
function Add-ToPath($path) {
    $currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
    if ($currentPath -notlike "*$path*") {
        [Environment]::SetEnvironmentVariable("Path", "$currentPath;$path", "User")
        $env:Path = "$env:Path;$path"
        Write-Host "Added $path to PATH" -ForegroundColor Green
    }
}

# 1. Check Python
Write-Host "Checking Python installation..." -ForegroundColor Yellow
if (Test-Command python) {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ $pythonVersion" -ForegroundColor Green
    
    # Check version
    $version = [version]((python --version 2>&1) -replace 'Python ', '')
    if ($version -lt [version]"3.8.0") {
        Write-Error "Python 3.8 or higher is required. Found $version"
    }
} else {
    Write-Error "Python not found. Please install Python 3.8+ from https://www.python.org"
}

# 2. Check pip
Write-Host "`nChecking pip..." -ForegroundColor Yellow
if (Test-Command pip) {
    $pipVersion = pip --version
    Write-Host "✓ $pipVersion" -ForegroundColor Green
} else {
    Write-Error "pip not found. Please ensure Python is properly installed"
}

# 3. Check Git
Write-Host "`nChecking Git..." -ForegroundColor Yellow
if (Test-Command git) {
    $gitVersion = git --version
    Write-Host "✓ $gitVersion" -ForegroundColor Green
} else {
    Write-Warning "Git not found. Install from https://git-scm.com"
}

# 4. Check Terraform
Write-Host "`nChecking Terraform..." -ForegroundColor Yellow
if (Test-Command terraform) {
    $tfVersion = terraform version -json | ConvertFrom-Json
    Write-Host "✓ Terraform $($tfVersion.terraform_version)" -ForegroundColor Green
} else {
    Write-Warning "Terraform not found. Install from https://terraform.io/downloads"
    
    if ($Force) {
        Write-Host "Attempting to install Terraform..." -ForegroundColor Yellow
        
        # Download Terraform
        $tfVersion = "1.5.0"
        $tfUrl = "https://releases.hashicorp.com/terraform/$tfVersion/terraform_${tfVersion}_windows_amd64.zip"
        $tfZip = "$env:TEMP\terraform.zip"
        $tfDir = "C:\terraform"
        
        try {
            Invoke-WebRequest -Uri $tfUrl -OutFile $tfZip
            
            if (-not (Test-Path $tfDir)) {
                New-Item -ItemType Directory -Path $tfDir -Force | Out-Null
            }
            
            Expand-Archive -Path $tfZip -DestinationPath $tfDir -Force
            Add-ToPath $tfDir
            
            Write-Host "✓ Terraform installed to $tfDir" -ForegroundColor Green
        } catch {
            Write-Error "Failed to install Terraform: $_"
        } finally {
            Remove-Item $tfZip -ErrorAction SilentlyContinue
        }
    }
}

# 5. Check Sublime Text
Write-Host "`nChecking Sublime Text..." -ForegroundColor Yellow
$sublimePaths = @(
    "${env:ProgramFiles}\Sublime Text\sublime_text.exe",
    "${env:ProgramFiles(x86)}\Sublime Text\sublime_text.exe",
    "${env:LocalAppData}\Programs\Sublime Text\sublime_text.exe"
)

$sublimeFound = $false
foreach ($path in $sublimePaths) {
    if (Test-Path $path) {
        Write-Host "✓ Sublime Text found at $path" -ForegroundColor Green
        $sublimeFound = $true
        break
    }
}

if (-not $sublimeFound) {
    Write-Error "Sublime Text not found. Install from https://sublimetext.com"
}

# 6. Find Packages directory
Write-Host "`nFinding Sublime Text Packages directory..." -ForegroundColor Yellow
$packagesDir = "$env:APPDATA\Sublime Text\Packages"
if (Test-Path $packagesDir) {
    Write-Host "✓ Packages directory: $packagesDir" -ForegroundColor Green
} else {
    Write-Error "Sublime Text Packages directory not found at $packagesDir"
}

# 7. Install test dependencies
if (-not $SkipDependencies) {
    Write-Host "`nInstalling test dependencies..." -ForegroundColor Yellow
    
    # Create virtual environment
    $venvPath = ".\venv"
    if (-not (Test-Path $venvPath)) {
        python -m venv $venvPath
        Write-Host "✓ Created virtual environment" -ForegroundColor Green
    }
    
    # Activate virtual environment
    & "$venvPath\Scripts\Activate.ps1"
    
    # Upgrade pip
    python -m pip install --upgrade pip
    
    # Install requirements
    if (Test-Path ".\Terraform\requirements-test.txt") {
        pip install -r ".\Terraform\requirements-test.txt"
        Write-Host "✓ Test dependencies installed" -ForegroundColor Green
    } else {
        Write-Warning "requirements-test.txt not found"
    }
}

# 8. Download terraform-ls
Write-Host "`nChecking terraform-ls..." -ForegroundColor Yellow
$terraformLsPath = ".\Terraform\bin\terraform-ls.exe"

if (-not (Test-Path $terraformLsPath)) {
    Write-Host "Downloading terraform-ls..." -ForegroundColor Yellow
    
    $lsVersion = "0.32.0"
    $lsUrl = "https://github.com/hashicorp/terraform-ls/releases/download/v$lsVersion/terraform-ls_${lsVersion}_windows_amd64.zip"
    $lsZip = "$env:TEMP\terraform-ls.zip"
    
    try {
        # Create bin directory
        $binDir = ".\Terraform\bin"
        if (-not (Test-Path $binDir)) {
            New-Item -ItemType Directory -Path $binDir -Force | Out-Null
        }
        
        # Download and extract
        Invoke-WebRequest -Uri $lsUrl -OutFile $lsZip
        Expand-Archive -Path $lsZip -DestinationPath $binDir -Force
        
        Write-Host "✓ terraform-ls downloaded" -ForegroundColor Green
    } catch {
        Write-Warning "Failed to download terraform-ls: $_"
    } finally {
        Remove-Item $lsZip -ErrorAction SilentlyContinue
    }
} else {
    Write-Host "✓ terraform-ls already installed" -ForegroundColor Green
}

# 9. Setup plugin
if ($DevMode) {
    Write-Host "`nSetting up development mode..." -ForegroundColor Yellow
    
    $pluginPath = "$packagesDir\Terraform"
    $currentPath = (Get-Location).Path + "\Terraform"
    
    if (Test-Path $pluginPath) {
        if ($Force) {
            Remove-Item $pluginPath -Recurse -Force
        } else {
            Write-Warning "Plugin directory already exists at $pluginPath"
            $response = Read-Host "Do you want to replace it? (y/n)"
            if ($response -ne 'y') {
                Write-Host "Skipping plugin setup" -ForegroundColor Yellow
                return
            }
            Remove-Item $pluginPath -Recurse -Force
        }
    }
    
    # Create symbolic link
    if ($isAdmin) {
        try {
            New-Item -ItemType SymbolicLink -Path $pluginPath -Target $currentPath -Force | Out-Null
            Write-Host "✓ Created symbolic link to development directory" -ForegroundColor Green
        } catch {
            Write-Error "Failed to create symbolic link: $_"
        }
    } else {
        Write-Warning "Administrator privileges required for symbolic link"
        Write-Host "Copying plugin files instead..." -ForegroundColor Yellow
        Copy-Item -Path $currentPath -Destination $pluginPath -Recurse -Force
        Write-Host "✓ Copied plugin files" -ForegroundColor Green
    }
}

# 10. Run tests
Write-Host "`nRunning tests..." -ForegroundColor Yellow
Push-Location ".\Terraform"
try {
    python tests\run_tests.py -v
    Write-Host "`n✓ Tests completed" -ForegroundColor Green
} catch {
    Write-Warning "Some tests failed: $_"
} finally {
    Pop-Location
}

# Summary
Write-Host "`n=============================================" -ForegroundColor Cyan
Write-Host "Setup Summary" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan

Write-Host "`nEnvironment:" -ForegroundColor Yellow
Write-Host "  Python: $((python --version 2>&1))" -ForegroundColor White
Write-Host "  Packages Dir: $packagesDir" -ForegroundColor White
Write-Host "  Plugin Path: $packagesDir\Terraform" -ForegroundColor White

Write-Host "`nNext Steps:" -ForegroundColor Yellow
Write-Host "  1. Open Sublime Text" -ForegroundColor White
Write-Host "  2. Install LSP package via Package Control" -ForegroundColor White
Write-Host "  3. Restart Sublime Text" -ForegroundColor White
Write-Host "  4. Open a .tf file to test" -ForegroundColor White

Write-Host "`nUseful Commands:" -ForegroundColor Yellow
Write-Host "  Run tests: python Terraform\tests\run_tests.py" -ForegroundColor White
Write-Host "  Run specific test: python Terraform\tests\run_tests.py test_plugin" -ForegroundColor White
Write-Host "  Run with coverage: cd Terraform\tests && coverage run -m pytest" -ForegroundColor White

Write-Host "`nSetup complete!" -ForegroundColor Green