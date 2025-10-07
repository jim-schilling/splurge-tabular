# splurge-tabular

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-197%20passed-green.svg)](https://github.com/jim-schilling/splurge-tabular)
[![Coverage](https://img.shields.io/badge/coverage-95%25-green.svg)](https://github.com/jim-schilling/splurge-tabular)

A modern, high-performance Python library for tabular data processing with both in-memory and streaming capabilities.

## ✨ Features

- **Dual Processing Modes**: Choose between memory-efficient streaming or full in-memory processing
- **Type Safety**: Full type annotations with modern Python typing
- **Robust Error Handling**: Comprehensive exception hierarchy with detailed error messages
- **Flexible Data Input**: Support for CSV, JSON, and custom data formats
- **High Performance**: Optimized for both small datasets and large-scale processing
- **Production Ready**: 95% test coverage with 197 comprehensive tests
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
