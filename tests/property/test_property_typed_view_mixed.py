from __future__ import annotations

from hypothesis import given
from hypothesis import strategies as st

from splurge_tabular.tabular_data_model import TabularDataModel


@given(
    # Generate between 1 and 4 columns, mixing digits, floats, and words
    cols=st.lists(st.sampled_from(["int", "float", "str"]), min_size=1, max_size=4),
    nrows=st.integers(min_value=1, max_value=12),
)
def test_typed_view_mixed_columns(cols: list[str], nrows: int):
    header = [f"c{i}" for i in range(len(cols))]
    rows = []
    for r in range(nrows):
        row = []
        for t in cols:
            if t == "int":
                row.append(str(r * 10 + 1))
            elif t == "float":
                row.append(f"{r}.{r + 1}")
            else:
                row.append(f"s{r}")
        rows.append(row)

    model = TabularDataModel([header] + rows, header_rows=1, skip_empty_rows=False)
    typed = model.to_typed()

    # For each column, ensure homogenous inferred types
    for name in typed.column_names:
        values = typed.column_values(name)
        types = {type(v) for v in values}
        assert len(types) == 1
        # ensure values are accessible
        for v in values:
            _ = v
