"""Run script that sets up the Python path correctly."""

import os
import sys
from pathlib import Path

# Add the src directory to the Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Import and run the main function
from main import main

if __name__ == "__main__":
    main()
