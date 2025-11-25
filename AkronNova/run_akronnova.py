#!/usr/bin/env python3
"""
Runner script for AkronNova Desktop AI Companion
"""

import sys
import os

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from main import main

if __name__ == "__main__":
    main()