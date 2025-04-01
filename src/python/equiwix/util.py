import os
import subprocess
from datetime import date

from dateutil.parser import parse


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


class Date(date):
    def __new__(cls, *args):
        if len(args) == 1:
            d = args[0]

            if isinstance(d, int):
                d = str(d)

            if isinstance(d, str):
                d = parse(d, dayfirst=False).date()

            return super().__new__(cls, d.year, d.month, d.day)

        return super().__new__(cls, *args)


EQUIWIX_END_OF_TIME = Date(20991231)

# Index starts from price 100
EQUIWIX_OPENING_LEVEL = 100.0
