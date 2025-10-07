# Splurge Tabular — API Reference

This document provides a comprehensive reference for the public API of the
`splurge_tabular` package. It includes class and function signatures, short
explanations, usage examples, and details about the custom exception
hierarchy (including error codes and context keys emitted by the library).

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
  - `splurge_tabular.exceptions` (exception hierarchy, error codes, context)
- Examples
- Error codes and context keys
- Tips and best practices

---

## Overview

`splurge_tabular` provides light-weight utilities and runtime models for working
with delimited tabular data (CSV/TSV-like), both in-memory and streaming.

Key concepts:
- TabularDataModel: in-memory model built from a list of rows (list[list[str]]).
- StreamingTabularDataModel: forward-only, memory-efficient model that accepts a
  stream of chunks (Iterator[list[list[str]]]).
- Utilities in `tabular_utils` and `common_utils` provide header processing,
  normalization, and robust helpers for accessing rows/columns safely.

---

## Module: `splurge_tabular.exceptions`

This module defines a hierarchy of custom exceptions used across the package.
All exceptions derive from `SplurgeTabularError`.

Public classes

- SplurgeTabularError(message: str, *, details: str | None = None, error_code: str | None = None, context: dict[str, str] | None = None)
  - Base exception. Attributes: `message`, `details`, `error_code`, `context`.
  - `__str__()` returns a readable string: `"Message (Details: ...) (code=...) (Context: k=v, ...)"`.

- SplurgeTabularTypeError(SplurgeTabularError)
  - Raised for invalid types or missing values where types are required.

- SplurgeTabularValueError(SplurgeTabularError)
  - Raised for invalid values or out-of-range values.

- SplurgeTabularKeyError(SplurgeTabularValueError)
  - Raised when a required mapping key is missing.

- SplurgeTabularIndexError(SplurgeTabularValueError)
  - Raised for out-of-range list indices.

- SplurgeTabularColumnError(SplurgeTabularValueError)
  - Column-specific errors (missing columns, dupes, etc.).

- SplurgeTabularRowError(SplurgeTabularValueError)
  - Row related errors (out-of-range indices, malformed rows).

- SplurgeTabularValidationError(SplurgeTabularError)
  - Validation failures.

- SplurgeTabularSchemaError(SplurgeTabularValidationError)
  - Schema mismatch errors.

- SplurgeTabularStreamError(SplurgeTabularError)
  - Streaming-specific errors.

- SplurgeTabularEncodingError(SplurgeTabularError)
  - Encoding/decoding issues.

- SplurgeTabularFileError(SplurgeTabularError)
  - File operation errors.

- SplurgeTabularFileNotFoundError(SplurgeTabularFileError)
  - File not found.

- SplurgeTabularFilePermissionError(SplurgeTabularFileError)
  - File permission errors.

- SplurgeTabularConfigurationError(SplurgeTabularValueError)
  - Configuration or parameter semantic errors.


### Error codes (common)

The library attaches optional `error_code` strings to many raised exceptions
where a machine-friendly code is useful. Common codes used in the library:

- `TYPE_INVALID` — invalid or unexpected type for a parameter.
- `CONFIG_INVALID` — a configuration parameter has an invalid value (out of range).
- `COLUMN_NOT_FOUND` — requested column name does not exist in the current model.
- `ROW_OUT_OF_RANGE` — requested row index is outside the available rows.
- `INDEX_OUT_OF_RANGE` — index provided into a sequence is out of range.
- `KEY_NOT_FOUND` — requested mapping key not present.
- `VALIDATION_EMPTY_NOT_ALLOWED` — empty data not allowed for this parameter.

Context keys provided vary by raise site but commonly include:
- `param` — the parameter name (e.g., `header_rows`, `chunk_size`).
- `value` or `received_type` — the provided value or type name.
- `column` — column name when column-specific errors occur.
- `requested_index` / `max_index` — index-related context.
- `available_hint` — a short hint showing available keys/columns when a lookup fails.


### ErrorCode enum (canonical)

The project provides a centralized `ErrorCode` enum in
`splurge_tabular.error_codes.ErrorCode`. Use these canonical members when
checking or raising errors. The enum is str-backed; exception constructors
accept either the enum member or a plain string.

Members:

- `ErrorCode.TYPE_INVALID` — equivalent string: `"TYPE_INVALID"`.
- `ErrorCode.CONFIG_INVALID` — equivalent string: `"CONFIG_INVALID"`.
- `ErrorCode.COLUMN_NOT_FOUND` — equivalent string: `"COLUMN_NOT_FOUND"`.
- `ErrorCode.ROW_OUT_OF_RANGE` — equivalent string: `"ROW_OUT_OF_RANGE"`.
- `ErrorCode.INDEX_OUT_OF_RANGE` — equivalent string: `"INDEX_OUT_OF_RANGE"`.
- `ErrorCode.KEY_NOT_FOUND` — equivalent string: `"KEY_NOT_FOUND"`.
- `ErrorCode.VALIDATION_EMPTY_NOT_ALLOWED` — equivalent string: `"VALIDATION_EMPTY_NOT_ALLOWED"`.

Example usage (recommended):

```
from splurge_tabular.error_codes import ErrorCode

try:
  model.column_index('missing')
except SplurgeTabularColumnError as e:
  if e.error_code == ErrorCode.COLUMN_NOT_FOUND.value:
    # handle missing column
    print('Missing column; available hint:', e.context.get('available_hint'))
  else:
    raise
```

When raising exceptions inside the library prefer passing the enum member
directly; the base exception will coerce it to a stable string value: 

```
raise SplurgeTabularTypeError('bad param', error_code=ErrorCode.TYPE_INVALID)
```


---

## Module: `splurge_tabular.tabular_data_model`

Public API

- class TabularDataModel
  - Constructor:
    - TabularDataModel(data: list[list[str]], *, header_rows: int = 1, skip_empty_rows: bool = True)
    - `data`: required list of rows (each row is a list of strings). Use
      `validate_data_structure` or rely on the constructor to validate input.
    - Raises `SplurgeTabularTypeError`, `SplurgeTabularConfigurationError` for
      invalid parameters.

  - Properties:
    - `column_names -> list[str]` — list of column names.
    - `row_count -> int` — number of data rows.
    - `column_count -> int` — number of columns.

  - Methods:
    - `column_index(name: str) -> int` — returns zero-based index for a column name. Raises `SplurgeTabularColumnError` if missing.
    - `column_type(name: str) -> DataType` — returns inferred data type for a column (lazy cached).
    - `column_values(name: str) -> list[str]` — all raw values for a column.
    - `cell_value(name: str, row_index: int) -> str` — raw cell value; raises `SplurgeTabularRowError` for out-of-range row.
    - `iter_rows()` — yield rows as dicts (column_name -> value).
    - `iter_rows_as_tuples()` — yield rows as tuples.
    - `row(index: int)` / `row_as_list(index)` / `row_as_tuple(index)` — accessors for rows.
    - `to_typed(type_configs=None) -> _TypedView` — returns a typed view wrapper.

- class _TypedView
  - Lightweight view that converts cell strings to typed Python values using `splurge_typer`'s `TypeInference` and `String` helpers.
  - Methods mirror the read-only accessors of `TabularDataModel` but return typed values.

Examples

```
from splurge_tabular.tabular_data_model import TabularDataModel

data = [["name", "age"], ["Alice", "30"], ["Bob", "25"]]
model = TabularDataModel(data, header_rows=1)
print(model.column_names)  # ['name', 'age']
print(model.column_index('age'))  # 1
print(model.cell_value('age', 0))  # '30'

typed = model.to_typed()
print(typed.cell_value('age', 0))  # 30 (int) if inference yields integer
```

---

## Module: `splurge_tabular.streaming_tabular_data_model`

Public API

- class StreamingTabularDataModel
  - Constructor:
    - StreamingTabularDataModel(stream: Iterator[list[list[str]]], *, header_rows: int = 1, skip_empty_rows: bool = True, chunk_size: int = 1000)
    - `stream` is an iterator over chunks; each chunk is a list of rows (list[list[str]]).
    - `chunk_size` must be >= 100 (MIN_CHUNK_SIZE); otherwise `SplurgeTabularConfigurationError` is raised.
    - If `stream` is `None`, `SplurgeTabularTypeError` is raised.

  - Properties/methods:
    - `column_names`, `column_count`
    - `column_index(name: str) -> int` — raises `SplurgeTabularColumnError` if not found.
    - Iteration yields rows as lists of strings. Rows may be padded or extend columns dynamically; new column names are generated for extra columns.
    - `iter_rows()` / `iter_rows_as_tuples()` — utility iterators that mirror TabularDataModel.
    - `clear_buffer()` and `reset_stream()` for stream management.

Examples

```
from splurge_tabular.streaming_tabular_data_model import StreamingTabularDataModel

# A simple stream that yields one chunk
stream = iter([[["h1", "h2"], ["r1", "r2"]]])
model = StreamingTabularDataModel(stream, header_rows=1)
for row in model:
    print(row)
```

---

## Module: `splurge_tabular.tabular_utils`

(See module docstrings for full details; these utilities are used internally and are
exposed for integration tests and advanced usage.)

Public helpers

- `process_headers(header_rows: list[list[str]], *, header_rows: int) -> tuple[list[list[str]], list[str]]`
  - Merge header rows into final `header_data` and `column_names` using standardization rules.

- `normalize_rows(rows: list[list[str]], *, skip_empty_rows: bool = True) -> list[list[str]]`
  - Normalize/pad rows and optionally skip empty rows.

- `standardize_column_names(headers: list[str], *, fill_empty: bool = True, prefix: str = 'column_') -> list[str]`
  - Fill blanks in headers with generated column names.

Examples

```
from splurge_tabular.tabular_utils import process_headers
headers, colnames = process_headers([["Name", ""], ["", "City"]], header_rows=2)
```

---

## Module: `splurge_tabular.common_utils`

Public helpers (selected)

- `safe_file_operation(file_path: str | Path) -> Path`
  - Validate and convert file path; raises `SplurgeTabularTypeError` for invalid inputs. Passes `error_code='TYPE_INVALID'` and context `{'param':'file_path'}` on errors.

- `standardize_column_names(headers: list[str], *, fill_empty: bool = True, prefix: str = 'column_') -> list[str]`

- `ensure_minimum_columns(row: list[str], min_columns: int, *, fill_value: str = '') -> list[str]`

- `safe_index_access(items: list[T], index: int, *, item_name: str = 'item', default: T | None = None) -> T`
  - Returns the indexed item or raises `SplurgeTabularIndexError` (with `error_code='INDEX_OUT_OF_RANGE'` and context containing `requested_index`/`max_index`).

- `safe_dict_access(data: dict[str, T], key: str, *, item_name: str = 'key', default: T | None = None) -> T`
  - Returns the value for `key`, or raises `SplurgeTabularColumnError` or `SplurgeTabularKeyError`.
  - Column errors include `error_code='COLUMN_NOT_FOUND'` and `context={'column': <name>, 'available_hint': <hint>}`.

- `validate_data_structure(data: Any, *, expected_type: type, param_name: str = 'data', allow_empty: bool = True) -> Any`
  - Validates type and emptiness; raises `SplurgeTabularTypeError`, `SplurgeTabularValidationError` with `error_code` and context.

- `create_parameter_validator(validators: dict[str, Callable[[Any], Any]]) -> Callable[[dict[str, Any]], dict[str, Any]]`
  - Helper to create parameter validators.

- `batch_validate_rows(rows: Iterable[list[str]], *, min_columns: int | None = None, max_columns: int | None = None, skip_empty: bool = True) -> Iterator[list[str]]`
  - Validates and normalizes rows in a batch; raises `SplurgeTabularTypeError` for malformed rows.

Examples

```
from splurge_tabular.common_utils import safe_dict_access

d = {'a': 1}
val = safe_dict_access(d, 'a')  # returns 1

try:
    safe_dict_access(d, 'b', item_name='column')
except Exception as e:
    print(e.error_code)  # 'COLUMN_NOT_FOUND'
    print(e.context)
```

---

## Module: `splurge_tabular.protocols`

This module contains protocol (interface) definitions used by the models, such
as `TabularDataProtocol` and `StreamingTabularDataProtocol`. These are typed
contracts useful for testing and integration with alternate data sources.

Refer to the module for full method/property signatures.

---

## Examples

### Simple CSV-like in-memory example

```
from splurge_tabular.tabular_data_model import TabularDataModel

data = [
    ['id', 'name', 'age'],
    ['1', 'Alice', '30'],
    ['2', 'Bob', '25'],
]
model = TabularDataModel(data, header_rows=1)
for r in model.iter_rows():
    print(r)
```

### Streaming example

```
from splurge_tabular.streaming_tabular_data_model import StreamingTabularDataModel

# A stream that yields one chunk at a time
stream = iter([
    [['id', 'name'], ['1', 'Alice'], ['2', 'Bob']],
])
model = StreamingTabularDataModel(stream, header_rows=1)
for r in model:
    print(r)
```

---

## Error codes and recommended handling

- Prefer catching specific exceptions (e.g., `SplurgeTabularColumnError`) when
  reacting to user input errors.
- For programmatic handling, inspect the `error_code` attribute rather than
  parsing human-readable messages.

Example error handling:

```
try:
    model.column_index('missing')
except SplurgeTabularColumnError as e:
    if e.error_code == 'COLUMN_NOT_FOUND':
        # handle missing column
        print('Missing column; available hint:', e.context.get('available_hint'))
    else:
        raise
```

---

## Tips and best practices

- Use `validate_data_structure` in entry points to provide consistent errors.
- Prefer the typed view (`to_typed`) when downstream code expects Python
  native types (int, float, bool) rather than raw strings.
- When using `StreamingTabularDataModel`, ensure the stream yields chunks in
  the expected format (list[list[str]]), and that `chunk_size` is sufficiently
  large to prevent excessive re-buffering.

---

If you want this reference to be machine-generated or trimmed to include only
public symbols discovered automatically, I can produce a generated variant
based on the codebase (docstrings, signatures, and raise-site analysis).
