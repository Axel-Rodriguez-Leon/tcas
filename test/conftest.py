import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(ROOT_DIR, "src")

# Add both repo root and src/ to sys.path so tests can import using either
# `from tcas...` or `from src.tcas...`.
sys.path.insert(0, SRC_DIR)
sys.path.insert(0, ROOT_DIR)
