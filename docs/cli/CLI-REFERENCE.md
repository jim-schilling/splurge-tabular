# Splurge Tabular — CLI Reference

This document provides a reference for the command-line interface (CLI) of the
`splurge_tabular` package.

---

## Overview

The `splurge_tabular` CLI provides access to package metadata and version
information. The CLI is intentionally lightweight and currently exposes minimal
functionality.

---

## Usage

Run the CLI using one of the following methods:

```bash
python -m splurge_tabular [options]
```

or

```bash
splurge-tabular [options]
```

(if installed as a console script)

---

## Commands and Options

### Global Options

- **`--version`**
  - Display the version number and exit.
  - Example: `python -m splurge_tabular --version`
  - Output: `splurge-tabular 2025.2.0`

### Default Behavior

When run without any arguments or options, the CLI displays help information:

```bash
python -m splurge_tabular
```

This will show the help message with available options.

---

## Examples

### Display version

```bash
$ python -m splurge_tabular --version
splurge-tabular 2025.2.0
```

### Display help

```bash
$ python -m splurge_tabular
usage: splurge-tabular [-h] [--version]

Splurge Tabular - Python tabular data processing framework

options:
  -h, --help     show this help message and exit
  --version      show program's version number and exit
```

---

## Exit Codes

- **0**: Success
- **Non-zero**: Error (for future error conditions)

---

## Notes

- The CLI is currently minimal and primarily serves as a way to access package
  version information.
- Future versions may add additional commands for data processing operations.
- For programmatic use, import the package modules directly rather than using
  the CLI.

---

