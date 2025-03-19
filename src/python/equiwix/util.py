import os
import subprocess


def get_equiwix_home():
    """Return the root directory of this repo."""
    try:
        # Run Git command to get repo root
        output = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"],
            stderr=subprocess.STDOUT,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__)),  # Start from current file's dir
        ).strip()
        return output
    except subprocess.CalledProcessError:
        raise RuntimeError("Not inside a Git repository or Git is not installed")
