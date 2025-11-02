import pytest

from splurge_tabular.exceptions import (
    SplurgeTabularLookupError,
    SplurgeTabularTypeError,
    SplurgeTabularValueError,
)
from splurge_tabular.streaming_tabular_data_model import StreamingTabularDataModel
from splurge_tabular.tabular_data_model import TabularDataModel


def test_tabular_init_header_rows_negative_raises_config_error():
    data = [["col1", "col2"], ["1", "2"]]
    with pytest.raises(SplurgeTabularValueError):
        TabularDataModel(data, header_rows=-1)


def test_tabular_column_index_missing_raises_column_error():
    data = [["col1", "col2"], ["1", "2"]]
    model = TabularDataModel(data, header_rows=1)
    with pytest.raises(SplurgeTabularLookupError):
        model.column_index("missing")


def test_tabular_cell_value_row_out_of_range_raises_row_error():
    data = [["col1", "col2"], ["1", "2"]]
    model = TabularDataModel(data, header_rows=1)
    with pytest.raises(SplurgeTabularLookupError):
        model.cell_value("col1", 5)


def test_streaming_init_stream_none_raises_type_error():
    with pytest.raises(SplurgeTabularTypeError):
        StreamingTabularDataModel(None)


def test_streaming_init_chunk_size_too_small_raises_value_error():
    # stream is an iterator over chunks (each chunk is a list of rows)
    stream = iter([[["h1", "h2"], ["r1", "r2"]]])
    with pytest.raises(SplurgeTabularValueError):
        StreamingTabularDataModel(stream, chunk_size=50)


def test_streaming_init_header_rows_negative_raises_value_error():
    stream = iter([[["h1", "h2"], ["r1", "r2"]]])
    with pytest.raises(SplurgeTabularValueError):
        StreamingTabularDataModel(stream, header_rows=-1)
