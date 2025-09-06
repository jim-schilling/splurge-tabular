"""
Unit tests for splurge_tabular.common_utils module.

Tests core utility functions for data validation and safe operations.
"""

from pathlib import Path

import pytest

from splurge_tabular.common_utils import (
    batch_validate_rows,
    create_error_context,
    create_parameter_validator,
    ensure_minimum_columns,
    is_empty_or_none,
    normalize_string,
    safe_dict_access,
    safe_file_operation,
    safe_index_access,
    safe_string_operation,
    standardize_column_names,
    validate_data_structure,
    validate_string_parameters,
)
from splurge_tabular.exceptions import SplurgeTypeError, SplurgeValidationError, SplurgeValueError


class TestSafeFileOperation:
    """Test the safe_file_operation function."""

    def test_valid_string_path(self):
        """Test with valid string path."""
        result = safe_file_operation("test.txt")
        assert isinstance(result, Path)
        assert str(result) == "test.txt"

    def test_valid_path_object(self):
        """Test with valid Path object."""
        path = Path("test.txt")
        result = safe_file_operation(path)
        assert isinstance(result, Path)
        assert result == path

    def test_invalid_type(self):
        """Test with invalid type."""
        with pytest.raises(SplurgeTypeError) as exc_info:
            safe_file_operation(123)

        assert "file_path must be a string or Path object" in str(exc_info.value)
        assert "Expected str or Path, received: int" in str(exc_info.value)

    def test_none_value(self):
        """Test with None value."""
        with pytest.raises(SplurgeTypeError) as exc_info:
            safe_file_operation(None)

        assert "file_path must be a string or Path object" in str(exc_info.value)


class TestSafeIndexAccess:
    """Test the safe_index_access function."""

    def test_valid_index(self):
        """Test accessing valid index."""
        data = ["a", "b", "c"]
        result = safe_index_access(data, 1)
        assert result == "b"

    def test_index_out_of_range_positive(self):
        """Test index out of range (positive)."""
        data = ["a", "b", "c"]
        with pytest.raises(SplurgeValueError) as exc_info:
            safe_index_access(data, 5)

        assert "item index 5 out of range" in str(exc_info.value)
        assert "Valid range: 0 to 2, got 5" in str(exc_info.value)

    def test_index_out_of_range_negative(self):
        """Test index out of range (negative)."""
        data = ["a", "b", "c"]
        with pytest.raises(SplurgeValueError) as exc_info:
            safe_index_access(data, -5)

        assert "item index -5 out of range" in str(exc_info.value)
        assert "Valid range: 0 to 2, got -5" in str(exc_info.value)

    def test_empty_list(self):
        """Test accessing index in empty list."""
        data = []
        with pytest.raises(SplurgeValueError) as exc_info:
            safe_index_access(data, 0)

        assert "item index 0 out of range" in str(exc_info.value)
        assert "Valid range: 0 to -1, got 0" in str(exc_info.value)

    def test_with_default(self):
        """Test with default value."""
        data = ["a", "b", "c"]
        result = safe_index_access(data, 5, default="default")
        assert result == "default"


class TestSafeDictAccess:
    """Test the safe_dict_access function."""

    def test_valid_key(self):
        """Test accessing valid dictionary key."""
        data = {"name": "John", "age": 30}
        result = safe_dict_access(data, "name")
        assert result == "John"

    def test_missing_key_without_default(self):
        """Test accessing missing key without default."""
        data = {"name": "John"}
        with pytest.raises(SplurgeValueError) as exc_info:
            safe_dict_access(data, "age")

        assert "key 'age' not found" in str(exc_info.value)
        assert "Available keys: ['name']" in str(exc_info.value)

    def test_missing_key_with_default(self):
        """Test accessing missing key with default."""
        data = {"name": "John"}
        result = safe_dict_access(data, "age", default=25)
        assert result == 25

    def test_none_dict_raises_type_error(self):
        """Test with None dictionary raises TypeError."""
        with pytest.raises(TypeError):
            safe_dict_access(None, "key")


class TestValidateDataStructure:
    """Test the validate_data_structure function."""

    def test_valid_list(self):
        """Test validating valid list."""
        data = ["a", "b", "c"]
        result = validate_data_structure(data, expected_type=list)
        assert result == data

    def test_invalid_type(self):
        """Test validating with wrong type."""
        data = "not a list"
        with pytest.raises(SplurgeTypeError) as exc_info:
            validate_data_structure(data, expected_type=list, param_name="test_data")

        assert "test_data must be list, got str" in str(exc_info.value)
        assert "Expected list, received: str" in str(exc_info.value)

    def test_empty_list_allowed(self):
        """Test empty list when allowed."""
        data = []
        result = validate_data_structure(data, expected_type=list, allow_empty=True)
        assert result == data

    def test_empty_list_not_allowed(self):
        """Test empty list when not allowed."""
        data = []
        with pytest.raises(SplurgeValidationError) as exc_info:
            validate_data_structure(data, expected_type=list, allow_empty=False)

        assert "data cannot be empty" in str(exc_info.value)
        assert "Empty list not allowed" in str(exc_info.value)

    def test_custom_param_name(self):
        """Test with custom parameter name."""
        data = "not a list"
        with pytest.raises(SplurgeTypeError) as exc_info:
            validate_data_structure(data, expected_type=list, param_name="my_param")

        assert "my_param must be list, got str" in str(exc_info.value)
        assert "Expected list, received: str" in str(exc_info.value)


class TestIsEmptyOrNone:
    """Test the is_empty_or_none function."""

    def test_none_value(self):
        """Test with None value."""
        assert is_empty_or_none(None) is True

    def test_empty_string(self):
        """Test with empty string."""
        assert is_empty_or_none("") is True

    def test_whitespace_string_trim(self):
        """Test whitespace string with trimming."""
        assert is_empty_or_none("   ") is True

    def test_whitespace_string_no_trim(self):
        """Test whitespace string without trimming."""
        assert is_empty_or_none("   ", trim=False) is False

    def test_non_empty_string(self):
        """Test non-empty string."""
        assert is_empty_or_none("hello") is False

    def test_zero_number(self):
        """Test with zero."""
        assert is_empty_or_none(0) is False

    def test_false_boolean(self):
        """Test with False."""
        assert is_empty_or_none(False) is False

    def test_empty_list(self):
        """Test with empty list."""
        assert is_empty_or_none([]) is False

    def test_empty_dict(self):
        """Test with empty dict."""
        assert is_empty_or_none({}) is False


class TestStandardizeColumnNames:
    """Test the standardize_column_names function."""

    def test_fill_empty_headers(self):
        """Test filling empty headers with generated names."""
        columns = ["Name", "", "City"]
        result = standardize_column_names(columns)
        expected = ["Name", "column_1", "City"]
        assert result == expected

    def test_no_empty_headers(self):
        """Test when no empty headers exist."""
        columns = ["Name", "Age", "City"]
        result = standardize_column_names(columns)
        assert result == columns

    def test_all_empty_headers(self):
        """Test when all headers are empty."""
        columns = ["", "", ""]
        result = standardize_column_names(columns)
        expected = ["column_0", "column_1", "column_2"]
        assert result == expected

    def test_custom_prefix(self):
        """Test with custom prefix."""
        columns = ["Name", "", "City"]
        result = standardize_column_names(columns, prefix="field_")
        expected = ["Name", "field_1", "City"]
        assert result == expected

    def test_no_fill_empty(self):
        """Test when fill_empty is False."""
        columns = ["Name", "", "City"]
        result = standardize_column_names(columns, fill_empty=False)
        assert result == columns


class TestEnsureMinimumColumns:
    """Test the ensure_minimum_columns function."""

    def test_no_padding_needed(self):
        """Test when row already has minimum columns."""
        row = ["a", "b", "c"]
        result = ensure_minimum_columns(row, 3)
        assert result == ["a", "b", "c"]

    def test_padding_needed(self):
        """Test when row needs padding."""
        row = ["a", "b"]
        result = ensure_minimum_columns(row, 4)
        assert result == ["a", "b", "", ""]

    def test_exact_minimum(self):
        """Test when row has exactly minimum columns."""
        row = ["a", "b", "c"]
        result = ensure_minimum_columns(row, 3)
        assert result == ["a", "b", "c"]

    def test_empty_row(self):
        """Test with empty row."""
        row = []
        result = ensure_minimum_columns(row, 2)
        assert result == ["", ""]

    def test_minimum_zero(self):
        """Test with minimum columns of zero."""
        row = ["a", "b"]
        result = ensure_minimum_columns(row, 0)
        assert result == ["a", "b"]

    def test_none_row_raises_error(self):
        """Test with None row raises TypeError."""
        with pytest.raises(TypeError):
            ensure_minimum_columns(None, 3)


class TestCreateParameterValidator:
    """Test the create_parameter_validator function."""

    def test_valid_parameters(self):
        """Test validation of valid parameters."""

        def validate_name(value):
            if not isinstance(value, str) or not value.strip():
                raise SplurgeValueError("name must be non-empty string")
            return value

        def validate_age(value):
            if not isinstance(value, int) or value < 0:
                raise SplurgeValueError("age must be non-negative integer")
            return value

        validator = create_parameter_validator({"name": validate_name, "age": validate_age})
        params = {"name": "John", "age": 25}
        result = validator(params)
        assert result == params

    def test_invalid_parameter(self):
        """Test validation with invalid parameter."""

        def validate_age(value):
            if not isinstance(value, int) or value < 0:
                raise SplurgeValueError("age must be non-negative integer")
            return value

        validator = create_parameter_validator({"age": validate_age})
        params = {"age": "not an int"}
        with pytest.raises(SplurgeValueError) as exc_info:
            validator(params)

        assert "age must be non-negative integer" in str(exc_info.value)

    def test_missing_parameter(self):
        """Test with missing parameter (should not raise error)."""

        def validate_name(value):
            if not isinstance(value, str) or not value.strip():
                raise SplurgeValueError("name must be non-empty string")
            return value

        validator = create_parameter_validator({"name": validate_name})
        params = {"other_param": "value"}
        result = validator(params)
        assert result == {}


class TestBatchValidateRows:
    """Test the batch_validate_rows function."""

    def test_valid_rows(self):
        """Test validation of valid rows."""
        rows = [["a", "b"], ["c", "d"], ["e", "f"]]
        result = list(batch_validate_rows(rows, min_columns=2))
        assert result == rows

    def test_invalid_row_type(self):
        """Test validation with invalid row type."""
        rows = [["a", "b"], "not a list", ["e", "f"]]
        with pytest.raises(SplurgeTypeError) as exc_info:
            list(batch_validate_rows(rows))

        assert "Row 1 must be a list" in str(exc_info.value)

    def test_empty_rows_list(self):
        """Test with empty rows list."""
        result = list(batch_validate_rows([], min_columns=1))
        assert result == []

    def test_skip_empty_rows(self):
        """Test skipping empty rows."""
        rows = [["a", "b"], ["", ""], ["c", "d"]]
        result = list(batch_validate_rows(rows, skip_empty=True))
        expected = [["a", "b"], ["c", "d"]]
        assert result == expected

    def test_min_columns_padding(self):
        """Test minimum columns padding."""
        rows = [["a", "b"], ["c"]]
        result = list(batch_validate_rows(rows, min_columns=3))
        expected = [["a", "b", ""], ["c", "", ""]]
        assert result == expected


class TestCreateErrorContext:
    """Test the create_error_context function."""

    def test_basic_error_context(self):
        """Test basic error context creation."""
        context = create_error_context("file processing")
        expected = "Operation: file processing"
        assert context == expected

    def test_full_error_context(self):
        """Test error context with all parameters."""
        context = create_error_context(
            "data validation", file_path="data.csv", row_number=5, column_name="email", additional_info="invalid format"
        )
        expected = "Operation: data validation | File: data.csv | Row: 5 | Column: email | Info: invalid format"
        assert context == expected

    def test_partial_error_context(self):
        """Test error context with some parameters."""
        context = create_error_context("parsing", file_path="test.txt", row_number=10)
        expected = "Operation: parsing | File: test.txt | Row: 10"
        assert context == expected


class TestNormalizeString:
    """Test the normalize_string function."""

    def test_basic_normalization(self):
        """Test basic string normalization."""
        result = normalize_string("  Hello World  ")
        assert result == "Hello World"

    def test_empty_string(self):
        """Test with empty string."""
        result = normalize_string("")
        assert result == ""

    def test_only_whitespace(self):
        """Test with only whitespace."""
        result = normalize_string("   ")
        assert result == ""

    def test_none_input(self):
        """Test with None input."""
        result = normalize_string(None)
        assert result == ""

    def test_no_trim(self):
        """Test with trim=False."""
        result = normalize_string("  Hello  ", trim=False)
        assert result == "  Hello  "

    def test_custom_empty_default(self):
        """Test with custom empty default."""
        result = normalize_string("", empty_default="N/A")
        assert result == "N/A"


class TestSafeStringOperation:
    """Test the safe_string_operation function."""

    def test_valid_string(self):
        """Test with valid string."""
        result = safe_string_operation("hello", str.upper)
        assert result == "HELLO"

    def test_empty_string(self):
        """Test with empty string."""
        result = safe_string_operation("", str.upper)
        assert result == ""

    def test_none_value(self):
        """Test with None value."""
        result = safe_string_operation(None, str.upper)
        assert result == ""

    def test_custom_empty_default(self):
        """Test with custom empty default."""
        result = safe_string_operation("", str.upper, empty_default="N/A")
        assert result == "N/A"


class TestValidateStringParameters:
    """Test the validate_string_parameters function."""

    def test_valid_string(self):
        """Test validation of valid string."""
        result = validate_string_parameters("hello", "test_param")
        assert result == "hello"

    def test_none_value_allowed(self):
        """Test None value when allowed."""
        result = validate_string_parameters(None, "test_param", allow_none=True)
        assert result == ""

    def test_none_value_not_allowed(self):
        """Test None value when not allowed."""
        with pytest.raises(SplurgeTypeError) as exc_info:
            validate_string_parameters(None, "test_param", allow_none=False)

        assert "test_param cannot be None" in str(exc_info.value)

    def test_empty_string_not_allowed(self):
        """Test empty string when not allowed."""
        with pytest.raises(SplurgeValueError) as exc_info:
            validate_string_parameters("", "test_param", allow_empty=False)

        assert "test_param cannot be empty" in str(exc_info.value)

    def test_min_length_validation(self):
        """Test minimum length validation."""
        with pytest.raises(SplurgeValueError) as exc_info:
            validate_string_parameters("hi", "test_param", min_length=5)

        assert "test_param must be at least 5 characters long" in str(exc_info.value)

    def test_max_length_validation(self):
        """Test maximum length validation."""
        with pytest.raises(SplurgeValueError) as exc_info:
            validate_string_parameters("this is too long", "test_param", max_length=10)

        assert "test_param must be at most 10 characters long" in str(exc_info.value)
