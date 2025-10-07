# splurge-tabular Detailed Documentation

> ⚠️ Release notice — Breaking changes in 2025.1.0
>
> The 2025.1.0 release introduces breaking changes to the exceptions and error codes used throughout this library. Code that depends on exact exception classes, message text, or literal error-code strings may require updates.
>
> Highlights:
>
> - Exceptions now include a structured `error_code` (the `ErrorCode` enum in `splurge_tabular.error_codes`) and an optional `context` mapping for additional details.
> - Several exception subclasses were added or reorganized to give callers finer-grained control (configuration, column, index, row, and validation errors).
> - Prefer programmatic checks against `ErrorCode` values and exception classes instead of parsing message strings.
>
> See `docs/API-REFERENCE.md` (ErrorCode and Exceptions sections), `CHANGELOG.md`, and the detailed migration guide at `docs/notes/MIGRATION-TO-2025.1.0.md` for complete migration guidance and examples.

## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [API Reference](#api-reference)
- [Usage Examples](#usage-examples)
- [Error Handling](#error-handling)
- [Performance Considerations](#performance-considerations)
- [Testing](#testing)
- [Contributing](#contributing)

## Overview

splurge-tabular is a modern Python library for tabular data processing that provides both in-memory and streaming capabilities. It's designed for production use with comprehensive error handling, type safety, and high test coverage.

### Key Features
- **Dual Processing Modes**: Memory and streaming models
- **Type Safety**: Full type annotations
- **Error Resilience**: Comprehensive exception handling
- **High Performance**: Optimized for various data sizes
- **Production Ready**: 95% test coverage, modern packaging

## Installation

```bash
pip install splurge-tabular
```

### Development Installation

```bash
git clone https://github.com/jim-schilling/splurge-tabular.git
cd splurge-tabular
pip install -e .[dev]
```

## Quick Start

### Basic Usage

```python
from splurge_tabular import TabularDataModel

# Create data
data = [
    ["name", "age", "city"],
    ["Alice", "25", "New York"],
    ["Bob", "30", "London"]
]

# Create model
model = TabularDataModel(data)

# Access data
print(f"Columns: {model.column_names}")
print(f"Rows: {model.row_count}")

for row in model:
    print(row)
```

### Streaming for Large Datasets

```python
from splurge_tabular import StreamingTabularDataModel
import io

# Large CSV data
csv_data = """name,age,city
Alice,25,New York
Bob,30,London
..."""

stream = io.StringIO(csv_data)
model = StreamingTabularDataModel(stream)

for row in model:
    print(row)
```

## API Reference

### TabularDataModel

Full in-memory tabular data processing model.

#### Constructor
```python
TabularDataModel(data: list[list[str]], *, header_rows: int = 1, skip_empty_rows: bool = True)
```

#### Properties
- `column_names: list[str]` - List of column names
- `row_count: int` - Number of data rows
- `column_count: int` - Number of columns

#### Methods
- `column_index(name: str) -> int` - Get column index by name
- `column_values(name: str) -> list[str]` - Get all values for a column
- `cell_value(name: str, row_index: int) -> str` - Get specific cell value
- `row(index: int) -> dict[str, str]` - Get row as dictionary
- `row_as_list(index: int) -> list[str]` - Get row as list
- `__iter__() -> Iterator[list[str]]` - Iterate over rows
- `iter_rows() -> Generator[dict[str, str]]` - Iterate as dictionaries

### StreamingTabularDataModel

Memory-efficient streaming processing for large datasets.

#### Constructor
```python
StreamingTabularDataModel(
    stream: Iterator[list[list[str]]],
    *,
    header_rows: int = 1,
    skip_empty_rows: bool = True,
    chunk_size: int = 1000
)
```

#### Properties
- `column_names: list[str]` - List of column names
- `column_count: int` - Number of columns

#### Methods
- `__iter__() -> Iterator[list[str]]` - Iterate over rows
- `iter_rows() -> Generator[dict[str, str]]` - Iterate as dictionaries
- `clear_buffer() -> None` - Clear internal buffer
- `reset_stream() -> None` - Reset stream position

### Utility Functions

#### Data Processing
```python
from splurge_tabular import process_headers, normalize_rows

# Process headers
header_data = [["Name", "Age"], ["", "Years"]]
processed_data, column_names = process_headers(header_data, header_rows=2)

# Normalize rows
rows = [["Alice", "25"], ["Bob"]]  # Inconsistent lengths
normalized = normalize_rows(rows, skip_empty_rows=True)
```

#### Validation
```python
from splurge_tabular import validate_data_structure, ensure_minimum_columns

# Validate data structure
validate_data_structure(data, expected_type=list, allow_empty=False)

# Ensure minimum columns
padded_row = ensure_minimum_columns(["Alice"], min_columns=2)
# Result: ["Alice", ""]
```

#### File Operations
```python
from splurge_tabular import safe_file_operation
from pathlib import Path

# Safe file path validation
path = safe_file_operation(Path("data.csv"))
```

## Usage Examples

### CSV Processing Pipeline

```python
import csv
from pathlib import Path
from splurge_tabular import TabularDataModel, process_headers

def process_csv_file(file_path: str) -> TabularDataModel:
    """Process CSV file into TabularDataModel."""

    # Read CSV
    with Path(file_path).open('r', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

    # Process headers if needed
    if len(data) > 1:
        processed_data, column_names = process_headers([data[0]], header_rows=1)
        data[0] = processed_data[0]

    # Create model
    model = TabularDataModel(data)

    return model

# Usage
model = process_csv_file("data.csv")
print(f"Processed {model.row_count} rows with columns: {model.column_names}")
```

### JSON to Tabular Conversion

```python
import json
from splurge_tabular import TabularDataModel

def json_to_tabular(json_data: list[dict]) -> TabularDataModel:
    """Convert JSON array to tabular format."""

    if not json_data:
        return TabularDataModel([])

    # Extract headers from first item
    headers = list(json_data[0].keys())

    # Convert to rows
    rows = []
    for item in json_data:
        row = [str(item.get(header, '')) for header in headers]
        rows.append(row)

    # Combine headers and data
    data = [headers] + rows

    return TabularDataModel(data)

# Usage
json_data = [
    {"name": "Alice", "age": 25, "city": "New York"},
    {"name": "Bob", "age": 30, "city": "London"}
]

model = json_to_tabular(json_data)
for row_dict in model.iter_rows():
    print(row_dict)
```

### Batch Processing

```python
from pathlib import Path
from splurge_tabular import TabularDataModel, SplurgeError

def process_batch_files(file_paths: list[str]) -> list[TabularDataModel]:
    """Process multiple files with error handling."""

    results = []
    errors = []

    for file_path in file_paths:
        try:
            # Read and process file
            content = Path(file_path).read_text()
            lines = content.split('\n')
            data = [line.split(',') for line in lines if line.strip()]

            model = TabularDataModel(data)
            results.append(model)

        except SplurgeError as e:
            errors.append((file_path, str(e)))
        except Exception as e:
            errors.append((file_path, f"Unexpected error: {e}"))

    if errors:
        print(f"Processed {len(results)} files successfully")
        print(f"Errors in {len(errors)} files:")
        for file_path, error in errors:
            print(f"  {file_path}: {error}")

    return results
```

### Memory-Efficient Large File Processing

```python
from splurge_tabular import StreamingTabularDataModel
import csv

def process_large_csv_streaming(file_path: str, batch_size: int = 1000):
    """Process large CSV files efficiently."""

    def csv_stream_generator():
        """Generate chunks of CSV data."""
        with open(file_path, 'r', newline='') as f:
            reader = csv.reader(f)
            chunk = []

            for row in reader:
                chunk.append(row)
                if len(chunk) >= batch_size:
                    yield chunk
                    chunk = []

            if chunk:  # Yield remaining rows
                yield chunk

    # Create streaming model
    stream = csv_stream_generator()
    model = StreamingTabularDataModel(stream)

    # Process data
    row_count = 0
    for row in model:
        # Process row (e.g., validate, transform, save to database)
        row_count += 1

        if row_count % 10000 == 0:
            print(f"Processed {row_count} rows")

    print(f"Total processed: {row_count} rows")
    print(f"Columns: {model.column_names}")
```

## Error Handling

### Exception Hierarchy

```
SplurgeError (base)
├── SplurgeParameterError    # Invalid parameters
├── SplurgeValidationError   # Data validation failures
├── SplurgeFileError         # File operation errors
│   ├── SplurgeFileNotFoundError
│   └── SplurgeFilePermissionError
└── SplurgeRangeError        # Index/range errors
```

### Error Handling Examples

```python
from splurge_tabular import (
    TabularDataModel,
    SplurgeParameterError,
    SplurgeValidationError,
    SplurgeFileError
)

def safe_data_processing(data):
    """Process data with comprehensive error handling."""

    try:
        model = TabularDataModel(data)

        # Validate minimum requirements
        if model.row_count == 0:
            raise SplurgeValidationError("No data rows found")

        if model.column_count < 2:
            raise SplurgeValidationError("Minimum 2 columns required")

        return model

    except SplurgeParameterError as e:
        print(f"Parameter error: {e}")
        print(f"Details: {e.details}")
        return None

    except SplurgeValidationError as e:
        print(f"Validation error: {e}")
        print(f"Details: {e.details}")
        return None

    except SplurgeFileError as e:
        print(f"File error: {e}")
        print(f"Details: {e.details}")
        return None

    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
```

## Performance Considerations

### Memory Usage

- **TabularDataModel**: Loads all data into memory
  - Suitable for: Small to medium datasets (< 100MB)
  - Advantages: Fast random access, full feature set

- **StreamingTabularDataModel**: Processes data in chunks
  - Suitable for: Large datasets (> 100MB)
  - Advantages: Low memory footprint, scalable

### Choosing the Right Model

```python
def choose_model(data_size_mb: float, access_pattern: str) -> str:
    """Recommend appropriate model based on requirements."""

    if data_size_mb < 50:
        return "TabularDataModel"  # Small data, use in-memory

    if access_pattern == "sequential":
        return "StreamingTabularDataModel"  # Large data, sequential access

    if access_pattern == "random":
        if data_size_mb < 200:
            return "TabularDataModel"  # Medium data, random access
        else:
            return "StreamingTabularDataModel"  # Large data, streaming preferred

    return "StreamingTabularDataModel"  # Default to streaming
```

### Performance Tips

1. **Use Streaming for Large Files**: Reduces memory usage significantly
2. **Batch Processing**: Process data in chunks when possible
3. **Type Validation**: Enable type checking only when needed
4. **Error Handling**: Use specific exceptions for better performance

## Testing

### Running Tests

```bash
# All tests
python -m pytest

# With coverage
python -m pytest --cov=splurge_tabular --cov-report=html

# Specific test categories
python -m pytest tests/unit/ -v
python -m pytest tests/integration/ -v
python -m pytest tests/e2e/ -v
```

### Test Coverage

- **Unit Tests**: 172 tests covering individual components
- **Integration Tests**: 13 tests for component interactions
- **E2E Tests**: 12 tests for complete workflows
- **Total Coverage**: 95% across all code

### Writing Tests

```python
import pytest
from splurge_tabular import TabularDataModel, SplurgeValidationError

def test_data_validation():
    """Test data validation functionality."""

    # Valid data
    valid_data = [["name", "age"], ["Alice", "25"]]
    model = TabularDataModel(valid_data)
    assert model.row_count == 1

    # Invalid data
    with pytest.raises(SplurgeValidationError):
        TabularDataModel([])  # Empty data
```

## Contributing

### Development Workflow

1. **Research**: Understand requirements and constraints
2. **Plan**: Create detailed implementation plan
3. **Implement**: Write code following TDD/BDD practices
4. **Test**: Ensure comprehensive test coverage
5. **Document**: Update documentation as needed

### Code Standards

- **Type Annotations**: All functions and methods
- **Docstrings**: Google-style docstrings
- **Naming**: descriptive, auxiliary verbs (e.g., `is_valid`, `has_data`)
- **Error Handling**: Use appropriate exception types
- **Testing**: Minimum 85% coverage target

### Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Ensure all tests pass
5. Update documentation
6. Submit pull request

### Commit Message Format

```
type(scope): description

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

---

For more information or support, please open an issue on GitHub.