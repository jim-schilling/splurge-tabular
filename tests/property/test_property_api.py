from __future__ import annotations

from typing import Any

import pytest
from hypothesis import given
from hypothesis import strategies as st

from splurge_tabular.common_utils import (
    ensure_minimum_columns,
    safe_dict_access,
    safe_index_access,
    standardize_column_names,
)
from splurge_tabular.exceptions import (
    SplurgeTabularColumnError,
    SplurgeTabularIndexError,
    SplurgeTabularKeyError,
)
from splurge_tabular.tabular_data_model import TabularDataModel


@given(headers=st.lists(st.text(min_size=0, max_size=20), min_size=0, max_size=10))
def test_standardize_column_names_preserves_length_and_non_empty(headers: list[str]):
    result = standardize_column_names(headers, fill_empty=True, prefix="c_")
    assert len(result) == len(headers)
    for i, name in enumerate(result):
        # name should be non-empty
        assert isinstance(name, str) and name != ""
        if headers[i] and headers[i].strip():
            assert name == headers[i].strip()
        else:
            assert name.startswith("c_")


@given(
    row=st.lists(st.text(min_size=0, max_size=10), min_size=0, max_size=8),
    min_columns=st.integers(min_value=0, max_value=12),
    fill_value=st.text(min_size=0, max_size=3),
)
def test_ensure_minimum_columns_pads_correctly(row: list[str], min_columns: int, fill_value: str):
    padded = ensure_minimum_columns(row, min_columns, fill_value=fill_value)
    assert len(padded) >= min_columns
    # original items preserved in order as prefix
    for i, v in enumerate(row):
        assert padded[i] == v
    # padding uses fill_value
    if len(row) < min_columns:
        assert all(x == fill_value for x in padded[len(row) :])


@given(
    items=st.lists(st.integers(), min_size=0, max_size=6),
    index=st.integers(min_value=-5, max_value=10),
    default=st.one_of(st.none(), st.integers()),
)
def test_safe_index_access_behaviour(items: list[int], index: int, default: Any):
    if 0 <= index < len(items):
        assert safe_index_access(items, index, default=default) == items[index]
    else:
        if default is not None:
            assert safe_index_access(items, index, default=default) == default
        else:
            with pytest.raises(SplurgeTabularIndexError):
                safe_index_access(items, index)


@given(
    keys=st.lists(st.text(min_size=1, max_size=6), min_size=0, max_size=6, unique=True),
    lookup=st.text(min_size=0, max_size=6),
)
def test_safe_dict_access_behaviour(keys: list[str], lookup: str):
    d = {k: f"v:{k}" for k in keys}
    if lookup in d:
        assert safe_dict_access(d, lookup) == d[lookup]
        assert safe_dict_access(d, lookup, default="x") == d[lookup]
    else:
        # default should be returned if provided
        assert safe_dict_access(d, lookup, default="x") == "x"
        # missing without default raises appropriate error depending on item_name
        with pytest.raises(SplurgeTabularColumnError):
            safe_dict_access(d, lookup, item_name="column")
        with pytest.raises(SplurgeTabularKeyError):
            safe_dict_access(d, lookup, item_name="key")


@given(
    rows=st.lists(st.lists(st.text(min_size=0, max_size=6), min_size=1, max_size=5), min_size=1, max_size=8),
    header_rows=st.integers(min_value=0, max_value=2),
)
def test_tabular_data_model_basic_invariants(rows: list[list[str]], header_rows: int):
    # ensure header_rows is not larger than rows-1 (keep at least one data row)
    hr = min(header_rows, max(0, len(rows) - 1))
    model = TabularDataModel(rows, header_rows=hr, skip_empty_rows=False)
    # column_names may be longer than the actual column_count (headers can
    # specify more names than the first data row has); ensure the relation
    # holds that there are at least as many column names as reported columns.
    assert len(model.column_names) >= model.column_count
    # column_index should return a valid index and map back to the same name
    for name in model.column_names:
        idx = model.column_index(name)
    # index should be within the range of known column names (headers)
    assert 0 <= idx < len(model.column_names)
    assert model.column_names[idx] == name
    # iterating rows yields row_count rows
    assert sum(1 for _ in model) == model.row_count
    # row dict keys correspond to column_names
    if model.row_count > 0:
        rowdict = next(model.iter_rows())
        keys = list(rowdict.keys())
    # rowdict keys should be a subset of known column names. We avoid
    # asserting strict ordering because header names can duplicate and
    # streaming rows may dynamically extend columns.
    assert set(keys).issubset(set(model.column_names))
