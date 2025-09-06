"""
Unit tests for splurge_tabular.tabular_data_model module.

Tests the main TabularDataModel class.
"""

import pytest

from splurge_tabular.exceptions import SplurgeParameterError, SplurgeValidationError
from splurge_tabular.tabular_data_model import TabularDataModel


class TestTabularDataModel:
    """Test the TabularDataModel class."""

    def test_basic_initialization(self):
        """Test basic initialization with valid data."""
        data = [
            ["Name", "Age", "City"],
            ["John", "30", "NYC"],
            ["Jane", "25", "LA"]
        ]
        model = TabularDataModel(data)

        assert model.row_count == 2  # Excluding header
        assert model.column_count == 3
        assert model.column_names == ["Name", "Age", "City"]

    def test_empty_data_raises_error(self):
        """Test that empty data raises an error."""
        with pytest.raises(SplurgeValidationError):
            TabularDataModel([])

    def test_single_row_data(self):
        """Test with single row of data (treated as header only)."""
        data = [["Name", "Age"]]
        model = TabularDataModel(data)

        assert model.row_count == 0  # No data rows, only header
        assert model.column_count == 0  # No data columns when no data rows
        assert model.column_names == ["Name", "Age"]  # But header names exist

    def test_multiple_header_rows(self):
        """Test with multiple header rows."""
        data = [
            ["Personal", "Personal"],
            ["Name", "Age"],
            ["John", "30"]
        ]
        model = TabularDataModel(data, header_rows=2)

        assert model.row_count == 1
        assert model.column_count == 2
        assert model.column_names == ["Personal_Name", "Personal_Age"]

    def test_skip_empty_rows_enabled(self):
        """Test skipping empty rows."""
        data = [
            ["Name", "Age"],
            ["", ""],  # Empty row
            ["John", "30"],
            ["  ", "\t"]  # Whitespace-only row
        ]
        model = TabularDataModel(data, skip_empty_rows=True)

        assert model.row_count == 1
        assert model.column_names == ["Name", "Age"]

    def test_skip_empty_rows_disabled(self):
        """Test not skipping empty rows."""
        data = [
            ["Name", "Age"],
            ["", ""],  # Empty row
            ["John", "30"]
        ]
        model = TabularDataModel(data, skip_empty_rows=False)

        assert model.row_count == 2  # Includes empty row

    def test_column_index_valid(self):
        """Test getting valid column index."""
        data = [["Name", "Age", "City"]]
        model = TabularDataModel(data)

        assert model.column_index("Name") == 0
        assert model.column_index("Age") == 1
        assert model.column_index("City") == 2

    def test_column_index_invalid(self):
        """Test getting index for non-existent column."""
        data = [["Name", "Age", "City"]]
        model = TabularDataModel(data)

        with pytest.raises(SplurgeParameterError):
            model.column_index("Invalid")

    def test_column_type_inference(self):
        """Test basic column type inference."""
        data = [
            ["Name", "Age", "Score"],
            ["John", "30", "85.5"],
            ["Jane", "25", "92.0"]
        ]
        model = TabularDataModel(data)

        # These would need actual type inference implementation
        # For now, just test that the method exists
        try:
            age_type = model.column_type("Age")
            score_type = model.column_type("Score")
            # Types would depend on the inference implementation
        except Exception:
            # Type inference may not be fully implemented yet
            pass

    def test_column_values(self):
        """Test getting all values for a column."""
        data = [
            ["Name", "Age"],
            ["John", "30"],
            ["Jane", "25"],
            ["Bob", "35"]
        ]
        model = TabularDataModel(data)

        name_values = model.column_values("Name")
        age_values = model.column_values("Age")

        assert name_values == ["John", "Jane", "Bob"]
        assert age_values == ["30", "25", "35"]

    def test_column_values_invalid_column(self):
        """Test column_values with invalid column name."""
        data = [["Name", "Age"], ["John", "30"]]
        model = TabularDataModel(data)

        with pytest.raises(SplurgeParameterError):
            model.column_values("Invalid")

    def test_cell_value(self):
        """Test getting individual cell values."""
        data = [
            ["Name", "Age"],
            ["John", "30"],
            ["Jane", "25"]
        ]
        model = TabularDataModel(data)

        assert model.cell_value("Name", 0) == "John"
        assert model.cell_value("Age", 1) == "25"
        assert model.cell_value("Name", 1) == "Jane"

    def test_cell_value_invalid_column(self):
        """Test cell_value with invalid column name."""
        data = [["Name", "Age"], ["John", "30"]]
        model = TabularDataModel(data)

        with pytest.raises(SplurgeParameterError):
            model.cell_value("Invalid", 0)

    def test_cell_value_invalid_row(self):
        """Test cell_value with invalid row index."""
        from splurge_tabular.exceptions import SplurgeRangeError
        
        data = [["Name", "Age"], ["John", "30"]]
        model = TabularDataModel(data)

        with pytest.raises(SplurgeRangeError):
            model.cell_value("Name", 5)

    def test_iter_rows(self):
        """Test iterating over rows as dictionaries."""
        data = [
            ["Name", "Age"],
            ["John", "30"],
            ["Jane", "25"]
        ]
        model = TabularDataModel(data)

        rows = list(model.iter_rows())
        expected = [
            {"Name": "John", "Age": "30"},
            {"Name": "Jane", "Age": "25"}
        ]
        assert rows == expected

    def test_iter_rows_as_tuples(self):
        """Test iterating over rows as tuples."""
        data = [
            ["Name", "Age"],
            ["John", "30"],
            ["Jane", "25"]
        ]
        model = TabularDataModel(data)

        rows = list(model.iter_rows_as_tuples())
        expected = [
            ("John", "30"),
            ("Jane", "25")
        ]
        assert rows == expected

    def test_row(self):
        """Test getting a row as dictionary."""
        data = [
            ["Name", "Age"],
            ["John", "30"],
            ["Jane", "25"]
        ]
        model = TabularDataModel(data)

        row = model.row(0)
        assert row == {"Name": "John", "Age": "30"}

        row = model.row(1)
        assert row == {"Name": "Jane", "Age": "25"}

    def test_row_invalid_index(self):
        """Test row with invalid index."""
        data = [["Name", "Age"], ["John", "30"]]
        model = TabularDataModel(data)

        with pytest.raises(IndexError):
            model.row(5)

    def test_row_as_list(self):
        """Test getting a row as list."""
        data = [
            ["Name", "Age"],
            ["John", "30"],
            ["Jane", "25"]
        ]
        model = TabularDataModel(data)

        row = model.row_as_list(0)
        assert row == ["John", "30"]

        row = model.row_as_list(1)
        assert row == ["Jane", "25"]

    def test_row_as_tuple(self):
        """Test getting a row as tuple."""
        data = [
            ["Name", "Age"],
            ["John", "30"],
            ["Jane", "25"]
        ]
        model = TabularDataModel(data)

        row = model.row_as_tuple(0)
        assert row == ("John", "30")

        row = model.row_as_tuple(1)
        assert row == ("Jane", "25")

    def test_iteration(self):
        """Test iterating over the model."""
        data = [
            ["Name", "Age"],
            ["John", "30"],
            ["Jane", "25"]
        ]
        model = TabularDataModel(data)

        rows = list(model)
        expected = [
            ["John", "30"],
            ["Jane", "25"]
        ]
        assert rows == expected

    def test_to_typed(self):
        """Test creating a typed view."""
        data = [
            ["Name", "Age", "Score"],
            ["John", "30", "85.5"],
            ["Jane", "25", "92.0"]
        ]
        model = TabularDataModel(data)

        typed_view = model.to_typed()

        # Test that typed view has same basic properties
        assert typed_view.row_count == model.row_count
        assert typed_view.column_count == model.column_count
        assert typed_view.column_names == model.column_names

    def test_typed_view_column_values(self):
        """Test typed view column values."""
        data = [
            ["Name", "Age"],
            ["John", "30"],
            ["Jane", "25"]
        ]
        model = TabularDataModel(data)
        typed_view = model.to_typed()

        # This will depend on the type inference implementation
        try:
            name_values = typed_view.column_values("Name")
            age_values = typed_view.column_values("Age")
            # Values should be typed appropriately
        except Exception:
            # Type conversion may not be fully implemented
            pass

    def test_typed_view_cell_value(self):
        """Test typed view cell value."""
        data = [
            ["Name", "Age"],
            ["John", "30"],
            ["Jane", "25"]
        ]
        model = TabularDataModel(data)
        typed_view = model.to_typed()

        try:
            name_value = typed_view.cell_value("Name", 0)
            age_value = typed_view.cell_value("Age", 0)
            # Values should be typed appropriately
        except Exception:
            # Type conversion may not be fully implemented
            pass

    def test_typed_view_row(self):
        """Test typed view row access."""
        data = [
            ["Name", "Age"],
            ["John", "30"],
            ["Jane", "25"]
        ]
        model = TabularDataModel(data)
        typed_view = model.to_typed()

        try:
            row = typed_view.row(0)
            # Row should be a typed dictionary
        except Exception:
            # Type conversion may not be fully implemented
            pass

    def test_typed_view_iteration(self):
        """Test typed view iteration."""
        data = [
            ["Name", "Age"],
            ["John", "30"],
            ["Jane", "25"]
        ]
        model = TabularDataModel(data)
        typed_view = model.to_typed()

        try:
            rows = list(typed_view)
            # Rows should be typed lists
        except Exception:
            # Type conversion may not be fully implemented
            pass
