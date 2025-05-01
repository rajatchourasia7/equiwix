import argparse

from equiwix.log_utils import add_logging_args, configure_logging
from equiwix.ticker_univ import SP500TickerUniv, TickerUniv


def add_ticker_manually(tickers):
    TickerUniv().add(tickers)

def add_tickers_from_source(source):
    if source == "sp500":
        SP500TickerUniv().add()
    else:
        raise ValueError(f"Unsupported source: {source}")

def get_args():
    parser = argparse.ArgumentParser(description="Add tickers to a universe.")
    add_logging_args(parser)

    subparsers = parser.add_subparsers(dest="command", help="Sub-command help")

    # Subparser for adding a single ticker manually
    manual_parser = subparsers.add_parser(
        "add-tickers", help="Add tickers manually"
    )
    manual_parser.add_argument(
        "tickers", nargs="+", type=str, help="The tickers to add"
    )
    add_logging_args(manual_parser)

    # Subparser for adding tickers from a source
    source_parser = subparsers.add_parser(
        "add-from-source", help="Add tickers from a source"
    )
    source_parser.add_argument(
        "source",
        type=str,
        choices=["sp500"],
        help="The source of tickers (e.g., SP500)"
    )
    add_logging_args(source_parser)

    return parser.parse_args()


def main():
    args = get_args()
    configure_logging(args.log_level)

    # Handle subcommands
    if args.command == "add-tickers":
        add_ticker_manually(args.tickers)
    elif args.command == "add-from-source":
        add_tickers_from_source(args.source)

if __name__ == "__main__":
    main()