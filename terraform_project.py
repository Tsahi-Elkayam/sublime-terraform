"""
Terraform project detection and management
Detects root modules and manages project context
"""

import os
import glob
import json
import sublime
from .terraform_settings import get_settings

class TerraformProject:
    """Represents a Terraform project/root module"""
    
    def __init__(self, root_path):
        self.root_path = root_path
        self.name = os.path.basename(root_path)
        self.modules = []
        self.providers = []
        self.backend = None
        self.terraform_version = None
        
        self._analyze_project()
    
    def _analyze_project(self):
        """Analyze the project structure"""
        # Check for terraform files
        tf_files = glob.glob(os.path.join(self.root_path, "*.tf"))
        
        # Check for terraform.tfstate
        state_file = os.path.join(self.root_path, "terraform.tfstate")
        if os.path.exists(state_file):
            self._parse_state_file(state_file)
        
        # Check for .terraform directory
        terraform_dir = os.path.join(self.root_path, ".terraform")
        if os.path.exists(terraform_dir):
            self._analyze_terraform_dir(terraform_dir)
        
        # Parse main configuration
        for tf_file in tf_files:
            self._parse_tf_file(tf_file)
    
    def _parse_state_file(self, state_file):
        """Parse terraform.tfstate for project info"""
        try:
            with open(state_file, 'r') as f:
                state = json.load(f)
                self.terraform_version = state.get("terraform_version")
        except (json.JSONDecodeError, IOError):
            pass
    
    def _analyze_terraform_dir(self, terraform_dir):
        """Analyze .terraform directory"""
        # Check for modules
        modules_dir = os.path.join(terraform_dir, "modules")
        if os.path.exists(modules_dir):
            modules_json = os.path.join(modules_dir, "modules.json")
            if os.path.exists(modules_json):
                try:
                    with open(modules_json, 'r') as f:
                        data = json.load(f)
                        self.modules = data.get("Modules", [])
                except (json.JSONDecodeError, IOError):
                    pass
    
    def _parse_tf_file(self, tf_file):
        """Parse a .tf file for configuration"""
        # This is a simplified parser
        # In a real implementation, we'd use HCL parser
        try:
            with open(tf_file, 'r') as f:
                content = f.read()
                
                # Look for terraform block
                if "terraform {" in content:
                    # Extract required_version
                    import re
                    version_match = re.search(r'required_version\s*=\s*"([^"]+)"', content)
                    if version_match:
                        self.terraform_version = version_match.group(1)
                    
                    # Extract backend
                    backend_match = re.search(r'backend\s+"([^"]+)"', content)
                    if backend_match:
                        self.backend = backend_match.group(1)
        except IOError:
            pass
    
    def is_initialized(self):
        """Check if project is initialized (has .terraform directory)"""
        return os.path.exists(os.path.join(self.root_path, ".terraform"))
    
    def get_info(self):
        """Get project information summary"""
        return {
            "name": self.name,
            "path": self.root_path,
            "initialized": self.is_initialized(),
            "terraform_version": self.terraform_version,
            "backend": self.backend,
            "module_count": len(self.modules)
        }

class TerraformProjectDetector:
    """Detects and manages Terraform projects in workspace"""
    
    _instance = None
    _projects = {}
    
    @classmethod
    def initialize(cls):
        """Initialize the project detector"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    @classmethod
    def cleanup(cls):
        """Cleanup resources"""
        cls._projects.clear()
        cls._instance = None
    
    @classmethod
    def detect_project(cls, view):
        """Detect project for a given view"""
        if not view or not view.file_name():
            return None
        
        file_path = view.file_name()
        
        # Check if we already know about this project
        for root_path, project in cls._projects.items():
            if file_path.startswith(root_path):
                return project
        
        # Find project root
        root_path = cls._find_project_root(file_path)
        if root_path:
            # Create project instance
            project = TerraformProject(root_path)
            cls._projects[root_path] = project
            return project
        
        return None
    
    @classmethod
    def _find_project_root(cls, file_path):
        """Find the root of a Terraform project"""
        current_dir = os.path.dirname(file_path)
        
        # Check configured root modules first
        settings = get_settings()
        root_modules = settings.get("root_modules", [])
        
        for root_module in root_modules:
            if file_path.startswith(root_module):
                return root_module
        
        # Walk up directory tree looking for indicators
        while current_dir != os.path.dirname(current_dir):  # Not at root
            # Check for root module indicators
            if cls._is_root_module(current_dir):
                return current_dir
            
            # Check exclusions
            exclude_patterns = settings.get("exclude_root_modules", [])
            if any(current_dir.endswith(pattern) for pattern in exclude_patterns):
                current_dir = os.path.dirname(current_dir)
                continue
            
            current_dir = os.path.dirname(current_dir)
        
        # Default to file directory
        return os.path.dirname(file_path)
    
    @classmethod
    def _is_root_module(cls, directory):
        """Check if directory is a root module"""
        indicators = [
            ".terraform",
            "terraform.tfstate",
            ".terraform.lock.hcl",
            "terragrunt.hcl"
        ]
        
        for indicator in indicators:
            if os.path.exists(os.path.join(directory, indicator)):
                return True
        
        # Check for backend configuration
        tf_files = glob.glob(os.path.join(directory, "*.tf"))
        for tf_file in tf_files:
            try:
                with open(tf_file, 'r') as f:
                    content = f.read()
                    if "backend" in content and "terraform {" in content:
                        return True
            except IOError:
                continue
        
        return False
    
    @classmethod
    def get_all_projects(cls):
        """Get all detected projects"""
        return list(cls._projects.values())
    
    @classmethod
    def refresh_projects(cls, window):
        """Refresh all projects in window folders"""
        cls._projects.clear()
        
        for folder in window.folders():
            # Walk directory tree
            for root, dirs, files in os.walk(folder):
                # Skip ignored directories
                settings = get_settings()
                ignore_dirs = settings.get("ignore_directory_names", [])
                dirs[:] = [d for d in dirs if d not in ignore_dirs]
                
                # Check if this is a root module
                if any(f.endswith('.tf') for f in files):
                    if cls._is_root_module(root):
                        project = TerraformProject(root)
                        cls._projects[root] = project

class TerraformProjectStatusCommand(sublime_plugin.WindowCommand):
    """Show current project status"""
    
    def run(self):
        view = self.window.active_view()
        if not view:
            return
        
        project = TerraformProjectDetector.detect_project(view)
        if not project:
            sublime.status_message("No Terraform project detected")
            return
        
        info = project.get_info()
        
        status_lines = [
            f"Project: {info['name']}",
            f"Path: {info['path']}",
            f"Initialized: {'Yes' if info['initialized'] else 'No'}",
        ]
        
        if info['terraform_version']:
            status_lines.append(f"Terraform Version: {info['terraform_version']}")
        
        if info['backend']:
            status_lines.append(f"Backend: {info['backend']}")
        
        status_lines.append(f"Modules: {info['module_count']}")
        
        # Show in quick panel
        self.window.show_quick_panel(
            [[line] for line in status_lines],
            lambda idx: None,
            sublime.MONOSPACE_FONT
        )

class TerraformProjectRefreshCommand(sublime_plugin.WindowCommand):
    """Refresh Terraform projects in workspace"""
    
    def run(self):
        TerraformProjectDetector.refresh_projects(self.window)
        projects = TerraformProjectDetector.get_all_projects()
        
        if projects:
            sublime.status_message(f"Found {len(projects)} Terraform project(s)")
        else:
            sublime.status_message("No Terraform projects found")

class TerraformProjectSwitchCommand(sublime_plugin.WindowCommand):
    """Switch between Terraform projects"""
    
    def run(self):
        projects = TerraformProjectDetector.get_all_projects()
        
        if not projects:
            sublime.status_message("No Terraform projects found")
            return
        
        items = []
        for project in projects:
            info = project.get_info()
            status = "✓" if info['initialized'] else "✗"
            items.append([
                f"{status} {info['name']}",
                info['path']
            ])
        
        self.window.show_quick_panel(
            items,
            lambda idx: self.on_project_selected(idx, projects),
            placeholder="Select project to open"
        )
    
    def on_project_selected(self, index, projects):
        """Handle project selection"""
        if index < 0:
            return
        
        project = projects[index]
        
        # Open a file from the project
        tf_files = glob.glob(os.path.join(project.root_path, "*.tf"))
        if tf_files:
            self.window.open_file(tf_files[0])
        else:
            # Just open the folder
            self.window.run_command("prompt_open_folder")