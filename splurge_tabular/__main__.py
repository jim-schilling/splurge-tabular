"""Module entry-point to run the Splurge Tabular CLI.

This module allows running the package as a script using:

    python -m splurge_tabular

It simply forwards execution to :func:`splurge_tabular.cli.main`.
"""

import sys

from .cli import main

if __name__ == "__main__":
    sys.exit(main())
