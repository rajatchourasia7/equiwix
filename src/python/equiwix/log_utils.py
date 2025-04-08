import logging


def add_logging_args(parser):
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level (default: INFO)"
    )


def configure_logging(log_level_str):
    logging.basicConfig(
        level=getattr(logging, log_level_str.upper()),
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
