# Terraform Plugin for Sublime Text 4

A comprehensive Terraform plugin for Sublime Text 4 that provides intelligent code completion, syntax highlighting, formatting, and integration with Terraform Cloud.

## Features

### 🚀 IntelliSense & Auto-completion
- Provider, resource, and data source completion
- Attribute and argument suggestions
- Module and variable references
- Built-in function completion
- Context-aware suggestions

### 🎨 Syntax Highlighting
- Full HCL2 syntax support (Terraform 0.12+)
- Terraform Stacks support (.tfstack.hcl, .tfdeploy.hcl)
- String interpolation highlighting
- Heredoc support

### ✅ Validation & Diagnostics
- Real-time syntax validation
- Semantic validation with terraform-ls
- Integration with `terraform validate`
- Error highlighting and quick fixes

### 🧭 Code Navigation
- Go to Definition (F12)
- Find All References (Shift+F12)
- Symbol navigation (Ctrl+R)
- Peek Definition (Alt+F12)

### 📝 Code Formatting
- Auto-format with `terraform fmt`
- Format on save (configurable)
- Format selection

### 🔧 Terraform Commands
- Initialize (`terraform init`)
- Validate (`terraform validate`)
- Plan (`terraform plan`)
- Apply (`terraform apply`)
- And more...

### 📦 Module & Provider Explorer
- Visual module hierarchy
- Provider listings with versions
- Direct links to documentation
- Resource explorer

### ☁️ Terraform Cloud Integration
- OAuth authentication
- Workspace management
- Run history viewing
- Log inspection

### 📋 Code Snippets
- Resource templates
- Variable declarations
- Module blocks
- Dynamic blocks
- And more...

## Installation

### Via Package Control (Recommended)

1. Install [Package Control](https://packagecontrol.io/installation) if you haven't already
2. Open Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`)
3. Type "Package Control: Install Package"
4. Search for "Terraform"
5. Press Enter to install

### Manual Installation

1. Clone this repository into your Sublime Text Packages directory:
   ```bash
   cd ~/Library/Application\ Support/Sublime\ Text/Packages/  # macOS
   cd ~/.config/sublime-text/Packages/                         # Linux
   cd %APPDATA%\Sublime Text\Packages\                        # Windows
   
   git clone https://github.com/yourusername/sublime-terraform.git Terraform
   ```

2. Restart Sublime Text

## Dependencies

### Required
- **Sublime Text 4** (Build 4000 or higher)
- **LSP Package** - Install via Package Control
- **Terraform CLI** - [Install Terraform](https://www.terraform.io/downloads)

### Optional
- **terraform-ls** - Will be auto-downloaded on first use

## Configuration

### Basic Settings

Open `Preferences → Package Settings → Terraform → Settings` and customize:

```json
{
    // Path to terraform binary
    "terraform_path": "terraform",
    
    // Format on save
    "format_on_save": true,
    
    // Language server settings
    "language_server": {
        "enabled": true,
        "path": ""  // Auto-detected if empty
    }
}
```

### Key Bindings

Default key bindings:

- **Format**: `Ctrl+Shift+F`
- **Validate**: `Ctrl+Shift+V`
- **Initialize**: `Ctrl+Shift+I`
- **Plan**: `Ctrl+Shift+P`
- **Show Modules**: `Ctrl+Shift+M`

Customize in `Preferences → Package Settings → Terraform → Key Bindings`.

## Usage

### Getting Started

1. Open a Terraform project folder
2. The plugin will automatically activate for `.tf` files
3. Start typing to see auto-completion
4. Use Command Palette for Terraform commands

### Language Server

The plugin uses `terraform-ls` for intelligent features. On first use:
1. The plugin will attempt to download terraform-ls automatically
2. If that fails, [download manually](https://github.com/hashicorp/terraform-ls/releases)
3. Set the path in settings: `"language_server.path": "/path/to/terraform-ls"`

### Terraform Cloud

To use Terraform Cloud features:

1. Run "Terraform Cloud: Login" from Command Palette
2. Choose authentication method:
   - Use existing `terraform login` token
   - Enter token manually
   - Generate new token in browser
3. Select your organization
4. View workspaces and runs

### Module Explorer

- **View Modules**: `Ctrl+Shift+M` or Command Palette
- **View Providers**: Command Palette → "Terraform: Show Providers"
- **View Resources**: Command Palette → "Terraform: Show Resources"

## Troubleshooting

### Language Server Not Starting

1. Check if terraform-ls is installed:
   ```bash
   terraform-ls --version
   ```

2. Verify LSP package is installed
3. Check Sublime Text console for errors (`View → Show Console`)

### Formatting Not Working

1. Ensure terraform binary is in PATH:
   ```bash
   terraform version
   ```

2. Check format_on_save setting
3. Try manual format: Command Palette → "Terraform: Format Document"

### Auto-completion Not Working

1. Ensure file has `.tf` extension
2. Check if project is initialized (`terraform init`)
3. Verify language server is running
4. Try restarting Sublime Text

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This plugin is released under the MIT License. See [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the [HashiCorp Terraform VSCode extension](https://github.com/hashicorp/vscode-terraform)
- Uses [terraform-ls](https://github.com/hashicorp/terraform-ls) for language features
- Built for the Sublime Text community

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/sublime-terraform/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/sublime-terraform/discussions)
- **Documentation**: [Wiki](https://github.com/yourusername/sublime-terraform/wiki)