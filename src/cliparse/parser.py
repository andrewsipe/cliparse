"""
BaseParser - Argparse with standard flags built-in.
"""

import argparse
import sys
from typing import Optional, List


class BaseParser(argparse.ArgumentParser):
    """
    Extended ArgumentParser with common flags included by default.

    Standard flags:
        -h, --help: Show help message
        -r, --recursive: Process directories recursively
        -n, --dry-run: Preview changes without executing
        -y, --yes: Skip confirmation prompts
        -v, --verbose: Enable verbose output

    Args:
        description: Program description
        epilog: Text after help
        standard_flags: List of flags to include. Options:
            'recursive', 'dry-run', 'yes', 'verbose'
            Default: all of them
        **kwargs: Additional arguments passed to ArgumentParser

    Example:
        parser = BaseParser(description="Process files")
        parser.add_argument('files', nargs='+')
        parser.add_argument('--custom', help='Custom option')
        args = parser.parse_args()
    """

    # Standard flag definitions
    STANDARD_FLAGS = {
        "recursive": {
            "flags": ["-R", "--recursive"],
            "action": "store_true",
            "help": "Process directories recursively",
        },
        "dry-run": {
            "flags": ["-n", "--dry-run"],
            "action": "store_true",
            "help": "Show what would be done without making changes",
        },
        "yes": {
            "flags": ["-y", "--yes"],
            "action": "store_true",
            "help": "Automatically answer yes to all prompts",
        },
        "verbose": {
            "flags": ["-v", "--verbose"],
            "action": "store_true",
            "help": "Enable verbose output",
        },
    }

    def __init__(
        self,
        description: Optional[str] = None,
        epilog: Optional[str] = None,
        standard_flags: Optional[List[str]] = None,
        **kwargs,
    ):
        # Determine which standard flags to include
        if standard_flags is None:
            # Include all by default
            standard_flags = list(self.STANDARD_FLAGS.keys())

        # Initialize parent ArgumentParser
        super().__init__(description=description, epilog=epilog, **kwargs)

        # Add standard flags
        self._add_standard_flags(standard_flags)

        # Store which standard flags were added
        self._standard_flags = standard_flags

    def _add_standard_flags(self, flags: List[str]) -> None:
        """Add standard flags to the parser."""
        for flag_name in flags:
            if flag_name not in self.STANDARD_FLAGS:
                raise ValueError(
                    f"Unknown standard flag: {flag_name}. "
                    f"Available: {list(self.STANDARD_FLAGS.keys())}"
                )

            flag_def = self.STANDARD_FLAGS[flag_name]
            self.add_argument(
                *flag_def["flags"], action=flag_def["action"], help=flag_def["help"]
            )

    def get_standard_flags(self) -> List[str]:
        """Return list of standard flags included in this parser."""
        return self._standard_flags.copy()

    def parse_args(self, args=None, namespace=None):
        """
        Parse arguments with enhanced error handling.

        Exits with code 2 on error (standard argparse behavior).
        """
        try:
            return super().parse_args(args, namespace)
        except SystemExit as e:
            # Re-raise with same exit code
            sys.exit(e.code)


# Convenience function for quick parser creation
def create_parser(
    description: str, standard_flags: Optional[List[str]] = None, **kwargs
) -> BaseParser:
    """
    Convenience function to create a BaseParser.

    Args:
        description: Program description
        standard_flags: List of standard flags to include
        **kwargs: Additional arguments for BaseParser

    Returns:
        Configured BaseParser instance

    Example:
        parser = create_parser("Process files", standard_flags=['verbose', 'dry-run'])
        parser.add_argument('files', nargs='+')
    """
    return BaseParser(description=description, standard_flags=standard_flags, **kwargs)
