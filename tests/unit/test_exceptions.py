"""
Unit tests for splurge_tabular.exceptions module.

Tests the custom exception hierarchy and error message formatting.
"""

from splurge_tabular.exceptions import (
    SplurgeTabularError,
    SplurgeTabularLookupError,
    SplurgeTabularTypeError,
    SplurgeTabularValueError,
)


class TestSplurgeError:
    """Test the base SplurgeError class."""

    def test_basic_error(self):
        """Test basic error without details."""
        error = SplurgeTabularError("Test message")
        assert "Test message" in str(error)
        assert error.message == "Test message"
        assert error.details == {}

    def test_error_with_details(self):
        """Test error with additional details."""
        error = SplurgeTabularError("Test message", details={"extra_info": "Extra info"})
        assert "[splurge-tabular] Test message" in str(error)
        assert "extra_info='Extra info'" in str(error)
        assert error.message == "Test message"
        assert error.details == {"extra_info": "Extra info"}

    def test_error_inheritance(self):
        """Test that SplurgeError inherits from Exception."""
        error = SplurgeTabularError("Test")
        assert isinstance(error, Exception)


class TestSplurgeTypeError:
    """Test SplurgeTypeError class."""

    def test_type_error_creation(self):
        """Test creating a type error."""
        error = SplurgeTabularTypeError("Invalid type")
        assert "Invalid type" in str(error)
        assert isinstance(error, SplurgeTabularError)
        assert isinstance(error, Exception)

    def test_type_error_with_details(self):
        """Test type error with details."""
        error = SplurgeTabularTypeError("Invalid type", details={"expected_type": "int", "got_type": "str"})
        assert "[splurge-tabular.type] Invalid type" in str(error)
        assert "expected_type='int'" in str(error)
        assert "got_type='str'" in str(error)


class TestSplurgeValueError:
    """Test SplurgeValueError class."""

    def test_value_error_creation(self):
        """Test creating a value error."""
        error = SplurgeTabularValueError("Invalid value")
        assert str(error) == "[splurge-tabular.value] Invalid value"
        assert isinstance(error, SplurgeTabularError)

    def test_value_error_with_details(self):
        """Test value error with details."""
        error = SplurgeTabularValueError("Invalid value", details={"reason": "Value out of range"})
        assert "[splurge-tabular.value] Invalid value" in str(error)
        assert "reason='Value out of range'" in str(error)


class TestExceptionHierarchy:
    """Test the exception hierarchy relationships."""

    def test_all_exceptions_inherit_from_splurge_error(self):
        """Test that all custom exceptions inherit from SplurgeError."""
        exceptions = [
            SplurgeTabularTypeError("test"),
            SplurgeTabularValueError("test"),
            SplurgeTabularLookupError("test"),
        ]

        for exc in exceptions:
            assert isinstance(exc, SplurgeTabularError)
            assert isinstance(exc, Exception)
