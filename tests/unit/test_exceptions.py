"""
Unit tests for splurge_tabular.exceptions module.

Tests the custom exception hierarchy and error message formatting.
"""

import pytest

from splurge_tabular.exceptions import (
    SplurgeError,
    SplurgeFileError,
    SplurgeFileNotFoundError,
    SplurgeFilePermissionError,
    SplurgeParameterError,
    SplurgeRangeError,
    SplurgeValidationError,
)


class TestSplurgeError:
    """Test the base SplurgeError class."""

    def test_basic_error(self):
        """Test basic error without details."""
        error = SplurgeError("Test message")
        assert str(error) == "Test message"
        assert error.message == "Test message"
        assert error.details is None

    def test_error_with_details(self):
        """Test error with additional details."""
        error = SplurgeError("Test message", details="Extra info")
        assert str(error) == "Test message (Details: Extra info)"
        assert error.message == "Test message"
        assert error.details == "Extra info"

    def test_error_inheritance(self):
        """Test that SplurgeError inherits from Exception."""
        error = SplurgeError("Test")
        assert isinstance(error, Exception)


class TestSplurgeParameterError:
    """Test SplurgeParameterError class."""

    def test_parameter_error_creation(self):
        """Test creating a parameter error."""
        error = SplurgeParameterError("Invalid parameter")
        assert str(error) == "Invalid parameter"
        assert isinstance(error, SplurgeError)
        assert isinstance(error, Exception)

    def test_parameter_error_with_details(self):
        """Test parameter error with details."""
        error = SplurgeParameterError("Invalid parameter", details="Expected int, got str")
        assert str(error) == "Invalid parameter (Details: Expected int, got str)"


class TestSplurgeValidationError:
    """Test SplurgeValidationError class."""

    def test_validation_error_creation(self):
        """Test creating a validation error."""
        error = SplurgeValidationError("Validation failed")
        assert str(error) == "Validation failed"
        assert isinstance(error, SplurgeError)

    def test_validation_error_with_details(self):
        """Test validation error with details."""
        error = SplurgeValidationError("Schema validation failed", details="Missing required field")
        assert str(error) == "Schema validation failed (Details: Missing required field)"


class TestSplurgeRangeError:
    """Test SplurgeRangeError class."""

    def test_range_error_creation(self):
        """Test creating a range error."""
        error = SplurgeRangeError("Index out of range")
        assert str(error) == "Index out of range"
        assert isinstance(error, SplurgeError)

    def test_range_error_with_details(self):
        """Test range error with details."""
        error = SplurgeRangeError("Index out of range", details="Index 5, max 3")
        assert str(error) == "Index out of range (Details: Index 5, max 3)"


class TestSplurgeFileError:
    """Test SplurgeFileError class."""

    def test_file_error_creation(self):
        """Test creating a file error."""
        error = SplurgeFileError("File operation failed")
        assert str(error) == "File operation failed"
        assert isinstance(error, SplurgeError)

    def test_file_error_with_details(self):
        """Test file error with details."""
        error = SplurgeFileError("File operation failed", details="Permission denied")
        assert str(error) == "File operation failed (Details: Permission denied)"


class TestSplurgeFileNotFoundError:
    """Test SplurgeFileNotFoundError class."""

    def test_file_not_found_error_creation(self):
        """Test creating a file not found error."""
        error = SplurgeFileNotFoundError("File not found")
        assert str(error) == "File not found"
        assert isinstance(error, SplurgeFileError)
        assert isinstance(error, SplurgeError)

    def test_file_not_found_error_with_details(self):
        """Test file not found error with details."""
        error = SplurgeFileNotFoundError("File not found", details="Path: /nonexistent/file.txt")
        assert str(error) == "File not found (Details: Path: /nonexistent/file.txt)"


class TestSplurgeFilePermissionError:
    """Test SplurgeFilePermissionError class."""

    def test_file_permission_error_creation(self):
        """Test creating a file permission error."""
        error = SplurgeFilePermissionError("Permission denied")
        assert str(error) == "Permission denied"
        assert isinstance(error, SplurgeFileError)
        assert isinstance(error, SplurgeError)

    def test_file_permission_error_with_details(self):
        """Test file permission error with details."""
        error = SplurgeFilePermissionError("Permission denied", details="Cannot write to file")
        assert str(error) == "Permission denied (Details: Cannot write to file)"


class TestExceptionHierarchy:
    """Test the exception hierarchy relationships."""

    def test_all_exceptions_inherit_from_splurge_error(self):
        """Test that all custom exceptions inherit from SplurgeError."""
        exceptions = [
            SplurgeParameterError("test"),
            SplurgeValidationError("test"),
            SplurgeRangeError("test"),
            SplurgeFileError("test"),
            SplurgeFileNotFoundError("test"),
            SplurgeFilePermissionError("test"),
        ]

        for exc in exceptions:
            assert isinstance(exc, SplurgeError)
            assert isinstance(exc, Exception)

    def test_file_exceptions_inherit_from_file_error(self):
        """Test that file-specific exceptions inherit from SplurgeFileError."""
        file_exceptions = [
            SplurgeFileNotFoundError("test"),
            SplurgeFilePermissionError("test"),
        ]

        for exc in file_exceptions:
            assert isinstance(exc, SplurgeFileError)
            assert isinstance(exc, SplurgeError)
            assert isinstance(exc, Exception)
