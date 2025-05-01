import argparse

from equiwix.index_engine.divisor import IndexLevelDivisorDAO
from equiwix.log_utils import add_logging_args, configure_logging


def get_args():
    parser = argparse.ArgumentParser(description="Update the divisor for a given source.")
    parser.add_argument("--source", required=True, help="The source identifier.")
    parser.add_argument("--divisor", required=True, type=float, help="The divisor value.")
    parser.add_argument("--start_date", required=True, help="The start date for the divisor.")

    add_logging_args(parser)

    return parser.parse_args()


def main():
    args = get_args()
    configure_logging(args.log_level)

    dao = IndexLevelDivisorDAO(args.source)
    dao.set(args.divisor, args.start_date)


if __name__ == "__main__":
    main()
