# Changelog

All notable changes to the Terraform Sublime Text plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive test suite with unit, integration, and performance tests
- CI/CD pipeline with GitHub Actions
- Test coverage reporting
- Performance benchmarks for large files
- Mock data for testing terraform-ls integration

### Changed
- Improved error handling in all components
- Enhanced performance for parsing large Terraform files

### Fixed
- Memory leaks in module parser
- Race conditions in concurrent file parsing

## [1.0.0] - 2024-01-20

### Added
- Initial release of Terraform Sublime Text plugin
- Full Language Server Protocol support via terraform-ls
- IntelliSense for providers, resources, and functions
- Syntax highlighting for HCL2 and Terraform Stacks
- Code formatting with terraform fmt
- Integrated Terraform commands (init, plan, apply, etc.)
- Module and provider explorer
- Terraform Cloud/HCP integration
- Project detection and management
- Rich code snippets
- Go to Definition and Find References
- Format on save option
- Validation and diagnostics
- Multi-root workspace support

### Security
- Secure token storage for Terraform Cloud
- No credentials stored in plain text

## Testing Milestones

### Test Coverage Goals
- [x] Unit test coverage > 80%
- [x] Integration test coverage for all major workflows
- [x] Performance tests for files with 1000+ resources
- [x] Syntax highlighting tests
- [x] Cross-platform testing (Windows, macOS, Linux)

### Performance Benchmarks
- Module parsing: < 500ms for 500 modules
- Resource finding: < 500ms for 2000 resources
- Project detection: < 100ms for deep directory structures
- LSP initialization: < 2 seconds

### Known Issues
- Performance degradation with files > 10,000 lines
- Memory usage increases with multiple large projects open
- LSP may timeout on very large workspaces

## Versioning

This project uses Semantic Versioning:
- MAJOR version for incompatible API changes
- MINOR version for backwards-compatible functionality additions
- PATCH version for backwards-compatible bug fixes

## Deprecation Policy

Features marked as deprecated will be:
1. Marked in documentation with deprecation notice
2. Maintained for at least 2 minor versions
3. Removed in the next major version

[Unreleased]: https://github.com/yourusername/sublime-terraform/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/yourusername/sublime-terraform/releases/tag/v1.0.0