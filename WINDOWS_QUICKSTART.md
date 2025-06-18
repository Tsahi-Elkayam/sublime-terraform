# 🚀 Windows Quick Start Guide

Get the Terraform Sublime Text plugin running on Windows in 5 minutes!

## 📋 Prerequisites Checklist

- [ ] Windows 10/11
- [ ] Python 3.8+ ([Download](https://python.org))
- [ ] Sublime Text 4 ([Download](https://sublimetext.com))
- [ ] Git ([Download](https://git-scm.com))
- [ ] Terraform ([Download](https://terraform.io/downloads))

## 🏃 Quick Install (5 minutes)

### 1️⃣ Clone and Setup (PowerShell)

```powershell
# Clone the repository
cd $HOME\Documents
git clone https://github.com/yourusername/sublime-terraform.git
cd sublime-terraform

# Run automated setup
.\Terraform\scripts\windows-setup.ps1 -DevMode
```

### 2️⃣ Install LSP Package

1. Open Sublime Text
2. Press `Ctrl+Shift+P`
3. Type "Install Package"
4. Search for "LSP" and install
5. Restart Sublime Text

### 3️⃣ Test the Plugin

Create `test.tf`:
```hcl
resource "aws_instance" "test" {
  ami = "ami-12345"
}
```

Open in Sublime Text and:
- Type `resource "` - see auto-completion!
- Press `Ctrl+Shift+F` - format the file!
- Press `Ctrl+Shift+P`, type "Terraform" - see all commands!

## 🧪 Run Tests (2 minutes)

### Option 1: Simple Test

```cmd
cd sublime-terraform\Terraform
test.bat
```

### Option 2: Interactive Menu

```cmd
cd sublime-terraform\Terraform\scripts
test-windows.bat
```

### Option 3: PowerShell

```powershell
cd sublime-terraform\Terraform
python tests\run_tests.py -v
```

## 📁 Important Paths

| Item | Path |
|------|------|
| Sublime Packages | `%APPDATA%\Sublime Text\Packages` |
| Plugin Location | `%APPDATA%\Sublime Text\Packages\Terraform` |
| Settings File | `%APPDATA%\Sublime Text\Packages\User\Terraform.sublime-settings` |

## ⚙️ Quick Settings

`Preferences → Package Settings → Terraform → Settings`:

```json
{
    "terraform_path": "terraform",
    "format_on_save": true,
    "language_server": {
        "enabled": true
    }
}
```

## 🔑 Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Format | `Ctrl+Shift+F` |
| Command Palette | `Ctrl+Shift+P` |
| Go to Definition | `F12` |
| Find References | `Shift+F12` |
| Show Modules | `Ctrl+Shift+M` |

## 🆘 Quick Fixes

### terraform-ls not found?
```powershell
# Download manually
cd sublime-terraform\Terraform
Invoke-WebRequest -Uri "https://github.com/hashicorp/terraform-ls/releases/download/v0.32.0/terraform-ls_0.32.0_windows_amd64.zip" -OutFile terraform-ls.zip
Expand-Archive terraform-ls.zip -DestinationPath bin\
del terraform-ls.zip
```

### Permission denied?
Run PowerShell as Administrator

### Path issues?
Use double backslashes in JSON: `"C:\\terraform\\terraform.exe"`

## ✅ Verify Everything Works

1. **Check Console**: `View → Show Console` (no errors)
2. **Test Completion**: Type `resource "` in a .tf file
3. **Test Formatting**: Press `Ctrl+Shift+F`
4. **Test Commands**: `Ctrl+Shift+P` → "Terraform: Validate"

## 📚 Next Steps

- Read [Full Windows Guide](WINDOWS_GUIDE.md)
- Run complete test suite
- Explore all features
- Report Windows-specific issues

---

**Need help?** Open an issue with:
- Windows version (`winver`)
- Python version (`python --version`)
- Error messages from Console (`Ctrl+~`)

Happy Terraforming on Windows! 🎉🪟