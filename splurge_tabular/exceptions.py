"""Custom exception classes for splurge-tabular package.

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


class SplurgeTypeError(SplurgeError):
    """
    Exception raised for invalid or missing types.

    This exception is raised when function or method parameters have
    invalid or missing types.
    """

    pass


class SplurgeValueError(SplurgeError):
    """
    Exception raised for invalid values or out-of-range values.

    This exception is raised when values are invalid or outside expected ranges,
    such as invalid numeric values or other value errors.
    """

    pass


class SplurgeKeyError(SplurgeValueError):
    """
    Exception raised for missing keys in dictionaries or mappings.

    This exception is raised when a required key is missing from a dictionary
    or mapping.
    """

    pass


class SplurgeIndexError(SplurgeValueError):
    """
    Exception raised for out-of-bounds indices in lists or sequences.

    This exception is raised when an index is out of the valid range for a list
    or sequence.
    """

    pass


class SplurgeColumnError(SplurgeValueError):
    """
    Exception raised for column-related errors in tabular data.

    This exception is raised for issues such as invalid or missing column names,
    duplicate columns, or column-specific validation failures.
    """

    pass


class SplurgeRowError(SplurgeValueError):
    """
    Exception raised for row-related errors in tabular data.

    This exception is raised for issues such as invalid row indices,
    malformed rows, or row-specific validation failures.
    """

    pass


class SplurgeValidationError(SplurgeError):
    """
    Exception raised for data validation failures.

    This exception is raised when data fails validation checks, such as
    schema validation, format validation, or business rule validation.
    """

    pass


class SplurgeSchemaError(SplurgeValidationError):
    """
    Exception raised for schema validation failures in tabular data.

    This exception is raised when data does not match the expected schema,
    such as data type mismatches or missing required columns.
    """

    pass


class SplurgeStreamError(SplurgeError):
    """
    Exception raised for errors during streaming tabular data operations.

    This exception is raised for issues such as stream corruption,
    read/write failures, or invalid stream states.
    """

    pass


class SplurgeEncodingError(SplurgeError):
    """
    Exception raised for encoding-related errors in tabular data.

    This exception is raised for issues such as invalid character encodings
    or decoding failures in tabular data files.
    """

    pass


class SplurgeFileError(SplurgeError):
    """
    Exception raised for file operation errors.

    This exception is raised when file operations fail, such as read/write
    errors, permission issues, or file not found.
    """

    pass


class SplurgeFileNotFoundError(SplurgeFileError):
    """
    Exception raised when a required file is not found.

    This exception is raised when attempting to access a file that does not exist.
    """

    pass


class SplurgeFilePermissionError(SplurgeFileError):
    """
    Exception raised for file permission errors.

    This exception is raised when file operations fail due to insufficient permissions.
    """

    pass
