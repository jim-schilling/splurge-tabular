"""Data type enumeration.

This module defines the :class:`DataType` enum which lists the supported data
types used throughout the package for inference and conversion.

Copyright (c) 2025 Jim Schilling

Please preserve this header and all related material when sharing!

This module is licensed under the MIT License.
"""

from enum import Enum


class DataType(Enum):
    """Enumeration of supported data types.

    Attributes:
        STRING: Text data.
        INTEGER: Whole numbers.
        FLOAT: Decimal numbers.
        BOOLEAN: True/False values.
        DATE: Calendar dates.
        TIME: Time values.
        DATETIME: Combined date and time.
        MIXED: Multiple types in a collection.
        EMPTY: Empty values.
        NONE: Null/None values.
    """

    STRING = "str"
    INTEGER = "int"
    FLOAT = "float"
    BOOLEAN = "bool"
    DATE = "date"
    TIME = "time"
    DATETIME = "datetime"
    MIXED = "mixed"
    EMPTY = "empty"
    NONE = "none"
