"""
Splurge Tabular Library

A Python library for tabular data processing with in-memory and streaming support.

Copyright (c) 2025 Jim Schilling

Please preserve this header and all related material when sharing!

This module is licensed under the MIT License.
"""

from __future__ import annotations

__version__ = "2025.0.0"

# Main classes
from splurge_tabular.tabular_data_model import TabularDataModel
from splurge_tabular.streaming_tabular_data_model import StreamingTabularDataModel

# Protocols
from splurge_tabular.protocols import TabularDataProtocol, StreamingTabularDataProtocol

# Utility functions
from splurge_tabular.common_utils import safe_file_operation, validate_data_structure, ensure_minimum_columns
from splurge_tabular.tabular_utils import process_headers, normalize_rows

# Exceptions
from splurge_tabular.exceptions import (
    SplurgeError,
    SplurgeParameterError,
    SplurgeValidationError,
    SplurgeFileError,
    SplurgeRangeError,
)

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
    "SplurgeError",
    "SplurgeParameterError",
    "SplurgeValidationError",
    "SplurgeFileError",
    "SplurgeRangeError",
]
