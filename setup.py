from setuptools import setup, find_packages

setup(
    name="equiwix",
    version="0.1",
    packages=find_packages(where="src/python"),
    package_dir={"": "src/python"},
    install_requires=[
        "pandas",
        "python-dateutil",
        "sqlalchemy",
        "yfinance",
        "plotly",
        "streamlit",
        "pandas_market_calendars",
    ],
    entry_points={
        "console_scripts": [
            "equiwix-run_dashboard = scripts.run_dashboard:main",
            "equiwix-sync_yfinance_data = scripts.sync_yfinance_data:main",
        ],
    },
)
