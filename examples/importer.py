"""Add parent directory to sys.path.

Importing this module allows the interpreter to find modules in the parent
directory.
"""

import sys
import os
sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..')))
