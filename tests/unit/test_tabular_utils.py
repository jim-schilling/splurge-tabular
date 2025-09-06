"""
Unit tests for splurge_tabular.tabular_utils module.

Tests header processing, row normalization, and utility functions.
"""

from splurge_tabular.tabular_utils import (
    auto_column_names,
    normalize_rows,
    process_headers,
    should_skip_row,
)


class TestProcessHeaders:
    """Test the process_headers function."""

    def test_single_header_row(self):
        """Test processing a single header row."""
        header_data = [["Name", "Age", "City"]]
        processed, column_names = process_headers(header_data, header_rows=1)

        assert processed == [["Name", "Age", "City"]]
        assert column_names == ["Name", "Age", "City"]

    def test_multiple_header_rows(self):
        """Test processing multiple header rows with merging."""
        header_data = [["Personal", "Personal", "Location"], ["Name", "Age", "City"]]
        processed, column_names = process_headers(header_data, header_rows=2)

        assert processed == [["Personal_Name", "Personal_Age", "Location_City"]]
        assert column_names == ["Personal_Name", "Personal_Age", "Location_City"]

    def test_empty_headers(self):
        """Test processing empty header data."""
        header_data = []
        processed, column_names = process_headers(header_data, header_rows=1)

        assert processed == []
        assert column_names == []

    def test_whitespace_in_headers(self):
        """Test handling of whitespace in header names."""
        header_data = [["  Name  ", " Age\t", "\nCity"]]
        processed, column_names = process_headers(header_data, header_rows=1)

        assert processed == [["  Name  ", " Age\t", "\nCity"]]
        assert column_names == ["Name", "Age", "City"]

    def test_empty_header_names(self):
        """Test handling of empty header names."""
        header_data = [["", "Name", ""]]
        processed, column_names = process_headers(header_data, header_rows=1)

        assert processed == [["", "Name", ""]]
        assert column_names == ["column_0", "Name", "column_2"]

    def test_mixed_empty_and_whitespace_headers(self):
        """Test handling of mixed empty and whitespace headers."""
        header_data = [["  ", "Name", "\t"]]
        processed, column_names = process_headers(header_data, header_rows=1)

        assert processed == [["  ", "Name", "\t"]]
        assert column_names == ["column_0", "Name", "column_2"]

    def test_irregular_header_lengths(self):
        """Test handling of irregular header row lengths."""
        header_data = [["A", "B"], ["C", "D", "E"]]
        processed, column_names = process_headers(header_data, header_rows=1)

        # Should return original data unchanged for single header row
        assert processed == [["A", "B"], ["C", "D", "E"]]
        # Column names should be based on max columns across all rows
        assert column_names == ["A", "B", "column_2"]


class TestNormalizeRows:
    """Test the normalize_rows function."""

    def test_empty_rows(self):
        """Test normalizing empty row list."""
        result = normalize_rows([], skip_empty_rows=True)
        assert result == []

    def test_uniform_row_lengths(self):
        """Test normalizing rows that already have uniform lengths."""
        rows = [["A", "B"], ["C", "D"], ["E", "F"]]
        result = normalize_rows(rows, skip_empty_rows=False)

        assert result == [["A", "B"], ["C", "D"], ["E", "F"]]

    def test_irregular_row_lengths(self):
        """Test normalizing rows with different lengths."""
        rows = [["A", "B"], ["C", "D", "E"], ["F"]]
        result = normalize_rows(rows, skip_empty_rows=False)

        assert result == [["A", "B", ""], ["C", "D", "E"], ["F", "", ""]]

    def test_skip_empty_rows_enabled(self):
        """Test skipping empty rows when enabled."""
        rows = [["A", "B"], ["", ""], ["C", "D"], ["  ", "\t"]]
        result = normalize_rows(rows, skip_empty_rows=True)

        assert result == [["A", "B"], ["C", "D"]]

    def test_skip_empty_rows_disabled(self):
        """Test not skipping empty rows when disabled."""
        rows = [["A", "B"], ["", ""], ["C", "D"]]
        result = normalize_rows(rows, skip_empty_rows=False)

        assert result == [["A", "B"], ["", ""], ["C", "D"]]

    def test_mixed_empty_and_whitespace_rows(self):
        """Test handling of rows with whitespace-only cells."""
        rows = [["A", "B"], ["  ", "\t"], ["C", "D"]]
        result = normalize_rows(rows, skip_empty_rows=True)

        assert result == [["A", "B"], ["C", "D"]]


class TestShouldSkipRow:
    """Test the should_skip_row function."""

    def test_empty_row(self):
        """Test skipping completely empty row."""
        row = ["", "", ""]
        assert should_skip_row(row) is True

    def test_whitespace_only_row(self):
        """Test skipping row with only whitespace."""
        row = ["  ", "\t", "\n"]
        assert should_skip_row(row) is True

    def test_mixed_whitespace_row(self):
        """Test skipping row with mixed whitespace."""
        row = ["", "  ", "\t"]
        assert should_skip_row(row) is True

    def test_non_empty_row(self):
        """Test not skipping row with actual content."""
        row = ["", "Name", ""]
        assert should_skip_row(row) is False

    def test_single_non_empty_cell(self):
        """Test not skipping row with one non-empty cell."""
        row = ["", "", "X"]
        assert should_skip_row(row) is False


class TestAutoColumnNames:
    """Test the auto_column_names function."""

    def test_zero_columns(self):
        """Test generating names for zero columns."""
        result = auto_column_names(0)
        assert result == []

    def test_single_column(self):
        """Test generating names for single column."""
        result = auto_column_names(1)
        assert result == ["column_0"]

    def test_multiple_columns(self):
        """Test generating names for multiple columns."""
        result = auto_column_names(3)
        assert result == ["column_0", "column_1", "column_2"]

    def test_large_number_of_columns(self):
        """Test generating names for many columns."""
        result = auto_column_names(5)
        expected = ["column_0", "column_1", "column_2", "column_3", "column_4"]
        assert result == expected
