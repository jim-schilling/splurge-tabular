"""
Unit tests for splurge_tabular.exceptions module.

Tests the custom exception hierarchy and error message formatting.
"""

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


class TestSplurgeError:
    """Test the base SplurgeError class."""

    def test_basic_error(self):
        """Test basic error without details."""
        error = SplurgeTabularError("Test message")
        assert str(error) == "Test message"
        assert error.message == "Test message"
        assert error.details is None

    def test_error_with_details(self):
        """Test error with additional details."""
        error = SplurgeTabularError("Test message", details="Extra info")
        assert str(error) == "Test message (Details: Extra info)"
        assert error.message == "Test message"
        assert error.details == "Extra info"

    def test_error_inheritance(self):
        """Test that SplurgeError inherits from Exception."""
        error = SplurgeTabularError("Test")
        assert isinstance(error, Exception)


class TestSplurgeTypeError:
    """Test SplurgeTypeError class."""

    def test_type_error_creation(self):
        """Test creating a type error."""
        error = SplurgeTabularTypeError("Invalid type")
        assert str(error) == "Invalid type"
        assert isinstance(error, SplurgeTabularError)
        assert isinstance(error, Exception)

    def test_type_error_with_details(self):
        """Test type error with details."""
        error = SplurgeTabularTypeError("Invalid type", details="Expected int, got str")
        assert str(error) == "Invalid type (Details: Expected int, got str)"


class TestSplurgeValidationError:
    """Test SplurgeValidationError class."""

    def test_validation_error_creation(self):
        """Test creating a validation error."""
        error = SplurgeTabularValidationError("Validation failed")
        assert str(error) == "Validation failed"
        assert isinstance(error, SplurgeTabularError)

    def test_validation_error_with_details(self):
        """Test validation error with details."""
        error = SplurgeTabularValidationError("Schema validation failed", details="Missing required field")
        assert str(error) == "Schema validation failed (Details: Missing required field)"


class TestSplurgeValueError:
    """Test SplurgeValueError class."""

    def test_value_error_creation(self):
        """Test creating a value error."""
        error = SplurgeTabularValueError("Invalid value")
        assert str(error) == "Invalid value"
        assert isinstance(error, SplurgeTabularError)

    def test_value_error_with_details(self):
        """Test value error with details."""
        error = SplurgeTabularValueError("Invalid value", details="Value out of range")
        assert str(error) == "Invalid value (Details: Value out of range)"


class TestSplurgeFileError:
    """Test SplurgeFileError class."""

    def test_file_error_creation(self):
        """Test creating a file error."""
        error = SplurgeTabularFileError("File operation failed")
        assert str(error) == "File operation failed"
        assert isinstance(error, SplurgeTabularError)

    def test_file_error_with_details(self):
        """Test file error with details."""
        error = SplurgeTabularFileError("File operation failed", details="Permission denied")
        assert str(error) == "File operation failed (Details: Permission denied)"


class TestSplurgeFileNotFoundError:
    """Test SplurgeFileNotFoundError class."""

    def test_file_not_found_error_creation(self):
        """Test creating a file not found error."""
        error = SplurgeTabularFileNotFoundError("File not found")
        assert str(error) == "File not found"
        assert isinstance(error, SplurgeTabularFileError)
        assert isinstance(error, SplurgeTabularError)

    def test_file_not_found_error_with_details(self):
        """Test file not found error with details."""
        error = SplurgeTabularFileNotFoundError("File not found", details="Path: /nonexistent/file.txt")
        assert str(error) == "File not found (Details: Path: /nonexistent/file.txt)"


class TestSplurgeFilePermissionError:
    """Test SplurgeFilePermissionError class."""

    def test_file_permission_error_creation(self):
        """Test creating a file permission error."""
        error = SplurgeTabularFilePermissionError("Permission denied")
        assert str(error) == "Permission denied"
        assert isinstance(error, SplurgeTabularFileError)
        assert isinstance(error, SplurgeTabularError)

    def test_file_permission_error_with_details(self):
        """Test file permission error with details."""
        error = SplurgeTabularFilePermissionError("Permission denied", details="Cannot write to file")
        assert str(error) == "Permission denied (Details: Cannot write to file)"


class TestExceptionHierarchy:
    """Test the exception hierarchy relationships."""

    def test_all_exceptions_inherit_from_splurge_error(self):
        """Test that all custom exceptions inherit from SplurgeError."""
        exceptions = [
            SplurgeTabularTypeError("test"),
            SplurgeTabularValueError("test"),
            SplurgeTabularKeyError("test"),
            SplurgeTabularIndexError("test"),
            SplurgeTabularColumnError("test"),
            SplurgeTabularRowError("test"),
            SplurgeTabularValidationError("test"),
            SplurgeTabularSchemaError("test"),
            SplurgeTabularStreamError("test"),
            SplurgeTabularEncodingError("test"),
            SplurgeTabularFileError("test"),
            SplurgeTabularFileNotFoundError("test"),
            SplurgeTabularFilePermissionError("test"),
        ]

        for exc in exceptions:
            assert isinstance(exc, SplurgeTabularError)
            assert isinstance(exc, Exception)

    def test_file_exceptions_inherit_from_file_error(self):
        """Test that file-specific exceptions inherit from SplurgeFileError."""
        file_exceptions = [
            SplurgeTabularFileNotFoundError("test"),
            SplurgeTabularFilePermissionError("test"),
        ]

        for exc in file_exceptions:
            assert isinstance(exc, SplurgeTabularFileError)
            assert isinstance(exc, SplurgeTabularError)
            assert isinstance(exc, Exception)
