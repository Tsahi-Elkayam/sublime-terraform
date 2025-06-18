# Terraform Sublime Text Plugin Features

## Core Language Features

### 1. IntelliSense & Auto-completion
- **Provider Completion**: Auto-complete provider names and configurations
- **Resource Completion**: Complete resource types and arguments
- **Data Source Completion**: Complete data source types and arguments
- **Attribute Completion**: Context-aware attribute suggestions
- **Module Completion**: Complete module sources and arguments
- **Variable Reference**: Complete variable references with `var.`, `local.`, `module.`
- **Function Completion**: Built-in Terraform functions
- **Block Completion**: Complete block types (lifecycle, provisioner, etc.)

### 2. Syntax Highlighting
- **HCL2 Support**: Full Terraform 0.12+ syntax
- **Terraform Stacks**: Support for .tfstack.hcl and .tfdeploy.hcl files
- **String Interpolation**: Highlight `${}` expressions
- **Functions**: Highlight built-in functions
- **Keywords**: Highlight Terraform keywords
- **Comments**: Single and multi-line comments
- **Here-docs**: Properly highlight heredoc strings

### 3. Validation & Diagnostics
- **Syntax Validation**: Real-time syntax error detection
- **Semantic Validation**: Type checking and reference validation
- **Deprecation Warnings**: Highlight deprecated syntax
- **terraform validate**: Integration with CLI validation
- **Missing Required Fields**: Highlight missing required attributes
- **Invalid References**: Detect references to undefined resources/variables

### 4. Code Navigation
- **Go to Definition**: Navigate to resource/variable definitions (F12)
- **Go to Declaration**: Navigate to where variables are declared
- **Find All References**: Find all usages of a resource/variable
- **Symbol Navigation**: Navigate to any symbol in workspace (Ctrl+R)
- **Peek Definition**: View definition without leaving current file
- **Breadcrumbs**: Show current location in resource hierarchy

### 5. Code Formatting
- **terraform fmt**: Automatic formatting using official formatter
- **Format on Save**: Optional automatic formatting
- **Format Selection**: Format only selected text
- **Indentation**: Proper HCL indentation rules

### 6. Refactoring
- **Rename Symbol**: Rename resources/variables across files
- **Extract Variable**: Extract expressions to variables
- **Extract Module**: Extract resources to a module

## Enhanced Features

### 7. Terraform Commands
- **terraform init**: Initialize working directory
- **terraform plan**: Create execution plan
- **terraform apply**: Apply changes
- **terraform destroy**: Destroy infrastructure
- **terraform refresh**: Update state file
- **Custom Commands**: Run any terraform command

### 8. Module & Provider Explorer
- **Module Tree View**: Visual hierarchy of modules
- **Provider List**: List of configured providers
- **Registry Links**: Direct links to documentation
- **Version Information**: Show module/provider versions
- **Source Icons**: Visual indicators for source types

### 9. HCP Terraform Integration
- **Authentication**: OAuth login to Terraform Cloud
- **Workspace View**: List and filter workspaces
- **Run History**: View past and current runs
- **Run Details**: Status, timing, and resource changes
- **Log Viewer**: View plan/apply logs
- **Quick Actions**: Trigger runs from editor

### 10. Code Snippets
- **Resource Snippets**: Common resource patterns
- **Variable Snippets**: Variable with validation
- **Output Snippets**: Output with description
- **Module Snippets**: Module blocks
- **Dynamic Blocks**: Dynamic block patterns
- **For Expressions**: For loop templates
- **Conditional Expressions**: Ternary operators

## Developer Experience

### 11. Project Management
- **Multi-root Workspaces**: Support multiple Terraform projects
- **Root Module Detection**: Automatic detection of root modules
- **Module Boundaries**: Understand module boundaries
- **Exclude Patterns**: Ignore specific directories

### 12. Documentation
- **Hover Documentation**: Show documentation on hover
- **Provider Docs**: Links to provider documentation
- **Function Docs**: Built-in function documentation
- **Quick Info**: Type information and descriptions

### 13. Error Handling
- **Error Highlighting**: Underline errors in editor
- **Error Panel**: List all errors in project
- **Quick Fixes**: Suggest fixes for common errors
- **Error Navigation**: Jump between errors

## Configuration & Customization

### 14. Settings
- **Language Server Settings**: Configure terraform-ls
- **Terraform Path**: Custom terraform binary location
- **Format Settings**: Formatting preferences
- **Validation Settings**: Validation options
- **Excluded Paths**: Directories to ignore
- **Experimental Features**: Toggle experimental features

### 15. Keybindings
- **Default Bindings**: Common shortcuts
- **Customizable**: User-defined shortcuts
- **Command Palette**: All commands available
- **Context Menus**: Right-click actions

## Integration Features

### 16. Build System
- **Build Tasks**: Run terraform commands as build tasks
- **Error Matching**: Parse terraform output for errors
- **Custom Build Commands**: User-defined build commands

### 17. Version Control
- **Git Integration**: Ignore .terraform directories
- **Diff Support**: Syntax highlighting in diffs
- **Merge Conflict Resolution**: Handle .tf merge conflicts

### 18. Performance
- **Incremental Parsing**: Parse only changed files
- **Lazy Loading**: Load features on demand
- **Caching**: Cache parsed information
- **Background Processing**: Non-blocking operations

## File Type Support
- **.tf**: Main Terraform configuration files
- **.tfvars**: Variable definition files
- **.tfvars.json**: JSON variable files
- **.tfstack.hcl**: Terraform Stack files
- **.tfdeploy.hcl**: Terraform deployment files
- **.tfstate**: State file viewing (read-only)
- **.tfplan**: Plan file viewing (read-only)