"""Add parent directory to sys.path.

Importing this module allows the interpreter to find modules in the parent
directory.
"""

import sys
import os
sys.path.append("..")
