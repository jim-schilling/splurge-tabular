"""String utilities for inference and conversion.

This module provides helpers for detecting and converting values represented
as strings. It offers extensive support for numeric, boolean, date/time, and
other common patterns.

Copyright (c) 2025 Jim Schilling

Please preserve this header and all related material when sharing!

This module is licensed under the MIT License.
"""

import re
from datetime import date, datetime, time
from typing import Any

from .data_type import DataType


class String:
    """
    Utility class for string type checking and conversion operations.

    This class provides static methods for:
    - Type validation (is_*_like methods)
    - Type conversion (to_* methods)
    - Type inference
    - String format validation
    """

    # Private class-level constants for datetime patterns
    _DATE_PATTERNS: list[str] = [
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%Y.%m.%d",
        "%Y%m%d",
        "%Y-%d-%m",
        "%Y/%d/%m",
        "%Y.%d.%m",
        "%Y%d%m",
        "%m-%d-%Y",
        "%m/%d/%Y",
        "%m.%d.%Y",
        "%m%d%Y",
    ]

    _TIME_PATTERNS: list[str] = [
        "%H:%M:%S",
        "%H:%M:%S.%f",
        "%H:%M",
        "%H%M",
        "%H%M%S",
        "%I:%M:%S.%f %p",
        "%I:%M:%S %p",
        "%I:%M %p",
        "%I:%M:%S%p",
        "%I:%M%p",
    ]

    _DATETIME_PATTERNS: list[str] = [
        "%Y-%m-%dT%H:%M:%S",  # T separator
        "%Y-%m-%d %H:%M:%S",  # Space separator
        "%Y/%m/%dT%H:%M:%S",  # T separator
        "%Y/%m/%d %H:%M:%S",  # Space separator
        "%Y.%m.%dT%H:%M:%S",  # T separator
        "%Y.%m.%d %H:%M:%S",  # Space separator
        "%Y%m%d%H%M%S",
        "%Y-%d-%mT%H:%M:%S",  # T separator
        "%Y-%d-%m %H:%M:%S",  # Space separator
        "%Y/%d/%mT%H:%M:%S",  # T separator
        "%Y/%d/%m %H:%M:%S",  # Space separator
        "%Y.%d.%mT%H:%M:%S",  # T separator
        "%Y.%d.%m %H:%M:%S",  # Space separator
        "%Y%d%m%H%M%S",
        "%m-%d-%YT%H:%M:%S",  # T separator
        "%m-%d-%Y %H:%M:%S",  # Space separator
        "%m/%d/%YT%H:%M:%S",  # T separator
        "%m/%d/%Y %H:%M:%S",  # Space separator
        "%m.%d.%YT%H:%M:%S",  # T separator
        "%m.%d.%Y %H:%M:%S",  # Space separator
        "%m%d%Y%H%M%S",
        "%Y-%m-%dT%H:%M:%S.%f",  # T separator
        "%Y-%m-%d %H:%M:%S.%f",  # Space separator
        "%Y/%m/%dT%H:%M:%S.%f",  # T separator
        "%Y/%m/%d %H:%M:%S.%f",  # Space separator
        "%Y.%m.%dT%H:%M:%S.%f",  # T separator
        "%Y.%m.%d %H:%M:%S.%f",  # Space separator
        "%Y%m%d%H%M%S%f",
        "%Y-%d-%mT%H:%M:%S.%f",  # T separator
        "%Y-%d-%m %H:%M:%S.%f",  # Space separator
        "%Y/%d/%mT%H:%M:%S.%f",  # T separator
        "%Y/%d/%m %H:%M:%S.%f",  # Space separator
        "%Y.%d.%mT%H:%M:%S.%f",  # T separator
        "%Y.%d.%m %H:%M:%S.%f",  # Space separator
        "%Y%d%m%H%M%S%f",
        "%m-%d-%YT%H:%M:%S.%f",  # T separator
        "%m-%d-%Y %H:%M:%S.%f",  # Space separator
        "%m/%d/%YT%H:%M:%S.%f",  # T separator
        "%m/%d/%Y %H:%M:%S.%f",  # Space separator
        "%m.%d.%YT%H:%M:%S.%f",  # T separator
        "%m.%d.%Y %H:%M:%S.%f",  # Space separator
        "%m%d%Y%H%M%S%f",
    ]

    # Private class-level constants for regex patterns
    _FLOAT_REGEX = re.compile(r"""^[-+]?(\d+\.?\d*|\.\d+)$""")
    _INTEGER_REGEX = re.compile(r"""^[-+]?\d+$""")
    _DATE_YYYY_MM_DD_REGEX = re.compile(r"""^\d{4}[-/.]?\d{2}[-/.]?\d{2}$""")
    _DATE_MM_DD_YYYY_REGEX = re.compile(r"""^\d{2}[-/.]?\d{2}[-/.]?\d{4}$""")
    _DATETIME_YYYY_MM_DD_REGEX = re.compile(
        r"""^\d{4}[-/.]?\d{2}[-/.]?\d{2}[T ]?\d{2}[:]?\d{2}([:]?\d{2}([.]?\d{5})?)?$""",
    )
    _DATETIME_MM_DD_YYYY_REGEX = re.compile(
        r"""^\d{2}[-/.]?\d{2}[-/.]?\d{4}[T ]?\d{2}[:]?\d{2}([:]?\d{2}([.]?\d{5})?)?$""",
    )
    _TIME_24HOUR_REGEX = re.compile(r"""^(\d{1,2}):(\d{2})(:(\d{2})([.](\d+))?)?$""")
    _TIME_12HOUR_REGEX = re.compile(r"""^(\d{1,2}):(\d{2})(:(\d{2})([.](\d+))?)?\s*(AM|PM|am|pm)$""")
    _TIME_COMPACT_REGEX = re.compile(r"""^(\d{2})(\d{2})(\d{2})?$""")

    @classmethod
    def is_bool_like(
        cls,
        value: str | bool | None,
        *,
        trim: bool = True,
    ) -> bool:
        """
        Check if value can be interpreted as a boolean.

        Args:
            value: Value to check (string or bool)
            trim: Whether to trim whitespace before checking

        Returns:
            True if value is bool or string representing boolean ('true'/'false'/'yes'/'no')

        Examples:
            >>> String.is_bool_like('true')  # True
            >>> String.is_bool_like('false') # True
            >>> String.is_bool_like('yes')   # True
            >>> String.is_bool_like('no')    # True
            >>> String.is_bool_like('TRUE')  # True
            >>> String.is_bool_like('FALSE') # True
            >>> String.is_bool_like('1')     # False
        """
        if value is None:
            return False

        if isinstance(value, bool):
            return True

        if isinstance(value, str):
            normalized = value.strip().lower() if trim else value.lower()
            return normalized in ["true", "false", "yes", "no"]

    @classmethod
    def is_none_like(
        cls,
        value: Any,
        *,
        trim: bool = True,
    ) -> bool:
        """
        Check if value represents None/null.

        Args:
            value: Value to check
            trim: Whether to trim whitespace before checking

        Returns:
            True if value is None or string 'none'/'null'

        Examples:
            >>> String.is_none_like(None)    # True
            >>> String.is_none_like('none')  # True
            >>> String.is_none_like('null')  # True
        """
        if value is None:
            return True

        if isinstance(value, str):
            normalized = value.strip().lower() if trim else value.lower()
            return normalized in ["none", "null"]

        return False

    @classmethod
    def is_empty_like(
        cls,
        value: Any,
        *,
        trim: bool = True,
    ) -> bool:
        """
        Check if value is an empty string or contains only whitespace.

        Args:
            value: Value to check
            trim: Whether to trim whitespace before checking

        Returns:
            True if value is empty string or contains only whitespace

        Examples:
            >>> String.is_empty_like('')      # True
            >>> String.is_empty_like('   ')   # True
            >>> String.is_empty_like('abc')   # False
            >>> String.is_empty_like(None)    # False
        """
        if value is None:
            return False

        if not isinstance(value, str):
            return False

        return not value.strip() if trim else not value

    @classmethod
    def is_float_like(
        cls,
        value: str | float | None,
        *,
        trim: bool = True,
    ) -> bool:
        """
        Check if value can be interpreted as a float.

        Args:
            value: Value to check (string or float)
            trim: Whether to trim whitespace before checking

        Returns:
            True if value is float or string representing a float

        Examples:
            >>> String.is_float_like('1.23')  # True
            >>> String.is_float_like('-1.23') # True
            >>> String.is_float_like('1')     # True
        """
        if value is None:
            return False

        if isinstance(value, float):
            return True

        if isinstance(value, str):
            normalized = value.strip() if trim else value
            return cls._FLOAT_REGEX.match(normalized) is not None

        return False  # type: ignore

    @classmethod
    def is_int_like(
        cls,
        value: str | int | None,
        *,
        trim: bool = True,
    ) -> bool:
        """
        Check if value can be interpreted as an integer.

        Args:
            value: Value to check (string or int)
            trim: Whether to trim whitespace before checking

        Returns:
            True if value is int or string representing an integer

        Examples:
            >>> String.is_int_like('123')   # True
            >>> String.is_int_like('-123')  # True
            >>> String.is_int_like('1.23')  # False
        """
        if value is None:
            return False

        if isinstance(value, int):
            return True

        if isinstance(value, str):
            normalized = value.strip() if trim else value
            return cls._INTEGER_REGEX.match(normalized) is not None

    @classmethod
    def is_numeric_like(
        cls,
        value: str | float | None,
        *,
        trim: bool = True,
    ) -> bool:
        """
        Check if value can be interpreted as a number (int or float).

        Args:
            value: Value to check (string, float, or int)
            trim: Whether to trim whitespace before checking

        Returns:
            True if value is numeric or string representing a number

        Examples:
            >>> String.is_numeric_like('123')   # True
            >>> String.is_numeric_like('1.23')  # True
            >>> String.is_numeric_like('abc')   # False
        """
        if value is None:
            return False

        if isinstance(value, int | float):
            return True

        if isinstance(value, str):
            return cls.is_float_like(value, trim=trim) or cls.is_int_like(value, trim=trim)

    @classmethod
    def is_category_like(
        cls,
        value: str | None,
        *,
        trim: bool = True,
    ) -> bool:
        """
        Check if value is non-numeric (categorical).

        Args:
            value: Value to check
            trim: Whether to trim whitespace before checking

        Returns:
            True if value is not numeric

        Examples:
            >>> String.is_category_like('abc')   # True
            >>> String.is_category_like('123')   # False
            >>> String.is_category_like('1.23')  # False
        """
        if value is None:
            return False

        return not cls.is_numeric_like(value, trim=trim)

    @classmethod
    def _is_date_like(cls, value: str) -> bool:
        """
        Internal method to check if string matches common date formats.

        Args:
            value: String to check

        Returns:
            True if string matches a supported date format

        Note:
            Supports multiple date formats including:
            - YYYY-MM-DD
            - YYYY/MM/DD
            - YYYY.MM.DD
            - YYYYMMDD
            And their variations with different date component orders
        """
        for pattern in cls._DATE_PATTERNS:
            try:
                datetime.strptime(value, pattern)
                return True
            except ValueError:
                pass

        return False

    @classmethod
    def _is_time_like(cls, value: str) -> bool:
        """
        Internal method to check if string matches common time formats.

        Args:
            value: String to check

        Returns:
            True if string matches a supported time format

        Note:
            Supports multiple time formats including:
            - HH:MM:SS
            - HH:MM:SS.microseconds
            - HH:MM
            - HHMMSS
            - HHMM
            And 12-hour format variations with AM/PM
        """
        for pattern in cls._TIME_PATTERNS:
            try:
                datetime.strptime(value, pattern)
                return True
            except ValueError:
                pass

        return False

    @classmethod
    def is_date_like(
        cls,
        value: str | date | None,
        *,
        trim: bool = True,
    ) -> bool:
        """
        Check if value can be interpreted as a date.

        Args:
            value: Value to check (string or date)
            trim: Whether to trim whitespace before checking

        Returns:
            True if value is date or string in supported date format

        Examples:
            >>> String.is_date_like('2023-01-01')  # True
            >>> String.is_date_like('01/01/2023')  # True
            >>> String.is_date_like('20230101')    # True
        """
        if not value:
            return False

        if isinstance(value, date):
            return True

        if isinstance(value, str):
            normalized = value.strip() if trim else value

            if String._DATE_YYYY_MM_DD_REGEX.match(normalized) and cls._is_date_like(normalized):
                return True

            if String._DATE_MM_DD_YYYY_REGEX.match(normalized) and cls._is_date_like(normalized):
                return True

        return False

    @classmethod
    def _is_datetime_like(cls, value: str) -> bool:
        """
        Internal method to check if string matches common datetime formats.

        Args:
            value: String to check

        Returns:
            True if string matches a supported datetime format

        Note:
            Supports multiple datetime formats including:
            - YYYY-MM-DDTHH:MM:SS
            - YYYY/MM/DDTHH:MM:SS
            - YYYY.MM.DDTHH:MM:SS
            - YYYYMMDDHHMMSS
            And their variations with different date component orders and optional microseconds
        """
        for pattern in cls._DATETIME_PATTERNS:
            try:
                datetime.strptime(value, pattern)
                return True
            except ValueError:
                pass

        return False

    @classmethod
    def is_datetime_like(
        cls,
        value: str | datetime | None,
        *,
        trim: bool = True,
    ) -> bool:
        """
        Check if value can be interpreted as a datetime.

        Args:
            value: Value to check (string or datetime)
            trim: Whether to trim whitespace before checking

        Returns:
            True if value is datetime or string in supported datetime format

        Examples:
            >>> String.is_datetime_like('2023-01-01T12:00:00')     # True (T separator)
            >>> String.is_datetime_like('2023-01-01 12:00:00')     # True (space separator)
            >>> String.is_datetime_like('2023-01-01T12:00:00.123') # True
            >>> String.is_datetime_like('2023-01-01')              # False
        """
        if not value:
            return False

        if isinstance(value, datetime):
            return True

        if isinstance(value, str):
            normalized = value.strip() if trim else value

            if String._DATETIME_YYYY_MM_DD_REGEX.match(normalized) and cls._is_datetime_like(normalized):
                return True

            if String._DATETIME_MM_DD_YYYY_REGEX.match(normalized) and cls._is_datetime_like(normalized):
                return True

        return False

    @classmethod
    def is_time_like(
        cls,
        value: str | time | None,
        *,
        trim: bool = True,
    ) -> bool:
        """
        Check if value can be interpreted as a time.

        Args:
            value: Value to check (string or time)
            trim: Whether to trim whitespace before checking

        Returns:
            True if value is time or string in supported time format

        Examples:
            >>> String.is_time_like('14:30:00')     # True
            >>> String.is_time_like('14:30:00.123') # True
            >>> String.is_time_like('2:30 PM')      # True
            >>> String.is_time_like('143000')       # True
            >>> String.is_time_like('2023-01-01')   # False
        """
        if not value:
            return False

        if isinstance(value, time):
            return True

        if isinstance(value, str):
            normalized = value.strip() if trim else value

            if String._TIME_24HOUR_REGEX.match(normalized) and cls._is_time_like(normalized):
                return True

            if String._TIME_12HOUR_REGEX.match(normalized) and cls._is_time_like(normalized):
                return True

            if String._TIME_COMPACT_REGEX.match(normalized) and cls._is_time_like(normalized):
                return True

        return False

    @classmethod
    def to_bool(
        cls,
        value: str | bool | None,
        *,
        default: bool | None = None,
        trim: bool = True,
    ) -> bool | None:
        """
        Convert value to boolean.

        Args:
            value: Value to convert
            default: Default value if conversion fails
            trim: Whether to trim whitespace before converting

        Returns:
            Boolean value or default if conversion fails

        Examples:
            >>> String.to_bool('true')   # True
            >>> String.to_bool('false')  # False
            >>> String.to_bool('yes')    # True
            >>> String.to_bool('no')     # False
            >>> String.to_bool('TRUE')   # True
            >>> String.to_bool('FALSE')  # False
        """
        if isinstance(value, bool):
            return value

        if cls.is_bool_like(value, trim=trim):
            if isinstance(value, str):
                normalized = value.strip().lower() if trim else value.lower()
                return normalized in ["true", "yes"]
            return str(value).lower() in ["true", "yes"]

        return default

    @classmethod
    def to_float(
        cls,
        value: str | float | None,
        *,
        default: float | None = None,
        trim: bool = True,
    ) -> float | None:
        """
        Convert value to float.

        Args:
            value: Value to convert
            default: Default value if conversion fails
            trim: Whether to trim whitespace before converting

        Returns:
            Float value or default if conversion fails

        Examples:
            >>> String.to_float('1.23')  # 1.23
            >>> String.to_float('-1.23') # -1.23
            >>> String.to_float('abc')   # None
        """
        if cls.is_float_like(value, trim=trim) and value is not None:
            return float(value)
        return default

    @classmethod
    def to_int(
        cls,
        value: str | int | None,
        *,
        default: int | None = None,
        trim: bool = True,
    ) -> int | None:
        """
        Convert value to integer.

        Args:
            value: Value to convert
            default: Default value if conversion fails
            trim: Whether to trim whitespace before converting

        Returns:
            Integer value or default if conversion fails

        Examples:
            >>> String.to_int('123')   # 123
            >>> String.to_int('-123')  # -123
            >>> String.to_int('1.23')  # None
        """
        if cls.is_int_like(value, trim=trim) and value is not None:
            return int(value)
        return default

    @classmethod
    def to_date(
        cls,
        value: str | date | None,
        *,
        default: date | None = None,
        trim: bool = True,
    ) -> date | None:
        """
        Convert value to date.

        Args:
            value: Value to convert
            default: Default value if conversion fails
            trim: Whether to trim whitespace before converting

        Returns:
            Date value or default if conversion fails

        Examples:
            >>> String.to_date('2023-01-01')  # datetime.date(2023, 1, 1)
            >>> String.to_date('01/01/2023')  # datetime.date(2023, 1, 1)
            >>> String.to_date('invalid')     # None
        """
        if isinstance(value, date):
            return value

        if not cls.is_date_like(value, trim=trim):
            return default

        if not isinstance(value, str):
            return default

        normalized = value.strip() if trim else value

        for pattern in cls._DATE_PATTERNS:
            try:
                tmp_value = datetime.strptime(normalized, pattern)
                return tmp_value.date()
            except ValueError:
                pass

        return default

    @classmethod
    def to_datetime(
        cls,
        value: str | datetime | None,
        *,
        default: datetime | None = None,
        trim: bool = True,
    ) -> datetime | None:
        """
        Convert value to datetime.

        Args:
            value: Value to convert
            default: Default value if conversion fails
            trim: Whether to trim whitespace before converting

        Returns:
            Datetime value or default if conversion fails

        Examples:
            >>> String.to_datetime('2023-01-01T12:00:00')     # datetime(2023, 1, 1, 12, 0) (T separator)
            >>> String.to_datetime('2023-01-01 12:00:00')     # datetime(2023, 1, 1, 12, 0) (space separator)
            >>> String.to_datetime('2023-01-01T12:00:00.123') # datetime(2023, 1, 1, 12, 0, 0, 123000)
            >>> String.to_datetime('invalid')                 # None
        """
        if isinstance(value, datetime):
            return value

        if not cls.is_datetime_like(value, trim=trim):
            return default

        if not isinstance(value, str):
            return default

        normalized = value.strip() if trim else value

        for pattern in cls._DATETIME_PATTERNS:
            try:
                return datetime.strptime(normalized, pattern)
            except ValueError:
                pass

        return default

    @classmethod
    def to_time(
        cls,
        value: str | time | None,
        *,
        default: time | None = None,
        trim: bool = True,
    ) -> time | None:
        """
        Convert value to time.

        Args:
            value: Value to convert
            default: Default value if conversion fails
            trim: Whether to trim whitespace before converting

        Returns:
            Time value or default if conversion fails

        Examples:
            >>> String.to_time('14:30:00')     # datetime.time(14, 30)
            >>> String.to_time('2:30 PM')      # datetime.time(14, 30)
            >>> String.to_time('143000')       # datetime.time(14, 30, 0)
            >>> String.to_time('invalid')      # None
        """
        if isinstance(value, time):
            return value

        if not cls.is_time_like(value, trim=trim):
            return default

        if not isinstance(value, str):
            return default

        normalized = value.strip() if trim else value

        for pattern in cls._TIME_PATTERNS:
            try:
                tvalue = datetime.strptime(normalized, pattern)
                return tvalue.time()
            except ValueError:
                pass

        return default

    @classmethod
    def has_leading_zero(
        cls,
        value: str | None,
        *,
        trim: bool = True,
    ) -> bool:
        """
        Check if string value has leading zero.

        Args:
            value: Value to check
            trim: Whether to trim whitespace before checking

        Returns:
            True if value starts with '0'

        Examples:
            >>> String.has_leading_zero('01')    # True
            >>> String.has_leading_zero('10')    # False
            >>> String.has_leading_zero(' 01')   # True (with trim=True)
        """
        if value is None:
            return False

        return value.strip().startswith("0") if trim else value.startswith("0")

    @classmethod
    def infer_type(
        cls,
        value: str | bool | int | float | date | time | datetime | None,
        *,
        trim: bool = True,
    ) -> DataType:
        """
        Infer the most appropriate data type for a value.

        Args:
            value: Value to check
            trim: Whether to trim whitespace before checking

        Returns:
            DataType enum value representing the inferred type

        Examples:
            >>> String.infer_type('123')           # DataType.INTEGER
            >>> String.infer_type('1.23')          # DataType.FLOAT
            >>> String.infer_type('2023-01-01')    # DataType.DATE
            >>> String.infer_type('true')          # DataType.BOOLEAN
            >>> String.infer_type('abc')           # DataType.STRING
        """
        # Handle non-string types first
        if isinstance(value, bool):
            return DataType.BOOLEAN
        if isinstance(value, int):
            return DataType.INTEGER
        if isinstance(value, float):
            return DataType.FLOAT
        if isinstance(value, datetime):
            return DataType.DATETIME
        if isinstance(value, time):
            return DataType.TIME
        if isinstance(value, date):
            return DataType.DATE

        # Handle string and None types
        if cls.is_none_like(value, trim=trim):
            return DataType.NONE

        if cls.is_empty_like(value, trim=trim):
            return DataType.EMPTY

        if isinstance(value, str):
            if cls.is_bool_like(value, trim=trim):
                return DataType.BOOLEAN

            if cls.is_datetime_like(value, trim=trim):
                return DataType.DATETIME

            if cls.is_time_like(value, trim=trim):
                return DataType.TIME

            if cls.is_date_like(value, trim=trim):
                return DataType.DATE

            if cls.is_int_like(value, trim=trim):
                return DataType.INTEGER

            if cls.is_float_like(value, trim=trim):
                return DataType.FLOAT

        return DataType.STRING

    @classmethod
    def infer_type_name(
        cls,
        value: str | bool | float | date | time | datetime | None,
        *,
        trim: bool = True,
    ) -> str:
        """
        Infer the most appropriate data type name for a value.

        Args:
            value: Value to check
            trim: Whether to trim whitespace before checking

        Returns:
            String name of the inferred type

        Examples:
            >>> String.infer_type_name('123')           # 'INTEGER'
            >>> String.infer_type_name('1.23')          # 'FLOAT'
            >>> String.infer_type_name('2023-01-01')    # 'DATE'
            >>> String.infer_type_name('true')          # 'BOOLEAN'
            >>> String.infer_type_name('abc')           # 'STRING'
        """
        return cls.infer_type(value, trim=trim).name
