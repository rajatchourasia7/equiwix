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
            "equiwix-sync_yfinance_data = scripts.sync_yfinance_data:main",
            "equiwix-launch_dashboard = scripts.launch_dashboard:main",
        ],
    },
    include_package_data=True,
)
