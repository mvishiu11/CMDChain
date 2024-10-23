"""
This module defines standard linting process.
"""

import subprocess
import sys


def main():
    """
    Main linting function that runs black, pylint, and mypy on the project.
    """
    tools = ["black .", "pylint .", "mypy ."]

    for tool in tools:
        try:
            subprocess.run(tool, shell=True, check=True)
        except subprocess.CalledProcessError:
            print(f"Failed: {tool}")
            sys.exit(1)


if __name__ == "__main__":
    main()
