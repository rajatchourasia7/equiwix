"""
This script is used to create the database and tables for the Equiwix application.
"""

from equiwix.db.creation import create_db_and_tables


def main():
    # Call the utility function to create the database and tables
    create_db_and_tables()

if __name__ == "__main__":
    main()
