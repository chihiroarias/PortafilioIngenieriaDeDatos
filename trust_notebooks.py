"""
Script to trust all Jupyter notebooks in the project
This allows interactive outputs (maps, widgets) to render in VS Code
"""

import subprocess
import sys
from pathlib import Path

# Find all notebook files
notebooks_dir = Path("docs/Practicos")
notebooks = list(notebooks_dir.glob("*.ipynb"))

print(f"Found {len(notebooks)} notebooks to trust")
print("=" * 60)

for notebook in notebooks:
    print(f"Trusting: {notebook.name}")
    try:
        result = subprocess.run(
            ["jupyter", "trust", str(notebook)],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"  ✅ {result.stdout.strip()}")
    except subprocess.CalledProcessError as e:
        print(f"  ❌ Error: {e.stderr}")
    except FileNotFoundError:
        print(f"  ❌ jupyter command not found. Install with: pip install jupyter")
        sys.exit(1)

print("=" * 60)
print("✅ All notebooks trusted!")
print("\nNow you can:")
print("1. Open notebooks in VS Code")
print("2. Execute all cells (Ctrl+Shift+P → 'Execute All Cells')")
print("3. Save (Ctrl+S)")
print("4. Run: mkdocs build")
