# splurge-tabular
[![PyPI version](https://badge.fury.io/py/splurge-dsv.svg)](https://pypi.org/project/splurge-dsv/)
[![Python versions](https://img.shields.io/pypi/pyversions/splurge-tabular.svg)](https://pypi.org/project/splurge-dsv/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

[![CI](https://github.com/jim-schilling/splurge-tabular/actions/workflows/ci-quick-test.yml/badge.svg)](https://github.com/jim-schilling/splurge-tabular/actions/workflows/ci-quick-test.yml)
[![Coverage](https://img.shields.io/badge/coverage-96%25-brightgreen.svg)](https://github.com/jim-schilling/splurge-tabular)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![mypy](https://img.shields.io/badge/mypy-checked-black)](https://mypy-lang.org/)

A modern, high-performance Python library for tabular data processing with both in-memory and streaming capabilities.

> ⚠️ Release notice — Breaking changes in 2025.1.0
>
> The 2025.1.0 release introduces breaking changes to the exceptions and error codes raised by this library. Callers that depend on exact exception classes, message text, or literal error-code strings may need to update their code.
>
> Key changes:
>
> - Exceptions now carry structured metadata: an `error_code` (an `ErrorCode` enum) and an optional `context` dict.
> - Some error types were reorganized into more specific subclasses (for example, configuration-, column-, row-, and validation-related errors).
> - The textual formatting of some exception messages was stabilized to preserve backward compatibility where possible, but callers should prefer programmatic inspection of `error_code` and exception class.
>
> Migration:
>
> - Inspect raised exceptions for `error_code` (recommended) rather than parsing messages.
> - See `docs/API-REFERENCE.md` (ErrorCode section) and `CHANGELOG.md` for the full list of changed codes and examples.
>
> If you rely on the previous exception shapes or messages and need help migrating, open an issue or consult the API reference in `docs/` or the detailed migration guide: `docs/notes/MIGRATION-TO-2025.1.0.md`.

## ✨ Features

- **Dual Processing Modes**: Choose between memory-efficient streaming or full in-memory processing
- **Type Safety**: Full type annotations with modern Python typing
- **Robust Error Handling**: Comprehensive exception hierarchy with detailed error messages
- **Flexible Data Input**: Support for CSV, JSON, and custom data formats
- **High Performance**: Optimized for both small datasets and large-scale processing
- **Production Ready**: 96% test coverage with 219 comprehensive tests
- **Modern Packaging**: Built with modern Python standards and best practices

## 🚀 Quick Start

### Installation

```bash
pip install splurge-tabular
```

### Basic Usage

```python
from splurge_tabular import TabularDataModel, StreamingTabularDataModel

# In-memory processing
data = [
    ["name", "age", "city"],
    ["Alice", "25", "New York"],
    ["Bob", "30", "London"]
]

model = TabularDataModel(data)
print(f"Columns: {model.column_names}")
print(f"Row count: {model.row_count}")

# Access data
for row in model:
    print(row)

# Streaming processing for large datasets
import io
csv_data = """name,age,city
Alice,25,New York
Bob,30,London"""

stream = io.StringIO(csv_data)
streaming_model = StreamingTabularDataModel(stream)
for row in streaming_model:
    print(row)
```

## 📋 Requirements

- Python 3.10+
- Dependencies automatically managed via `pip`

## 🧪 Testing

The library includes comprehensive test suites:

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=splurge_tabular

# Run specific test categories
python -m pytest tests/unit/        # Unit tests
python -m pytest tests/integration/ # Integration tests
python -m pytest tests/e2e/         # End-to-end tests
```

## 📚 Documentation

- [Detailed Documentation](docs/README-details.md) - Comprehensive API reference and examples
- [Changelog](CHANGELOG.md) - Version history and release notes

## 🏗️ Architecture

### Core Components

- **`TabularDataModel`**: Full in-memory tabular data processing
- **`StreamingTabularDataModel`**: Memory-efficient streaming processing
- **Exception Hierarchy**: Comprehensive error handling with `SplurgeError` base class
- **Utility Functions**: Data validation, normalization, and processing helpers

### Design Principles

- **SOLID Principles**: Single responsibility, open-closed, etc.
- **DRY**: Don't Repeat Yourself
- **KISS**: Keep It Simple, Stupid
- **Type Safety**: Full type annotations throughout
- **Error Resilience**: Fail fast with clear error messages

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/jim-schilling/splurge-tabular.git
cd splurge-tabular

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .[dev]

# Run tests
python -m pytest
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Jim Schilling**
- GitHub: [@jim-schilling](https://github.com/jim-schilling)

## 🙏 Acknowledgments

- Built with modern Python best practices
- Inspired by the need for robust, type-safe tabular data processing
- Thanks to the Python community for excellent tools and libraries
