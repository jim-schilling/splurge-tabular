from __future__ import annotations

import pytest
from hypothesis import given
from hypothesis import strategies as st

from splurge_tabular.common_utils import batch_validate_rows
from splurge_tabular.exceptions import (
    SplurgeTabularTypeError,
    SplurgeTabularValueError,
)
from splurge_tabular.tabular_data_model import TabularDataModel


@given(rows=st.lists(st.one_of(st.integers(), st.text(), st.none()), min_size=1, max_size=10))
def test_batch_validate_rows_invalid_shape(rows):
    # batch_validate_rows expects iterable of list[str]; passing wrong shapes should raise
    with pytest.raises(SplurgeTabularTypeError):
        list(batch_validate_rows(rows, min_columns=1))


def test_tabular_data_model_header_rows_invalid():
    data = [["a"]]
    with pytest.raises(SplurgeTabularValueError):
        TabularDataModel(data, header_rows=-1)
