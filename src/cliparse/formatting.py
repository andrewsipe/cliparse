"""
Generic console formatting utilities.

Provides Rich-aware formatting with graceful fallback to plain text.
Font-agnostic and reusable across CLI projects.
"""

import importlib.util
import re
from typing import Optional


# Check for Rich availability
RICH_AVAILABLE: bool = importlib.util.find_spec("rich") is not None

if RICH_AVAILABLE:
    from rich.console import Console
    from rich.theme import Theme

    # Simple theme for generic CLI use
    _THEME = Theme(
        {
            "success": "success",
            "error": "red",
            "warning": "yellow",
            "info": "blue",
            "dim": "dim",
        }
    )

    # Module-level console singleton
    _console: Optional[Console] = None

    def get_console() -> Console:
        """Get or create Rich console instance."""
        global _console
        if _console is None:
            _console = Console(theme=_THEME)
        return _console
else:
    _console = None

    def get_console() -> None:
        """Rich not available."""
        return None


def emit(message: str, end: str = "\n") -> None:
    """
    Emit a message via Rich console if available, otherwise print().

    Args:
        message: Message to emit (may contain Rich markup)
        end: End character (default: newline)
    """
    if RICH_AVAILABLE and _console:
        get_console().print(message, end=end)
    else:
        # Strip Rich markup for plain text
        clean_message = re.sub(r"\[/?[^\]]+\]", "", message)
        print(clean_message, end=end)


def success(message: str) -> str:
    """
    Format success message.

    Args:
        message: Message text

    Returns:
        Formatted message (Rich markup if available)
    """
    if RICH_AVAILABLE:
        return f"[success]✓[/success] {message}"
    return f"✓ {message}"


def error(message: str) -> str:
    """
    Format error message.

    Args:
        message: Message text

    Returns:
        Formatted message (Rich markup if available)
    """
    if RICH_AVAILABLE:
        return f"[error]✗[/error] {message}"
    return f"✗ {message}"


def warning(message: str) -> str:
    """
    Format warning message.

    Args:
        message: Message text

    Returns:
        Formatted message (Rich markup if available)
    """
    if RICH_AVAILABLE:
        return f"[warning]⚠[/warning] {message}"
    return f"⚠ {message}"


def info(message: str) -> str:
    """
    Format info message.

    Args:
        message: Message text

    Returns:
        Formatted message (Rich markup if available)
    """
    if RICH_AVAILABLE:
        return f"[info]ℹ[/info] {message}"
    return f"ℹ {message}"


def status_message(label: str, message: str) -> str:
    """
    Format a status message with label.

    Args:
        label: Status label (e.g., "SUCCESS", "ERROR")
        message: Message text

    Returns:
        Formatted message
    """
    if RICH_AVAILABLE:
        # Use appropriate color based on label
        label_lower = label.lower()
        if "error" in label_lower or "fail" in label_lower:
            style = "error"
        elif "warn" in label_lower:
            style = "warning"
        elif "success" in label_lower or "ok" in label_lower:
            style = "success"
        else:
            style = "info"

        return f"[{style}]{label}[/{style}] {message}"
    return f"{label} {message}"


def print_success(message: str) -> None:
    """Print success message."""
    emit(success(message))


def print_error(message: str) -> None:
    """Print error message."""
    emit(error(message))


def print_warning(message: str) -> None:
    """Print warning message."""
    emit(warning(message))


def print_info(message: str) -> None:
    """Print info message."""
    emit(info(message))
