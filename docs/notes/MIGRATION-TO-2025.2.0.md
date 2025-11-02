# Migration guide — 2025.2.0

This document explains breaking changes introduced in splurge-tabular 2025.2.0 and provides migration steps, examples, and exception mapping guidance to help upgrade safely.

## Summary

- **Release**: 2025.2.0
- **Area affected**: Exception hierarchy and error handling
- **Migration goal**: Update code to use the simplified exception hierarchy and new exception structure with `details` dictionary instead of the removed `ErrorCode` enum and multiple exception subclasses.

## Why this change

In 2025.2.0, we simplified the exception hierarchy and error handling approach:

- **Removed**: `ErrorCode` enum (`splurge_tabular.error_codes.ErrorCode`)
- **Removed**: Many specific exception subclasses (ConfigurationError, ColumnError, RowError, ValidationError, etc.)
- **Simplified**: Exception hierarchy to 4 core classes
- **Updated**: Exception structure uses `details` dictionary (replaces `context`)
- **Changed**: Exception string format includes domain prefix: `"[domain] Message (details)"`

This simplification makes the API easier to use while maintaining structured error information through the `details` dictionary.

## High-level migration steps

1. **Remove `ErrorCode` enum imports and usage** — The enum no longer exists.
2. **Update exception imports** — Use only the 4 available exception classes.
3. **Update exception catching** — Catch the simplified exception hierarchy.
4. **Use `details` dictionary** — Access structured error information via `exc.details` instead of `exc.context`.
5. **Update string matching** — Exception messages now include domain prefix (e.g., `"[splurge-tabular.value]"`).

## Exception hierarchy

### Current (2025.2.0)

```python
SplurgeTabularError (base)
├── SplurgeTabularTypeError
├── SplurgeTabularValueError
└── SplurgeTabularLookupError (subclass of SplurgeTabularValueError)
```

### Removed exceptions

The following exception classes from 2025.1.0 are **no longer available**:

- `SplurgeTabularConfigurationError`
- `SplurgeTabularColumnError`
- `SplurgeTabularRowError`
- `SplurgeTabularKeyError`
- `SplurgeTabularIndexError`
- `SplurgeTabularValidationError`
- `SplurgeTabularSchemaError`
- `SplurgeTabularStreamError`
- `SplurgeTabularEncodingError`
- `SplurgeTabularFileError`
- `SplurgeTabularFileNotFoundError`
- `SplurgeTabularFilePermissionError`

## Exception structure

### Constructor signature

All exceptions follow this pattern:

```python
ExceptionClass(
    message: str,
    *,
    error_code: str | None = None,
    details: dict[str, Any] | None = None
)
```

### Attributes

- `message` (str): Human-readable error message
- `error_code` (str | None): Optional error code string (not an enum)
- `details` (dict[str, Any]): Dictionary of structured error details (defaults to `{}`)
- `domain` (str): Exception domain (e.g., `"splurge-tabular.type"`)
- `full_code` (str): Combined domain and error_code

### String representation

Exceptions format as: `"[domain] Message (key1='value1', key2='value2')"`

Example:
```python
"[splurge-tabular.value] Data cannot be empty (param='data')"
"[splurge-tabular.lookup] Row index 5 out of range (index='5', max_index='3')"
```

## Migration examples

### Example 1: ErrorCode enum removal

**Before (2025.1.0):**
```python
from splurge_tabular.error_codes import ErrorCode
from splurge_tabular.exceptions import SplurgeTabularColumnError

try:
    model.column_index('missing')
except SplurgeTabularColumnError as exc:
    if exc.error_code == ErrorCode.COLUMN_NOT_FOUND:
        handle_missing_column()
```

**After (2025.2.0):**
```python
from splurge_tabular.exceptions import SplurgeTabularLookupError

try:
    model.column_index('missing')
except SplurgeTabularLookupError as exc:
    # Check details dictionary for structured information
    if 'column' in exc.details or 'name' in exc.details:
        handle_missing_column()
    # Or check message content if needed
    if 'not found' in exc.message.lower():
        handle_missing_column()
```

### Example 2: Exception class changes

**Before (2025.1.0):**
```python
from splurge_tabular.exceptions import (
    SplurgeTabularConfigurationError,
    SplurgeTabularValidationError,
    SplurgeTabularColumnError
)

try:
    model = TabularDataModel(data, header_rows=-1)
except SplurgeTabularConfigurationError:
    handle_config_error()
except SplurgeTabularValidationError:
    handle_validation_error()
except SplurgeTabularColumnError:
    handle_column_error()
```

**After (2025.2.0):**
```python
from splurge_tabular.exceptions import (
    SplurgeTabularTypeError,
    SplurgeTabularValueError,
    SplurgeTabularLookupError
)

try:
    model = TabularDataModel(data, header_rows=-1)
except SplurgeTabularValueError as exc:
    # Check details to determine error type
    if exc.details.get('param') == 'header_rows':
        handle_config_error()
    elif exc.details.get('param') == 'data':
        handle_validation_error()
except SplurgeTabularLookupError:
    handle_column_error()
except SplurgeTabularTypeError:
    handle_type_error()
```

### Example 3: Context to Details migration

**Before (2025.1.0):**
```python
try:
    model.column_index('missing')
except SplurgeTabularColumnError as exc:
    column_name = exc.context.get('column')
    available = exc.context.get('available_hint')
```

**After (2025.2.0):**
```python
try:
    model.column_index('missing')
except SplurgeTabularLookupError as exc:
    column_name = exc.details.get('column') or exc.details.get('name')
    # Note: available_hint may not be available in details
```

### Example 4: String message parsing

**Before (2025.1.0):**
```python
try:
    model = TabularDataModel([])
except Exception as e:
    if "cannot be empty" in str(e):
        handle_empty_data()
```

**After (2025.2.0):**
```python
try:
    model = TabularDataModel([])
except SplurgeTabularValueError as exc:
    # Option 1: Check details
    if exc.details.get('param') == 'data':
        handle_empty_data()
    # Option 2: Check message (includes domain prefix)
    if "cannot be empty" in exc.message:
        handle_empty_data()
    # Option 3: Check string representation
    if "cannot be empty" in str(exc):
        handle_empty_data()
```

## Exception mapping guide

### Type errors

**Old**: `SplurgeTabularTypeError` with `ErrorCode.TYPE_INVALID`  
**New**: `SplurgeTabularTypeError`  
**Details keys**: `param`, `value`, `received_type`

```python
# Raised when:
# - header_rows is not an integer
# - data is not a list of lists
# - stream is None
```

### Value errors

**Old**: `SplurgeTabularConfigurationError`, `SplurgeTabularValidationError`  
**New**: `SplurgeTabularValueError`  
**Details keys**: `param`, `value`

```python
# Raised when:
# - data is empty
# - header_rows is negative
# - chunk_size is too small
```

### Lookup errors

**Old**: `SplurgeTabularColumnError`, `SplurgeTabularRowError`, `SplurgeTabularIndexError`, `SplurgeTabularKeyError`  
**New**: `SplurgeTabularLookupError`  
**Details keys**: `column`, `name`, `index`, `max_index`

```python
# Raised when:
# - Column name not found
# - Row index out of range
# - Any lookup operation fails
```

## Common details keys

The `details` dictionary commonly includes:

- `param`: Parameter name (e.g., `"header_rows"`, `"chunk_size"`, `"data"`)
- `value`: Provided value as string (e.g., `"-1"`, `"50"`)
- `received_type`: Type name when type mismatch occurs (e.g., `"str"`, `"float"`)
- `column` or `name`: Column name for column-related errors
- `index`: Row or column index for out-of-range errors
- `max_index`: Maximum valid index
- `row_index`: Row index in batch validation errors

## Testing recommendations

### Update test assertions

**Before:**
```python
def test_column_not_found():
    with pytest.raises(SplurgeTabularColumnError) as exc_info:
        model.column_index('missing')
    assert exc_info.value.error_code == ErrorCode.COLUMN_NOT_FOUND
    assert exc_info.value.context['column'] == 'missing'
```

**After:**
```python
def test_column_not_found():
    with pytest.raises(SplurgeTabularLookupError) as exc_info:
        model.column_index('missing')
    # Check exception class and details
    assert isinstance(exc_info.value, SplurgeTabularLookupError)
    assert exc_info.value.details.get('column') == 'missing' or exc_info.value.details.get('name') == 'missing'
    # Or check message
    assert 'not found' in exc_info.value.message.lower()
```

### Update exception matching

**Before:**
```python
with pytest.raises(SplurgeTabularConfigurationError, match="header_rows"):
    TabularDataModel(data, header_rows=-1)
```

**After:**
```python
# Option 1: Match on exception class and message
with pytest.raises(SplurgeTabularValueError, match="header_rows"):
    TabularDataModel(data, header_rows=-1)

# Option 2: Check details after catching
with pytest.raises(SplurgeTabularValueError) as exc_info:
    TabularDataModel(data, header_rows=-1)
assert exc_info.value.details.get('param') == 'header_rows'
```

## Backward compatibility notes

- **Message text**: While message text format changed (now includes domain prefix), core message content remains similar for easier migration.
- **Exception base class**: `SplurgeTabularError` still exists and can be caught to handle all exceptions.
- **Structured data**: The `details` dictionary provides the same structured information that `context` provided, just under a different attribute name.

## Migration checklist

- [ ] Remove all imports of `ErrorCode` from `splurge_tabular.error_codes`
- [ ] Update exception imports to use only: `SplurgeTabularError`, `SplurgeTabularTypeError`, `SplurgeTabularValueError`, `SplurgeTabularLookupError`
- [ ] Replace `SplurgeTabularConfigurationError` catches with `SplurgeTabularValueError` and check `details['param']`
- [ ] Replace `SplurgeTabularColumnError` catches with `SplurgeTabularLookupError`
- [ ] Replace `SplurgeTabularRowError` and `SplurgeTabularIndexError` catches with `SplurgeTabularLookupError`
- [ ] Replace `exc.context` with `exc.details`
- [ ] Replace `exc.error_code == ErrorCode.X` checks with `exc.details` checks or message parsing
- [ ] Update string matching to account for domain prefix in exception messages
- [ ] Update tests to assert on `details` dictionary instead of `error_code` enum

## Where to find details

- **Exceptions**: `splurge_tabular/exceptions.py`
- **API reference**: `docs/api/API-REFERENCE.md` (contains exception documentation)
- **Changelog**: `CHANGELOG.md` (release notes)
- **Examples**: `examples/api_usage.py` (usage examples)

## Getting help

If you need assistance migrating large codebases or have questions about specific migration scenarios:

1. Review the API reference: `docs/api/API-REFERENCE.md`
2. Check examples: `examples/api_usage.py`
3. Open an issue in the repository with:
   - Your current exception handling code
   - The specific migration challenge you're facing
   - Any error messages you're encountering

---

## Quick reference: Exception mapping table

| Old Exception (2025.1.0) | New Exception (2025.2.0) | Details Keys |
|---------------------------|---------------------------|--------------|
| `SplurgeTabularConfigurationError` | `SplurgeTabularValueError` | `param`, `value` |
| `SplurgeTabularColumnError` | `SplurgeTabularLookupError` | `column`, `name` |
| `SplurgeTabularRowError` | `SplurgeTabularLookupError` | `index`, `max_index` |
| `SplurgeTabularIndexError` | `SplurgeTabularLookupError` | `index`, `max_index` |
| `SplurgeTabularKeyError` | `SplurgeTabularLookupError` | (key-related) |
| `SplurgeTabularValidationError` | `SplurgeTabularValueError` | `param`, `value` |
| `SplurgeTabularTypeError` | `SplurgeTabularTypeError` | `param`, `value`, `received_type` |
| (with `ErrorCode` enum) | (no enum, use `details` dict) | N/A |

---

*Last updated: 2025-02-0X*

