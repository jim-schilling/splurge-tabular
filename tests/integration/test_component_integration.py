"""
Integration tests for splurge_tabular package.

Tests component interactions and data flow between modules.
"""

import pytest

from splurge_tabular.common_utils import batch_validate_rows, ensure_minimum_columns, standardize_column_names
from splurge_tabular.exceptions import (
    SplurgeTabularLookupError,
    SplurgeTabularTypeError,
    SplurgeTabularValueError,
)
from splurge_tabular.streaming_tabular_data_model import StreamingTabularDataModel
from splurge_tabular.tabular_data_model import TabularDataModel
from splurge_tabular.tabular_utils import normalize_rows, process_headers


class TestDataFlowIntegration:
    """Test data flow between components."""

    def test_tabular_utils_to_tabular_data_model(self):
        """Test data processing pipeline from utils to data model."""
        # Raw data with issues
        raw_data = [
            ["Name", "Age", "City"],
            ["", "25", "NYC"],  # Empty name
            ["John", "", "LA"],  # Empty age
            ["Jane", "30", "Chicago"],
            ["", "", ""],  # Completely empty row
        ]

        # Step 1: Process headers using tabular_utils
        headers, column_names = process_headers([raw_data[0]], header_rows=1)
        assert column_names == ["Name", "Age", "City"]

        # Step 2: Normalize rows using tabular_utils
        normalized_data = normalize_rows(raw_data[1:], skip_empty_rows=True)
        assert len(normalized_data) == 3  # Empty row should be skipped

        # Step 3: Create data model with processed data
        final_data = [column_names] + normalized_data
        model = TabularDataModel(final_data)

        assert model.row_count == 3
        assert model.column_count == 3
        assert model.column_names == ["Name", "Age", "City"]

    def test_common_utils_with_data_models(self):
        """Test common utilities working with data models."""
        data = [
            ["Name", "Age", "Score"],
            ["John", "25", "85.5"],
            ["Jane", "30", "92.0"],
            ["Bob", "28", "78.5"],
        ]

        model = TabularDataModel(data)

        # Test standardize_column_names integration
        original_names = model.column_names
        standardized = standardize_column_names(original_names)
        assert standardized == original_names  # Already standardized

        # Test ensure_minimum_columns with model data
        row_data = model.row_as_list(0)
        padded = ensure_minimum_columns(row_data, 5)
        assert len(padded) == 5
        assert padded[-2:] == ["", ""]  # Padding added

        # Test batch_validate_rows with model iteration
        rows_list = list(model)
        validated_rows = list(batch_validate_rows(rows_list, min_columns=3))
        assert len(validated_rows) == len(rows_list)

    def test_streaming_vs_memory_models_consistency(self):
        """Test that streaming and memory models produce consistent results."""
        data = [
            ["Name", "Age", "City"],
            ["John", "25", "NYC"],
            ["Jane", "30", "LA"],
            ["Bob", "28", "Chicago"],
        ]

        # Create both models
        memory_model = TabularDataModel(data)
        streaming_model = StreamingTabularDataModel(iter([data]))  # Wrap data in iterator

        # Compare basic properties
        assert memory_model.column_count == streaming_model.column_count
        assert memory_model.column_names == streaming_model.column_names

        # Compare data iteration
        memory_rows = list(memory_model.iter_rows())
        streaming_rows = list(streaming_model.iter_rows())

        assert memory_rows == streaming_rows

    def test_data_validation_pipeline(self):
        """Test complete data validation pipeline."""
        # Raw data with various issues
        raw_data = [
            ["Name", "Age", "City"],
            ["John", "25", "NYC"],
            ["Jane", "not_a_number", "LA"],  # Invalid age
            ["Bob", "28", "Chicago"],
            ["", "30", ""],  # Partial empty
        ]

        # Step 2: Process headers
        headers, column_names = process_headers([raw_data[0]], header_rows=1)

        # Step 3: Normalize and validate rows
        data_rows = raw_data[1:]
        normalized_rows = list(batch_validate_rows(data_rows, min_columns=3))

        # Step 4: Create final dataset
        final_data = [column_names] + normalized_rows
        model = TabularDataModel(final_data)

        # Verify the pipeline worked
        assert model.row_count == 4
        assert all(len(row) == 3 for row in model)  # All rows have 3 columns


class TestComponentInteractions:
    """Test interactions between different components."""

    def test_header_processing_with_column_standardization(self):
        """Test header processing combined with column name standardization."""
        # Complex headers that need processing
        data = [
            ["First Name", "Last Name", "Email Address"],
            ["John", "Doe", "john@example.com"],
            ["Jane", "Smith", "jane@example.com"],
        ]

        # Process headers
        headers, column_names = process_headers([data[0]], header_rows=1)

        # Standardize column names (though these are already good)
        standardized_names = standardize_column_names(column_names)

        # Create model with standardized names
        processed_data = [standardized_names] + data[1:]
        model = TabularDataModel(processed_data)

        assert model.column_names == ["First Name", "Last Name", "Email Address"]

    def test_row_padding_with_model_creation(self):
        """Test row padding integration with model creation."""
        # Data with inconsistent row lengths
        data = [
            ["Name", "Age", "City", "Country"],
            ["John", "25", "NYC"],  # Missing country
            ["Jane", "30"],  # Missing city and country
            ["Bob", "28", "Chicago", "USA"],
        ]

        # Pad rows to minimum columns
        padded_data = []
        for i, row in enumerate(data):
            if i == 0:  # Header row
                padded_data.append(row)
            else:
                padded_row = ensure_minimum_columns(row, 4)
                padded_data.append(padded_row)

        # Create model
        model = TabularDataModel(padded_data)

        assert model.row_count == 3
        assert all(len(row) == 4 for row in model)

        # Check padding worked
        rows = list(model)
        assert rows[0][3] == ""  # John missing country
        assert rows[1][2] == ""  # Jane missing city
        assert rows[1][3] == ""  # Jane missing country

    def test_empty_row_handling_pipeline(self):
        """Test empty row handling through the complete pipeline."""
        data = [
            ["Name", "Age", "City"],
            ["", "", ""],  # Completely empty
            ["John", "", "NYC"],  # Partial empty
            ["", "25", ""],  # Partial empty
            ["Jane", "30", "LA"],  # Complete
        ]

        # Process with empty row skipping
        headers, column_names = process_headers([data[0]], header_rows=1)
        data_rows = data[1:]

        # Use batch validation with empty row skipping
        validated_rows = list(batch_validate_rows(data_rows, min_columns=3, skip_empty=True))

        # Create final dataset
        final_data = [column_names] + validated_rows
        model = TabularDataModel(final_data)

        # Should have only 3 rows (empty row skipped)
        assert model.row_count == 3

        # Verify no completely empty rows remain
        for row in model:
            assert not all(cell == "" for cell in row)


class TestDataModelComparisons:
    """Test comparisons and interactions between different data models."""

    def test_model_data_consistency(self):
        """Test that different model creation methods produce consistent results."""
        data = [
            ["Name", "Age", "City"],
            ["John", "25", "NYC"],
            ["Jane", "30", "LA"],
        ]

        # Create models with different configurations
        model1 = TabularDataModel(data, header_rows=1, skip_empty_rows=True)
        model2 = TabularDataModel(data, header_rows=1, skip_empty_rows=False)

        # Basic properties should be the same
        assert model1.column_names == model2.column_names
        assert model1.column_count == model2.column_count

        # Row count should be the same for this data
        assert model1.row_count == model2.row_count

    def test_cross_model_data_access(self):
        """Test accessing data across different model types."""
        data = [
            ["Name", "Age", "City"],
            ["John", "25", "NYC"],
            ["Jane", "30", "LA"],
        ]

        memory_model = TabularDataModel(data)
        streaming_model = StreamingTabularDataModel(iter([data]))

        # Test column access consistency - streaming model doesn't have column_values
        # So we compare by iterating through rows
        memory_rows = list(memory_model.iter_rows())
        streaming_rows = list(streaming_model.iter_rows())

        assert memory_rows == streaming_rows

        # Test column index consistency
        for col_name in memory_model.column_names:
            mem_index = memory_model.column_index(col_name)
            stream_index = streaming_model.column_index(col_name)
            assert mem_index == stream_index

        # Note: Streaming model doesn't have cell_value method like memory model


class TestErrorPropagation:
    """Test error propagation across component boundaries."""

    def test_validation_error_in_pipeline(self):
        """Test validation errors propagate correctly through pipeline."""
        # Data with validation issues
        data = [
            ["Name", "Age"],
            ["John", "25"],
            ["Jane", "not_a_number"],  # This would cause issues in typed conversion
        ]

        model = TabularDataModel(data)

        # Basic operations should work
        assert model.row_count == 2
        assert model.cell_value("Name", 0) == "John"

        # Test error in column access
        with pytest.raises(SplurgeTabularValueError):
            model.column_values("NonExistentColumn")

    def test_parameter_validation_integration(self):
        """Test parameter validation works with data models."""
        # Test with invalid header_rows (need non-empty data first)
        data = [["Name", "Age"], ["John", "25"]]
        from splurge_tabular.exceptions import SplurgeTabularValueError

        with pytest.raises(SplurgeTabularValueError):
            TabularDataModel(data, header_rows=-1)  # Invalid header_rows

        with pytest.raises(SplurgeTabularTypeError):
            TabularDataModel("not_a_list")  # Invalid data type

    def test_boundary_condition_handling(self):
        """Test boundary conditions are handled consistently."""
        # Empty data after header
        data = [["Name", "Age"]]  # Only header, no data rows

        model = TabularDataModel(data)
        assert model.row_count == 0
        assert model.column_count == 0  # No data rows means no columns determined

        # Test access to non-existent row
        with pytest.raises(SplurgeTabularLookupError):
            model.row(0)

        # Test cell access to non-existent row
        with pytest.raises(SplurgeTabularLookupError):
            model.cell_value("Name", 0)
