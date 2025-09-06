"""
Unit tests for splurge_tabular.exceptions module.

Tests the custom exception hierarchy and error message formatting.
"""

from splurge_tabular.exceptions import (
    SplurgeColumnError,
    SplurgeEncodingError,
    SplurgeError,
    SplurgeFileError,
    SplurgeFileNotFoundError,
    SplurgeFilePermissionError,
    SplurgeIndexError,
    SplurgeKeyError,
    SplurgeRowError,
    SplurgeSchemaError,
    SplurgeStreamError,
    SplurgeTypeError,
    SplurgeValidationError,
    SplurgeValueError,
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


class TestSplurgeTypeError:
    """Test SplurgeTypeError class."""

    def test_type_error_creation(self):
        """Test creating a type error."""
        error = SplurgeTypeError("Invalid type")
        assert str(error) == "Invalid type"
        assert isinstance(error, SplurgeError)
        assert isinstance(error, Exception)

    def test_type_error_with_details(self):
        """Test type error with details."""
        error = SplurgeTypeError("Invalid type", details="Expected int, got str")
        assert str(error) == "Invalid type (Details: Expected int, got str)"


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


class TestSplurgeValueError:
    """Test SplurgeValueError class."""

    def test_value_error_creation(self):
        """Test creating a value error."""
        error = SplurgeValueError("Invalid value")
        assert str(error) == "Invalid value"
        assert isinstance(error, SplurgeError)

    def test_value_error_with_details(self):
        """Test value error with details."""
        error = SplurgeValueError("Invalid value", details="Value out of range")
        assert str(error) == "Invalid value (Details: Value out of range)"


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
            SplurgeTypeError("test"),
            SplurgeValueError("test"),
            SplurgeKeyError("test"),
            SplurgeIndexError("test"),
            SplurgeColumnError("test"),
            SplurgeRowError("test"),
            SplurgeValidationError("test"),
            SplurgeSchemaError("test"),
            SplurgeStreamError("test"),
            SplurgeEncodingError("test"),
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
