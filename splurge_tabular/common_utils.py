"""Common utility functions for splurge-tabular package.

This module provides reusable utility functions and patterns to reduce
code duplication across the package.

Copyright (c) 2025 Jim Schilling

Please preserve this header and all related material when sharing!

This module is licensed under the MIT License.
"""

from collections.abc import Iterable, Iterator
from typing import Any, TypeVar

from .exceptions import SplurgeTabularTypeError

T = TypeVar("T")


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


def batch_validate_rows(
    rows: Iterable[list[str]],
    *,
    min_columns: int | None = None,
    max_columns: int | None = None,
    skip_empty: bool = True,
) -> Iterator[list[str]]:
    """Validate and normalize rows in a batch operation.

    Args:
        rows (Iterable[list[str]]): Iterable of row data.
        min_columns (int | None): Minimum columns per row (pad if needed).
        max_columns (int | None): Maximum columns per row (truncate if needed).
        skip_empty (bool): Whether to skip completely empty rows.

    Yields:
        list[str]: Validated and normalized rows.

    Raises:
        SplurgeTabularTypeError: If row validation fails.
    """
    for row_idx, row in enumerate(rows):
        # Validate row is list-like before attempting to iterate
        if not isinstance(row, list):
            raise SplurgeTabularTypeError(
                message=f"Row {row_idx} must be a list, got {type(row).__name__}",
                details={"row_index": str(row_idx), "received_type": type(row).__name__},
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


def normalize_string(
    value: str | None,
    *,
    trim: bool = True,
    handle_empty: bool = True,
    empty_default: str = "",
) -> str:
    """Normalize string values with consistent handling of None, empty, and whitespace.

    Args:
        value (str | None): String value to normalize.
        trim (bool): Whether to trim whitespace.
        handle_empty (bool): Whether to handle empty values specially.
        empty_default (str): Default value for empty strings.

    Returns:
        str: Normalized string value.
    """
    if value is None:
        return empty_default if handle_empty else ""

    if not isinstance(value, str):
        return str(value)  # type: ignore

    if trim:
        value = value.strip()

    if handle_empty and not value:
        return empty_default

    return value


def is_empty_or_none(value: Any, *, trim: bool = True) -> bool:
    """Check if a value is None, empty, or contains only whitespace.

    Args:
        value (Any): Value to check.
        trim (bool): Whether to trim whitespace before checking.

    Returns:
        bool: True if value is empty, None, or whitespace-only.
    """
    if value is None:
        return True

    if not isinstance(value, str):
        return False

    return not value.strip() if trim else not value
