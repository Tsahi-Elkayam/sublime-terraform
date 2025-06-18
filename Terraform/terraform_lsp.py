"""
Terraform Language Server Protocol (LSP) integration
Configures terraform-ls for use with the LSP package
"""

import os

import sublime
from LSP.plugin import AbstractPlugin, register_plugin, unregister_plugin
from LSP.plugin.core.typing import Any, Dict, List, Optional, Tuple


class TerraformLSPPlugin(AbstractPlugin):
    """LSP plugin configuration for terraform-ls"""

    @classmethod
    def name(cls) -> str:
        """The name of the plugin"""
        return "terraform-ls"

    @classmethod
    def configuration(cls) -> Tuple[sublime.Settings, str]:
        """Return the plugin configuration"""
        settings = sublime.load_settings("Terraform.sublime-settings")
        config_path = "${packages}/Terraform/terraform-ls.json"
        return (settings, config_path)

    @classmethod
    def can_start(
        cls,
        window: sublime.Window,
        initiating_view: sublime.View,
        workspace_folders: List[str],
        configuration: Dict,
    ) -> Optional[str]:
        """Determine if the server can start"""
        # Check if we have a Terraform file
        if not initiating_view:
            return None

        file_name = initiating_view.file_name()
        if not file_name:
            return None

        # Check file extension
        if not cls.is_terraform_file(file_name):
            return None

        # Check if terraform-ls exists
        server_path = cls.get_server_path(configuration)
        if not server_path or not os.path.exists(server_path):
            return "terraform-ls not found. Please install it or configure the path in settings."

        return None

    @classmethod
    def is_terraform_file(cls, file_name: str) -> bool:
        """Check if file is a Terraform file"""
        base_name = os.path.basename(file_name)
        return any(
            [
                base_name.endswith(".tf"),
                base_name.endswith(".tfvars"),
                base_name.endswith(".tfstack.hcl"),
                base_name.endswith(".tfdeploy.hcl"),
                base_name == "terraform.tfvars.json",
                base_name.endswith(".tf.json"),
            ]
        )

    @classmethod
    def get_server_path(cls, configuration: Dict) -> Optional[str]:
        """Get the path to terraform-ls binary"""
        # First check configuration
        server_path = configuration.get("command", [None])[0]
        if server_path and os.path.exists(server_path):
            return server_path

        # Check package bin directory
        package_dir = os.path.dirname(os.path.dirname(__file__))
        bin_dir = os.path.join(package_dir, "bin")

        if sublime.platform() == "windows":
            binary_name = "terraform-ls.exe"
        else:
            binary_name = "terraform-ls"

        local_path = os.path.join(bin_dir, binary_name)
        if os.path.exists(local_path):
            return local_path

        # Check PATH
        import shutil

        return shutil.which("terraform-ls")

    def on_pre_server_command(self, command: Dict[str, Any], done_callback) -> bool:
        """Hook to modify server commands before execution"""
        # We can intercept and modify commands here if needed
        done_callback(command)
        return True

    @classmethod
    def additional_variables(cls) -> Dict[str, str]:
        """Additional variables for configuration expansion"""
        return {
            "terraform_ls_version": "0.32.0",
            "platform": sublime.platform(),
            "arch": sublime.arch(),
        }

    @classmethod
    def get_initialize_params(
        cls, configuration: dict, workspace_folders: List[str]
    ) -> dict:
        """Get additional initialization parameters"""
        params = {
            "processId": os.getpid(),
            "clientInfo": {"name": "Sublime Text Terraform", "version": "1.0.0"},
            "trace": "off",
            "workspaceFolders": [
                {"uri": f"file://{folder}", "name": os.path.basename(folder)}
                for folder in workspace_folders
            ],
        }

        # Add experimental capabilities if enabled
        settings = sublime.load_settings("Terraform.sublime-settings")
        if settings.get("experimental_features.prefill_required_fields"):
            params["initializationOptions"] = {
                "experimentalFeatures": {"prefillRequiredFields": True}
            }

        return params


def plugin_loaded():
    """Register the plugin when loaded"""
    register_plugin(TerraformLSPPlugin)


def plugin_unloaded():
    """Unregister the plugin when unloaded"""
    unregister_plugin(TerraformLSPPlugin)


# Create the LSP configuration file content
LSP_CONFIG = {
    "enabled": True,
    "command": ["${terraform_ls_path}", "serve"],
    "languages": [
        {
            "languageId": "terraform",
            "scopes": ["source.terraform"],
            "syntaxes": [
                "Packages/Terraform/syntaxes/Terraform.sublime-syntax",
                "Packages/Terraform/syntaxes/TerraformVars.sublime-syntax",
            ],
        },
        {
            "languageId": "terraform-vars",
            "scopes": ["source.terraform.vars"],
            "syntaxes": ["Packages/Terraform/syntaxes/TerraformVars.sublime-syntax"],
        },
    ],
    "initializationOptions": {
        "indexing": {
            "ignorePaths": [],
            "ignoreDirectoryNames": [".terraform", "terraform.tfstate.d"],
        },
        "experimentalFeatures": {"prefillRequiredFields": True, "validateOnSave": True},
    },
    "settings": {
        "terraform-ls": {
            "rootModulePaths": [],
            "excludeModulePaths": [],
            "ignoreSingleFileWarning": False,
            "terraformExecPath": "terraform",
            "terraformExecTimeout": "30s",
            "terraformLogFilePath": "",
        }
    },
    "selector": "source.terraform | source.terraform.vars",
    "priority_selector": "source.terraform | source.terraform.vars",
}
