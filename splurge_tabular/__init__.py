"""Splurge Tabular Library.

A Python library for tabular data processing with in-memory and streaming support.

Copyright (c) 2025 Jim Schilling

Please preserve this header and all related material when sharing!

This module is licensed under the MIT License.
"""

from __future__ import annotations

__version__ = "2025.2.0"

# Main classes
# Utility functions
from .common_utils import ensure_minimum_columns

# Exceptions
from .exceptions import (
    SplurgeTabularError,
    SplurgeTabularLookupError,
    SplurgeTabularTypeError,
    SplurgeTabularValueError,
)

# Protocols
from .protocols import StreamingTabularDataProtocol, TabularDataProtocol
from .streaming_tabular_data_model import StreamingTabularDataModel
from .tabular_data_model import TabularDataModel
from .tabular_utils import normalize_rows, process_headers

__all__ = [
    # Version
    "__version__",
    # Main classes
    "TabularDataModel",
    "StreamingTabularDataModel",
    # Protocols
    "TabularDataProtocol",
    "StreamingTabularDataProtocol",
    # Utilities
    "process_headers",
    "ensure_minimum_columns",
    "normalize_rows",
    # Exceptions
    "SplurgeTabularError",
    "SplurgeTabularTypeError",
    "SplurgeTabularValueError",
    "SplurgeTabularLookupError",
]
