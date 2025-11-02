"""Type inference and conversion utilities.

Provides a high-level API for inferring data types from values and converting
values to their inferred native Python types. The implementation is optimized
for both single-value and collection analysis and integrates with string
parsing and duck-typing utilities provided elsewhere in the package.

Copyright (c) 2025 Jim Schilling

Please preserve this header and all related material when sharing!

This module is licensed under the MIT License.
"""

from collections.abc import Iterable
from typing import Any

from .data_type import DataType
from .duck_typing import DuckTyping
from .exceptions import SplurgeTyperValueError
from .string import String


class TypeInference:
    """
    TypeInference class - Comprehensive type inference and value conversion utilities.

    This class provides a complete suite of methods for intelligent type analysis and conversion,
    designed to handle both individual values and collections efficiently. It integrates with
    string parsing and duck typing capabilities to provide robust type inference across
    diverse data sources.

    Core Capabilities:
    - Single value type inference for strings and native Python types
    - Collection profiling to determine dominant types across datasets
    - Automatic conversion of values to their inferred types
    - Performance-optimized processing for large datasets using incremental type checking
    - Mixed type detection and resolution
    - Configurable thresholds for performance tuning
    - Duck typing utilities for flexible object behavior analysis

    Performance Features:
    - Incremental type checking with early termination for large collections
    - Configurable threshold (_INCREMENTAL_TYPECHECK_THRESHOLD) for optimization
    - Efficient processing of datasets with 10,000+ items
    - Smart caching and reuse of type inference results

    Usage Examples:
        >>> from splurge_typer import TypeInference
        >>>
        >>> # Single value inference
        >>> ti = TypeInference()
        >>> ti.infer_type('123')           # DataType.INTEGER
        >>> ti.convert_value('123')        # 123
        >>>
        >>> # Collection profiling
        >>> ti.profile_values(['1', '2', '3'])           # DataType.INTEGER
        >>> ti.profile_values(['1.1', '2.2', '3.3'])     # DataType.FLOAT
        >>> ti.profile_values(['1', '2.2', 'abc'])       # DataType.MIXED
        >>>
        >>> # Performance optimization
        >>> ti.profile_values(large_dataset, use_incremental_typecheck=True)
        >>>
        >>> # Duck typing utilities
        >>> ti.is_list_like([1, 2, 3])        # True
        >>> ti.is_dict_like({'a': 1})         # True
        >>> ti.is_empty([])                   # True
    """

    _INCREMENTAL_TYPECHECK_THRESHOLD = 10_000

    @classmethod
    def get_incremental_typecheck_threshold(cls) -> int:
        """
        Get the threshold for incremental type checking optimization.

        This threshold determines when incremental type checking is enabled for performance
        optimization. For collections larger than this threshold, the system uses incremental
        type checking with early termination to avoid processing the entire collection when
        the result can be determined earlier.

        Returns:
            The threshold value (default: 10,000 items)

        Note:
            This value can be modified by changing the _INCREMENTAL_TYPECHECK_THRESHOLD class variable.
            Lower values enable optimization for smaller datasets but may reduce accuracy for
            edge cases that require full analysis.

        Examples:
            >>> TypeInference.get_incremental_typecheck_threshold()  # 10000
            >>> # Collections with <= 10,000 items use full analysis
            >>> # Collections with > 10,000 items use incremental checking
        """
        return cls._INCREMENTAL_TYPECHECK_THRESHOLD

    @staticmethod
    def can_infer(
        value: Any,
    ) -> bool:
        """
        Check if a string value can be inferred as a non-string type.

        This method determines whether a given value (typically a string) can be
        meaningfully converted to a more specific data type beyond just a generic string.
        It returns True if the value represents a boolean, integer, float, date, time,
        datetime, or other structured type.

        Args:
            value: The value to check (typically a string)

        Returns:
            True if the value can be inferred as a specific non-string type,
            False if it remains a generic string or is not a string at all

        Note:
            - Non-string values (int, float, bool, etc.) return False as they don't need inference
            - String values that represent structured data (dates, numbers, booleans) return True
            - Generic strings that don't match any pattern return False

        Examples:
            >>> TypeInference.can_infer('123')           # True (can be int)
            >>> TypeInference.can_infer('1.23')          # True (can be float)
            >>> TypeInference.can_infer('true')          # True (can be bool)
            >>> TypeInference.can_infer('2023-01-01')    # True (can be date)
            >>> TypeInference.can_infer('hello')         # False (remains string)
            >>> TypeInference.can_infer(123)             # False (already int)
            >>> TypeInference.can_infer(None)            # False (not a string)
        """
        if not isinstance(value, str):
            return False

        inferred_type = String.infer_type(value)
        return inferred_type != DataType.STRING

    @staticmethod
    def infer_type(
        value: str,
    ) -> DataType:
        """
        Infer the most appropriate data type for a given value.

        This method analyzes a value and determines the most suitable data type
        based on its content and structure. It supports comprehensive type detection
        including all major Python types and special cases.

        Args:
            value: The value to analyze (string, number, date/time object, or None)

        Returns:
            DataType enum value representing the inferred type

        Note:
            The inference process checks for types in order of specificity:
            1. Native types (bool, int, float, datetime objects) - returned as-is
            2. Special values (None, empty strings)
            3. Structured string patterns (datetimes, dates, times)
            4. Numeric patterns (integers, floats)
            5. Boolean patterns
            6. Fallback to STRING for unmatched values

        Examples:
            >>> TypeInference.infer_type('123')           # DataType.INTEGER
            >>> TypeInference.infer_type('1.23')          # DataType.FLOAT
            >>> TypeInference.infer_type('true')          # DataType.BOOLEAN
            >>> TypeInference.infer_type('2023-01-01')    # DataType.DATE
            >>> TypeInference.infer_type('2023-01-01T12:00:00')  # DataType.DATETIME
            >>> TypeInference.infer_type('14:30:00')      # DataType.TIME
            >>> TypeInference.infer_type('none')          # DataType.NONE
            >>> TypeInference.infer_type('')              # DataType.EMPTY
            >>> TypeInference.infer_type('hello world')   # DataType.STRING
            >>> TypeInference.infer_type(123)             # DataType.INTEGER (native type)
        """
        return String.infer_type(value)

    @classmethod
    def convert_value(
        cls,
        value: Any,
    ) -> Any:
        """
        Convert a value to its inferred type automatically.

        This method first infers the most appropriate data type for the given value,
        then converts the value to that type using appropriate conversion methods.
        It handles all supported data types including booleans, integers, floats,
        dates, times, datetimes, and special cases like None and empty strings.

        Args:
            value: The value to convert (string, number, date/time object, or None)

        Returns:
            The converted value in its inferred type, or the original value if
            no conversion is needed/applicable

        Note:
            - String representations are converted to their appropriate native types
            - Native Python types (int, float, bool, etc.) are returned as-is
            - Invalid conversions return None or empty string for their respective types
            - Date/time conversions use the String module's parsing capabilities

        Examples:
            >>> TypeInference.convert_value('123')           # 123 (int)
            >>> TypeInference.convert_value('1.23')          # 1.23 (float)
            >>> TypeInference.convert_value('true')          # True (bool)
            >>> TypeInference.convert_value('2023-01-01')    # datetime.date(2023, 1, 1)
            >>> TypeInference.convert_value('none')          # None
            >>> TypeInference.convert_value('')              # '' (empty string)
            >>> TypeInference.convert_value(123)             # 123 (already int, no conversion)
            >>> TypeInference.convert_value('invalid')       # 'invalid' (remains string)
        """
        inferred_type = cls.infer_type(value)

        if inferred_type == DataType.BOOLEAN:
            return String.to_bool(value)
        if inferred_type == DataType.INTEGER:
            return String.to_int(value)
        if inferred_type == DataType.FLOAT:
            return String.to_float(value)
        if inferred_type == DataType.DATE:
            return String.to_date(value)
        if inferred_type == DataType.TIME:
            return String.to_time(value)
        if inferred_type == DataType.DATETIME:
            return String.to_datetime(value)
        if inferred_type == DataType.NONE:
            return None
        if inferred_type == DataType.EMPTY:
            return ""
        return value

    @staticmethod
    def _determine_type_from_counts(
        types: dict[str, int],
        count: int,
        *,
        allow_special_cases: bool = True,
    ) -> DataType | None:
        """
        Determine the data type based on type counts.

        Args:
            types: Dictionary of type counts
            count: Total number of values processed
            allow_special_cases: Whether to apply special case logic (all-digit strings, etc.)

        Returns:
            DataType if a definitive type can be determined, None otherwise
        """
        if types[DataType.EMPTY.name] == count:
            return DataType.EMPTY

        if types[DataType.NONE.name] == count:
            return DataType.NONE

        if types[DataType.NONE.name] + types[DataType.EMPTY.name] == count:
            return DataType.NONE

        if types[DataType.BOOLEAN.name] + types[DataType.EMPTY.name] == count:
            return DataType.BOOLEAN

        if types[DataType.STRING.name] + types[DataType.EMPTY.name] == count:
            return DataType.STRING

        # For early termination, skip complex logic that requires full analysis
        if not allow_special_cases:
            return None

        if types[DataType.DATE.name] + types[DataType.EMPTY.name] == count:
            return DataType.DATE

        if types[DataType.DATETIME.name] + types[DataType.EMPTY.name] == count:
            return DataType.DATETIME

        if types[DataType.TIME.name] + types[DataType.EMPTY.name] == count:
            return DataType.TIME

        if types[DataType.INTEGER.name] + types[DataType.EMPTY.name] == count:
            return DataType.INTEGER

        if types[DataType.FLOAT.name] + types[DataType.INTEGER.name] + types[DataType.EMPTY.name] == count:
            return DataType.FLOAT

        return None

    @classmethod
    def profile_values(
        cls,
        values: Iterable[Any],
        *,
        trim: bool = True,
        use_incremental_typecheck: bool = True,
    ) -> DataType:
        """
        Infer the most appropriate data type for a collection of values.

        This function analyzes a collection of values and determines the most
        appropriate data type that can represent all values in the collection.
        For lists of more than _INCREMENTAL_TYPECHECK_THRESHOLD items, it uses weighted incremental checks
        to short-circuit early when enough information is available to determine
        the final data type. For lists of _INCREMENTAL_TYPECHECK_THRESHOLD or fewer items, incremental
        type checking is disabled and a single pass is used.

        Args:
            values: Collection of values to analyze
            trim: Whether to trim whitespace before checking
            use_incremental_typecheck: Whether to use incremental type checking for early termination.
                                    For lists of _INCREMENTAL_TYPECHECK_THRESHOLD or fewer items, this is always False.

        Returns:
            DataType enum value representing the inferred type

        Raises:
            SplurgeTyperValueError: If values is not iterable

        Examples:
            >>> profile_values(['1', '2', '3'])           # DataType.INTEGER
            >>> profile_values(['1.1', '2.2', '3.3'])     # DataType.FLOAT
            >>> profile_values(['1', '2.2', 'abc'])       # DataType.MIXED
            >>> profile_values(['true', 'false'])         # DataType.BOOLEAN
            >>> profile_values(['1', '2', '3'], use_incremental_typecheck=False)  # Full analysis
        """
        if not DuckTyping.is_iterable_not_string(values):
            raise SplurgeTyperValueError(message="values must be iterable", error_code="value-not-iterable")

        # Convert to list to handle generators and ensure we can iterate multiple times
        values_list: list[Any] = list(values)

        if not values_list:
            return DataType.EMPTY

        # Only enable incremental type checking for lists larger than the threshold
        if len(values_list) <= cls.get_incremental_typecheck_threshold():
            use_incremental_typecheck = False

        # Sequential processing with incremental checks
        types = {
            DataType.BOOLEAN.name: 0,
            DataType.DATE.name: 0,
            DataType.TIME.name: 0,
            DataType.DATETIME.name: 0,
            DataType.INTEGER.name: 0,
            DataType.FLOAT.name: 0,
            DataType.STRING.name: 0,
            DataType.EMPTY.name: 0,
            DataType.NONE.name: 0,
        }

        count = 0
        total_count = len(values_list)

        # Check points for early termination (25%, 50%, 75%) - only used if incremental checking is enabled
        check_points = {}
        if use_incremental_typecheck:
            check_points = {
                int(total_count * 0.25): False,
                int(total_count * 0.50): False,
                int(total_count * 0.75): False,
            }

        # First pass: count types with incremental checks
        for value in values_list:
            inferred_type = String.infer_type(value, trim=trim)
            types[inferred_type.name] += 1
            count += 1

            # Check for early termination at check points (only if incremental checking is enabled)
            if use_incremental_typecheck and count in check_points:
                # Only do early termination for very clear cases that don't involve
                # the special all-digit string logic or mixed int/float detection

                # Early detection of MIXED type: if we have both numeric/temporal types AND string types
                numeric_temporal_count = (
                    types[DataType.INTEGER.name]
                    + types[DataType.FLOAT.name]
                    + types[DataType.DATE.name]
                    + types[DataType.DATETIME.name]
                    + types[DataType.TIME.name]
                )
                string_count = types[DataType.STRING.name]

                if numeric_temporal_count > 0 and string_count > 0:
                    return DataType.MIXED

                early_result = cls._determine_type_from_counts(types, count, allow_special_cases=False)
                if early_result is not None:
                    return early_result

        # Final determination based on complete analysis
        final_result = cls._determine_type_from_counts(types, count, allow_special_cases=True)
        if final_result is not None:
            return final_result

        # Special case: if we have mixed DATE, TIME, DATETIME, INTEGER types,
        # check if all values are all-digit strings and prioritize INTEGER
        if types[DataType.DATE.name] + types[DataType.TIME.name] + types[DataType.DATETIME.name] + types[
            DataType.INTEGER.name
        ] + types[DataType.EMPTY.name] == count and (
            types[DataType.DATE.name] > 0
            or types[DataType.TIME.name] > 0
            or types[DataType.DATETIME.name] > 0
            or types[DataType.EMPTY.name] > 0
        ):
            # Second pass: check if all non-empty values are all-digit strings (with optional +/- signs)
            all_digit_values = True
            for value in values_list:
                if not String.is_empty_like(value, trim=trim) and not String.is_int_like(value, trim=trim):
                    all_digit_values = False
                    break

            if all_digit_values:
                return DataType.INTEGER

        return DataType.MIXED

    @staticmethod
    def is_list_like(value: Any) -> bool:
        """
        Check if value behaves like a list (duck typing).

        This method performs duck typing to determine if a value has list-like behavior,
        checking for the presence of common list methods.

        Args:
            value: Value to check for list-like behavior

        Returns:
            True if value is a list or has list-like behavior (append, remove, index methods)

        Examples:
            >>> TypeInference.is_list_like([1, 2, 3])        # True
            >>> TypeInference.is_list_like((1, 2, 3))        # False
            >>> TypeInference.is_list_like('abc')            # False
            >>> from collections import deque
            >>> TypeInference.is_list_like(deque([1, 2, 3])) # True
        """
        return DuckTyping.is_list_like(value)

    @staticmethod
    def is_dict_like(value: Any) -> bool:
        """
        Check if value behaves like a dictionary (duck typing).

        This method performs duck typing to determine if a value has dictionary-like behavior,
        checking for the presence of common dictionary methods.

        Args:
            value: Value to check for dictionary-like behavior

        Returns:
            True if value is a dict or has dict-like behavior (keys, get, values methods)

        Examples:
            >>> TypeInference.is_dict_like({'a': 1})         # True
            >>> TypeInference.is_dict_like([1, 2, 3])        # False
            >>> TypeInference.is_dict_like('abc')            # False
            >>> from collections import OrderedDict
            >>> TypeInference.is_dict_like(OrderedDict([('a', 1)])) # True
        """
        return DuckTyping.is_dict_like(value)

    @staticmethod
    def is_iterable(value: Any) -> bool:
        """
        Check if value is iterable.

        This method determines if a value supports iteration, either through the
        Iterable protocol or by having common iteration-related methods.

        Args:
            value: Value to check for iterability

        Returns:
            True if value is iterable (supports iteration)

        Examples:
            >>> TypeInference.is_iterable([1, 2, 3])         # True
            >>> TypeInference.is_iterable((1, 2, 3))         # True
            >>> TypeInference.is_iterable('abc')             # True
            >>> TypeInference.is_iterable(123)               # False
            >>> TypeInference.is_iterable({'a': 1})          # True
        """
        return DuckTyping.is_iterable(value)

    @staticmethod
    def is_iterable_not_string(value: Any) -> bool:
        """
        Check if value is iterable but not a string.

        This is useful for distinguishing between collections (lists, tuples, sets, etc.)
        and string values, which are also iterable but often need different handling.

        Args:
            value: Value to check

        Returns:
            True if value is iterable and not a string

        Examples:
            >>> TypeInference.is_iterable_not_string([1, 2, 3])  # True
            >>> TypeInference.is_iterable_not_string((1, 2, 3))  # True
            >>> TypeInference.is_iterable_not_string({'a': 1})   # True
            >>> TypeInference.is_iterable_not_string('abc')      # False
            >>> TypeInference.is_iterable_not_string(123)        # False
        """
        return DuckTyping.is_iterable_not_string(value)

    @staticmethod
    def is_empty(value: Any) -> bool:
        """
        Check if value is empty (None, empty string, or empty collection).

        This method provides a unified way to check for emptiness across different
        types of values, handling None, strings, and collections consistently.

        Args:
            value: Value to check for emptiness

        Returns:
            True if value is None, empty string, or empty collection

        Examples:
            >>> TypeInference.is_empty(None)           # True
            >>> TypeInference.is_empty('')             # True
            >>> TypeInference.is_empty('   ')          # True (whitespace-only)
            >>> TypeInference.is_empty([])             # True
            >>> TypeInference.is_empty({})             # True
            >>> TypeInference.is_empty(set())          # True
            >>> TypeInference.is_empty('abc')          # False
            >>> TypeInference.is_empty([1, 2, 3])      # False
        """
        return DuckTyping.is_empty(value)
