"""
Settings management for Terraform plugin
"""

import sublime
import os

class TerraformSettings:
    """Manages Terraform plugin settings"""
    
    SETTINGS_FILE = "Terraform.sublime-settings"
    
    def __init__(self):
        self.settings = None
        self.load_settings()
    
    def load_settings(self):
        """Load settings from file"""
        self.settings = sublime.load_settings(self.SETTINGS_FILE)
    
    def get(self, key, default=None):
        """Get a setting value"""
        if self.settings:
            return self.settings.get(key, default)
        return default
    
    def set(self, key, value):
        """Set a setting value"""
        if self.settings:
            self.settings.set(key, value)
            sublime.save_settings(self.SETTINGS_FILE)
    
    def add_on_change(self, key, callback):
        """Add a callback for when a setting changes"""
        if self.settings:
            self.settings.add_on_change(key, callback)
    
    def clear_on_change(self, key):
        """Remove a callback for a setting"""
        if self.settings:
            self.settings.clear_on_change(key)

# Global settings instance
_settings = None

def get_settings():
    """Get the global settings instance"""
    global _settings
    if _settings is None:
        _settings = TerraformSettings()
    return _settings

# Default settings content
DEFAULT_SETTINGS = {
    "terraform_path": "terraform",
    
    "language_server": {
        "enabled": True,
        "path": "",  # Auto-detected if empty
        "args": ["serve"],
        "log_file": "",
        "log_level": "info"
    },
    
    "format_on_save": True,
    "validate_on_save": False,
    
    "experimental_features": {
        "prefill_required_fields": True,
        "validate_on_save": False
    },
    
    "root_modules": [],
    "exclude_root_modules": [],
    
    "ignore_directory_names": [
        ".terraform",
        "terraform.tfstate.d",
        ".terragrunt-cache"
    ],
    
    "terraform_cloud": {
        "organization": "",
        "token": ""  # Store in secure storage instead
    },
    
    "code_lens": {
        "reference_count": False  # Can impact performance
    },
    
    "module_explorer": {
        "show_providers": True,
        "show_modules": True,
        "show_resources": False
    },
    
    "completion": {
        "trigger_characters": [".", "[", "(", ",", " "],
        "complete_required_fields": True
    },
    
    "diagnostics": {
        "enable_terraform_validate": True,
        "validate_on_open": False,
        "validate_on_change": True
    }
}

def create_default_settings():
    """Create default settings file"""
    settings = sublime.load_settings(TerraformSettings.SETTINGS_FILE)
    
    # Only set defaults if they don't exist
    for key, value in DEFAULT_SETTINGS.items():
        if settings.get(key) is None:
            settings.set(key, value)
    
    sublime.save_settings(TerraformSettings.SETTINGS_FILE)