"""
Cliparse - Consistent argparse with smart flag pass-through.

Provides:

- BaseParser: argparse with standard flags included

- @register_script: Decorator for script registration

- Coordinator: Execute multiple scripts with flag filtering

- Formatting: Generic console formatting utilities

- Errors: Generic exception classes

- Logging: Generic logging setup
"""

from .parser import BaseParser, create_parser
from .registry import (
    register_script,
    Coordinator,
    ScriptRegistry,
    ScriptMetadata,
    ExecutionResult,
    BatchResults,
)
from .formatting import (
    RICH_AVAILABLE,
    get_console,
    emit,
    success,
    error,
    warning,
    info,
    status_message,
    print_success,
    print_error,
    print_warning,
    print_info,
)
from .errors import (
    CliparseError,
    ValidationError,
    ParseError,
    ConfigurationError,
    ExitCode,
    format_error,
)
from .logging import (
    Verbosity,
    VERBOSITY_TO_LEVEL,
    setup_logger,
    setup_logger_from_verbosity,
    get_logger,
)

__version__ = "0.1.0"

__all__ = [
    # Parser
    "BaseParser",
    "create_parser",
    # Registry
    "register_script",
    "Coordinator",
    "ScriptRegistry",
    "ScriptMetadata",
    # Results
    "ExecutionResult",
    "BatchResults",
    # Formatting
    "RICH_AVAILABLE",
    "get_console",
    "emit",
    "success",
    "error",
    "warning",
    "info",
    "status_message",
    "print_success",
    "print_error",
    "print_warning",
    "print_info",
    # Errors
    "CliparseError",
    "ValidationError",
    "ParseError",
    "ConfigurationError",
    "ExitCode",
    "format_error",
    # Logging
    "Verbosity",
    "VERBOSITY_TO_LEVEL",
    "setup_logger",
    "setup_logger_from_verbosity",
    "get_logger",
]
