# Changelog

All notable changes to this project will be documented in this file.

## [2025.2.0] - 2025-11-02

### Changed
- **Simplified Exception Hierarchy**: Reduced from 12+ exception classes to 4 core classes for easier use and maintenance
  - **Removed**: `SplurgeTabularConfigurationError`, `SplurgeTabularColumnError`, `SplurgeTabularRowError`, `SplurgeTabularIndexError`, `SplurgeTabularKeyError`, `SplurgeTabularValidationError`, `SplurgeTabularSchemaError`, `SplurgeTabularStreamError`, `SplurgeTabularEncodingError`, `SplurgeTabularFileError`, `SplurgeTabularFileNotFoundError`, `SplurgeTabularFilePermissionError`
  - **Current**: `SplurgeTabularError` (base), `SplurgeTabularTypeError`, `SplurgeTabularValueError`, `SplurgeTabularLookupError`
- **Exception Structure**: Updated exception constructor to use `details` dictionary instead of `context`
  - Exceptions now format as: `"[domain] Message (key1='value1', key2='value2')"`
  - Structured error information available via `exc.details` dictionary
- **Type Validation**: Added explicit type checking for `header_rows` parameter in `TabularDataModel.__init__`
  - Now raises `SplurgeTabularTypeError` when `header_rows` is not an integer

### Removed
- **ErrorCode Enum**: Removed `splurge_tabular.error_codes.ErrorCode` enum module
  - Error codes are now optional string values passed to exception constructors
  - Use `details` dictionary for structured error information instead

### Fixed
- **Empty Row Handling**: Fixed tests that incorrectly assumed empty rows were preserved when `skip_empty_rows=True` (default)
  - Updated tests to use `skip_empty_rows=False` when testing empty row behavior
- **Exception Message Format**: Standardized exception string representation to include domain prefix
  - Format: `"[splurge-tabular.type] Message (details)"` for better error identification

### Documentation
- **API Reference**: Completely updated `docs/api/API-REFERENCE.md` to reflect current implementation
  - Removed references to non-existent exceptions and ErrorCode enum
  - Updated all exception signatures and examples
  - Added comprehensive examples for typed views and error handling
- **CLI Reference**: Created `docs/cli/CLI-REFERENCE.md` documenting the command-line interface
- **Migration Guide**: Added `docs/notes/MIGRATION-TO-2025.2.0.md` with detailed migration instructions
  - Exception mapping table
  - Code examples for common migration scenarios
  - Testing recommendations
- **Docstrings**: Improved and standardized all docstrings throughout the codebase
  - All docstrings now follow Google-style format
  - Added missing `Args`, `Returns`, `Raises`, and `Yields` sections
  - Ensured docstrings accurately reflect current implementation

### Testing
- **Test Updates**: Updated exception tests to match new exception structure
  - Fixed tests expecting `None` for `details` to expect empty dict `{}`
  - Updated string format assertions to account for domain prefix
  - All 168 tests passing

---

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