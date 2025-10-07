from __future__ import annotations

from enum import Enum


class ErrorCode(str, Enum):
    """Centralized error codes used across the splurge_tabular package.

    Use `ErrorCode.<NAME>.value` when passing into exceptions to ensure a
    stable machine-readable string value.
    """

    TYPE_INVALID = "TYPE_INVALID"
    CONFIG_INVALID = "CONFIG_INVALID"
    COLUMN_NOT_FOUND = "COLUMN_NOT_FOUND"
    ROW_OUT_OF_RANGE = "ROW_OUT_OF_RANGE"
    INDEX_OUT_OF_RANGE = "INDEX_OUT_OF_RANGE"
    KEY_NOT_FOUND = "KEY_NOT_FOUND"
    VALIDATION_EMPTY_NOT_ALLOWED = "VALIDATION_EMPTY_NOT_ALLOWED"
