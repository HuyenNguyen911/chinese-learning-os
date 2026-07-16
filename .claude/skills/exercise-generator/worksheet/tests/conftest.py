import sys
import pathlib

# Make build_worksheet.py importable from the tests without packaging.
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
