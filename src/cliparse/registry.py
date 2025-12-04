"""
Script registry and coordination system for multi-script projects.
"""
import sys
import importlib
from typing import Dict, List, Optional, Callable, Any, Set
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ScriptMetadata:
    """Metadata for a registered script."""
    name: str
    description: str
    parser_factory: Callable
    supported_flags: Set[str]
    module_path: Optional[str] = None

    def supports_flag(self, flag: str) -> bool:
        """Check if this script supports a given flag."""
        return flag in self.supported_flags


class ScriptRegistry:
    """
    Central registry for scripts with metadata.

    Singleton pattern - all registrations go to the same registry.
    """
    _instance = None
    _scripts: Dict[str, ScriptMetadata] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def register(
        cls,
        name: str,
        description: str,
        parser_factory: Callable,
        supported_flags: List[str]
    ) -> None:
        """
        Register a script with metadata.

        Args:
            name: Unique script identifier
            description: Script description
            parser_factory: Function that returns configured parser
            supported_flags: List of flags this script accepts
        """
        metadata = ScriptMetadata(
            name=name,
            description=description,
            parser_factory=parser_factory,
            supported_flags=set(supported_flags)
        )
        cls._scripts[name] = metadata

    @classmethod
    def get(cls, name: str) -> Optional[ScriptMetadata]:
        """Get script metadata by name."""
        return cls._scripts.get(name)

    @classmethod
    def list_all(cls) -> List[str]:
        """List all registered script names."""
        return list(cls._scripts.keys())

    @classmethod
    def get_all(cls) -> Dict[str, ScriptMetadata]:
        """Get all registered scripts."""
        return cls._scripts.copy()

    @classmethod
    def clear(cls) -> None:
        """Clear all registered scripts (useful for testing)."""
        cls._scripts.clear()


def register_script(
    name: str,
    description: Optional[str] = None,
    supports: Optional[List[str]] = None
):
    """
    Decorator to register a script parser factory.

    Args:
        name: Unique script identifier
        description: Script description (defaults to parser description)
        supports: List of flags this script supports (e.g., ['-R', '--dry-run'])

    Example:
        @register_script(
            name='process-fonts',
            description='Process font files',
            supports=['-R', '--dry-run', '-v', '--format']
        )
        def create_parser():
            parser = BaseParser(description="Font processor")
            parser.add_argument('--format', choices=['otf', 'ttf'])
            return parser
    """
    def decorator(parser_factory: Callable):
        # Get description from parser if not provided
        desc = description
        if desc is None:
            parser = parser_factory()
            desc = parser.description or name

        # Register with the global registry
        ScriptRegistry.register(
            name=name,
            description=desc,
            parser_factory=parser_factory,
            supported_flags=supports or []
        )

        return parser_factory

    return decorator


@dataclass
class ExecutionResult:
    """Result from executing a script."""
    script_name: str
    success: bool
    exit_code: int = 0
    error_message: Optional[str] = None


@dataclass
class BatchResults:
    """Aggregated results from batch execution."""
    results: List[ExecutionResult] = field(default_factory=list)

    @property
    def all_success(self) -> bool:
        """Check if all scripts succeeded."""
        return all(r.success for r in self.results)

    @property
    def failed_count(self) -> int:
        """Count of failed scripts."""
        return sum(1 for r in self.results if not r.success)

    @property
    def success_count(self) -> int:
        """Count of successful scripts."""
        return sum(1 for r in self.results if r.success)

    def summary(self) -> str:
        """Generate a summary string."""
        total = len(self.results)
        success = self.success_count
        failed = self.failed_count

        lines = [f"Executed {total} script(s):"]
        lines.append(f"  ✓ Success: {success}")

        if failed > 0:
            lines.append(f"  ✗ Failed: {failed}")
            for result in self.results:
                if not result.success:
                    lines.append(f"    - {result.script_name}: {result.error_message}")

        return "\n".join(lines)


class Coordinator:
    """
    Coordinates execution of multiple scripts with intelligent flag filtering.
    """

    def __init__(self):
        self.registry = ScriptRegistry()

    def load_scripts(self, module_paths: List[str]) -> None:
        """
        Load scripts from module paths.

        Scripts must use @register_script decorator to be discovered.

        Args:
            module_paths: List of module paths (e.g., ['my_package.script_a'])
        """
        for module_path in module_paths:
            try:
                importlib.import_module(module_path)
            except ImportError as e:
                print(f"Warning: Could not import {module_path}: {e}", file=sys.stderr)

    def load_scripts_from_directory(self, directory: str, pattern: str = "*Replacer.py") -> None:
        """
        Load scripts from a directory by importing Python files.

        Args:
            directory: Directory path to search
            pattern: Glob pattern for script files
        """
        dir_path = Path(directory)

        for script_file in dir_path.glob(pattern):
            if script_file.stem.startswith('_'):
                continue

            # Import the module
            module_name = script_file.stem
            try:
                # Add directory to path temporarily
                sys.path.insert(0, str(dir_path))
                importlib.import_module(module_name)
                sys.path.pop(0)
            except Exception as e:
                print(f"Warning: Could not load {script_file}: {e}", file=sys.stderr)

    def filter_args_for_script(
        self,
        script_name: str,
        all_args: List[str]
    ) -> List[str]:
        """
        Filter command-line arguments for a specific script.

        Only passes flags that the script declares it supports.

        Args:
            script_name: Name of the script
            all_args: Full argument list from sys.argv

        Returns:
            Filtered argument list for this script
        """
        script = self.registry.get(script_name)
        if not script:
            raise ValueError(f"Unknown script: {script_name}")

        filtered = []
        skip_next = False

        for i, arg in enumerate(all_args):
            if skip_next:
                skip_next = False
                continue

            # Check if this is a flag
            if arg.startswith('-'):
                # Handle --flag=value format
                if '=' in arg:
                    flag = arg.split('=')[0]
                    if script.supports_flag(flag):
                        filtered.append(arg)
                # Handle -flag value format
                else:
                    if script.supports_flag(arg):
                        filtered.append(arg)
                        # Check if next arg is a value (not a flag)
                        if i + 1 < len(all_args) and not all_args[i + 1].startswith('-'):
                            filtered.append(all_args[i + 1])
                            skip_next = True
                    else:
                        # Flag not supported - skip it and its value if present
                        if i + 1 < len(all_args) and not all_args[i + 1].startswith('-'):
                            skip_next = True
            else:
                # Positional argument - always include
                filtered.append(arg)

        return filtered

    def run(
        self,
        scripts: List[str],
        args: Optional[List[str]] = None
    ) -> BatchResults:
        """
        Run multiple scripts with filtered arguments.

        Args:
            scripts: List of script names to run
            args: Command-line arguments (defaults to sys.argv[1:])

        Returns:
            BatchResults with execution results
        """
        if args is None:
            args = sys.argv[1:]

        results = BatchResults()

        for script_name in scripts:
            result = self._run_single_script(script_name, args)
            results.results.append(result)

        return results

    def _run_single_script(
        self,
        script_name: str,
        all_args: List[str]
    ) -> ExecutionResult:
        """Run a single script with filtered arguments."""
        script = self.registry.get(script_name)

        if not script:
            return ExecutionResult(
                script_name=script_name,
                success=False,
                exit_code=1,
                error_message=f"Script not found: {script_name}"
            )

        try:
            # Filter arguments for this script
            filtered_args = self.filter_args_for_script(script_name, all_args)

            # Create parser and parse arguments
            parser = script.parser_factory()
            parsed_args = parser.parse_args(filtered_args)

            # Success - script would run with these args
            # (In real usage, you'd call the script's main function here)
            return ExecutionResult(
                script_name=script_name,
                success=True,
                exit_code=0
            )

        except SystemExit as e:
            return ExecutionResult(
                script_name=script_name,
                success=False,
                exit_code=e.code,
                error_message="Argument parsing failed"
            )
        except Exception as e:
            return ExecutionResult(
                script_name=script_name,
                success=False,
                exit_code=1,
                error_message=str(e)
            )

    def list_scripts(self) -> List[str]:
        """List all registered script names."""
        return self.registry.list_all()

    def get_script_info(self, script_name: str) -> Optional[ScriptMetadata]:
        """Get metadata for a script."""
        return self.registry.get(script_name)

