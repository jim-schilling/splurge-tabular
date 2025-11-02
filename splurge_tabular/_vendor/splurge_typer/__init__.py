"""splurge-typer package.

Utilities for inferring Python data types from strings and converting between
different data representations.

This package exposes the primary APIs used by consumers:

Examples:

    >>> from splurge_typer import TypeInference, DataType
    >>> ti = TypeInference()
    >>> ti.infer_type('123')
    DataType.INTEGER

Attributes:
    __version__ (str): The package version.

Copyright (c) 2025 Jim Schilling

Please preserve this header and all related material when sharing!

This module is licensed under the MIT License.
"""

from .data_type import DataType
from .duck_typing import DuckTyping
from .string import String
from .type_inference import TypeInference

__version__ = "2025.3.0"
__all__ = [
    __version__,
    "DataType",
    "String",
    "TypeInference",
    "DuckTyping",
    # Exception classes are available from the submodule `splurge_typer.exceptions`
]
