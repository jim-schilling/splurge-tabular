"""Custom exception classes for splurge-tabular package.

This module defines a hierarchy of custom exceptions for proper error handling
and user-friendly error messages throughout the package.

Copyright (c) 2025 Jim Schilling

Please preserve this header and all related material when sharing!

This module is licensed under the MIT License.
"""

from __future__ import annotations

from ._vendor.splurge_exceptions.core.exceptions import SplurgeFrameworkError


class SplurgeTabularError(SplurgeFrameworkError):
    """Base exception for all splurge-tabular errors.

    This is the root exception that all other splurge exceptions inherit from,
    allowing users to catch all splurge-related errors with a single except
    clause.
    """

    _domain = "splurge-tabular"


class SplurgeTabularTypeError(SplurgeTabularError):
    """Exception raised for invalid or missing types.

    This exception is raised when function or method parameters have
    invalid or missing types.
    """

    _domain = "splurge-tabular.type"


class SplurgeTabularValueError(SplurgeTabularError):
    """Exception raised for invalid values or out-of-range values.

    This exception is raised when values are invalid or outside expected
    ranges, such as invalid numeric values.
    """

    _domain = "splurge-tabular.value"


class SplurgeTabularLookupError(SplurgeTabularValueError):
    """Exception raised for missing lookups or out-of-bounds lookups.

    This exception is raised when a required key is missing from a dictionary
    or mapping, or when an index is out of bounds for a list or sequence,
    or when any other lookup operation fails.
    """

    _domain = "splurge-tabular.lookup"
