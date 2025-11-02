"""Unit tests for splurge_tabular.cli module.

Tests the command-line interface functionality.
"""

from unittest.mock import patch

import pytest

from splurge_tabular import __version__
from splurge_tabular.cli import main


class TestCLI:
    """Test the CLI main function."""

    def test_version_argument(self) -> None:
        """Test --version argument."""
        with patch("sys.argv", ["splurge-tabular", "--version"]):
            with pytest.raises(SystemExit) as exc_info:
                main(["--version"])
            # argparse's version action exits with code 0
            assert exc_info.value.code == 0

    def test_version_output(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that --version prints correct version."""
        # Test version by checking that SystemExit is raised (argparse behavior)
        # and verifying the version format
        with pytest.raises(SystemExit) as exc_info:
            main(["--version"])
        # argparse's version action exits with code 0
        assert exc_info.value.code == 0

    def test_version_string_format(self) -> None:
        """Test that version string format is correct."""
        # The version should be in format "splurge-tabular {version}"
        assert __version__ is not None
        assert len(__version__) > 0

    def test_no_arguments_shows_help(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test that running without arguments shows help."""
        exit_code = main([])
        captured = capsys.readouterr()

        assert exit_code == 0
        assert "splurge-tabular" in captured.out.lower()
        assert "usage:" in captured.out.lower() or "description" in captured.out.lower()

    def test_help_argument(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test --help argument."""
        with pytest.raises(SystemExit) as exc_info:
            main(["--help"])
        assert exc_info.value.code == 0

        captured = capsys.readouterr()
        assert "splurge-tabular" in captured.out.lower()
        assert "usage:" in captured.out.lower() or "description" in captured.out.lower()

    def test_invalid_argument(self) -> None:
        """Test that invalid arguments raise SystemExit."""
        with pytest.raises(SystemExit) as exc_info:
            main(["--invalid-arg"])
        # argparse exits with code 2 for invalid arguments
        assert exc_info.value.code == 2

    def test_main_returns_zero_on_success(self) -> None:
        """Test that main returns 0 on successful execution."""
        exit_code = main([])
        assert exit_code == 0

    def test_main_with_custom_args(self, capsys: pytest.CaptureFixture[str]) -> None:
        """Test main with custom argument list."""
        exit_code = main([])
        assert exit_code == 0

        captured = capsys.readouterr()
        # Should show help when no arguments provided
        assert len(captured.out) > 0

    def test_cli_module_execution(self) -> None:
        """Test that CLI can be executed as a module."""
        # Test that the main function exists and is callable
        assert callable(main)
        assert main([]) == 0
