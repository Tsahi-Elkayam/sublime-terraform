"""
Terraform command integration for Sublime Text
Provides commands for init, plan, apply, validate, and format
"""

import json
import os
import subprocess
import threading

import sublime
import sublime_plugin

from .terraform_settings import get_settings


class TerraformCommand(sublime_plugin.WindowCommand):
    """Base class for Terraform commands"""

    def get_terraform_path(self):
        """Get the path to terraform binary"""
        return get_settings().get("terraform_path", "terraform")

    def get_working_dir(self):
        """Get the working directory for terraform commands"""
        view = self.window.active_view()
        if view and view.file_name():
            return os.path.dirname(view.file_name())

        # Fall back to project folder
        folders = self.window.folders()
        if folders:
            return folders[0]

        return None

    def run_terraform_command(self, args, working_dir=None, callback=None):
        """Run a terraform command asynchronously"""
        if not working_dir:
            working_dir = self.get_working_dir()

        if not working_dir:
            sublime.error_message("No Terraform project found")
            return

        # Create output panel
        panel = self.window.create_output_panel("terraform")
        self.window.run_command("show_panel", {"panel": "output.terraform"})

        # Build command
        terraform_path = self.get_terraform_path()
        cmd = [terraform_path] + args

        # Run in thread
        thread = threading.Thread(
            target=self._run_command_thread, args=(cmd, working_dir, panel, callback)
        )
        thread.start()

    def _run_command_thread(self, cmd, working_dir, panel, callback):
        """Run command in a separate thread"""
        try:
            # Update panel with command
            panel.run_command(
                "append",
                {
                    "characters": f"Running: {' '.join(cmd)}\n",
                    "force": True,
                    "scroll_to_end": True,
                },
            )

            # Set up environment
            env = os.environ.copy()
            env["TF_IN_AUTOMATION"] = "1"  # Disable interactive prompts

            # Run the command
            process = subprocess.Popen(
                cmd,
                cwd=working_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                env=env,
                universal_newlines=True,
            )

            # Stream output
            for line in process.stdout:
                panel.run_command(
                    "append", {"characters": line, "force": True, "scroll_to_end": True}
                )

            process.wait()

            # Show completion status
            if process.returncode == 0:
                panel.run_command(
                    "append",
                    {
                        "characters": "\n✓ Command completed successfully\n",
                        "force": True,
                        "scroll_to_end": True,
                    },
                )
            else:
                panel.run_command(
                    "append",
                    {
                        "characters": f"\n✗ Command failed with exit code {process.returncode}\n",
                        "force": True,
                        "scroll_to_end": True,
                    },
                )

            # Call callback if provided
            if callback:
                sublime.set_timeout(lambda: callback(process.returncode == 0), 0)

        except Exception as e:
            panel.run_command(
                "append",
                {
                    "characters": f"\n✗ Error: {str(e)}\n",
                    "force": True,
                    "scroll_to_end": True,
                },
            )


class TerraformInitCommand(TerraformCommand):
    """Run terraform init"""

    def run(self):
        self.run_terraform_command(["init"])

    def is_enabled(self):
        return self.get_working_dir() is not None


class TerraformInitCurrentFolderCommand(TerraformCommand):
    """Run terraform init in the current file's folder"""

    def run(self):
        view = self.window.active_view()
        if view and view.file_name():
            working_dir = os.path.dirname(view.file_name())
            self.run_terraform_command(["init"], working_dir)

    def is_enabled(self):
        view = self.window.active_view()
        return view and view.file_name() and view.file_name().endswith(".tf")


class TerraformValidateCommand(TerraformCommand):
    """Run terraform validate"""

    def run(self):
        self.run_terraform_command(
            ["validate", "-json"], callback=self.handle_validate_result
        )

    def handle_validate_result(self, success):
        """Handle validation results"""
        if success:
            sublime.status_message("✓ Terraform configuration is valid")
        else:
            self.window.run_command("show_panel", {"panel": "output.terraform"})


class TerraformPlanCommand(TerraformCommand):
    """Run terraform plan"""

    def run(self):
        self.run_terraform_command(["plan", "-no-color"])


class TerraformApplyCommand(TerraformCommand):
    """Run terraform apply"""

    def run(self):
        # Ask for confirmation
        if sublime.ok_cancel_dialog("Are you sure you want to apply changes?", "Apply"):
            self.run_terraform_command(["apply", "-auto-approve", "-no-color"])


class TerraformDestroyCommand(TerraformCommand):
    """Run terraform destroy"""

    def run(self):
        # Ask for confirmation with strong warning
        message = (
            "⚠️ WARNING: This will DESTROY all resources!\n\n"
            "Are you absolutely sure you want to continue?"
        )
        if sublime.ok_cancel_dialog(message, "DESTROY"):
            self.run_terraform_command(["destroy", "-auto-approve", "-no-color"])


class TerraformFormatCommand(sublime_plugin.TextCommand):
    """Format current file with terraform fmt"""

    def run(self, edit):
        if not self.view.file_name():
            return

        # Save current position
        selections = list(self.view.sel())
        viewport_position = self.view.viewport_position()

        # Get terraform path
        terraform_path = get_settings().get("terraform_path", "terraform")

        # Run terraform fmt
        try:
            result = subprocess.run(
                [terraform_path, "fmt", "-"],
                input=self.view.substr(sublime.Region(0, self.view.size())),
                capture_output=True,
                text=True,
                check=True,
            )

            # Replace content
            formatted_content = result.stdout
            if formatted_content != self.view.substr(
                sublime.Region(0, self.view.size())
            ):
                self.view.replace(
                    edit, sublime.Region(0, self.view.size()), formatted_content
                )

                # Restore position
                self.view.sel().clear()
                for sel in selections:
                    self.view.sel().add(sel)
                self.view.set_viewport_position(viewport_position, False)

                sublime.status_message("✓ Formatted with terraform fmt")

        except subprocess.CalledProcessError as e:
            sublime.error_message(f"terraform fmt failed: {e.stderr}")
        except FileNotFoundError:
            sublime.error_message("terraform binary not found")

    def is_enabled(self):
        return self.view.file_name() and (
            self.view.file_name().endswith(".tf")
            or self.view.file_name().endswith(".tfvars")
        )


class TerraformFormatOnSaveListener(sublime_plugin.EventListener):
    """Format Terraform files on save if enabled"""

    def on_pre_save(self, view):
        if not self.should_format(view):
            return

        # Check if format on save is enabled
        settings = get_settings()
        if not settings.get("format_on_save", False):
            return

        # Run format command
        view.run_command("terraform_format")

    def should_format(self, view):
        """Check if view should be formatted"""
        if not view.file_name():
            return False

        return view.file_name().endswith(".tf") or view.file_name().endswith(".tfvars")


class TerraformOutputCommand(TerraformCommand):
    """Show terraform outputs"""

    def run(self):
        self.run_terraform_command(["output", "-json"], callback=self.show_outputs)

    def show_outputs(self, success):
        """Display outputs in a quick panel"""
        if not success:
            return

        # Parse output from panel
        panel = self.window.find_output_panel("terraform")
        if not panel:
            return

        content = panel.substr(sublime.Region(0, panel.size()))

        # Find JSON output
        try:
            # Extract JSON from output
            import re

            json_match = re.search(r"\{[\s\S]*\}", content)
            if not json_match:
                return

            outputs = json.loads(json_match.group())

            # Format for quick panel
            items = []
            for name, data in outputs.items():
                value = data.get("value", "")
                sensitive = data.get("sensitive", False)

                if sensitive:
                    value_display = "<sensitive>"
                else:
                    value_display = str(value)[:100]  # Truncate long values

                items.append([name, value_display])

            if items:
                self.window.show_quick_panel(
                    items,
                    lambda idx: (
                        self.copy_output(list(outputs.keys())[idx], outputs)
                        if idx >= 0
                        else None
                    ),
                )
            else:
                sublime.status_message("No outputs found")

        except json.JSONDecodeError:
            sublime.error_message("Failed to parse terraform outputs")

    def copy_output(self, name, outputs):
        """Copy output value to clipboard"""
        value = outputs[name].get("value", "")
        sublime.set_clipboard(str(value))
        sublime.status_message(f"Copied output '{name}' to clipboard")


class TerraformRefreshCommand(TerraformCommand):
    """Run terraform refresh"""

    def run(self):
        self.run_terraform_command(["refresh"])


class TerraformShowCommand(TerraformCommand):
    """Show current terraform state"""

    def run(self):
        self.run_terraform_command(["show", "-no-color"])
