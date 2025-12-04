"""
Generic logging configuration for CLI applications.

Provides simple logging setup with verbosity control.
Font-agnostic and reusable across CLI projects.
"""
import logging
from enum import IntEnum
from typing import Optional


class Verbosity(IntEnum):
    """Verbosity levels following common CLI conventions."""
    QUIET = 0      # Minimal output, errors only
    BRIEF = 1      # Normal user interface messages (default)
    VERBOSE = 2    # Descriptive, thorough descriptions
    DEBUG = 3      # Internal execution steps, developer-focused


# Map verbosity to logging levels
VERBOSITY_TO_LEVEL = {
    Verbosity.QUIET: logging.ERROR,
    Verbosity.BRIEF: logging.INFO,
    Verbosity.VERBOSE: logging.INFO,
    Verbosity.DEBUG: logging.DEBUG,
}


def setup_logger(
    name: str,
    verbose: bool = False,
    quiet: bool = False,
    level: Optional[int] = None
) -> logging.Logger:
    """
    Setup a basic logger with console output.

    Args:
        name: Logger name (typically __name__)
        verbose: Enable verbose (DEBUG) output
        quiet: Enable quiet (ERROR only) output
        level: Explicit logging level (overrides verbose/quiet)

    Returns:
        Configured logger

    Example:
        logger = setup_logger(__name__, verbose=True)
        logger.info("Processing files...")
        logger.debug("Detailed debug info")
    """
    logger = logging.getLogger(name)

    # Determine logging level
    if level is not None:
        log_level = level
    elif quiet:
        log_level = logging.ERROR
    elif verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    logger.setLevel(log_level)

    # Only add handler if one doesn't exist
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setLevel(log_level)

        # Simple formatter - just the message
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)

        logger.addHandler(handler)

    return logger


def setup_logger_from_verbosity(
    name: str,
    verbosity: Verbosity = Verbosity.BRIEF
) -> logging.Logger:
    """
    Setup logger from Verbosity enum.

    Args:
        name: Logger name
        verbosity: Verbosity level

    Returns:
        Configured logger
    """
    level = VERBOSITY_TO_LEVEL.get(verbosity, logging.INFO)
    return setup_logger(name, level=level)


def get_logger(name: str) -> logging.Logger:
    """
    Get or create a logger with default settings.

    Args:
        name: Logger name

    Returns:
        Logger instance
    """
    return logging.getLogger(name)

