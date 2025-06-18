# Windows Guide for Terraform Sublime Text Plugin

This guide provides step-by-step instructions for installing, testing, and using the Terraform plugin on Windows.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Development Setup](#development-setup)
3. [Installing the Plugin](#installing-the-plugin)
4. [Running Tests](#running-tests)
5. [Using the Plugin](#using-the-plugin)
6. [Troubleshooting](#troubleshooting)
7. [Windows-Specific Tips](#windows-specific-tips)

## Prerequisites

### 1. Install Python (3.8 or higher)

Download from [python.org](https://www.python.org/downloads/windows/)

```powershell
# Verify installation
python --version
# Should show: Python 3.8.x or higher

# Verify pip
pip --version
```

### 2. Install Sublime Text 4

Download from [sublimetext.com](https://www.sublimetext.com/)

- Default installation path: `C:\Program Files\Sublime Text`
- User packages path: `%APPDATA%\Sublime Text\Packages`

### 3. Install Terraform

Download from [terraform.io](https://www.terraform.io/downloads)

```powershell
# Option 1: Using Chocolatey
choco install terraform

# Option 2: Using Scoop
scoop install terraform

# Option 3: Manual installation
# 1. Download terraform_1.5.0_windows_amd64.zip
# 2. Extract to C:\terraform
# 3. Add C:\terraform to PATH

# Verify installation
terraform version
```

### 4. Install Git (for development)

Download from [git-scm.com](https://git-scm.com/download/win)

```powershell
# Verify installation
git --version
```

## Development Setup

### 1. Clone the Repository

```powershell
# Using Command Prompt or PowerShell
cd %USERPROFILE%\Documents
git clone https://github.com/yourusername/sublime-terraform.git
cd sublime-terraform
```

### 2. Create Virtual Environment (Recommended)

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
# PowerShell
.\venv\Scripts\Activate.ps1

# Command Prompt
venv\Scripts\activate.bat

# If you get execution policy error in PowerShell:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Install Test Dependencies

```powershell
# Make sure virtual environment is activated
pip install -r Terraform\requirements-test.txt
```

### 4. Setup Test Environment

```powershell
cd Terraform\tests
python setup_test_env.py

# This will:
# - Check Python version
# - Check Terraform installation
# - Install test dependencies
# - Create necessary directories
```

## Installing the Plugin

### Option 1: Development Installation (Recommended for Testing)

```powershell
# Find Sublime Text packages directory
echo %APPDATA%\Sublime Text\Packages

# Create symbolic link (Run as Administrator)
# PowerShell
New-Item -ItemType SymbolicLink -Path "$env:APPDATA\Sublime Text\Packages\Terraform" -Target "C:\path\to\sublime-terraform\Terraform"

# Or Command Prompt (Admin)
mklink /D "%APPDATA%\Sublime Text\Packages\Terraform" "C:\path\to\sublime-terraform\Terraform"
```

### Option 2: Manual Installation

```powershell
# Copy the plugin folder
xcopy /E /I "C:\path\to\sublime-terraform\Terraform" "%APPDATA%\Sublime Text\Packages\Terraform"
```

### Option 3: Package Installation

```powershell
# Build the package
cd sublime-terraform
python build_package.py

# Copy to Installed Packages
copy Terraform.sublime-package "%APPDATA%\Sublime Text\Installed Packages\"
```

### Install LSP Package (Required)

1. Open Sublime Text
2. Press `Ctrl+Shift+P` to open Command Palette
3. Type "Package Control: Install Package"
4. Search for "LSP" and install it
5. Restart Sublime Text

## Running Tests

### Using PowerShell

```powershell
# Navigate to project directory
cd C:\path\to\sublime-terraform\Terraform

# Run all tests
python tests\run_tests.py

# Run specific test file
python tests\run_tests.py test_plugin

# Run with verbose output
python tests\run_tests.py -v

# Run with coverage
cd tests
coverage run -m pytest
coverage report
coverage html
# Open htmlcov\index.html in browser
```

### Using Make (with Git Bash or WSL)

If you have Git Bash or WSL installed:

```bash
# In Git Bash
cd /c/path/to/sublime-terraform/Terraform
make test
make test-all
make coverage
```

### Using Batch Scripts

Create `test.bat` in project root:

```batch
@echo off
cd /d %~dp0\Terraform
python tests\run_tests.py %*
```

Then run:
```powershell
.\test.bat
.\test.bat -v
.\test.bat test_plugin
```

### Windows-Specific Test Commands

```powershell
# Run tests with Windows paths
python -m pytest tests\ -v

# Run specific test
python -m pytest tests\test_plugin.py::TestPlugin::test_plugin_loaded

# Run with debugging
python -m pytest tests\ -v -s --tb=short

# Performance tests
python tests\run_tests.py --performance

# Integration tests
python tests\run_tests.py --integration
```

## Using the Plugin

### 1. Verify Installation

1. Open Sublime Text
2. Open Console: `View → Show Console` (or `Ctrl+~`)
3. Check for errors
4. You should see: "Terraform plugin v1.0.0 loaded successfully"

### 2. Configure Settings

1. Open settings: `Preferences → Package Settings → Terraform → Settings`
2. Configure Windows paths:

```json
{
    "terraform_path": "C:\\terraform\\terraform.exe",
    "language_server": {
        "path": "C:\\Users\\YourName\\AppData\\Roaming\\Sublime Text\\Packages\\Terraform\\bin\\terraform-ls.exe"
    },
    "format_on_save": true
}
```

### 3. Create Test Project

```powershell
# Create test directory
mkdir C:\terraform-test
cd C:\terraform-test

# Create main.tf
echo resource "null_resource" "test" {} > main.tf
```

### 4. Test Features

1. **Open the file** in Sublime Text
2. **Auto-completion**: Type `resource "` and see suggestions
3. **Formatting**: Press `Ctrl+Shift+F` to format
4. **Commands**: Press `Ctrl+Shift+P` and type "Terraform" to see all commands
5. **Validation**: Save the file to trigger validation

### 5. Terraform Commands

Use Command Palette (`Ctrl+Shift+P`):

- `Terraform: Initialize` - Run terraform init
- `Terraform: Validate` - Validate configuration
- `Terraform: Plan` - Show execution plan
- `Terraform: Format Document` - Format current file

## Troubleshooting

### Common Windows Issues

#### 1. terraform-ls Not Found

```powershell
# The plugin will try to download it automatically
# If it fails, download manually:

# Download terraform-ls
Invoke-WebRequest -Uri "https://github.com/hashicorp/terraform-ls/releases/download/v0.32.0/terraform-ls_0.32.0_windows_amd64.zip" -OutFile terraform-ls.zip

# Extract
Expand-Archive terraform-ls.zip -DestinationPath .

# Copy to plugin directory
copy terraform-ls.exe "%APPDATA%\Sublime Text\Packages\Terraform\bin\"
```

#### 2. Permission Errors

Run PowerShell as Administrator for:
- Creating symbolic links
- Installing to Program Files
- Modifying PATH

#### 3. Path Issues

Windows uses backslashes, but in JSON settings, use double backslashes:
```json
{
    "terraform_path": "C:\\Program Files\\Terraform\\terraform.exe"
}
```

#### 4. Execution Policy

If PowerShell scripts are blocked:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### 5. Long Path Support

Enable long path support in Windows:
```powershell
# Run as Administrator
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```

### Debug Mode

Enable debug logging:

1. Open Sublime Text Console (`Ctrl+~`)
2. Enable debug mode:
```python
sublime.log_commands(True)
sublime.log_input(True)
```

### Check Installation

```python
# In Sublime Console
import sys
print(sys.path)

# Check if plugin loaded
sublime.run_command("terraform_init")
```

## Windows-Specific Tips

### 1. File Associations

Associate `.tf` files with Sublime Text:
```powershell
# Right-click on .tf file → Open with → Choose another app → Sublime Text
# Check "Always use this app"
```

### 2. Environment Variables

Add to PATH permanently:
```powershell
# User PATH
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\terraform", [EnvironmentVariableTarget]::User)

# System PATH (Admin required)
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\terraform", [EnvironmentVariableTarget]::Machine)
```

### 3. Windows Terminal Integration

Add Terraform profile to Windows Terminal:
```json
{
    "name": "Terraform",
    "commandline": "powershell.exe -NoExit -Command \"& {Set-Location 'C:\\terraform-projects'}\"",
    "icon": "🏗️"
}
```

### 4. PowerShell Aliases

Add to PowerShell profile:
```powershell
# Open profile
notepad $PROFILE

# Add aliases
Set-Alias tf terraform
Set-Alias tfi "terraform init"
Set-Alias tfp "terraform plan"
Set-Alias tfa "terraform apply"
```

### 5. Batch Scripts

Create helpful batch scripts:

`tf-test.bat`:
```batch
@echo off
cd /d %1
terraform init
terraform validate
terraform plan
```

## Performance Tips

1. **Exclude from Windows Defender**:
   - Add Sublime Text to exclusions
   - Add project directories to exclusions

2. **Disable Windows Search Indexing** for `.terraform` directories

3. **Use SSD** for Terraform projects

4. **Configure Git** for Windows:
   ```powershell
   git config --global core.autocrlf true
   git config --global core.longpaths true
   ```

## Next Steps

1. ✅ Run the test suite to verify everything works
2. ✅ Create a sample Terraform project
3. ✅ Test all plugin features
4. ✅ Report any Windows-specific issues

## Getting Help

- **Windows Issues**: Check Console output (`Ctrl+~`)
- **Path Problems**: Use forward slashes or double backslashes
- **Permission Issues**: Run as Administrator
- **Bug Reports**: Include Windows version and Sublime Text version

---

Happy Terraforming on Windows! 🚀🪟