# Terraform Sublime Text Plugin Structure

## Complete File Structure

```
Terraform/
├── plugin.py                              # Main plugin entry point
├── terraform_lsp.py                       # LSP client configuration
├── terraform_commands.py                  # Terraform CLI command integration
├── terraform_formatter.py                 # Code formatting functionality
├── terraform_cloud.py                     # Terraform Cloud/HCP integration
├── terraform_module_explorer.py           # Module/provider explorer
├── terraform_project.py                   # Project detection and management
├── terraform_settings.py                  # Settings management
├── install.py                            # Installation helper script
│
├── syntaxes/
│   ├── Terraform.sublime-syntax          # Main HCL2 syntax definition
│   └── TerraformVars.sublime-syntax      # .tfvars syntax definition
│
├── bin/                                  # Binary directory (auto-created)
│   └── terraform-ls                      # Language server (auto-downloaded)
│
├── messages/
│   ├── install.txt                       # Installation message
│   └── 1.0.0.txt                        # Release notes
│
├── Terraform.sublime-settings            # Default settings
├── terraform-ls.json                     # LSP configuration
├── Main.sublime-menu                     # Main menu integration
├── Context.sublime-menu                  # Context menu items
├── Default.sublime-commands              # Command palette entries
├── Default.sublime-keymap                # Keyboard shortcuts
├── Terraform.sublime-build               # Build system configuration
├── Terraform.sublime-completions         # Code snippets
├── messages.json                         # Package Control messages
├── package.json                          # Package Control metadata
├── README.md                             # User documentation
├── LICENSE                               # MIT License
├── .gitignore                           # Git ignore file
├── test_syntax.tf                       # Syntax test file (exclude from package)
└── PLUGIN_STRUCTURE.md                  # This file
```

## Core Components

### 1. Plugin Core (`plugin.py`)
- Initializes the plugin
- Manages global state
- Downloads terraform-ls if needed
- Registers event listeners

### 2. Language Server (`terraform_lsp.py`)
- Configures terraform-ls for LSP package
- Provides IntelliSense features
- Handles code navigation
- Manages diagnostics

### 3. Commands (`terraform_commands.py`)
- Terraform CLI integration
- Async command execution
- Output panel management
- Format on save functionality

### 4. Module Explorer (`terraform_module_explorer.py`)
- Parses Terraform files
- Shows modules, providers, resources
- Quick navigation
- Documentation links

### 5. Terraform Cloud (`terraform_cloud.py`)
- OAuth authentication
- Workspace management
- Run history viewing
- Log inspection

### 6. Project Management (`terraform_project.py`)
- Root module detection
- Multi-root workspace support
- Project status tracking
- Project switching

### 7. Settings (`terraform_settings.py`)
- Centralized settings management
- Default configuration
- Settings migration

## Installation Instructions

### For Development

1. Clone into Sublime Text Packages directory:
   ```bash
   cd ~/Library/Application\ Support/Sublime\ Text/Packages/  # macOS
   # or
   cd ~/.config/sublime-text/Packages/                         # Linux
   # or
   cd %APPDATA%\Sublime Text\Packages\                        # Windows
   
   git clone <repository> Terraform
   ```

2. Install dependencies:
   - Install LSP package via Package Control
   - Install Terraform CLI
   - Run `python3 install.py` (optional)

3. Restart Sublime Text

### For Distribution via Package Control

1. Fork the repository
2. Update URLs in package.json and README.md
3. Submit to Package Control:
   - Fork https://github.com/wbond/package_control_channel
   - Add entry to repository.json
   - Submit pull request

## Key Features Implementation

### Auto-completion
- Implemented via terraform-ls and LSP
- Context-aware suggestions
- Function and provider completion

### Syntax Highlighting
- Full HCL2 support
- Terraform Stacks support
- String interpolation
- Heredoc support

### Code Navigation
- Go to Definition (LSP)
- Find References (LSP)
- Symbol navigation
- Module jumping

### Formatting
- Uses terraform fmt
- Format on save option
- Selection formatting

### Validation
- Real-time via terraform-ls
- On-demand via terraform validate
- Error highlighting

## Configuration

### User Settings Location
- macOS: `~/Library/Application Support/Sublime Text/Packages/User/Terraform.sublime-settings`
- Linux: `~/.config/sublime-text/Packages/User/Terraform.sublime-settings`
- Windows: `%APPDATA%\Sublime Text\Packages\User\Terraform.sublime-settings`

### Key Settings
- `terraform_path`: Path to terraform binary
- `format_on_save`: Enable/disable format on save
- `language_server.enabled`: Enable/disable LSP
- `language_server.path`: Path to terraform-ls

## Testing

### Manual Testing
1. Open test_syntax.tf to verify syntax highlighting
2. Test auto-completion in a .tf file
3. Test formatting with Ctrl+Shift+F
4. Test Terraform commands from palette
5. Test go to definition with F12

### Automated Testing
- Use Sublime Text's syntax test system
- Test with various Terraform versions
- Verify LSP integration

## Troubleshooting

### Common Issues

1. **terraform-ls not starting**
   - Check console for errors
   - Verify LSP package installed
   - Check terraform-ls binary exists

2. **No auto-completion**
   - Ensure project is initialized
   - Check if terraform-ls is running
   - Verify file has .tf extension

3. **Formatting not working**
   - Check terraform is in PATH
   - Verify format_on_save setting
   - Check file syntax is valid

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## Package Maintenance

### Updating terraform-ls
1. Update version in plugin.py
2. Test download functionality
3. Update documentation

### Adding Features
1. Implement in appropriate module
2. Add menu/command entries
3. Update documentation
4. Add tests if applicable

### Release Process
1. Update version in package.json
2. Create release notes in messages/
3. Tag release in git
4. Update Package Control channel