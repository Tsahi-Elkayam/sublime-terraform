"""
Module and Provider Explorer for Terraform files
Shows modules and providers used in the current file
"""

import os
import re
import json
import sublime
import sublime_plugin
from .terraform_settings import get_settings

class TerraformModuleParser:
    """Parse Terraform files for modules and providers"""
    
    @staticmethod
    def parse_file(view):
        """Parse a view for modules and providers"""
        content = view.substr(sublime.Region(0, view.size()))
        
        modules = TerraformModuleParser.find_modules(content)
        providers = TerraformModuleParser.find_providers(content)
        resources = TerraformModuleParser.find_resources(content)
        
        return {
            "modules": modules,
            "providers": providers,
            "resources": resources
        }
    
    @staticmethod
    def find_modules(content):
        """Find all module blocks in content"""
        modules = []
        
        # Regex to match module blocks
        module_pattern = r'module\s+"([^"]+)"\s*\{([^}]*)\}'
        
        for match in re.finditer(module_pattern, content, re.DOTALL):
            name = match.group(1)
            block_content = match.group(2)
            
            # Extract source
            source_match = re.search(r'source\s*=\s*"([^"]+)"', block_content)
            source = source_match.group(1) if source_match else "unknown"
            
            # Determine source type
            source_type = TerraformModuleParser.get_source_type(source)
            
            # Extract version if present
            version_match = re.search(r'version\s*=\s*"([^"]+)"', block_content)
            version = version_match.group(1) if version_match else None
            
            modules.append({
                "name": name,
                "source": source,
                "source_type": source_type,
                "version": version,
                "line": content[:match.start()].count('\n') + 1
            })
        
        return modules
    
    @staticmethod
    def find_providers(content):
        """Find all provider configurations"""
        providers = []
        
        # Find required_providers block
        req_providers_pattern = r'required_providers\s*\{([^}]*)\}'
        req_match = re.search(req_providers_pattern, content, re.DOTALL)
        
        if req_match:
            providers_block = req_match.group(1)
            
            # Parse each provider
            provider_pattern = r'(\w+)\s*=\s*\{([^}]*)\}'
            
            for match in re.finditer(provider_pattern, providers_block):
                name = match.group(1)
                config = match.group(2)
                
                # Extract source
                source_match = re.search(r'source\s*=\s*"([^"]+)"', config)
                source = source_match.group(1) if source_match else f"hashicorp/{name}"
                
                # Extract version
                version_match = re.search(r'version\s*=\s*"([^"]+)"', config)
                version = version_match.group(1) if version_match else "latest"
                
                providers.append({
                    "name": name,
                    "source": source,
                    "version": version
                })
        
        # Also find provider blocks
        provider_pattern = r'provider\s+"([^"]+)"'
        for match in re.finditer(provider_pattern, content):
            name = match.group(1)
            if not any(p["name"] == name for p in providers):
                providers.append({
                    "name": name,
                    "source": f"hashicorp/{name}",
                    "version": "latest"
                })
        
        return providers
    
    @staticmethod
    def find_resources(content):
        """Find all resources in content"""
        resources = []
        
        # Regex to match resource blocks
        resource_pattern = r'resource\s+"([^"]+)"\s+"([^"]+)"'
        
        for match in re.finditer(resource_pattern, content):
            resource_type = match.group(1)
            resource_name = match.group(2)
            
            resources.append({
                "type": resource_type,
                "name": resource_name,
                "line": content[:match.start()].count('\n') + 1
            })
        
        return resources
    
    @staticmethod
    def get_source_type(source):
        """Determine the type of module source"""
        if source.startswith("./") or source.startswith("../"):
            return "local"
        elif source.startswith("git::") or source.endswith(".git"):
            return "git"
        elif source.startswith("github.com/"):
            return "github"
        elif source.startswith("app.terraform.io/") or source.count("/") >= 2:
            return "registry"
        elif source.startswith("http://") or source.startswith("https://"):
            return "http"
        else:
            return "unknown"

class TerraformShowModulesCommand(sublime_plugin.WindowCommand):
    """Show modules in the current file"""
    
    def run(self):
        view = self.window.active_view()
        if not view:
            return
        
        # Parse the file
        parsed = TerraformModuleParser.parse_file(view)
        modules = parsed["modules"]
        
        if not modules:
            sublime.status_message("No modules found in current file")
            return
        
        # Create quick panel items
        items = []
        for module in modules:
            icon = self.get_module_icon(module["source_type"])
            version_str = f" (v{module['version']})" if module["version"] else ""
            items.append([
                f"{icon} {module['name']}{version_str}",
                f"Source: {module['source']}",
                f"Line {module['line']}"
            ])
        
        # Show quick panel
        self.window.show_quick_panel(
            items,
            lambda idx: self.on_select(idx, modules, view),
            placeholder="Select a module to jump to"
        )
    
    def get_module_icon(self, source_type):
        """Get icon for module source type"""
        icons = {
            "local": "📁",
            "git": "🔗",
            "github": "🐙",
            "registry": "📦",
            "http": "🌐",
            "unknown": "❓"
        }
        return icons.get(source_type, "📦")
    
    def on_select(self, index, modules, view):
        """Handle module selection"""
        if index < 0:
            return
        
        module = modules[index]
        
        # Jump to module definition
        point = view.text_point(module["line"] - 1, 0)
        view.sel().clear()
        view.sel().add(sublime.Region(point))
        view.show_at_center(point)
        
        # If it's a registry module, offer to open documentation
        if module["source_type"] == "registry":
            if sublime.ok_cancel_dialog(
                f"Open documentation for {module['source']}?",
                "Open"
            ):
                import webbrowser
                url = f"https://registry.terraform.io/modules/{module['source']}"
                webbrowser.open(url)

class TerraformShowProvidersCommand(sublime_plugin.WindowCommand):
    """Show providers in the current file"""
    
    def run(self):
        view = self.window.active_view()
        if not view:
            return
        
        # Parse the file
        parsed = TerraformModuleParser.parse_file(view)
        providers = parsed["providers"]
        
        if not providers:
            sublime.status_message("No providers found in current file")
            return
        
        # Create quick panel items
        items = []
        for provider in providers:
            items.append([
                f"🔌 {provider['name']}",
                f"Source: {provider['source']}",
                f"Version: {provider['version']}"
            ])
        
        # Show quick panel
        self.window.show_quick_panel(
            items,
            lambda idx: self.on_select(idx, providers),
            placeholder="Select a provider to view documentation"
        )
    
    def on_select(self, index, providers):
        """Handle provider selection"""
        if index < 0:
            return
        
        provider = providers[index]
        
        # Open provider documentation
        if sublime.ok_cancel_dialog(
            f"Open documentation for {provider['name']} provider?",
            "Open"
        ):
            import webbrowser
            # Construct documentation URL
            if provider["source"].startswith("hashicorp/"):
                url = f"https://registry.terraform.io/providers/{provider['source']}/latest/docs"
            else:
                url = f"https://registry.terraform.io/providers/{provider['source']}"
            webbrowser.open(url)

class TerraformModuleExplorerListener(sublime_plugin.EventListener):
    """Event listener for module explorer features"""
    
    def on_hover(self, view, point, hover_zone):
        """Show module/provider info on hover"""
        if hover_zone != sublime.HOVER_TEXT:
            return
        
        # Check if we're hovering over a module source
        if view.match_selector(point, "string.quoted.double.terraform"):
            line = view.line(point)
            line_text = view.substr(line)
            
            # Check if this is a module source line
            if "source" in line_text and "module" in view.substr(view.line(line.begin() - 100)):
                source_match = re.search(r'source\s*=\s*"([^"]+)"', line_text)
                if source_match:
                    source = source_match.group(1)
                    self.show_module_hover(view, point, source)
    
    def show_module_hover(self, view, point, source):
        """Show hover popup for module source"""
        source_type = TerraformModuleParser.get_source_type(source)
        
        content = f"""
        <div style="padding: 10px;">
            <h3>Module Source</h3>
            <p><strong>Type:</strong> {source_type}</p>
            <p><strong>Source:</strong> <code>{source}</code></p>
        """
        
        if source_type == "registry":
            content += f"""
            <p><a href="https://registry.terraform.io/modules/{source}">View on Terraform Registry</a></p>
            """
        
        content += "</div>"
        
        view.show_popup(
            content,
            flags=sublime.HIDE_ON_MOUSE_MOVE_AWAY,
            location=point,
            max_width=600
        )

class TerraformShowResourcesCommand(sublime_plugin.WindowCommand):
    """Show all resources in the current file"""
    
    def run(self):
        view = self.window.active_view()
        if not view:
            return
        
        # Parse the file
        parsed = TerraformModuleParser.parse_file(view)
        resources = parsed["resources"]
        
        if not resources:
            sublime.status_message("No resources found in current file")
            return
        
        # Group resources by type
        grouped = {}
        for resource in resources:
            resource_type = resource["type"]
            if resource_type not in grouped:
                grouped[resource_type] = []
            grouped[resource_type].append(resource)
        
        # Create quick panel items
        items = []
        flat_resources = []
        
        for resource_type, resources_list in sorted(grouped.items()):
            for resource in resources_list:
                items.append([
                    f"🔧 {resource['type']}.{resource['name']}",
                    f"Line {resource['line']}"
                ])
                flat_resources.append(resource)
        
        # Show quick panel
        self.window.show_quick_panel(
            items,
            lambda idx: self.on_select(idx, flat_resources, view),
            placeholder="Select a resource to jump to"
        )
    
    def on_select(self, index, resources, view):
        """Handle resource selection"""
        if index < 0:
            return
        
        resource = resources[index]
        
        # Jump to resource definition
        point = view.text_point(resource["line"] - 1, 0)
        view.sel().clear()
        view.sel().add(sublime.Region(point))
        view.show_at_center(point)