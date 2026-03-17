# pythonhelper-toolkit

A Python package to analyze Python scripts automatically.

## Installation
```bash
pip install pythonhelper-toolkit
```

## Usage
```python
from pythonhelper import CodeAnalyzer

ca = CodeAnalyzer("my_script.py")

ca.count_functions()
ca.count_lines()
ca.find_imports()
ca.detect_comments()
ca.style_report()
ca.full_report()
```

## Features

* **`count_functions()`** — Count total functions defined in the script
* **`count_lines()`** — Total, non-blank, and blank line counts
* **`find_imports()`** — List all imported modules
* **`detect_comments()`** — Count single-line comments and docstrings
* **`style_report()`** — Basic PEP8 style checks (no extra dependencies)
* **`full_report()`** — Run all checks at once
