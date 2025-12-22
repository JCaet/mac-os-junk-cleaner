# macOS Junk Cleaner

A Python-based CLI utility to scan and remove macOS-specific junk files (e.g., `.DS_Store`, `._*`, `.Spotlight-V100`) from directories.

## Installation

```bash
pip install .
```

## Usage

### Scan
To see what would be cleaned with a detailed summary:
```bash
mac-clean scan /path/to/dir
```

### Clean
The `clean` command is used for removal. For safety, it **defaults to dry-run mode**.

```bash
# Preview deletion (Dry-run)
mac-clean clean /path/to/dir

# Perform actual deletion
mac-clean clean /path/to/dir --force
```

## Development

### Setup
1. Clone the repository.
2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
3. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

### Linting and Formatting
This project uses [Ruff](https://github.com/astral-sh/ruff) for linting and formatting.

```bash
# Lint
ruff check .

# Format
ruff format .
```

### Testing
```bash
pytest
```

