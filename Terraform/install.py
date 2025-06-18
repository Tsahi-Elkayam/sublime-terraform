#!/usr/bin/env python3
"""
Installation helper script for Terraform Sublime Text plugin
This script helps with initial setup and dependency checking
"""

import json
import os
import platform
import shutil
import subprocess
import sys
import urllib.request


def check_sublime_version():
    """Check if Sublime Text 4 is installed"""
    print("🔍 Checking Sublime Text version...")
    # This check would need to be done from within Sublime
    print("✓ Please ensure you have Sublime Text 4 (Build 4000+)")


def check_terraform():
    """Check if Terraform is installed"""
    print("\n🔍 Checking Terraform installation...")
    try:
        result = subprocess.run(
            ["terraform", "version"], capture_output=True, text=True
        )
        if result.returncode == 0:
            print(f"✓ Terraform found: {result.stdout.split()[1]}")
            return True
    except FileNotFoundError:
        pass

    print("❌ Terraform not found in PATH")
    print("   Please install from: https://www.terraform.io/downloads")
    return False


def check_lsp_package():
    """Check if LSP package is installed"""
    print("\n🔍 Checking LSP package...")
    packages_path = get_packages_path()
    lsp_path = os.path.join(packages_path, "LSP")

    if os.path.exists(lsp_path):
        print("✓ LSP package found")
        return True

    print("❌ LSP package not found")
    print("   Please install via Package Control:")
    print("   1. Ctrl/Cmd + Shift + P")
    print("   2. Package Control: Install Package")
    print("   3. Search for 'LSP'")
    return False


def get_packages_path():
    """Get Sublime Text packages directory"""
    system = platform.system()
    home = os.path.expanduser("~")

    if system == "Darwin":  # macOS
        return os.path.join(home, "Library/Application Support/Sublime Text/Packages")
    elif system == "Linux":
        return os.path.join(home, ".config/sublime-text/Packages")
    elif system == "Windows":
        return os.path.join(os.environ["APPDATA"], "Sublime Text", "Packages")
    else:
        raise Exception(f"Unsupported platform: {system}")


def download_terraform_ls():
    """Download terraform-ls binary"""
    print("\n🔍 Checking terraform-ls...")

    # Check if already exists
    bin_dir = os.path.join(os.path.dirname(__file__), "bin")

    system = platform.system().lower()
    if system == "windows":
        binary_name = "terraform-ls.exe"
    else:
        binary_name = "terraform-ls"

    binary_path = os.path.join(bin_dir, binary_name)

    if os.path.exists(binary_path):
        print("✓ terraform-ls already installed")
        return True

    print("📥 Downloading terraform-ls...")

    # Create bin directory
    os.makedirs(bin_dir, exist_ok=True)

    # Download URL
    version = "0.32.0"
    arch_map = {
        "x86_64": "amd64",
        "amd64": "amd64",
        "aarch64": "arm64",
        "arm64": "arm64",
    }
    machine = platform.machine().lower()
    arch = arch_map.get(machine, "amd64")

    if system == "windows":
        file_ext = "zip"
    else:
        file_ext = "tar.gz"

    url = f"https://github.com/hashicorp/terraform-ls/releases/download/v{version}/terraform-ls_{version}_{system}_{arch}.{file_ext}"

    try:
        # Download
        print(f"   URL: {url}")
        urllib.request.urlretrieve(url, f"terraform-ls.{file_ext}")

        # Extract
        if file_ext == "zip":
            import zipfile

            with zipfile.ZipFile(f"terraform-ls.{file_ext}", "r") as zf:
                zf.extractall(bin_dir)
        else:
            import tarfile

            with tarfile.open(f"terraform-ls.{file_ext}", "r:gz") as tf:
                tf.extractall(bin_dir)

        # Clean up
        os.remove(f"terraform-ls.{file_ext}")

        # Make executable on Unix
        if system != "windows":
            os.chmod(binary_path, 0o755)

        print("✓ terraform-ls downloaded successfully")
        return True

    except Exception as e:
        print(f"❌ Failed to download terraform-ls: {e}")
        print("   You can download manually from:")
        print("   https://github.com/hashicorp/terraform-ls/releases")
        return False


def create_initial_settings():
    """Create initial settings if they don't exist"""
    print("\n🔍 Checking settings...")

    packages_path = get_packages_path()
    user_path = os.path.join(packages_path, "User")
    settings_file = os.path.join(user_path, "Terraform.sublime-settings")

    if os.path.exists(settings_file):
        print("✓ Settings file exists")
        return

    print("📝 Creating default settings...")
    os.makedirs(user_path, exist_ok=True)

    default_settings = {
        "terraform_path": "terraform",
        "format_on_save": True,
        "language_server": {"enabled": True},
    }

    with open(settings_file, "w") as f:
        json.dump(default_settings, f, indent=4)

    print("✓ Default settings created")


def main():
    """Main installation helper"""
    print("🚀 Terraform Sublime Text Plugin Setup")
    print("=" * 50)

    # Run checks
    check_sublime_version()
    terraform_ok = check_terraform()
    lsp_ok = check_lsp_package()
    terraform_ls_ok = download_terraform_ls()
    create_initial_settings()

    # Summary
    print("\n" + "=" * 50)
    print("📋 Setup Summary:")
    print(f"   Terraform: {'✓' if terraform_ok else '❌'}")
    print(f"   LSP Package: {'✓' if lsp_ok else '❌'}")
    print(f"   terraform-ls: {'✓' if terraform_ls_ok else '❌'}")

    if terraform_ok and lsp_ok and terraform_ls_ok:
        print("\n✅ Setup complete! Restart Sublime Text to activate the plugin.")
    else:
        print("\n⚠️  Some components are missing. Please install them manually.")

    print("\n📖 For more information, see README.md")


if __name__ == "__main__":
    main()
