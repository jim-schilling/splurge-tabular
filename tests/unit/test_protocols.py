"""Unit tests for splurge_tabular.protocols module.

Tests protocol definitions and runtime protocol checking.
"""

from splurge_tabular import (
    StreamingTabularDataModel,
    StreamingTabularDataProtocol,
    TabularDataModel,
    TabularDataProtocol,
)
from splurge_tabular._vendor.splurge_typer.data_type import DataType


class TestTabularDataProtocol:
    """Test TabularDataProtocol runtime checking and interface."""

    def test_tabular_data_model_implements_protocol(self) -> None:
        """Test that TabularDataModel implements TabularDataProtocol."""
        data = [["Name", "Age"], ["Alice", "28"], ["Bob", "35"]]
        model = TabularDataModel(data)

        assert isinstance(model, TabularDataProtocol)

    def test_protocol_properties(self) -> None:
        """Test that protocol properties are accessible."""
        data = [["Name", "Age"], ["Alice", "28"], ["Bob", "35"]]
        model = TabularDataModel(data)

        # Test all protocol properties
        assert hasattr(model, "column_names")
        assert hasattr(model, "row_count")
        assert hasattr(model, "column_count")

        assert isinstance(model.column_names, list)
        assert isinstance(model.row_count, int)
        assert isinstance(model.column_count, int)

    def test_protocol_methods(self) -> None:
        """Test that all protocol methods are callable."""
        data = [["Name", "Age"], ["Alice", "28"], ["Bob", "35"]]
        model = TabularDataModel(data)

        # Test all protocol methods exist and are callable
        assert callable(model.column_index)
        assert callable(model.column_type)
        assert callable(model.column_values)
        assert callable(model.cell_value)
        assert callable(model.row)
        assert callable(model.row_as_list)
        assert callable(model.row_as_tuple)
        assert callable(model.iter_rows)
        assert callable(model.iter_rows_as_tuples)

    def test_protocol_column_index(self) -> None:
        """Test column_index method via protocol."""
        data = [["Name", "Age"], ["Alice", "28"], ["Bob", "35"]]
        model = TabularDataModel(data)

        assert model.column_index("Name") == 0
        assert model.column_index("Age") == 1

    def test_protocol_column_type(self) -> None:
        """Test column_type method via protocol."""
        data = [["Name", "Age"], ["Alice", "28"], ["Bob", "35"]]
        model = TabularDataModel(data)

        col_type = model.column_type("Age")
        assert isinstance(col_type, DataType)

    def test_protocol_column_values(self) -> None:
        """Test column_values method via protocol."""
        data = [["Name", "Age"], ["Alice", "28"], ["Bob", "35"]]
        model = TabularDataModel(data)

        values = model.column_values("Name")
        assert isinstance(values, list)
        assert all(isinstance(v, str) for v in values)

    def test_protocol_cell_value(self) -> None:
        """Test cell_value method via protocol."""
        data = [["Name", "Age"], ["Alice", "28"], ["Bob", "35"]]
        model = TabularDataModel(data)

        value = model.cell_value("Name", 0)
        assert isinstance(value, str)
        assert value == "Alice"

    def test_protocol_row(self) -> None:
        """Test row method via protocol."""
        data = [["Name", "Age"], ["Alice", "28"], ["Bob", "35"]]
        model = TabularDataModel(data)

        row_dict = model.row(0)
        assert isinstance(row_dict, dict)
        assert all(isinstance(k, str) for k in row_dict.keys())
        assert all(isinstance(v, str) for v in row_dict.values())

    def test_protocol_row_as_list(self) -> None:
        """Test row_as_list method via protocol."""
        data = [["Name", "Age"], ["Alice", "28"], ["Bob", "35"]]
        model = TabularDataModel(data)

        row_list = model.row_as_list(0)
        assert isinstance(row_list, list)
        assert all(isinstance(v, str) for v in row_list)

    def test_protocol_row_as_tuple(self) -> None:
        """Test row_as_tuple method via protocol."""
        data = [["Name", "Age"], ["Alice", "28"], ["Bob", "35"]]
        model = TabularDataModel(data)

        row_tuple = model.row_as_tuple(0)
        assert isinstance(row_tuple, tuple)
        assert all(isinstance(v, str) for v in row_tuple)

    def test_protocol_iteration(self) -> None:
        """Test __iter__ method via protocol."""
        data = [["Name", "Age"], ["Alice", "28"], ["Bob", "35"]]
        model = TabularDataModel(data)

        rows = list(model)
        assert len(rows) == 2
        assert all(isinstance(row, list) for row in rows)
        assert all(isinstance(v, str) for row in rows for v in row)

    def test_protocol_iter_rows(self) -> None:
        """Test iter_rows method via protocol."""
        data = [["Name", "Age"], ["Alice", "28"], ["Bob", "35"]]
        model = TabularDataModel(data)

        rows = list(model.iter_rows())
        assert len(rows) == 2
        assert all(isinstance(row, dict) for row in rows)
        assert all(isinstance(k, str) for row in rows for k in row.keys())
        assert all(isinstance(v, str) for row in rows for v in row.values())

    def test_protocol_iter_rows_as_tuples(self) -> None:
        """Test iter_rows_as_tuples method via protocol."""
        data = [["Name", "Age"], ["Alice", "28"], ["Bob", "35"]]
        model = TabularDataModel(data)

        rows = list(model.iter_rows_as_tuples())
        assert len(rows) == 2
        assert all(isinstance(row, tuple) for row in rows)
        assert all(isinstance(v, str) for row in rows for v in row)

    def test_protocol_duck_typing(self) -> None:
        """Test protocol-based duck typing."""

        def process_tabular_data(model: TabularDataProtocol) -> list[str]:
            """Function that accepts any TabularDataProtocol."""
            return model.column_names

        data = [["Name", "Age"], ["Alice", "28"]]
        model = TabularDataModel(data)

        result = process_tabular_data(model)
        assert result == ["Name", "Age"]


class TestStreamingTabularDataProtocol:
    """Test StreamingTabularDataProtocol runtime checking and interface."""

    def test_streaming_tabular_data_model_implements_protocol(self) -> None:
        """Test that StreamingTabularDataModel implements StreamingTabularDataProtocol."""

        def create_stream():
            yield [["Name", "Age"], ["Alice", "28"], ["Bob", "35"]]

        model = StreamingTabularDataModel(create_stream())
        assert isinstance(model, StreamingTabularDataProtocol)

    def test_streaming_protocol_properties(self) -> None:
        """Test that streaming protocol properties are accessible."""

        def create_stream():
            yield [["Name", "Age"], ["Alice", "28"], ["Bob", "35"]]

        model = StreamingTabularDataModel(create_stream())

        # Test all protocol properties
        assert hasattr(model, "column_names")
        assert hasattr(model, "column_count")

        assert isinstance(model.column_names, list)
        assert isinstance(model.column_count, int)

    def test_streaming_protocol_methods(self) -> None:
        """Test that all streaming protocol methods are callable."""

        def create_stream():
            yield [["Name", "Age"], ["Alice", "28"], ["Bob", "35"]]

        model = StreamingTabularDataModel(create_stream())

        # Test all protocol methods exist and are callable
        assert callable(model.column_index)
        assert callable(model.iter_rows)
        assert callable(model.iter_rows_as_tuples)
        assert callable(model.clear_buffer)
        assert callable(model.reset_stream)

    def test_streaming_protocol_column_index(self) -> None:
        """Test column_index method via streaming protocol."""

        def create_stream():
            yield [["Name", "Age"], ["Alice", "28"], ["Bob", "35"]]

        model = StreamingTabularDataModel(create_stream())

        assert model.column_index("Name") == 0
        assert model.column_index("Age") == 1

    def test_streaming_protocol_iteration(self) -> None:
        """Test __iter__ method via streaming protocol."""

        def create_stream():
            yield [["Name", "Age"], ["Alice", "28"], ["Bob", "35"]]

        model = StreamingTabularDataModel(create_stream())

        rows = list(model)
        assert len(rows) == 2
        assert all(isinstance(row, list) for row in rows)
        assert all(isinstance(v, str) for row in rows for v in row)

    def test_streaming_protocol_iter_rows(self) -> None:
        """Test iter_rows method via streaming protocol."""

        def create_stream():
            yield [["Name", "Age"], ["Alice", "28"], ["Bob", "35"]]

        model = StreamingTabularDataModel(create_stream())

        rows = list(model.iter_rows())
        assert len(rows) == 2
        assert all(isinstance(row, dict) for row in rows)
        assert all(isinstance(k, str) for row in rows for k in row.keys())
        assert all(isinstance(v, str) for row in rows for v in row.values())

    def test_streaming_protocol_iter_rows_as_tuples(self) -> None:
        """Test iter_rows_as_tuples method via streaming protocol."""

        def create_stream():
            yield [["Name", "Age"], ["Alice", "28"], ["Bob", "35"]]

        model = StreamingTabularDataModel(create_stream())

        rows = list(model.iter_rows_as_tuples())
        assert len(rows) == 2
        assert all(isinstance(row, tuple) for row in rows)
        assert all(isinstance(v, str) for row in rows for v in row)

    def test_streaming_protocol_clear_buffer(self) -> None:
        """Test clear_buffer method via streaming protocol."""

        def create_stream():
            yield [["Name", "Age"], ["Alice", "28"], ["Bob", "35"]]

        model = StreamingTabularDataModel(create_stream())

        # Clear buffer should not raise
        model.clear_buffer()
        assert len(model._buffer) == 0

    def test_streaming_protocol_reset_stream(self) -> None:
        """Test reset_stream method via streaming protocol."""

        def create_stream():
            yield [["Name", "Age"], ["Alice", "28"], ["Bob", "35"]]

        model = StreamingTabularDataModel(create_stream())

        # Reset stream should not raise
        model.reset_stream()
        assert not model._is_initialized

    def test_streaming_protocol_duck_typing(self) -> None:
        """Test protocol-based duck typing for streaming protocol."""

        def process_streaming_data(model: StreamingTabularDataProtocol) -> list[str]:
            """Function that accepts any StreamingTabularDataProtocol."""
            return model.column_names

        def create_stream():
            yield [["Name", "Age"], ["Alice", "28"]]

        model = StreamingTabularDataModel(create_stream())

        result = process_streaming_data(model)
        assert result == ["Name", "Age"]


class TestProtocolRuntimeChecking:
    """Test runtime protocol checking functionality."""

    def test_tabular_protocol_is_runtime_checkable(self) -> None:
        """Test that TabularDataProtocol is runtime checkable."""
        assert hasattr(TabularDataProtocol, "__instancecheck__")

        data = [["Name", "Age"], ["Alice", "28"]]
        model = TabularDataModel(data)

        # Runtime check should work
        assert isinstance(model, TabularDataProtocol)

    def test_streaming_protocol_is_runtime_checkable(self) -> None:
        """Test that StreamingTabularDataProtocol is runtime checkable."""
        assert hasattr(StreamingTabularDataProtocol, "__instancecheck__")

        def create_stream():
            yield [["Name", "Age"], ["Alice", "28"]]

        model = StreamingTabularDataModel(create_stream())

        # Runtime check should work
        assert isinstance(model, StreamingTabularDataProtocol)

    def test_non_protocol_object_not_matches(self) -> None:
        """Test that non-protocol objects don't match protocols."""

        class NotAProtocol:
            pass

        obj = NotAProtocol()

        # Should not match TabularDataProtocol
        assert not isinstance(obj, TabularDataProtocol)
        assert not isinstance(obj, StreamingTabularDataProtocol)
