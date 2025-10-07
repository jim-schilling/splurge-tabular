from __future__ import annotations

from typing import Any

import pytest
from hypothesis import given
from hypothesis import strategies as st

from splurge_tabular.common_utils import batch_validate_rows, validate_data_structure
from splurge_tabular.exceptions import (
    SplurgeTabularConfigurationError,
    SplurgeTabularTypeError,
)
from splurge_tabular.tabular_data_model import TabularDataModel


@given(obj=st.one_of(st.none(), st.integers(), st.text()))
def test_validate_data_structure_invalid_types(obj: Any):
    # validate_data_structure should raise TypeError if the type doesn't match expected
    with pytest.raises(SplurgeTabularTypeError):
        validate_data_structure(obj, expected_type=list, param_name="data")


@given(rows=st.lists(st.one_of(st.integers(), st.text(), st.none()), min_size=1, max_size=10))
def test_batch_validate_rows_invalid_shape(rows):
    # batch_validate_rows expects iterable of list[str]; passing wrong shapes should raise
    with pytest.raises(SplurgeTabularTypeError):
        list(batch_validate_rows(rows, min_columns=1))


def test_tabular_data_model_header_rows_invalid():
    data = [["a"]]
    with pytest.raises(SplurgeTabularConfigurationError):
        TabularDataModel(data, header_rows=-1)
