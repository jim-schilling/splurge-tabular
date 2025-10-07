"""Custom exception classes for splurge-tabular package.

This module defines a hierarchy of custom exceptions for proper error handling
and user-friendly error messages throughout the package.

Copyright (c) 2025 Jim Schilling

Please preserve this header and all related material when sharing!

This module is licensed under the MIT License.
"""

from __future__ import annotations

from splurge_tabular.error_codes import ErrorCode


class SplurgeTabularError(Exception):
    """Base exception for all splurge-tabular errors.

    This is the root exception that all other splurge exceptions inherit from,
    allowing users to catch all splurge-related errors with a single except
    clause.
    """

    def __init__(
        self,
        message: str,
        *,
        details: str | None = None,
        error_code: str | ErrorCode | None = None,
        context: dict[str, str] | None = None,
    ) -> None:
        """Initialize the exception.

        Args:
            message: Human-readable error message.
            details: Additional technical details for debugging.
            error_code: Optional machine-friendly error code.
            context: Optional dictionary with contextual information (file, row, column, etc.).
        """
        super().__init__(message)
        self.message = message
        self.details: str | None = details
        # Coerce ErrorCode enum to its string value if provided
        self.error_code: str | None
        if isinstance(error_code, ErrorCode):
            self.error_code = error_code.value
        else:
            self.error_code = error_code
        self.context: dict[str, str] | None = context

    def __str__(self) -> str:
        """Return string representation of the error.

        Returns:
            str: The error message, optionally with details, code, and context
                appended in parenthetical groups.
        """
        s = self.message
        if self.details:
            s += f" (Details: {self.details})"
        if self.error_code:
            s += f" (code={self.error_code})"
        if self.context:
            ctx = ", ".join(f"{k}={v}" for k, v in self.context.items())
            s += f" (Context: {ctx})"
        return s


class SplurgeTabularTypeError(SplurgeTabularError):
    """Exception raised for invalid or missing types.

    This exception is raised when function or method parameters have
    invalid or missing types.
    """


class SplurgeTabularValueError(SplurgeTabularError):
    """Exception raised for invalid values or out-of-range values.

    This exception is raised when values are invalid or outside expected
    ranges, such as invalid numeric values.
    """


class SplurgeTabularKeyError(SplurgeTabularValueError):
    """Exception raised for missing keys in dictionaries or mappings.

    This exception is raised when a required key is missing from a dictionary
    or mapping.
    """


class SplurgeTabularIndexError(SplurgeTabularValueError):
    """Exception raised for out-of-bounds indices in lists or sequences.

    This exception is raised when an index is out of the valid range for a
    list or sequence.
    """


class SplurgeTabularColumnError(SplurgeTabularValueError):
    """Exception raised for column-related errors in tabular data.

    This exception is raised for issues such as invalid or missing column
    names, duplicate columns, or column-specific validation failures.
    """


class SplurgeTabularRowError(SplurgeTabularValueError):
    """Exception raised for row-related errors in tabular data.

    This exception is raised for issues such as invalid row indices,
    malformed rows, or row-specific validation failures.
    """


class SplurgeTabularValidationError(SplurgeTabularError):
    """Exception raised for data validation failures.

    This exception is raised when data fails validation checks, such as
    schema validation, format validation, or business rule validation.
    """


class SplurgeTabularSchemaError(SplurgeTabularValidationError):
    """Exception raised for schema validation failures in tabular data.

    This exception is raised when data does not match the expected schema,
    such as data type mismatches or missing required columns.
    """


class SplurgeTabularStreamError(SplurgeTabularError):
    """Exception raised for errors during streaming tabular data operations.

    This exception is raised for issues such as stream corruption,
    read/write failures, or invalid stream states.
    """


class SplurgeTabularEncodingError(SplurgeTabularError):
    """Exception raised for encoding-related errors in tabular data.

    This exception is raised for issues such as invalid character encodings or
    decoding failures in tabular data files.
    """


class SplurgeTabularFileError(SplurgeTabularError):
    """Exception raised for file operation errors.

    This exception is raised when file operations fail, such as read/write
    errors, permission issues, or file not found.
    """


class SplurgeTabularFileNotFoundError(SplurgeTabularFileError):
    """Exception raised when a required file is not found.

    This exception is raised when attempting to access a file that does not
    exist.
    """


class SplurgeTabularFilePermissionError(SplurgeTabularFileError):
    """Exception raised for file permission errors.

    This exception is raised when file operations fail due to insufficient
    permissions.
    """


class SplurgeTabularConfigurationError(SplurgeTabularValueError):
    """Exception raised for invalid configuration or parameter values.

    Use this exception when a provided configuration value (for example,
    ``chunk_size`` or ``header_rows``) is syntactically correct but
    semantically invalid for runtime (out of allowed range, conflicting
    settings, etc.).
    """
