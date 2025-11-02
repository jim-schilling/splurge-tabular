# Splurge Tabular — API Reference

This document provides a comprehensive reference for the public API of the
`splurge_tabular` package. It includes class and function signatures, short
explanations, usage examples, and details about the custom exception
hierarchy.

This reference is generated and maintained manually. If you update public
APIs, please update this file.

---

## Table of contents

- Overview
- Public modules
  - `splurge_tabular.tabular_data_model` (TabularDataModel, _TypedView)
  - `splurge_tabular.streaming_tabular_data_model` (StreamingTabularDataModel)
  - `splurge_tabular.tabular_utils` (helpers for header and row processing)
  - `splurge_tabular.common_utils` (helper validation and access functions)
  - `splurge_tabular.protocols` (public protocols/interfaces)
  - `splurge_tabular.exceptions` (exception hierarchy)
- Examples
- Tips and best practices

---

## Overview

`splurge_tabular` provides light-weight utilities and runtime models for working
with delimited tabular data (CSV/TSV-like), both in-memory and streaming.

Key concepts:
- **TabularDataModel**: in-memory model built from a list of rows (`list[list[str]]`).
- **StreamingTabularDataModel**: forward-only, memory-efficient model that accepts a
  stream of chunks (`Iterator[list[list[str]]]`).
- **Utilities** in `tabular_utils` and `common_utils` provide header processing,
  normalization, and robust helpers for accessing rows/columns safely.

---

## Module: `splurge_tabular.exceptions`

This module defines a hierarchy of custom exceptions used across the package.
All exceptions derive from `SplurgeTabularError`.

### Public classes

- **SplurgeTabularError**(`message: str`, `*`, `error_code: str | None = None`, `details: dict[str, Any] | None = None`)
  - Base exception for all splurge-tabular errors.
  - Attributes: `message`, `details`, `error_code`, `domain`, `full_code`.
  - `__str__()` returns a formatted string: `"[domain] Message (details)"`.
  - The `details` parameter is a dictionary that defaults to an empty dict `{}`.

- **SplurgeTabularTypeError**(`SplurgeTabularError`)
  - Raised for invalid types or missing values where types are required.
  - Domain: `"splurge-tabular.type"`.

- **SplurgeTabularValueError**(`SplurgeTabularError`)
  - Raised for invalid values or out-of-range values.
  - Domain: `"splurge-tabular.value"`.

- **SplurgeTabularLookupError**(`SplurgeTabularValueError`)
  - Raised for missing lookups or out-of-bounds lookups.
  - Used when a required key is missing from a dictionary or mapping, or when
    an index is out of bounds for a list or sequence.
  - Domain: `"splurge-tabular.lookup"`.

### Exception details

The `details` dictionary commonly includes:
- `param` — the parameter name (e.g., `"header_rows"`, `"chunk_size"`).
- `value` or `received_type` — the provided value or type name.
- `column` or `name` — column name when column-specific errors occur.
- `index` / `max_index` — index-related context for out-of-range errors.

### Exception message format

Exceptions format their string representation as:
```
"[domain] Message (key1='value1', key2='value2')"
```

For example:
- `"[splurge-tabular.value] Data cannot be empty (param='data')"`
- `"[splurge-tabular.lookup] Row index 5 out of range (index='5', max_index='3')"`

---

## Module: `splurge_tabular.tabular_data_model`

### Public API

- **class TabularDataModel**

  - **Constructor:**
    ```python
    TabularDataModel(
        data: list[list[str]],
        *,
        header_rows: int = 1,
        skip_empty_rows: bool = True
    )
    ```
    - `data`: Required list of rows (each row is a list of strings).
    - `header_rows`: Number of header rows to merge into column names (default: 1).
    - `skip_empty_rows`: Whether to skip empty rows in data (default: True).
    - Raises:
      - `SplurgeTabularValueError`: If data is empty.
      - `SplurgeTabularTypeError`: If `header_rows` is not an integer or data is not a list of lists.
      - `SplurgeTabularValueError`: If `header_rows` is negative.

  - **Properties:**
    - `column_names -> list[str]` — List of column names in order.
    - `row_count -> int` — Number of data rows (excluding header rows).
    - `column_count -> int` — Number of columns.

  - **Methods:**
    - `column_index(name: str) -> int`
      - Returns zero-based index for a column name.
      - Raises `SplurgeTabularLookupError` if column name is not found.

    - `column_type(name: str) -> DataType`
      - Returns inferred data type for a column (lazy cached).
      - Raises `SplurgeTabularLookupError` if column name is not found.

    - `column_values(name: str) -> list[str]`
      - Returns all raw values for a column as strings.
      - Raises `SplurgeTabularLookupError` if column name is not found.

    - `cell_value(name: str, row_index: int) -> str`
      - Returns raw cell value as a string.
      - Raises `SplurgeTabularLookupError` if column name is not found or row index is out of range.

    - `row(index: int) -> dict[str, str]`
      - Returns a row as a dictionary mapping column names to values.
      - Raises `SplurgeTabularLookupError` if row index is out of range.

    - `row_as_list(index: int) -> list[str]`
      - Returns a row as a list of values.
      - Raises `SplurgeTabularLookupError` if row index is out of range.

    - `row_as_tuple(index: int) -> tuple[str, ...]`
      - Returns a row as a tuple of values.
      - Raises `SplurgeTabularLookupError` if row index is out of range.

    - `iter_rows() -> Generator[dict[str, str], None, None]`
      - Yields rows as dictionaries with column names as keys.

    - `iter_rows_as_tuples() -> Generator[tuple[str, ...], None, None]`
      - Yields rows as tuples of values.

    - `__iter__() -> Iterator[list[str]]`
      - Iterates over rows as lists of strings.

    - `to_typed(type_configs: dict[DataType, Any] | None = None) -> _TypedView`
      - Returns a typed view wrapper that converts cell strings to typed Python values.
      - `type_configs`: Optional overrides for default type conversion behavior.

- **class _TypedView**

  - Lightweight view that converts cell strings to typed Python values using
    `splurge_typer`'s `TypeInference` and `String` helpers.
  - Methods mirror the read-only accessors of `TabularDataModel` but return typed values.
  - Provides the same properties and methods as `TabularDataModel`:
    - `column_names`, `row_count`, `column_count`
    - `column_index(name: str) -> int`
    - `column_type(name: str) -> DataType`
    - `column_values(name: str) -> list[object]`
    - `cell_value(name: str, row_index: int) -> object`
    - `row(index: int) -> dict[str, object]`
    - `row_as_list(index: int) -> list[object]`
    - `row_as_tuple(index: int) -> tuple[object, ...]`
    - `iter_rows() -> Generator[dict[str, object], None, None]`
    - `iter_rows_as_tuples() -> Generator[tuple[object, ...], None, None]`
    - `__iter__() -> Iterator[list[object]]`

### Examples

```python
from splurge_tabular.tabular_data_model import TabularDataModel

data = [["name", "age"], ["Alice", "30"], ["Bob", "25"]]
model = TabularDataModel(data, header_rows=1)
print(model.column_names)  # ['name', 'age']
print(model.column_index('age'))  # 1
print(model.cell_value('age', 0))  # '30'

typed = model.to_typed()
print(typed.cell_value('age', 0))  # 30 (int) if inference yields integer

# Iterate over rows as dictionaries
for row_dict in model.iter_rows():
    print(row_dict)  # {'name': 'Alice', 'age': '30'}, etc.
```

---

## Module: `splurge_tabular.streaming_tabular_data_model`

### Public API

- **class StreamingTabularDataModel**

  - **Constructor:**
    ```python
    StreamingTabularDataModel(
        stream: Iterator[list[list[str]]],
        *,
        header_rows: int = 1,
        skip_empty_rows: bool = True,
        chunk_size: int = 1000
    )
    ```
    - `stream`: Iterator over chunks; each chunk is a list of rows (`list[list[str]]`).
    - `header_rows`: Number of header rows to merge into column names (default: 1).
    - `skip_empty_rows`: Whether to skip empty rows in data (default: True).
    - `chunk_size`: Maximum number of rows to keep in memory buffer (default: 1000, minimum: 100).
    - Raises:
      - `SplurgeTabularTypeError`: If stream is `None`.
      - `SplurgeTabularValueError`: If `header_rows` is negative or `chunk_size` is less than 100.

  - **Properties:**
    - `column_names -> list[str]` — List of column names in order.
    - `column_count -> int` — Number of columns.

  - **Methods:**
    - `column_index(name: str) -> int`
      - Returns zero-based index for a column name.
      - Raises `SplurgeTabularLookupError` if column name is not found.

    - `__iter__() -> Generator[list[str], None, None]`
      - Iterates over rows as lists of strings.
      - Yields rows from buffer first, then from stream.
      - New column names are auto-created if later rows contain more columns than the header.

    - `iter_rows() -> Generator[dict[str, str], None, None]`
      - Yields rows as dictionaries with column names as keys.

    - `iter_rows_as_tuples() -> Generator[tuple[str, ...], None, None]`
      - Yields rows as tuples of values.

    - `clear_buffer() -> None`
      - Clears the current buffer to free memory.
      - Note that buffered rows will not be available for iteration after calling this method.

    - `reset_stream() -> None`
      - Clears the buffer and resets initialization state.
      - Note: This does not actually reset the underlying stream iterator.
      - You must provide a new stream iterator if you want to re-read from the beginning.

### Examples

```python
from splurge_tabular.streaming_tabular_data_model import StreamingTabularDataModel

# A simple stream that yields one chunk
stream = iter([[["h1", "h2"], ["r1", "r2"]]])
model = StreamingTabularDataModel(stream, header_rows=1)
for row in model:
    print(row)  # ['r1', 'r2']

# Iterate as dictionaries
for row_dict in model.iter_rows():
    print(row_dict)  # {'h1': 'r1', 'h2': 'r2'}
```

---

## Module: `splurge_tabular.tabular_utils`

Public helpers for header processing and row normalization.

### Functions

- **process_headers**(`header_data: list[list[str]]`, `*`, `header_rows: int`) -> `tuple[list[list[str]], list[str]]`
  - Processes header rows and returns processed header data and column names.
  - Merges multiple header rows if `header_rows > 1`.
  - Standardizes column names and pads missing columns with generated names.

- **normalize_rows**(`rows: list[list[str]]`, `*`, `skip_empty_rows: bool`) -> `list[list[str]]`
  - Normalizes rows to equal length and optionally drops empty rows.
  - Pads shorter rows with empty strings to match the maximum column count.

- **should_skip_row**(`row: list[str]`) -> `bool`
  - Returns `True` if a row should be skipped because it is empty.
  - Checks if all cells in the row are empty or contain only whitespace.

- **auto_column_names**(`count: int`) -> `list[str]`
  - Generates default column names.
  - Returns a list of strings in format `"column_0"`, `"column_1"`, etc.

### Examples

```python
from splurge_tabular.tabular_utils import process_headers

headers, colnames = process_headers([["Name", ""], ["", "City"]], header_rows=2)
# colnames will be merged headers
```

---

## Module: `splurge_tabular.common_utils`

Public helper functions for validation and data processing.

### Functions

- **standardize_column_names**(`headers: list[str]`, `*`, `fill_empty: bool = True`, `prefix: str = "column_"`) -> `list[str]`
  - Standardizes column names by filling empty headers with generated names.
  - Example: `["Name", "", "City"]` -> `["Name", "column_1", "City"]`.

- **ensure_minimum_columns**(`row: list[str]`, `min_columns: int`, `*`, `fill_value: str = ""`) -> `list[str]`
  - Ensures a row has at least the minimum number of columns.
  - Pads the row with `fill_value` if needed.

- **batch_validate_rows**(`rows: Iterable[list[str]]`, `*`, `min_columns: int | None = None`, `max_columns: int | None = None`, `skip_empty: bool = True`) -> `Iterator[list[str]]`
  - Validates and normalizes rows in a batch operation.
  - Raises `SplurgeTabularTypeError` if a row is not a list.
  - Yields validated and normalized rows.

- **normalize_string**(`value: str | None`, `*`, `trim: bool = True`, `handle_empty: bool = True`, `empty_default: str = ""`) -> `str`
  - Normalizes string values with consistent handling of None, empty, and whitespace.

- **is_empty_or_none**(`value: Any`, `*`, `trim: bool = True`) -> `bool`
  - Checks if a value is None, empty, or contains only whitespace.

### Examples

```python
from splurge_tabular.common_utils import ensure_minimum_columns, standardize_column_names

# Pad row to minimum columns
row = ["a", "b"]
padded = ensure_minimum_columns(row, min_columns=4)  # ["a", "b", "", ""]

# Standardize column names
headers = ["Name", "", "City"]
standardized = standardize_column_names(headers)  # ["Name", "column_1", "City"]
```

---

## Module: `splurge_tabular.protocols`

This module contains protocol (interface) definitions used by the models.

### Protocols

- **TabularDataProtocol**
  - Protocol for tabular data models.
  - Defines the interface that all tabular data models should implement.
  - Includes properties: `column_names`, `row_count`, `column_count`.
  - Includes methods: `column_index()`, `column_type()`, `column_values()`,
    `cell_value()`, `row()`, `row_as_list()`, `row_as_tuple()`, `iter_rows()`,
    `iter_rows_as_tuples()`, `__iter__()`.

- **StreamingTabularDataProtocol**
  - Protocol for streaming tabular data models.
  - Defines the minimal interface for streaming data models.
  - Includes properties: `column_names`, `column_count`.
  - Includes methods: `column_index()`, `__iter__()`, `iter_rows()`,
    `iter_rows_as_tuples()`, `clear_buffer()`, `reset_stream()`.

Refer to the module source code for full method/property signatures.

---

## Examples

### Simple CSV-like in-memory example

```python
from splurge_tabular.tabular_data_model import TabularDataModel

data = [
    ['id', 'name', 'age'],
    ['1', 'Alice', '30'],
    ['2', 'Bob', '25'],
]
model = TabularDataModel(data, header_rows=1)
for r in model.iter_rows():
    print(r)  # {'id': '1', 'name': 'Alice', 'age': '30'}, etc.
```

### Streaming example

```python
from splurge_tabular.streaming_tabular_data_model import StreamingTabularDataModel

# A stream that yields one chunk at a time
stream = iter([
    [['id', 'name'], ['1', 'Alice'], ['2', 'Bob']],
])
model = StreamingTabularDataModel(stream, header_rows=1)
for r in model:
    print(r)  # ['1', 'Alice'], ['2', 'Bob']
```

### Typed view example

```python
from splurge_tabular.tabular_data_model import TabularDataModel

data = [["name", "age", "active"], ["Alice", "30", "true"], ["Bob", "25", "false"]]
model = TabularDataModel(data)
typed = model.to_typed()

# Access typed values
age = typed.cell_value('age', 0)  # 30 (int)
active = typed.cell_value('active', 0)  # True (bool)

# Iterate over typed rows
for row in typed.iter_rows():
    print(row)  # {'name': 'Alice', 'age': 30, 'active': True}, etc.
```

---

## Error handling

### Recommended practices

- Prefer catching specific exceptions (e.g., `SplurgeTabularLookupError`) when
  reacting to user input errors.
- Access the `details` dictionary for structured error information.
- Use `message` attribute for human-readable error messages.

### Example error handling

```python
from splurge_tabular.exceptions import SplurgeTabularLookupError

try:
    model.column_index('missing')
except SplurgeTabularLookupError as e:
    print(f"Error: {e.message}")
    print(f"Details: {e.details}")  # {'column': 'missing'}
    # Handle missing column
```

---

## Tips and best practices

- Use the typed view (`to_typed()`) when downstream code expects Python
  native types (int, float, bool) rather than raw strings.
- When using `StreamingTabularDataModel`, ensure the stream yields chunks in
  the expected format (`list[list[str]]`), and that `chunk_size` is sufficiently
  large to prevent excessive re-buffering (minimum: 100).
- The `header_rows` parameter allows merging multiple header rows into a single
  column name (e.g., `["Personal", "Name"]` becomes `"Personal_Name"`).
- Empty rows are skipped by default (`skip_empty_rows=True`). Set to `False`
  if you need to preserve empty rows in your data.

---
