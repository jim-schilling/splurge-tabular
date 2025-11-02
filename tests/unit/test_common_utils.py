"""
Unit tests for splurge_tabular.common_utils module.

Tests core utility functions for data validation and safe operations.
"""

import pytest

from splurge_tabular.common_utils import (
    batch_validate_rows,
    ensure_minimum_columns,
    is_empty_or_none,
    normalize_string,
    standardize_column_names,
)
from splurge_tabular.exceptions import SplurgeTabularTypeError


class TestIsEmptyOrNone:
    """Test the is_empty_or_none function."""

    def test_none_value(self):
        """Test with None value."""
        assert is_empty_or_none(None) is True

    def test_empty_string(self):
        """Test with empty string."""
        assert is_empty_or_none("") is True

    def test_whitespace_string_trim(self):
        """Test whitespace string with trimming."""
        assert is_empty_or_none("   ") is True

    def test_whitespace_string_no_trim(self):
        """Test whitespace string without trimming."""
        assert is_empty_or_none("   ", trim=False) is False

    def test_non_empty_string(self):
        """Test non-empty string."""
        assert is_empty_or_none("hello") is False

    def test_zero_number(self):
        """Test with zero."""
        assert is_empty_or_none(0) is False

    def test_false_boolean(self):
        """Test with False."""
        assert is_empty_or_none(False) is False

    def test_empty_list(self):
        """Test with empty list."""
        assert is_empty_or_none([]) is False

    def test_empty_dict(self):
        """Test with empty dict."""
        assert is_empty_or_none({}) is False


class TestStandardizeColumnNames:
    """Test the standardize_column_names function."""

    def test_fill_empty_headers(self):
        """Test filling empty headers with generated names."""
        columns = ["Name", "", "City"]
        result = standardize_column_names(columns)
        expected = ["Name", "column_1", "City"]
        assert result == expected

    def test_no_empty_headers(self):
        """Test when no empty headers exist."""
        columns = ["Name", "Age", "City"]
        result = standardize_column_names(columns)
        assert result == columns

    def test_all_empty_headers(self):
        """Test when all headers are empty."""
        columns = ["", "", ""]
        result = standardize_column_names(columns)
        expected = ["column_0", "column_1", "column_2"]
        assert result == expected

    def test_custom_prefix(self):
        """Test with custom prefix."""
        columns = ["Name", "", "City"]
        result = standardize_column_names(columns, prefix="field_")
        expected = ["Name", "field_1", "City"]
        assert result == expected

    def test_no_fill_empty(self):
        """Test when fill_empty is False."""
        columns = ["Name", "", "City"]
        result = standardize_column_names(columns, fill_empty=False)
        assert result == columns


class TestEnsureMinimumColumns:
    """Test the ensure_minimum_columns function."""

    def test_no_padding_needed(self):
        """Test when row already has minimum columns."""
        row = ["a", "b", "c"]
        result = ensure_minimum_columns(row, 3)
        assert result == ["a", "b", "c"]

    def test_padding_needed(self):
        """Test when row needs padding."""
        row = ["a", "b"]
        result = ensure_minimum_columns(row, 4)
        assert result == ["a", "b", "", ""]

    def test_exact_minimum(self):
        """Test when row has exactly minimum columns."""
        row = ["a", "b", "c"]
        result = ensure_minimum_columns(row, 3)
        assert result == ["a", "b", "c"]

    def test_empty_row(self):
        """Test with empty row."""
        row = []
        result = ensure_minimum_columns(row, 2)
        assert result == ["", ""]

    def test_minimum_zero(self):
        """Test with minimum columns of zero."""
        row = ["a", "b"]
        result = ensure_minimum_columns(row, 0)
        assert result == ["a", "b"]

    def test_none_row_raises_error(self):
        """Test with None row raises TypeError."""
        with pytest.raises(TypeError):
            ensure_minimum_columns(None, 3)


class TestBatchValidateRows:
    """Test the batch_validate_rows function."""

    def test_valid_rows(self):
        """Test validation of valid rows."""
        rows = [["a", "b"], ["c", "d"], ["e", "f"]]
        result = list(batch_validate_rows(rows, min_columns=2))
        assert result == rows

    def test_invalid_row_type(self):
        """Test validation with invalid row type."""
        rows = [["a", "b"], "not a list", ["e", "f"]]
        with pytest.raises(SplurgeTabularTypeError) as exc_info:
            list(batch_validate_rows(rows))

        assert "Row 1 must be a list" in str(exc_info.value)

    def test_empty_rows_list(self):
        """Test with empty rows list."""
        result = list(batch_validate_rows([], min_columns=1))
        assert result == []

    def test_skip_empty_rows(self):
        """Test skipping empty rows."""
        rows = [["a", "b"], ["", ""], ["c", "d"]]
        result = list(batch_validate_rows(rows, skip_empty=True))
        expected = [["a", "b"], ["c", "d"]]
        assert result == expected

    def test_min_columns_padding(self):
        """Test minimum columns padding."""
        rows = [["a", "b"], ["c"]]
        result = list(batch_validate_rows(rows, min_columns=3))
        expected = [["a", "b", ""], ["c", "", ""]]
        assert result == expected


class TestNormalizeString:
    """Test the normalize_string function."""

    def test_basic_normalization(self):
        """Test basic string normalization."""
        result = normalize_string("  Hello World  ")
        assert result == "Hello World"

    def test_empty_string(self):
        """Test with empty string."""
        result = normalize_string("")
        assert result == ""

    def test_only_whitespace(self):
        """Test with only whitespace."""
        result = normalize_string("   ")
        assert result == ""

    def test_none_input(self):
        """Test with None input."""
        result = normalize_string(None)
        assert result == ""

    def test_no_trim(self):
        """Test with trim=False."""
        result = normalize_string("  Hello  ", trim=False)
        assert result == "  Hello  "

    def test_custom_empty_default(self):
        """Test with custom empty default."""
        result = normalize_string("", empty_default="N/A")
        assert result == "N/A"
