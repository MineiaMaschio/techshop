"""Pytest configuration file.

This module configures pytest to properly resolve imports from the src directory.
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path.parent))
