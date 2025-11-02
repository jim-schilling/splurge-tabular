"""Duck typing utilities.

Utilities for determining object behavior based on method availability rather
than inheritance. These helpers are used to detect list-like, dict-like and
iterable behavior across arbitrary objects.

Copyright (c) 2025 Jim Schilling

Please preserve this header and all related material when sharing!

This module is licensed under the MIT License.
"""

from typing import Any


class DuckTyping:
    """Utilities for duck-typing checks.

    This class contains only static helpers that detect common behavioral
    characteristics (list-like, dict-like, iterable, empty) without
    requiring subclassing or protocol registration.
    """

    @staticmethod
    def is_list_like(value: Any) -> bool:
        """
        Check if value behaves like a list (duck typing).

        This method performs duck typing to determine if a value has list-like behavior,
        checking for the presence of common list methods (append, remove, index).

        Args:
            value: Value to check for list-like behavior

        Returns:
            True if value is a list or has list-like behavior (append, remove, index methods)

        Examples:
            >>> DuckTyping.is_list_like([1, 2, 3])        # True
            >>> DuckTyping.is_list_like((1, 2, 3))        # False
            >>> DuckTyping.is_list_like('abc')            # False
            >>> from collections import deque
            >>> DuckTyping.is_list_like(deque([1, 2, 3])) # True
        """
        if isinstance(value, list):
            return True

        return bool(
            hasattr(value, "__iter__")
            and hasattr(value, "append")
            and hasattr(value, "remove")
            and hasattr(value, "index"),
        )

    @staticmethod
    def is_dict_like(value: Any) -> bool:
        """
        Check if value behaves like a dictionary (duck typing).

        This method performs duck typing to determine if a value has dictionary-like behavior,
        checking for the presence of common dictionary methods (keys, get, values).

        Args:
            value: Value to check for dictionary-like behavior

        Returns:
            True if value is a dict or has dict-like behavior (keys, get, values methods)

        Examples:
            >>> DuckTyping.is_dict_like({'a': 1})         # True
            >>> DuckTyping.is_dict_like([1, 2, 3])        # False
            >>> DuckTyping.is_dict_like('abc')            # False
            >>> from collections import OrderedDict
            >>> DuckTyping.is_dict_like(OrderedDict([('a', 1)])) # True
        """
        if isinstance(value, dict):
            return True

        return bool(hasattr(value, "keys") and hasattr(value, "get") and hasattr(value, "values"))

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
            >>> DuckTyping.is_iterable([1, 2, 3])         # True
            >>> DuckTyping.is_iterable((1, 2, 3))         # True
            >>> DuckTyping.is_iterable('abc')             # True
            >>> DuckTyping.is_iterable(123)               # False
            >>> DuckTyping.is_iterable({'a': 1})          # True
        """
        try:
            # Try the most common approach first
            iter(value)
            return True
        except TypeError:
            # Check for iterator protocol methods
            return bool(hasattr(value, "__iter__") or hasattr(value, "__getitem__") or hasattr(value, "__next__"))

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
            >>> DuckTyping.is_iterable_not_string([1, 2, 3])  # True
            >>> DuckTyping.is_iterable_not_string((1, 2, 3))  # True
            >>> DuckTyping.is_iterable_not_string({'a': 1})   # True
            >>> DuckTyping.is_iterable_not_string('abc')      # False
            >>> DuckTyping.is_iterable_not_string(123)        # False
        """
        return bool(DuckTyping.is_iterable(value) and not isinstance(value, str))

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
            >>> DuckTyping.is_empty(None)           # True
            >>> DuckTyping.is_empty('')             # True
            >>> DuckTyping.is_empty('   ')          # True (whitespace-only)
            >>> DuckTyping.is_empty([])             # True
            >>> DuckTyping.is_empty({})             # True
            >>> DuckTyping.is_empty(set())          # True
            >>> DuckTyping.is_empty('abc')          # False
            >>> DuckTyping.is_empty([1, 2, 3])      # False
        """
        if value is None:
            return True

        if isinstance(value, str):
            return not value.strip()

        if hasattr(value, "__len__"):
            return len(value) == 0

        return False

    @staticmethod
    def get_behavior_type(value: Any) -> str:
        """
        Get a string describing the behavioral type of a value.

        This method analyzes a value and returns a string describing its
        behavioral characteristics based on duck typing.

        Args:
            value: Value to analyze

        Returns:
            String describing the behavioral type

        Examples:
            >>> DuckTyping.get_behavior_type([1, 2, 3])    # 'list-like'
            >>> DuckTyping.get_behavior_type({'a': 1})      # 'dict-like'
            >>> DuckTyping.get_behavior_type('abc')         # 'string'
            >>> DuckTyping.get_behavior_type(123)           # 'scalar'
            >>> DuckTyping.get_behavior_type(None)          # 'empty'
        """
        if DuckTyping.is_empty(value):
            return "empty"

        if isinstance(value, str):
            return "string"

        if DuckTyping.is_list_like(value):
            return "list-like"

        if DuckTyping.is_dict_like(value):
            return "dict-like"

        if DuckTyping.is_iterable(value):
            return "iterable"

        return "scalar"
