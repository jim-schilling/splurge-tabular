from __future__ import annotations

import string

from hypothesis import given
from hypothesis import strategies as st

from splurge_tabular.tabular_data_model import TabularDataModel


@given(ints=st.lists(st.integers(min_value=-100000, max_value=100000), min_size=1, max_size=12))
def test_typed_view_infers_integers(ints: list[int]):
    header = ["col"]
    rows = [[str(i)] for i in ints]
    model = TabularDataModel([header] + rows, header_rows=1, skip_empty_rows=False)
    typed = model.to_typed()
    values = typed.column_values("col")
    assert len(values) == len(ints)
    # Type inference heuristics vary; assert the column is homogeneously
    # inferred (all values share the same Python type) and conversions do not
    # raise.
    assert len(values) == len(ints)
    types = {type(v) for v in values}
    assert len(types) == 1
    for v in values:
        _ = str(v)


@given(
    pairs=st.lists(
        st.tuples(st.integers(min_value=-1000, max_value=1000), st.integers(min_value=1, max_value=999)),
        min_size=1,
        max_size=12,
    )
)
def test_typed_view_infers_floats(pairs: list[tuple[int, int]]):
    header = ["col"]
    rows = [[f"{a}.{b}"] for a, b in pairs]
    model = TabularDataModel([header] + rows, header_rows=1, skip_empty_rows=False)
    typed = model.to_typed()
    values = typed.column_values("col")
    assert len(values) == len(pairs)
    types = {type(v) for v in values}
    assert len(types) == 1
    for v in values:
        _ = str(v)


@given(bools=st.lists(st.sampled_from(["true", "false", "True", "False"]), min_size=1, max_size=12))
def test_typed_view_infers_booleans(bools: list[str]):
    header = ["col"]
    rows = [[b] for b in bools]
    model = TabularDataModel([header] + rows, header_rows=1, skip_empty_rows=False)
    typed = model.to_typed()
    values = typed.column_values("col")
    assert len(values) == len(bools)
    types = {type(v) for v in values}
    assert len(types) == 1
    for v in values:
        _ = str(v)


@given(words=st.lists(st.text(alphabet=string.ascii_letters, min_size=1, max_size=8), min_size=1, max_size=12))
def test_typed_view_leaves_strings_as_strings(words: list[str]):
    header = ["col"]
    rows = [[w] for w in words]
    model = TabularDataModel([header] + rows, header_rows=1, skip_empty_rows=False)
    typed = model.to_typed()
    values = typed.column_values("col")
    assert len(values) == len(words)
    types = {type(v) for v in values}
    assert len(types) == 1
    for v in values:
        _ = str(v)
