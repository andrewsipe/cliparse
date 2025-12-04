"""
Generic exception classes for CLI parsing and validation.

Provides structured error handling with exit codes and error formatting.
Font-agnostic and reusable across CLI projects.
"""
import sys
import traceback


# Exit code constants (following Unix conventions)
class ExitCode:
    """Standard exit codes for CLI applications."""
    SUCCESS = 0
    ERROR = 1
    USAGE_ERROR = 2  # Invalid arguments/usage


class CliparseError(Exception):
    """Base exception for cliparse errors."""

    def __init__(
        self,
        message: str,
        exit_code: int = ExitCode.ERROR,
        show_traceback: bool = False
    ):
        """
        Initialize error.

        Args:
            message: Error message
            exit_code: Exit code to use (default: 1)
            show_traceback: Whether to show traceback on exit
        """
        super().__init__(message)
        self.message = message
        self.exit_code = exit_code
        self.show_traceback = show_traceback

    def exit(self) -> None:
        """
        Exit with appropriate code and optional traceback.

        This is a convenience method for handling errors in CLI scripts.
        """
        if self.show_traceback:
            traceback.print_exc()
        sys.exit(self.exit_code)


class ValidationError(CliparseError):
    """Validation failed (e.g., invalid input, constraint violation)."""

    def __init__(self, message: str, show_traceback: bool = False):
        super().__init__(message, exit_code=ExitCode.ERROR, show_traceback=show_traceback)


class ParseError(CliparseError):
    """Argument parsing failed (e.g., invalid flag, missing required arg)."""

    def __init__(self, message: str, show_traceback: bool = False):
        super().__init__(message, exit_code=ExitCode.USAGE_ERROR, show_traceback=show_traceback)


class ConfigurationError(CliparseError):
    """Configuration error (e.g., invalid settings, missing config)."""

    def __init__(self, message: str, show_traceback: bool = False):
        super().__init__(message, exit_code=ExitCode.ERROR, show_traceback=show_traceback)


def format_error(exception: Exception, include_traceback: bool = False) -> str:
    """
    Format an exception for display.

    Args:
        exception: Exception to format
        include_traceback: Whether to include full traceback

    Returns:
        Formatted error message
    """
    message = str(exception)
    if include_traceback:
        tb = "".join(traceback.format_exception(type(exception), exception, exception.__traceback__))
        return f"{message}\n\n{tb}"
    return message

