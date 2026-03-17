import ast
import re


class CodeAnalyzer:

    def __init__(self, filepath):
        self.filepath = filepath
        with open(filepath, "r", encoding="utf-8") as f:
            self.source = f.read()
        self.lines = self.source.splitlines()

    def count_functions(self):
        """Count total number of functions defined in the script."""
        try:
            tree = ast.parse(self.source)
            count = sum(1 for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)))
            print(f"Functions found: {count}")
            return count
        except SyntaxError as e:
            print(f"Syntax error while parsing: {e}")
            return 0

    def count_lines(self):
        """Count total lines, non-empty lines, and blank lines."""
        total = len(self.lines)
        blank = sum(1 for line in self.lines if line.strip() == "")
        non_blank = total - blank
        print(f"Total lines     : {total}")
        print(f"Non-blank lines : {non_blank}")
        print(f"Blank lines     : {blank}")
        return {"total": total, "non_blank": non_blank, "blank": blank}

    def find_imports(self):
        """List all imported modules in the script."""
        try:
            tree = ast.parse(self.source)
            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    for alias in node.names:
                        imports.append(f"{module}.{alias.name}")
            if imports:
                print(f"Imports found ({len(imports)}):")
                for imp in imports:
                    print(f"  - {imp}")
            else:
                print("No imports found.")
            return imports
        except SyntaxError as e:
            print(f"Syntax error while parsing: {e}")
            return []

    def detect_comments(self):
        """Count single-line and multi-line (docstring) comments."""
        single_line = sum(1 for line in self.lines if line.strip().startswith("#"))
        try:
            tree = ast.parse(self.source)
            docstrings = 0
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module)):
                    if ast.get_docstring(node):
                        docstrings += 1
        except SyntaxError:
            docstrings = 0

        print(f"Single-line comments (#) : {single_line}")
        print(f"Docstrings               : {docstrings}")
        return {"single_line": single_line, "docstrings": docstrings}

    def style_report(self):
        """Basic PEP8 style check without external dependencies."""
        issues = []

        for i, line in enumerate(self.lines, start=1):
            # Line too long (PEP8 limit: 79 characters)
            if len(line) > 79:
                issues.append(f"Line {i}: Line too long ({len(line)} characters, max 79)")

            # Trailing whitespace
            if line != line.rstrip():
                issues.append(f"Line {i}: Trailing whitespace")

            # Tab instead of spaces
            if "\t" in line:
                issues.append(f"Line {i}: Tab character found (use 4 spaces instead)")

            # Missing space after comma
            if re.search(r",\S", line) and not line.strip().startswith("#"):
                issues.append(f"Line {i}: Missing space after comma")

            # Comparison using == with None or True/False
            if re.search(r"==\s*None|==\s*True|==\s*False", line):
                issues.append(f"Line {i}: Use 'is' instead of '==' when comparing with None/True/False")

            # Missing space around operators = + - * /
            if re.search(r"\w=[^=]", line) and "==" not in line and not line.strip().startswith("#"):
                if not re.search(r"\w\s=\s", line) and not re.search(r"def |class |import ", line):
                    issues.append(f"Line {i}: Missing space around '=' operator")

        if issues:
            print(f"Style issues found ({len(issues)}):")
            for issue in issues:
                print(f"  {issue}")
        else:
            print("No style issues found. Code looks clean!")

        return issues

    def full_report(self):
        """Run all checks and display a complete report."""
        print("=" * 50)
        print("PYTHON CODE ANALYSIS REPORT")
        print("=" * 50)
        print(f"File: {self.filepath}")
        print("-" * 50)
        print("LINE COUNT")
        self.count_lines()
        print("-" * 50)
        print("FUNCTIONS")
        self.count_functions()
        print("-" * 50)
        print("IMPORTS")
        self.find_imports()
        print("-" * 50)
        print("COMMENTS")
        self.detect_comments()
        print("-" * 50)
        print("STYLE REPORT")
        self.style_report()
        print("=" * 50)
