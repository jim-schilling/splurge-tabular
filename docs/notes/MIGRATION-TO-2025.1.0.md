# Migration guide — 2025.1.0

This document explains breaking changes introduced in splurge-tabular 2025.1.0 and provides migration steps, examples, and an error-code mapping to help upgrade safely.

Summary
-------

- Release: 2025.1.0
- Area affected: Exceptions and error codes
- Migration goal: Move callers from relying on message text and loose exception types to programmatic checks using exception classes and the new `ErrorCode` enum (`splurge_tabular.error_codes.ErrorCode`).

Why this change
----------------

Historically, callers inspected exception message text or caught coarse exception classes. That approach is brittle. In 2025.1.0 we improved observability and programmatic handling by:

- Adding an `error_code` (an `ErrorCode` enum) to most exceptions.
- Adding `context: dict[str, str] | None` to provide structured details for programmatic consumption.
- Introducing more specific exception subclasses (configuration, column, row, validation, file, etc.) so callers can catch precisely what they expect.

High-level migration steps
-------------------------

1. Stop parsing exception messages. Instead, inspect the exception class and `error_code` attribute.
2. Update except blocks to catch the new, more specific exception subclasses when appropriate.
3. When matching on specific errors, switch to `if exc.error_code == ErrorCode.SOMETHING:` rather than text matching.
4. Add tests that assert `exception.error_code` where business logic depends on specific error semantics.

Quick examples
--------------

Before (old pattern — fragile):

```python
try:
    model = TabularDataModel(data)
except Exception as e:
    # Previously code parsed message text
    if "header_rows" in str(e):
        handle_header_error()
    else:
        raise
```

After (preferred):

```python
from splurge_tabular.error_codes import ErrorCode
from splurge_tabular.exceptions import SplurgeTabularConfigurationError

try:
    model = TabularDataModel(data)
except SplurgeTabularConfigurationError as exc:
    if exc.error_code == ErrorCode.CONFIG_INVALID:
        handle_header_error()
    else:
        raise
```

Mapping of common changes
-------------------------

The table below shows common error categories and suggested checks. This is not exhaustive — consult `docs/API-REFERENCE.md` -> Exceptions / ErrorCode for a complete list.

- Old behavior: raised generic TypeError for invalid arguments
  - New: SplurgeTabularTypeError with ErrorCode.TYPE_INVALID
- Old behavior: ValueError or generic validation errors
  - New: SplurgeTabularValidationError with ErrorCode.VALIDATION_* (see enum)
- Old behavior: KeyError when a column name was missing
  - New: SplurgeTabularColumnError with ErrorCode.COLUMN_NOT_FOUND (and `context['available_hint']`)
- Old behavior: IndexError for row/column out of range
  - New: SplurgeTabularIndexError with ErrorCode.INDEX_OUT_OF_RANGE

Inspecting `error_code` and `context`
-----------------------------------

All high-level SplurgeTabular exceptions now expose two programmatic attributes in addition to the message:

- `error_code`: an `ErrorCode` enum value. Use it for exact programmatic checks.
- `context`: optional dict with string keys/values providing extra details (e.g., `{'row_index': '3'}`, `{'column': 'id'}`, `{'available_hint': "['a','b',...]"}`).

Testing recommendations
-----------------------

- Replace existing tests that assert exact exception message text with assertions on `error_code` and/or `exc.__class__`.
- Add at least one test to ensure a given operation raises the expected `ErrorCode`.

Example test before/after
```python
def test_old():
    with pytest.raises(ValueError):
        TabularDataModel(invalid)

def test_new():
    with pytest.raises(SplurgeTabularValidationError) as ei:
        TabularDataModel(invalid)
    assert ei.value.error_code == ErrorCode.VALIDATION_EMPTY_NOT_ALLOWED
```

Additional notes
----------------
- Backwards compatibility: We attempted to keep message formatting stable where reasonable, but message text should not be relied upon going forward.
- If your code must run on multiple library versions, prefer duck-typed checks: check for attribute `error_code` first, fallback to legacy message parsing only as last resort.

Where to find details
---------------------

- ErrorCode enum: `splurge_tabular/error_codes.py`
- Exceptions: `splurge_tabular/exceptions.py`
- API reference: `docs/API-REFERENCE.md` (contains ErrorCode and example usage)
- Changelog: `CHANGELOG.md` (release notes for 2025.1.0)

If you need assistance migrating large codebases, open an issue or start a discussion in the repository and provide examples of the existing error handling pattern. We can help craft targeted migration guidance.
