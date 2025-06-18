"""
Terraform Cloud / HCP Terraform integration
Provides workspace viewing and run management
"""

import json
import os
import urllib.error
import urllib.request

import sublime
import sublime_plugin

from .terraform_settings import get_settings


class TerraformCloudAPI:
    """API client for Terraform Cloud"""

    BASE_URL = "https://app.terraform.io/api/v2"

    def __init__(self, token=None):
        self.token = token or self.get_stored_token()

    def get_stored_token(self):
        """Get stored API token"""
        # First try secure storage
        token = self.get_secure_token()
        if token:
            return token

        # Fall back to settings (not recommended)
        settings = get_settings()
        return settings.get("terraform_cloud.token")

    def get_secure_token(self):
        """Get token from secure storage (platform-specific)"""
        # This would ideally use platform-specific secure storage
        # For now, we'll use a simple file-based approach
        token_file = os.path.expanduser("~/.terraform.d/credentials.tfrc.json")

        if os.path.exists(token_file):
            try:
                with open(token_file, "r") as f:
                    creds = json.load(f)
                    return (
                        creds.get("credentials", {})
                        .get("app.terraform.io", {})
                        .get("token")
                    )
            except (json.JSONDecodeError, IOError):
                pass

        return None

    def make_request(self, endpoint, method="GET", data=None):
        """Make an API request"""
        url = f"{self.BASE_URL}{endpoint}"

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/vnd.api+json",
        }

        request = urllib.request.Request(url, headers=headers, method=method)

        if data:
            request.data = json.dumps(data).encode("utf-8")

        try:
            response = urllib.request.urlopen(request)
            return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8")
            raise Exception(f"API Error {e.code}: {error_body}")

    def get_organizations(self):
        """Get list of organizations"""
        result = self.make_request("/organizations")
        return result.get("data", [])

    def get_workspaces(self, organization):
        """Get workspaces for an organization"""
        result = self.make_request(f"/organizations/{organization}/workspaces")
        return result.get("data", [])

    def get_runs(self, workspace_id):
        """Get runs for a workspace"""
        result = self.make_request(f"/workspaces/{workspace_id}/runs")
        return result.get("data", [])

    def get_run_details(self, run_id):
        """Get detailed information about a run"""
        return self.make_request(f"/runs/{run_id}")

    def get_plan_log(self, plan_id):
        """Get plan log output"""
        # This would require parsing the log URL from the plan object
        # For now, return a placeholder
        return "Plan log retrieval not yet implemented"


class TerraformCloudState:
    """Manages Terraform Cloud state for the plugin"""

    def __init__(self):
        self.token = None
        self.organization = None
        self.workspaces = []
        self.current_workspace = None
        self.runs = []

    def is_authenticated(self):
        """Check if we have a valid token"""
        return self.token is not None


# Global state instance
_cloud_state = TerraformCloudState()


class TerraformCloudLoginCommand(sublime_plugin.WindowCommand):
    """Login to Terraform Cloud"""

    def run(self):
        # Check for existing token
        api = TerraformCloudAPI()
        if api.token:
            if sublime.ok_cancel_dialog(
                "Already logged in to Terraform Cloud. Do you want to re-authenticate?",
                "Re-authenticate",
            ):
                self.prompt_for_token()
            else:
                self.select_organization()
        else:
            self.show_login_options()

    def show_login_options(self):
        """Show login options"""
        options = [
            ["Use Terraform CLI token", "Use existing token from terraform login"],
            ["Enter token manually", "Paste a token from Terraform Cloud"],
            ["Open Terraform Cloud", "Generate a new token in your browser"],
        ]

        self.window.show_quick_panel(
            options, self.on_login_option_selected, placeholder="Select login method"
        )

    def on_login_option_selected(self, index):
        """Handle login option selection"""
        if index == 0:
            # Try to use CLI token
            api = TerraformCloudAPI()
            token = api.get_secure_token()
            if token:
                _cloud_state.token = token
                sublime.status_message("✓ Using token from Terraform CLI")
                self.select_organization()
            else:
                sublime.error_message(
                    "No Terraform CLI token found.\n"
                    "Please run 'terraform login' first."
                )
        elif index == 1:
            # Manual token entry
            self.prompt_for_token()
        elif index == 2:
            # Open browser
            import webbrowser

            webbrowser.open("https://app.terraform.io/app/settings/tokens")
            self.prompt_for_token()

    def prompt_for_token(self):
        """Prompt for API token"""
        self.window.show_input_panel(
            "Enter Terraform Cloud API Token:", "", self.on_token_entered, None, None
        )

    def on_token_entered(self, token):
        """Handle token entry"""
        if not token:
            return

        # Validate token by making a test request
        api = TerraformCloudAPI(token)
        try:
            api.get_organizations()
            _cloud_state.token = token
            sublime.status_message("✓ Successfully authenticated to Terraform Cloud")
            self.select_organization()
        except Exception as e:
            sublime.error_message(f"Authentication failed: {str(e)}")

    def select_organization(self):
        """Select organization"""
        api = TerraformCloudAPI(_cloud_state.token)

        try:
            orgs = api.get_organizations()

            if not orgs:
                sublime.error_message("No organizations found")
                return

            items = []
            for org in orgs:
                items.append(
                    [org["attributes"]["name"], org["attributes"].get("email", "")]
                )

            self.window.show_quick_panel(
                items,
                lambda idx: self.on_organization_selected(idx, orgs),
                placeholder="Select organization",
            )

        except Exception as e:
            sublime.error_message(f"Failed to get organizations: {str(e)}")

    def on_organization_selected(self, index, orgs):
        """Handle organization selection"""
        if index < 0:
            return

        org = orgs[index]
        _cloud_state.organization = org["attributes"]["name"]

        # Save to settings
        settings = get_settings()
        settings.set("terraform_cloud.organization", _cloud_state.organization)

        sublime.status_message(f"✓ Selected organization: {_cloud_state.organization}")

        # Show workspaces
        self.window.run_command("terraform_cloud_show_workspaces")


class TerraformCloudShowWorkspacesCommand(sublime_plugin.WindowCommand):
    """Show Terraform Cloud workspaces"""

    def run(self):
        if not _cloud_state.token:
            self.window.run_command("terraform_cloud_login")
            return

        if not _cloud_state.organization:
            sublime.error_message("No organization selected")
            return

        api = TerraformCloudAPI(_cloud_state.token)

        try:
            workspaces = api.get_workspaces(_cloud_state.organization)
            _cloud_state.workspaces = workspaces

            if not workspaces:
                sublime.status_message("No workspaces found")
                return

            items = []
            for ws in workspaces:
                attrs = ws["attributes"]
                status = self.get_status_icon(attrs.get("latest-run", {}).get("status"))
                items.append(
                    [
                        f"{status} {attrs['name']}",
                        f"Environment: {attrs.get('environment', 'default')}",
                        f"Updated: {attrs.get('updated-at', 'Never')[:10]}",
                    ]
                )

            self.window.show_quick_panel(
                items,
                lambda idx: self.on_workspace_selected(idx),
                placeholder="Select workspace to view runs",
            )

        except Exception as e:
            sublime.error_message(f"Failed to get workspaces: {str(e)}")

    def get_status_icon(self, status):
        """Get icon for run status"""
        icons = {
            "applied": "✅",
            "planned": "📋",
            "planning": "⏳",
            "applying": "🔄",
            "errored": "❌",
            "canceled": "🚫",
            "discarded": "🗑️",
            "pending": "⏸️",
        }
        return icons.get(status, "❓")

    def on_workspace_selected(self, index):
        """Handle workspace selection"""
        if index < 0:
            return

        workspace = _cloud_state.workspaces[index]
        _cloud_state.current_workspace = workspace

        # Show runs for this workspace
        self.window.run_command("terraform_cloud_show_runs")

    def is_enabled(self):
        return _cloud_state.token is not None


class TerraformCloudShowRunsCommand(sublime_plugin.WindowCommand):
    """Show runs for current workspace"""

    def run(self):
        if not _cloud_state.current_workspace:
            sublime.error_message("No workspace selected")
            return

        api = TerraformCloudAPI(_cloud_state.token)
        workspace_id = _cloud_state.current_workspace["id"]

        try:
            runs = api.get_runs(workspace_id)
            _cloud_state.runs = runs

            if not runs:
                sublime.status_message("No runs found")
                return

            items = []
            for run in runs:
                attrs = run["attributes"]
                status_icon = self.get_status_icon(attrs["status"])
                items.append(
                    [
                        f"{status_icon} Run #{attrs.get('run-number', '?')}",
                        f"Status: {attrs['status']}",
                        f"Created: {attrs.get('created-at', '')[:19]}",
                    ]
                )

            self.window.show_quick_panel(
                items,
                lambda idx: self.on_run_selected(idx),
                placeholder="Select run to view details",
            )

        except Exception as e:
            sublime.error_message(f"Failed to get runs: {str(e)}")

    def get_status_icon(self, status):
        """Get icon for run status"""
        icons = {
            "applied": "✅",
            "planned": "📋",
            "planning": "⏳",
            "applying": "🔄",
            "errored": "❌",
            "canceled": "🚫",
            "discarded": "🗑️",
            "pending": "⏸️",
            "plan_queued": "📥",
            "apply_queued": "📤",
        }
        return icons.get(status, "❓")

    def on_run_selected(self, index):
        """Handle run selection"""
        if index < 0:
            return

        run = _cloud_state.runs[index]

        # Show run details
        attrs = run["attributes"]
        message = f"""
Run #{attrs.get('run-number', '?')}
Status: {attrs['status']}
Created: {attrs.get('created-at', '')}
Message: {attrs.get('message', 'No message')}

Resources:
  Added: {attrs.get('resource-additions', 0)}
  Changed: {attrs.get('resource-changes', 0)}
  Destroyed: {attrs.get('resource-destructions', 0)}
"""

        # Show in output panel
        panel = self.window.create_output_panel("terraform_cloud_run")
        panel.run_command("append", {"characters": message})
        self.window.run_command("show_panel", {"panel": "output.terraform_cloud_run"})

    def is_enabled(self):
        return _cloud_state.current_workspace is not None


class TerraformCloudLogoutCommand(sublime_plugin.WindowCommand):
    """Logout from Terraform Cloud"""

    def run(self):
        if sublime.ok_cancel_dialog(
            "Are you sure you want to logout from Terraform Cloud?", "Logout"
        ):
            global _cloud_state
            _cloud_state = TerraformCloudState()
            sublime.status_message("✓ Logged out from Terraform Cloud")

    def is_enabled(self):
        return _cloud_state.token is not None
