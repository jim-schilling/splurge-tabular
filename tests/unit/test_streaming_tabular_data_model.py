"""
Unit tests for splurge_tabular.streaming_tabular_data_model module.

Tests the StreamingTabularDataModel class for memory-efficient data processing.
"""

import pytest
from collections.abc import Iterator

from splurge_tabular.streaming_tabular_data_model import StreamingTabularDataModel


class TestStreamingTabularDataModel:
    """Test the StreamingTabularDataModel class."""

    def test_basic_initialization_with_headers(self):
        """Test basic initialization with header rows."""
        def data_stream() -> Iterator[list[list[str]]]:
            yield [["Name", "Age"], ["John", "30"], ["Jane", "25"]]

        model = StreamingTabularDataModel(data_stream())

        assert model.column_names == ["Name", "Age"]
        assert model.column_count == 2

    def test_initialization_without_headers(self):
        """Test initialization without header rows."""
        def data_stream() -> Iterator[list[list[str]]]:
            yield [["John", "30"], ["Jane", "25"]]

        model = StreamingTabularDataModel(data_stream(), header_rows=0)

        assert model.column_names == ["column_0", "column_1"]
        assert model.column_count == 2

    def test_multiple_header_rows(self):
        """Test with multiple header rows."""
        def data_stream() -> Iterator[list[list[str]]]:
            yield [["Personal", "Personal"], ["Name", "Age"], ["John", "30"]]

        model = StreamingTabularDataModel(data_stream(), header_rows=2)

        assert model.column_names == ["Personal_Name", "Personal_Age"]
        assert model.column_count == 2

    def test_column_index_valid(self):
        """Test getting valid column index."""
        def data_stream() -> Iterator[list[list[str]]]:
            yield [["Name", "Age"]]

        model = StreamingTabularDataModel(data_stream())

        assert model.column_index("Name") == 0
        assert model.column_index("Age") == 1

    def test_column_index_invalid(self):
        """Test getting index for non-existent column."""
        def data_stream() -> Iterator[list[list[str]]]:
            yield [["Name", "Age"]]

        model = StreamingTabularDataModel(data_stream())

        with pytest.raises(ValueError, match="Column name Invalid not found"):
            model.column_index("Invalid")

    def test_iteration_with_headers(self):
        """Test iterating over rows with headers."""
        def data_stream() -> Iterator[list[list[str]]]:
            yield [["Name", "Age"], ["John", "30"], ["Jane", "25"]]

        model = StreamingTabularDataModel(data_stream())
        rows = list(model)

        assert len(rows) == 2
        assert rows[0] == ["John", "30"]
        assert rows[1] == ["Jane", "25"]

    def test_iteration_without_headers(self):
        """Test iterating over rows without headers."""
        def data_stream() -> Iterator[list[list[str]]]:
            yield [["John", "30"], ["Jane", "25"]]

        model = StreamingTabularDataModel(data_stream(), header_rows=0)
        rows = list(model)

        assert len(rows) == 2
        assert rows[0] == ["John", "30"]
        assert rows[1] == ["Jane", "25"]

    def test_skip_empty_rows_enabled(self):
        """Test skipping empty rows when enabled."""
        def data_stream() -> Iterator[list[list[str]]]:
            yield [["Name", "Age"], ["John", "30"], ["", ""], ["Jane", "25"]]

        model = StreamingTabularDataModel(data_stream(), skip_empty_rows=True)
        rows = list(model)

        assert len(rows) == 2
        assert rows[0] == ["John", "30"]
        assert rows[1] == ["Jane", "25"]

    def test_skip_empty_rows_disabled(self):
        """Test not skipping empty rows when disabled."""
        def data_stream() -> Iterator[list[list[str]]]:
            yield [["Name", "Age"], ["John", "30"], ["", ""], ["Jane", "25"]]

        model = StreamingTabularDataModel(data_stream(), skip_empty_rows=False)
        rows = list(model)

        assert len(rows) == 3
        assert rows[0] == ["John", "30"]
        assert rows[1] == ["", ""]
        assert rows[2] == ["Jane", "25"]

    def test_iter_rows_as_dicts(self):
        """Test iterating rows as dictionaries."""
        def data_stream() -> Iterator[list[list[str]]]:
            yield [["Name", "Age"], ["John", "30"], ["Jane", "25"]]

        model = StreamingTabularDataModel(data_stream())
        rows = list(model.iter_rows())

        assert len(rows) == 2
        assert rows[0] == {"Name": "John", "Age": "30"}
        assert rows[1] == {"Name": "Jane", "Age": "25"}

    def test_iter_rows_as_tuples(self):
        """Test iterating rows as tuples."""
        def data_stream() -> Iterator[list[list[str]]]:
            yield [["Name", "Age"], ["John", "30"], ["Jane", "25"]]

        model = StreamingTabularDataModel(data_stream())
        rows = list(model.iter_rows_as_tuples())

        assert len(rows) == 2
        assert rows[0] == ("John", "30")
        assert rows[1] == ("Jane", "25")

    def test_chunked_stream_processing(self):
        """Test processing data in multiple chunks."""
        def data_stream() -> Iterator[list[list[str]]]:
            yield [["Name", "Age"], ["John", "30"]]
            yield [["Jane", "25"], ["Bob", "35"]]

        model = StreamingTabularDataModel(data_stream())
        rows = list(model)

        assert len(rows) == 3
        assert rows[0] == ["John", "30"]
        assert rows[1] == ["Jane", "25"]
        assert rows[2] == ["Bob", "35"]

    def test_row_normalization_shorter(self):
        """Test normalizing rows that are shorter than column count."""
        def data_stream() -> Iterator[list[list[str]]]:
            yield [["Name", "Age", "City"], ["John", "30"]]

        model = StreamingTabularDataModel(data_stream())
        rows = list(model)

        assert len(rows) == 1
        assert rows[0] == ["John", "30", ""]

    def test_row_normalization_longer(self):
        """Test normalizing rows that are longer than initial column count."""
        def data_stream() -> Iterator[list[list[str]]]:
            yield [["Name", "Age"], ["John", "30", "NYC"]]

        model = StreamingTabularDataModel(data_stream())
        rows = list(model)

        assert len(rows) == 1
        assert rows[0] == ["John", "30", "NYC"]
        # Column names should be extended
        assert len(model.column_names) == 3
        assert "column_2" in model.column_names

    def test_clear_buffer(self):
        """Test clearing the buffer."""
        def data_stream() -> Iterator[list[list[str]]]:
            yield [["Name", "Age"], ["John", "30"]]

        model = StreamingTabularDataModel(data_stream())
        # Buffer should have data after initialization
        assert len(model._buffer) > 0

        model.clear_buffer()
        assert len(model._buffer) == 0

    def test_reset_stream(self):
        """Test resetting the stream."""
        def data_stream() -> Iterator[list[list[str]]]:
            yield [["Name", "Age"], ["John", "30"]]

        model = StreamingTabularDataModel(data_stream())
        assert model._is_initialized is True

        model.reset_stream()
        assert model._is_initialized is False
        assert len(model._buffer) == 0

    def test_initialization_validation(self):
        """Test initialization parameter validation."""
        # Test None stream
        with pytest.raises(ValueError, match="Stream is required"):
            StreamingTabularDataModel(None)

        # Test negative header_rows
        def dummy_stream():
            return iter([])

        with pytest.raises(ValueError, match="Header rows must be greater than or equal to 0"):
            StreamingTabularDataModel(dummy_stream(), header_rows=-1)

        # Test small chunk_size
        with pytest.raises(ValueError, match="chunk_size must be at least 100"):
            StreamingTabularDataModel(dummy_stream(), chunk_size=50)

    def test_empty_stream_handling(self):
        """Test handling of empty streams."""
        def empty_stream() -> Iterator[list[list[str]]]:
            return iter([])

        model = StreamingTabularDataModel(empty_stream(), header_rows=0)
        rows = list(model)

        assert len(rows) == 0
        assert model.column_count == 0
