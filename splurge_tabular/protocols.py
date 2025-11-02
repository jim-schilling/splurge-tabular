"""Protocol definitions for splurge-tabular package.

This module defines Protocol classes that establish contracts for common interfaces
used throughout the package. These protocols enable better type checking and
ensure consistent behavior across related classes.

Copyright (c) 2025 Jim Schilling

Please preserve this header and all related material when sharing!

This module is licensed under the MIT License.
"""

from collections.abc import Generator, Iterator
from typing import Protocol, runtime_checkable

from ._vendor.splurge_typer.data_type import DataType


@runtime_checkable
class TabularDataProtocol(Protocol):
    """Protocol for tabular data models.

    This protocol defines the interface that all tabular data models should
    implement, ensuring consistent behavior across different implementations.
    """

    @property
    def column_names(self) -> list[str]:
        """List of column names in order.

        Returns:
            list[str]: Column names in their defined order.
        """
        ...  # pragma: no cover

    @property
    def row_count(self) -> int:
        """Number of data rows.

        Returns:
            int: Number of rows in the dataset.
        """
        ...  # pragma: no cover

    @property
    def column_count(self) -> int:
        """Number of columns.

        Returns:
            int: Number of columns in the dataset.
        """
        ...  # pragma: no cover

    def column_index(self, name: str) -> int:
        """Get the zero-based index of a column by name.

        Args:
            name (str): Column name to find.

        Returns:
            int: Zero-based index of the column.
        """
        ...  # pragma: no cover

    def column_type(self, name: str) -> DataType:
        """Get the inferred data type of a column.

        Args:
            name (str): Column name.

        Returns:
            DataType: Inferred data type for the column.
        """
        ...  # pragma: no cover

    def column_values(self, name: str) -> list[str]:
        """Return all values for a specific column.

        Args:
            name (str): Column name.

        Returns:
            list[str]: All values in the column.
        """
        ...  # pragma: no cover

    def cell_value(self, name: str, row_index: int) -> str:
        """Return the value of a specific cell.

        Args:
            name (str): Column name.
            row_index (int): Zero-based row index.

        Returns:
            str: Value at the specified cell.
        """
        ...  # pragma: no cover

    def row(self, index: int) -> dict[str, str]:
        """Return a row as a dictionary.

        Args:
            index (int): Zero-based row index.

        Returns:
            dict[str, str]: Row data mapping column names to values.
        """
        ...  # pragma: no cover

    def row_as_list(self, index: int) -> list[str]:
        """Return a row as a list of values.

        Args:
            index (int): Zero-based row index.

        Returns:
            list[str]: Row data as a list.
        """
        ...  # pragma: no cover

    def row_as_tuple(self, index: int) -> tuple[str, ...]:
        """Return a row as a tuple of values.

        Args:
            index (int): Zero-based row index.

        Returns:
            tuple[str, ...]: Row data as a tuple.
        """
        ...  # pragma: no cover

    def __iter__(self) -> Iterator[list[str]]:
        """Iterate over rows as lists of strings.

        Returns:
            Iterator[list[str]]: Iterator yielding rows as lists of strings.
        """
        ...  # pragma: no cover

    def iter_rows(self) -> Generator[dict[str, str], None, None]:
        """Iterate over rows as dictionaries.

        Returns:
            Generator[dict[str, str], None, None]: Generator yielding rows as dictionaries with column names as keys.
        """
        ...  # pragma: no cover

    def iter_rows_as_tuples(self) -> Generator[tuple[str, ...], None, None]:
        """Iterate over rows as tuples.

        Returns:
            Generator[tuple[str, ...], None, None]: Generator yielding rows as tuples of values.
        """
        ...  # pragma: no cover


@runtime_checkable
class StreamingTabularDataProtocol(Protocol):
    """Protocol for streaming tabular data models.

    This protocol defines the minimal interface for streaming data models that
    process data without loading everything into memory.
    """

    @property
    def column_names(self) -> list[str]:
        """List of column names in order.

        Returns:
            list[str]: Column names in their defined order.
        """
        ...  # pragma: no cover

    @property
    def column_count(self) -> int:
        """Number of columns.

        Returns:
            int: Number of columns in the dataset.
        """
        ...  # pragma: no cover

    def column_index(self, name: str) -> int:
        """Get the zero-based index of a column by name.

        Args:
            name (str): Column name to find.

        Returns:
            int: Zero-based index of the column.
        """
        ...  # pragma: no cover

    def __iter__(self) -> Iterator[list[str]]:
        """Iterate over rows as lists of strings.

        Returns:
            Iterator[list[str]]: Iterator yielding rows as lists of strings.
        """
        ...  # pragma: no cover

    def iter_rows(self) -> Generator[dict[str, str], None, None]:
        """Iterate over rows as dictionaries.

        Returns:
            Generator[dict[str, str], None, None]: Generator yielding rows as dictionaries with column names as keys.
        """
        ...  # pragma: no cover

    def iter_rows_as_tuples(self) -> Generator[tuple[str, ...], None, None]:
        """Iterate over rows as tuples.

        Returns:
            Generator[tuple[str, ...], None, None]: Generator yielding rows as tuples of values.
        """
        ...  # pragma: no cover

    def clear_buffer(self) -> None:
        """Clear any buffered data.

        This method should clear any internal buffers used for streaming data.
        """
        ...  # pragma: no cover

    def reset_stream(self) -> None:
        """Reset the stream to the beginning.

        This method should reset the stream position to allow re-reading from the start.
        """
        ...  # pragma: no cover
