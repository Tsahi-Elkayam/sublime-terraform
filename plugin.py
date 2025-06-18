"""
Terraform Plugin for Sublime Text 4
Main entry point and plugin initialization
"""

import os
import sublime
import sublime_plugin
from .terraform_lsp import TerraformLSPPlugin
from .terraform_commands import (
    TerraformInitCommand,
    TerraformValidateCommand,
    TerraformPlanCommand,
    TerraformApplyCommand,
    TerraformFormatCommand,
    TerraformFormatOnSaveListener
)
from .terraform_module_explorer import (
    TerraformShowModulesCommand,
    TerraformShowProvidersCommand,
    TerraformModuleExplorerListener
)
from .terraform_cloud import (
    TerraformCloudLoginCommand,
    TerraformCloudShowWorkspacesCommand,
    TerraformCloudShowRunsCommand
)
from .terraform_project import TerraformProjectDetector
from .terraform_settings import TerraformSettings

# Plugin version
__version__ = "1.0.0"

# Global settings instance
settings = None

def plugin_loaded():
    """Called when the plugin is loaded"""
    global settings
    
    # Initialize settings
    settings = TerraformSettings()
    
    # Check for required dependencies
    check_dependencies()
    
    # Initialize project detector
    TerraformProjectDetector.initialize()
    
    # Setup terraform-ls if needed
    setup_language_server()
    
    print(f"Terraform plugin v{__version__} loaded successfully")

def plugin_unloaded():
    """Called when the plugin is about to be unloaded"""
    # Cleanup any resources
    TerraformProjectDetector.cleanup()
    print("Terraform plugin unloaded")

def check_dependencies():
    """Check for required dependencies"""
    # Check if LSP package is installed
    try:
        import LSP
    except ImportError:
        sublime.error_message(
            "Terraform Plugin Error:\n\n"
            "The LSP package is required but not installed.\n"
            "Please install it via Package Control."
        )
        return False
    
    # Check for terraform binary
    terraform_path = settings.get("terraform_path", "terraform")
    if not check_terraform_binary(terraform_path):
        sublime.error_message(
            "Terraform Plugin Warning:\n\n"
            "Terraform binary not found in PATH.\n"
            "Some features will be disabled.\n"
            "Please install Terraform or configure the path in settings."
        )
    
    return True

def check_terraform_binary(terraform_path):
    """Check if terraform binary exists and is executable"""
    import subprocess
    try:
        subprocess.run(
            [terraform_path, "version"],
            capture_output=True,
            check=False
        )
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

def setup_language_server():
    """Setup terraform-ls language server"""
    ls_path = settings.get("language_server.path")
    
    if not ls_path:
        # Try to auto-download terraform-ls
        ls_path = download_terraform_ls()
        if ls_path:
            settings.set("language_server.path", ls_path)
    
    if ls_path and os.path.exists(ls_path):
        print(f"Using terraform-ls at: {ls_path}")
    else:
        print("terraform-ls not found, LSP features will be limited")

def download_terraform_ls():
    """Download terraform-ls binary if not present"""
    import platform
    import urllib.request
    import zipfile
    import tarfile
    import tempfile
    
    # Determine platform
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    if system == "windows":
        file_ext = "zip"
        binary_name = "terraform-ls.exe"
    else:
        file_ext = "tar.gz"
        binary_name = "terraform-ls"
    
    # Construct download URL
    version = "0.32.0"  # Latest stable version
    arch_map = {
        "x86_64": "amd64",
        "amd64": "amd64",
        "aarch64": "arm64",
        "arm64": "arm64"
    }
    arch = arch_map.get(machine, "amd64")
    
    url = f"https://github.com/hashicorp/terraform-ls/releases/download/v{version}/terraform-ls_{version}_{system}_{arch}.{file_ext}"
    
    try:
        # Download to temp directory
        with tempfile.TemporaryDirectory() as tmpdir:
            download_path = os.path.join(tmpdir, f"terraform-ls.{file_ext}")
            
            print(f"Downloading terraform-ls from {url}")
            urllib.request.urlretrieve(url, download_path)
            
            # Extract
            if file_ext == "zip":
                with zipfile.ZipFile(download_path, 'r') as zf:
                    zf.extractall(tmpdir)
            else:
                with tarfile.open(download_path, 'r:gz') as tf:
                    tf.extractall(tmpdir)
            
            # Move to package directory
            package_dir = os.path.dirname(__file__)
            bin_dir = os.path.join(package_dir, "bin")
            os.makedirs(bin_dir, exist_ok=True)
            
            src_path = os.path.join(tmpdir, binary_name)
            dst_path = os.path.join(bin_dir, binary_name)
            
            if os.path.exists(src_path):
                import shutil
                shutil.move(src_path, dst_path)
                
                # Make executable on Unix
                if system != "windows":
                    os.chmod(dst_path, 0o755)
                
                return dst_path
    
    except Exception as e:
        print(f"Failed to download terraform-ls: {e}")
        return None

class TerraformEventListener(sublime_plugin.EventListener):
    """Global event listener for Terraform files"""
    
    def on_activated_async(self, view):
        """Called when a view gains focus"""
        if self.is_terraform_file(view):
            # Update project context
            TerraformProjectDetector.detect_project(view)
    
    def on_load_async(self, view):
        """Called when a file is loaded"""
        if self.is_terraform_file(view):
            # Apply any Terraform-specific settings
            self.apply_terraform_settings(view)
    
    def on_hover(self, view, point, hover_zone):
        """Handle hover events for documentation"""
        if not self.is_terraform_file(view):
            return
        
        # This will be handled by LSP, but we can add custom hover info here
        pass
    
    def is_terraform_file(self, view):
        """Check if the view is a Terraform file"""
        if not view.file_name():
            return False
        
        name = os.path.basename(view.file_name())
        return (
            name.endswith('.tf') or 
            name.endswith('.tfvars') or
            name.endswith('.tfstack.hcl') or
            name.endswith('.tfdeploy.hcl')
        )
    
    def apply_terraform_settings(self, view):
        """Apply Terraform-specific view settings"""
        view.settings().set('word_wrap', False)
        view.settings().set('tab_size', 2)
        view.settings().set('translate_tabs_to_spaces', True)