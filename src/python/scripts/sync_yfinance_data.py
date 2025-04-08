#!/usr/bin/env python3

import argparse

from equiwix.data_ingestion.yfinance_sync import (YFINANCE_START_OF_TIME,
                                                  YFinanceDataSync)
from equiwix.index_engine.yfinance_computer import (
    YFinanceIndexConstituentsComputer, YFinanceIndexLevelComputer)
from equiwix.log_utils import add_logging_args, configure_logging
from equiwix.util import Date


def getargs():
    actions = ['sync', 'compute_constituents', 'compute_levels']
    modes = ['incremental', 'historical']

    parser = argparse.ArgumentParser(
        description="Sync YFinance data and compute index constituents and levels using "
        "YFinance data."
    )

    parser.add_argument("date", type=Date, help="Date for which to sync the data.")

    parser.add_argument(
        "--action", type=str, choices=actions, required=True, help=f'Choose from {actions}.'
    )

    parser.add_argument(
        "--mode",
        type=str,
        choices=modes,
        default='incremental',
        help=f"Pass incremental for single day's sync and historical to sync from "
        f"{YFINANCE_START_OF_TIME} till passed date.",
    )

    add_logging_args(parser)

    return parser.parse_args()


def main():
    args = getargs()

    configure_logging(args.log_level)

    sync_start_date = None
    if args.mode == 'historical':
        sync_start_date = YFINANCE_START_OF_TIME

    if args.action == 'sync':
        YFinanceDataSync(run_date=args.date, sync_start_date=sync_start_date).sync()
    elif args.action == 'compute_constituents':
        YFinanceIndexConstituentsComputer(
            run_date=args.date, sync_start_date=sync_start_date
        ).sync()
    elif args.action == 'compute_levels':
        YFinanceIndexLevelComputer(run_date=args.date, sync_start_date=sync_start_date).sync()
    else:
        raise ValueError(f'Unknown action {args.action}')


if __name__ == "__main__":
    main()
