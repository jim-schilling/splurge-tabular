"""Custom exception classes for splurge-typer package.

This module defines a hierarchy of custom exceptions for proper error handling
and user-friendly error messages throughout the package.

Copyright (c) 2025 Jim Schilling

Please preserve this header and all related material when sharing!

This module is licensed under the MIT License.
"""

from __future__ import annotations

from ._vendor.splurge_exceptions.core.exceptions import SplurgeFrameworkError


class SplurgeTyperError(SplurgeFrameworkError):
    """
    Base exception class for all splurge-typer errors.

    This is the root exception that all other splurge exceptions inherit from,
    allowing users to catch all splurge-related errors with a single except clause.
    """

    _domain = "splurge-typer"


class SplurgeTyperValueError(SplurgeTyperError):
    """Raised when input value is invalid for the requested operation."""

    _domain = "splurge-typer.value"
