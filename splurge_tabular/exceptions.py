"""
Custom exception classes for splurge-tabular package.

This module defines a hierarchy of custom exceptions for proper error handling
and user-friendly error messages throughout the package.

Copyright (c) 2025 Jim Schilling

Please preserve this header and all related material when sharing!

This module is licensed under the MIT License.
"""

from __future__ import annotations


class SplurgeError(Exception):
    """
    Base exception class for all splurge-tabular errors.

    This is the root exception that all other splurge exceptions inherit from,
    allowing users to catch all splurge-related errors with a single except clause.
    """

    def __init__(self, message: str, details: str | None = None) -> None:
        """
        Initialize SplurgeError.

        Args:
            message: Human-readable error message
            details: Additional technical details for debugging
        """
        super().__init__(message)
        self.message = message
        self.details = details

    def __str__(self) -> str:
        """Return string representation of the error."""
        if self.details:
            return f"{self.message} (Details: {self.details})"
        return self.message


class SplurgeParameterError(SplurgeError):
    """
    Exception raised for invalid or missing parameters.

    This exception is raised when function or method parameters are invalid,
    missing, or of incorrect type.
    """
    pass


class SplurgeValidationError(SplurgeError):
    """
    Exception raised for data validation failures.

    This exception is raised when data fails validation checks, such as
    schema validation, format validation, or business rule validation.
    """
    pass


class SplurgeRangeError(SplurgeError):
    """
    Exception raised for out-of-range values.

    This exception is raised when a value is outside the expected range,
    such as array indices, numeric ranges, or collection sizes.
    """
    pass


class SplurgeFileError(SplurgeError):
    """
    Base exception class for file-related errors.

    This is the base class for all file system related errors.
    """
    pass


class SplurgeFileNotFoundError(SplurgeFileError):
    """
    Exception raised when a required file is not found.

    This exception is raised when attempting to access a file that doesn't exist.
    """
    pass


class SplurgeFilePermissionError(SplurgeFileError):
    """
    Exception raised for file permission issues.

    This exception is raised when there are insufficient permissions to
    read from or write to a file.
    """
    pass
