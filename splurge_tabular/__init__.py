"""Splurge Tabular Library.

A Python library for tabular data processing with in-memory and streaming support.

Copyright (c) 2025 Jim Schilling

Please preserve this header and all related material when sharing!

This module is licensed under the MIT License.
"""

from __future__ import annotations

__version__ = "2025.1.0"

# Main classes
# Utility functions
from splurge_tabular.common_utils import ensure_minimum_columns, safe_file_operation, validate_data_structure

# Exceptions
from splurge_tabular.exceptions import (
    SplurgeTabularColumnError,
    SplurgeTabularEncodingError,
    SplurgeTabularError,
    SplurgeTabularFileError,
    SplurgeTabularFileNotFoundError,
    SplurgeTabularFilePermissionError,
    SplurgeTabularIndexError,
    SplurgeTabularKeyError,
    SplurgeTabularRowError,
    SplurgeTabularSchemaError,
    SplurgeTabularStreamError,
    SplurgeTabularTypeError,
    SplurgeTabularValidationError,
    SplurgeTabularValueError,
)

# Protocols
from splurge_tabular.protocols import StreamingTabularDataProtocol, TabularDataProtocol
from splurge_tabular.streaming_tabular_data_model import StreamingTabularDataModel
from splurge_tabular.tabular_data_model import TabularDataModel
from splurge_tabular.tabular_utils import normalize_rows, process_headers

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
    "safe_file_operation",
    "validate_data_structure",
    "process_headers",
    "ensure_minimum_columns",
    "normalize_rows",
    # Exceptions
    "SplurgeTabularError",
    "SplurgeTabularTypeError",
    "SplurgeTabularValueError",
    "SplurgeTabularKeyError",
    "SplurgeTabularIndexError",
    "SplurgeTabularColumnError",
    "SplurgeTabularRowError",
    "SplurgeTabularValidationError",
    "SplurgeTabularSchemaError",
    "SplurgeTabularStreamError",
    "SplurgeTabularEncodingError",
    "SplurgeTabularFileError",
    "SplurgeTabularFileNotFoundError",
    "SplurgeTabularFilePermissionError",
]
