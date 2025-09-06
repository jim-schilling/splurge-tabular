"""Shared utilities for tabular data processing.

This module centralizes header processing, row normalization, and helpers used
by in-memory and streaming tabular data models.

Copyright (c) 2025 Jim Schilling

Please preserve this header and all related material when sharing!

This module is licensed under the MIT License.
"""

from __future__ import annotations

import re


def process_headers(
    header_data: list[list[str]],
    *,
    header_rows: int,
) -> tuple[list[list[str]], list[str]]:
    """Process header rows and return processed header data and column names.

    Args:
        header_data: Raw header data rows.
        header_rows: Number of header rows to merge.

    Returns:
        Tuple of (processed_header_data, column_names).
    """
    processed_header_data = header_data.copy()

    if header_rows > 1:
        merged_headers: list[str] = []
        for row in header_data:
            while len(merged_headers) < len(row):
                merged_headers.append("")
            for j, name in enumerate(row):
                if merged_headers[j]:
                    merged_headers[j] = f"{merged_headers[j]}_{name}"
                else:
                    merged_headers[j] = name
        processed_header_data = [merged_headers]

    if processed_header_data and processed_header_data[0]:
        raw_names = processed_header_data[0]
        column_names = [
            re.sub(r"\s+", " ", name).strip() if name and re.sub(r"\s+", " ", name).strip() else f"column_{i}"
            for i, name in enumerate(raw_names)
        ]
    else:
        column_names = []

    column_count = max((len(row) for row in header_data), default=0)
    while len(column_names) < column_count:
        column_names.append(f"column_{len(column_names)}")

    return processed_header_data, column_names


def normalize_rows(
    rows: list[list[str]],
    *,
    skip_empty_rows: bool,
) -> list[list[str]]:
    """Normalize rows to equal length and optionally drop empty rows.

    Args:
        rows: List of rows to normalize.
        skip_empty_rows: Whether to skip rows that are empty or contain only whitespace.

    Returns:
        List of normalized rows with equal length.
    """
    if not rows:
        return []

    max_columns = max(len(row) for row in rows)
    normalized: list[list[str]] = []
    for row in rows:
        if len(row) < max_columns:
            row = row + [""] * (max_columns - len(row))
        normalized.append(row)

    if skip_empty_rows:
        normalized = [row for row in normalized if not should_skip_row(row)]

    return normalized


def should_skip_row(row: list[str]) -> bool:
    """Check if a row should be skipped because it is empty.

    Args:
        row: Row to check.

    Returns:
        True if the row is empty or contains only whitespace.
    """
    return all(cell.strip() == "" for cell in row)


def auto_column_names(count: int) -> list[str]:
    """Generate default column names.

    Args:
        count: Number of column names to generate.

    Returns:
        List of default column names in format "column_0", "column_1", etc.
    """
    return [f"column_{i}" for i in range(count)]
