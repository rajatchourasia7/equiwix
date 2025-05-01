import subprocess
import sys
from equiwix.util import get_equiwix_home

def main():
    # Point to the real source file in the project
    script_path = f'{get_equiwix_home()}/src/python/scripts/run_dashboard.py'
    print('Launching dashboard from', script_path)

    subprocess.run(
        ["streamlit", "run", str(script_path)] + sys.argv[1:],
        check=True
    )
