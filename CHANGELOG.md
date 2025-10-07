# Changelog

All notable changes to this project will be documented in this file.


## [2025.1.0] - 2025-10-05

## [2025.0.0] - 2025-09-06

### Added
- **Complete Project Foundation**: Modern Python package structure with pyproject.toml
- **Dual Processing Models**:
  - `TabularDataModel`: Full in-memory tabular data processing
  - `StreamingTabularDataModel`: Memory-efficient streaming processing for large datasets
- **Comprehensive Exception Hierarchy**:
  - `SplurgeError`: Base exception class
  - `SplurgeParameterError`: Invalid parameter errors
  - `SplurgeValidationError`: Data validation errors
  - `SplurgeFileError`: File operation errors
  - `SplurgeRangeError`: Index/range errors
- **Utility Functions**:
  - Data validation and normalization
  - File operation helpers
  - Column standardization
  - Row processing utilities
- **Type Safety**: Full type annotations throughout the codebase
- **Modern Packaging**: setuptools with modern Python standards

### Testing
- **197 Comprehensive Tests** with 95% coverage
- **Unit Tests** (172 tests): Individual component testing
- **Integration Tests** (13 tests): Component interaction validation
- **E2E Tests** (12 tests): Complete workflow testing
- Test categories include error handling, performance, and edge cases

### Documentation
- **Complete README.md**: Project overview, installation, and usage
- **Detailed API Documentation**: Comprehensive function and class references
- **Usage Examples**: Code samples for common use cases
- **Architecture Documentation**: Design principles and component relationships

### Quality Assurance
- **Code Style**: Ruff linting and formatting
- **Type Checking**: Full mypy compatibility
- **Error Handling**: Comprehensive exception coverage
- **Performance**: Optimized for both memory usage and speed

### Development
- **Modern Development Workflow**: Research → Plan → Implement → Test
- **BDD/TDD Approach**: Behavior and test-driven development
- **SOLID Principles**: Clean, maintainable architecture
- **DRY/KISS**: Code quality and simplicity

## [2025.0.0] - 2025-09-06

### Added
- Initial project structure and planning
- Basic package configuration
- Development environment setup
- Initial documentation framework

---

## Types of changes
- `Added` for new features
- `Changed` for changes in existing functionality
- `Deprecated` for soon-to-be removed features
- `Removed` for now removed features
- `Fixed` for any bug fixes
- `Security` for vulnerability fixes

## Version Format
This project uses [CalVer](https://calver.org/) versioning: `YYYY.MM.MICRO`

- `YYYY`: Year of release
- `MM`: Month of release
- `MICRO`: Patch version (0 for major releases)