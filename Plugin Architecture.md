# Terraform Sublime Text Plugin Architecture

## Overview
The Terraform plugin for Sublime Text 4 will be a comprehensive port of the VSCode extension, leveraging Sublime's Python API and LSP capabilities.

## Core Components

### 1. Language Server Integration (LSP)
- **Component**: `TerraformLSP`
- **Purpose**: Interface with terraform-ls for IntelliSense, validation, and code navigation
- **Dependencies**: LSP package for Sublime Text
- **Key Features**:
  - Auto-completion for resources, data sources, providers, attributes
  - Go to definition/declaration
  - Hover documentation
  - Diagnostics and validation
  - Symbol navigation

### 2. Syntax Highlighting
- **Component**: `Terraform.sublime-syntax` and `TerraformVars.sublime-syntax`
- **Purpose**: Provide HCL2 syntax highlighting for .tf, .tfvars, .tfstack.hcl files
- **Features**:
  - Support for Terraform 0.12+ syntax
  - Terraform Stacks support
  - Proper scoping for themes

### 3. Command Integration
- **Component**: `TerraformCommands`
- **Purpose**: Execute Terraform CLI commands from Sublime
- **Commands**:
  - `terraform init`
  - `terraform validate`
  - `terraform plan`
  - `terraform apply`
  - `terraform fmt`

### 4. Build Systems
- **Component**: `Terraform.sublime-build`
- **Purpose**: Integration with Sublime's build system for running Terraform commands

### 5. Formatting
- **Component**: `TerraformFormatter`
- **Purpose**: Auto-format on save using `terraform fmt`
- **Features**:
  - Format on save option
  - Format selection
  - Configurable timeout

### 6. Module Explorer
- **Component**: `TerraformModuleExplorer`
- **Purpose**: Side panel showing modules and providers
- **Features**:
  - Tree view of modules
  - Icons for local/git/registry modules
  - Quick access to documentation

### 7. HCP Terraform Integration
- **Component**: `TerraformCloud`
- **Purpose**: View and manage Terraform Cloud workspaces
- **Features**:
  - OAuth authentication
  - Workspace listing
  - Run status monitoring
  - Log viewing

### 8. Snippets
- **Component**: `Terraform.sublime-completions`
- **Purpose**: Code snippets for common patterns
- **Snippets**:
  - Resource blocks
  - Variable declarations
  - For expressions
  - Conditional expressions

### 9. Settings Management
- **Component**: `TerraformSettings`
- **Purpose**: Manage plugin configuration
- **Settings**:
  - Language server path
  - Terraform binary path
  - Format on save
  - Validation options
  - Excluded directories

### 10. Project Detection
- **Component**: `TerraformProject`
- **Purpose**: Detect and manage Terraform projects
- **Features**:
  - Root module detection
  - Multi-root workspace support
  - .terraform directory handling

## File Structure
```
Terraform/
├── plugin.py                          # Main plugin entry point
├── terraform_lsp.py                   # LSP client configuration
├── terraform_commands.py              # Command palette commands
├── terraform_formatter.py             # Formatting integration
├── terraform_cloud.py                 # HCP Terraform integration
├── terraform_module_explorer.py       # Module/provider explorer
├── terraform_project.py               # Project detection
├── terraform_settings.py              # Settings management
├── syntaxes/
│   ├── Terraform.sublime-syntax       # Main syntax definition
│   └── TerraformVars.sublime-syntax   # Variables syntax
├── build/
│   └── Terraform.sublime-build        # Build system
├── snippets/
│   └── Terraform.sublime-completions  # Code snippets
├── menus/
│   ├── Main.sublime-menu             # Main menu items
│   ├── Context.sublime-menu          # Context menu items
│   └── Command Palette.sublime-menu  # Command palette entries
├── keymaps/
│   ├── Default.sublime-keymap        # Cross-platform keybindings
│   ├── Default (Linux).sublime-keymap
│   ├── Default (OSX).sublime-keymap
│   └── Default (Windows).sublime-keymap
└── .python-version                    # Python version requirement
```

## Integration Points

### 1. LSP Package Integration
- Configure terraform-ls as an LSP client
- Handle automatic installation/updates of terraform-ls
- Map LSP capabilities to Sublime features

### 2. Sublime API Usage
- `sublime.View` for text manipulation
- `sublime.Window` for UI elements
- `sublime_plugin.TextCommand` for text commands
- `sublime_plugin.WindowCommand` for window commands
- `sublime_plugin.EventListener` for events

### 3. External Process Management
- Subprocess for terraform CLI commands
- Process pool for concurrent operations
- Output panel for command results

## Dependencies
1. **Required Packages**:
   - LSP (for language server support)
   - Package Control (for distribution)

2. **External Binaries**:
   - terraform-ls (bundled or auto-downloaded)
   - terraform CLI (user-installed)

## Key Differences from VSCode
1. **UI Components**: Use Sublime's quick panel and output panels instead of VSCode's tree views
2. **Settings**: JSON-based configuration in Sublime preferences
3. **Language**: Python instead of TypeScript
4. **Extension API**: Sublime's plugin API vs VSCode's extension API