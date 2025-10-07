"""Common utility functions for splurge-tabular package.

This module provides reusable utility functions and patterns to reduce
code duplication across the package.

Copyright (c) 2025 Jim Schilling

Please preserve this header and all related material when sharing!

This module is licensed under the MIT License.
"""

from collections.abc import Callable, Iterable, Iterator
from pathlib import Path
from typing import Any, TypeVar

from splurge_tabular.error_codes import ErrorCode
from splurge_tabular.exceptions import (
    SplurgeTabularColumnError,
    SplurgeTabularIndexError,
    SplurgeTabularKeyError,
    SplurgeTabularTypeError,
    SplurgeTabularValidationError,
    SplurgeTabularValueError,
)

T = TypeVar("T")


def safe_file_operation(file_path: str | Path) -> Path:
    """Validate and convert a file path with consistent error handling.

    Args:
        file_path (str | Path): Path to validate.

    Returns:
        Path: Validated :class:`pathlib.Path` object.

    Raises:
        SplurgeTabularTypeError: If ``file_path`` is not a str or Path.
        SplurgeTabularTypeError: If the provided path cannot be converted to a Path.
    """
    if not isinstance(file_path, str | Path):
        msg = f"file_path must be a string or Path object, got {type(file_path).__name__}"
        raise SplurgeTabularTypeError(
            msg,
            details=f"Expected str or Path, received: {type(file_path).__name__}",
            error_code=ErrorCode.TYPE_INVALID,
            context={"param": "file_path", "value": str(file_path)},
        )

    try:
        path = Path(file_path)
    except (TypeError, ValueError) as e:
        msg = f"file_path is not a valid path: {file_path}"
        raise SplurgeTabularTypeError(
            msg,
            details=str(e),
            error_code=ErrorCode.TYPE_INVALID,
            context={"param": "file_path", "value": str(file_path)},
        ) from e

    return path


def standardize_column_names(
    headers: list[str],
    *,
    fill_empty: bool = True,
    prefix: str = "column_",
) -> list[str]:
    """Standardize column names by filling empty headers with generated names.

    Args:
        headers (list[str]): List of header strings (may contain empty strings).
        fill_empty (bool): Whether to fill empty headers with generated names.
        prefix (str): Prefix for generated column names.

    Returns:
        list[str]: List of standardized column names.

    Example:
        ["Name", "", "City"] -> ["Name", "column_1", "City"]
    """
    if not fill_empty:
        return headers

    result = []
    for i, header in enumerate(headers):
        if header and header.strip():
            result.append(header.strip())
        else:
            result.append(f"{prefix}{i}")

    return result


def ensure_minimum_columns(
    row: list[str],
    min_columns: int,
    *,
    fill_value: str = "",
) -> list[str]:
    """Ensure a row has at least the minimum number of columns.

    Args:
        row (list[str]): Row data as list of strings.
        min_columns (int): Minimum number of columns required.
        fill_value (str): Value to use for padding missing columns.

    Returns:
        list[str]: Row data padded to the minimum number of columns.
    """
    if len(row) >= min_columns:
        return row

    # Pad with empty strings to reach minimum columns
    padded_row = row.copy()
    padded_row.extend([fill_value] * (min_columns - len(row)))
    return padded_row


def safe_index_access(
    items: list[T],
    index: int,
    *,
    item_name: str = "item",
    default: T | None = None,
) -> T:
    """Safely access list item by index with helpful error messages.

    Args:
        items (list[T]): List to access.
        index (int): Index to access.
        item_name (str): Name of items for error messages.
        default (T | None): Default value if index out of range (if None, raises).

    Returns:
        T: Item at index or the provided default.

    Raises:
        SplurgeTabularIndexError: If index is out of range and no default provided.
    """
    if 0 <= index < len(items):
        return items[index]

    if default is not None:
        return default

    msg = f"{item_name} index {index} out of range"
    raise SplurgeTabularIndexError(
        msg,
        details=f"Valid range: 0 to {len(items) - 1}, got {index}",
        error_code=ErrorCode.INDEX_OUT_OF_RANGE,
        context={"item_name": item_name, "requested_index": str(index), "max_index": str(len(items) - 1)},
    )


def safe_dict_access(
    data: dict[str, T],
    key: str,
    *,
    item_name: str = "key",
    default: T | None = None,
) -> T:
    """Safely access dictionary value by key with helpful error messages.

    Args:
        data (dict[str, T]): Dictionary to access.
        key (str): Key to access.
        item_name (str): Name of items for error messages.
        default (T | None): Default value if key not found (if None, raises).

    Returns:
        T: Value for key or default value.

    Raises:
        SplurgeTabularKeyError: If key not found and no default provided.
        SplurgeTabularColumnError: If item_name == 'column' and key missing.
    """
    if key in data:
        return data[key]

    if default is not None:
        return default

    available_keys = list(data.keys())[:5]  # Show first 5 keys
    key_hint = f"Available keys: {available_keys}"
    if len(data) > 5:
        key_hint += f" (and {len(data) - 5} more)"

    msg = f"{item_name} '{key}' not found"
    if item_name == "column":
        raise SplurgeTabularColumnError(
            msg,
            details=key_hint,
            error_code=ErrorCode.COLUMN_NOT_FOUND,
            context={"column": key, "available_hint": key_hint},
        )
    else:
        raise SplurgeTabularKeyError(
            msg,
            details=key_hint,
            error_code=ErrorCode.KEY_NOT_FOUND,
            context={"key": key, "available_hint": key_hint},
        )


def validate_data_structure(
    data: Any,
    *,
    expected_type: type,
    param_name: str = "data",
    allow_empty: bool = True,
) -> Any:
    """Validate data structure with consistent error handling.

    Args:
        data (Any): Data to validate.
        expected_type (type): Expected type of the data.
        param_name (str): Parameter name for error messages.
        allow_empty (bool): Whether empty data is allowed.

    Returns:
        Any: The validated data (unchanged if valid).

    Raises:
        SplurgeTabularTypeError: If data is wrong type or None when not allowed.
        SplurgeTabularValidationError: If data is empty and allow_empty is False.
    """
    if data is None:
        msg = f"{param_name} cannot be None"
        raise SplurgeTabularTypeError(
            msg,
            details=f"Expected {expected_type.__name__}, got None",
            error_code=ErrorCode.TYPE_INVALID,
            context={"param": param_name},
        )

    if not isinstance(data, expected_type):
        msg = f"{param_name} must be {expected_type.__name__}, got {type(data).__name__}"
        raise SplurgeTabularTypeError(
            msg,
            details=f"Expected {expected_type.__name__}, received: {type(data).__name__}",
            error_code=ErrorCode.TYPE_INVALID,
            context={"param": param_name, "received_type": type(data).__name__},
        )

    if not allow_empty and not data:
        msg = f"{param_name} cannot be empty"
        raise SplurgeTabularValidationError(
            msg,
            details=f"Empty {expected_type.__name__} not allowed",
            error_code=ErrorCode.VALIDATION_EMPTY_NOT_ALLOWED,
            context={"param": param_name},
        )

    return data


def create_parameter_validator(
    validators: dict[str, Callable[[Any], Any]],
) -> Callable[[dict[str, Any]], dict[str, Any]]:
    """
    Create a parameter validation function from a dictionary of validators.

    Args:
        validators: Dictionary mapping parameter names to validation functions

    Returns:
        Function that validates a dictionary of parameters

    Example:
        validator = create_parameter_validator({
            'name': lambda x: x if isinstance(x, str) and x.strip() else raise SplurgeValueError("name must be non-empty string"),
            'age': lambda x: x if isinstance(x, int) and x >= 0 else raise SplurgeValueError("age must be non-negative integer")
        })
        validated = validator({'name': 'John', 'age': 25})
    """

    def validate_parameters(params: dict[str, Any]) -> dict[str, Any]:
        """Validate a dict of parameters using the supplied validators.

        Args:
            params (dict[str, Any]): Dictionary of parameter values to validate.

        Returns:
            dict[str, Any]: A dictionary of validated parameter values (only
                keys present in the ``validators`` mapping are returned).
        """
        validated = {}
        for param_name, validator in validators.items():
            if param_name in params:
                validated[param_name] = validator(params[param_name])
        return validated

    return validate_parameters


def batch_validate_rows(
    rows: Iterable[list[str]],
    *,
    min_columns: int | None = None,
    max_columns: int | None = None,
    skip_empty: bool = True,
) -> Iterator[list[str]]:
    """
    Validate and normalize rows in a batch operation.

    Args:
        rows: Iterable of row data
        min_columns: Minimum columns per row (pad if needed)
        max_columns: Maximum columns per row (truncate if needed)
        skip_empty: Whether to skip completely empty rows

    Yields:
        Validated and normalized rows

    Raises:
        SplurgeTypeError: If row validation fails
    """
    for row_idx, row in enumerate(rows):
        # Validate row is list-like before attempting to iterate
        if not isinstance(row, list):
            msg = f"Row {row_idx} must be a list, got {type(row).__name__}"
            raise SplurgeTabularTypeError(
                msg,
                details="Each row must be a list of strings",
                error_code=ErrorCode.TYPE_INVALID,
                context={"row_index": str(row_idx), "received_type": type(row).__name__},
            )

        # Skip empty rows if requested (handle non-string cells safely)
        if skip_empty and not any((cell is not None and str(cell).strip()) for cell in row):
            continue

        # Ensure all cells are strings
        normalized_row = [str(cell) if cell is not None else "" for cell in row]

        # Apply column constraints
        if min_columns is not None and len(normalized_row) < min_columns:
            normalized_row = ensure_minimum_columns(normalized_row, min_columns)

        if max_columns is not None and len(normalized_row) > max_columns:
            normalized_row = normalized_row[:max_columns]

        yield normalized_row


def create_error_context(
    operation: str,
    *,
    file_path: str | Path | None = None,
    row_number: int | None = None,
    column_name: str | None = None,
    additional_info: str | None = None,
) -> str:
    """
    Create consistent error context information.

    Args:
        operation: Description of the operation that failed
        file_path: File path if applicable
        row_number: Row number if applicable
        column_name: Column name if applicable
        additional_info: Additional context information

    Returns:
        Formatted context string
    """
    context_parts = [f"Operation: {operation}"]

    if file_path is not None:
        context_parts.append(f"File: {file_path}")

    if row_number is not None:
        context_parts.append(f"Row: {row_number}")

    if column_name is not None:
        context_parts.append(f"Column: {column_name}")

    if additional_info is not None:
        context_parts.append(f"Info: {additional_info}")

    return " | ".join(context_parts)


def normalize_string(
    value: str | None,
    *,
    trim: bool = True,
    handle_empty: bool = True,
    empty_default: str = "",
) -> str:
    """
    Normalize string values with consistent handling of None, empty, and whitespace.

    Args:
        value: String value to normalize
        trim: Whether to trim whitespace
        handle_empty: Whether to handle empty values specially
        empty_default: Default value for empty strings

    Returns:
        Normalized string value
    """
    if value is None:
        return empty_default if handle_empty else ""

    if not isinstance(value, str):
        return str(value)

    if trim:
        value = value.strip()

    if handle_empty and not value:
        return empty_default

    return value


def is_empty_or_none(value: Any, *, trim: bool = True) -> bool:
    """
    Check if a value is None, empty, or contains only whitespace.

    Args:
        value: Value to check
        trim: Whether to trim whitespace before checking

    Returns:
        True if value is empty, None, or whitespace-only
    """
    if value is None:
        return True

    if not isinstance(value, str):
        return False

    return not value.strip() if trim else not value


def safe_string_operation(
    value: str | None,
    operation: Callable[[str], str],
    *,
    trim: bool = True,
    handle_empty: bool = True,
    empty_default: str = "",
) -> str:
    """
    Safely apply a string operation with consistent empty value handling.

    Args:
        value: String value to process
        operation: Function to apply to non-empty strings
        trim: Whether to trim whitespace
        handle_empty: Whether to handle empty values specially
        empty_default: Default value for empty strings

    Returns:
        Processed string value
    """
    normalized = normalize_string(value, trim=trim, handle_empty=handle_empty, empty_default=empty_default)

    if not normalized and handle_empty:
        return empty_default

    return operation(normalized)


def validate_string_parameters(
    value: Any,
    param_name: str,
    *,
    allow_none: bool = False,
    allow_empty: bool = False,
    min_length: int | None = None,
    max_length: int | None = None,
) -> str:
    """
    Validate string parameters with comprehensive error checking.

    Args:
        value: Value to validate
        param_name: Name of parameter for error messages
        allow_none: Whether None values are allowed
        allow_empty: Whether empty strings are allowed
        min_length: Minimum string length (if not None)
        max_length: Maximum string length (if not None)

    Returns:
        Validated string value

    Raises:
        SplurgeTypeError: If validation fails
        SplurgeValueError: If validation fails
    """
    if value is None:
        if not allow_none:
            msg = f"{param_name} cannot be None"
            raise SplurgeTabularTypeError(
                msg,
                details="None values are not allowed for this parameter",
            )
        return ""

    if not isinstance(value, str):
        msg = f"{param_name} must be a string, got {type(value).__name__}"
        raise SplurgeTabularTypeError(
            msg,
            details=f"Expected string, received: {value!r}",
        )

    if not value and not allow_empty:
        msg = f"{param_name} cannot be empty"
        raise SplurgeTabularValueError(
            msg,
            details="Empty strings are not allowed for this parameter",
        )

    if min_length is not None and len(value) < min_length:
        msg = f"{param_name} must be at least {min_length} characters long"
        raise SplurgeTabularValueError(
            msg,
            details=f"Got {len(value)} characters, minimum required: {min_length}",
        )

    if max_length is not None and len(value) > max_length:
        msg = f"{param_name} must be at most {max_length} characters long"
        raise SplurgeTabularValueError(
            msg,
            details=f"Got {len(value)} characters, maximum allowed: {max_length}",
        )

    return value
