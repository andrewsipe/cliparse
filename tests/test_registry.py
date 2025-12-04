"""Tests for registry system."""

import pytest
from cliparse.parser import BaseParser
from cliparse.registry import (
    ScriptRegistry,
    register_script,
    Coordinator,
    ExecutionResult,
    BatchResults,
)


@pytest.fixture(autouse=True)
def clear_registry():
    """Clear registry before each test."""
    ScriptRegistry.clear()
    yield
    ScriptRegistry.clear()


def test_register_script():
    """Test script registration."""

    @register_script(
        name="test-script", description="Test script", supports=["-v", "--custom"]
    )
    def create_parser():
        parser = BaseParser(description="Test")
        parser.add_argument("--custom")
        return parser

    # Check registration
    registry = ScriptRegistry()
    script = registry.get("test-script")

    assert script is not None
    assert script.name == "test-script"
    assert script.description == "Test script"
    assert "-v" in script.supported_flags
    assert "--custom" in script.supported_flags


def test_registry_list_all():
    """Test listing all scripts."""

    @register_script(name="script-a", supports=[])
    def create_parser_a():
        return BaseParser(description="Script A")

    @register_script(name="script-b", supports=[])
    def create_parser_b():
        return BaseParser(description="Script B")

    registry = ScriptRegistry()
    scripts = registry.list_all()

    assert "script-a" in scripts
    assert "script-b" in scripts


def test_coordinator_filter_args():
    """Test argument filtering for specific scripts."""

    @register_script(name="test-script", supports=["-v", "--verbose", "--custom"])
    def create_parser():
        parser = BaseParser(description="Test", standard_flags=["verbose"])
        parser.add_argument("--custom", type=int)
        return parser

    coordinator = Coordinator()

    # Filter args - should only keep supported flags
    all_args = ["file.txt", "-v", "--custom", "42", "--unsupported", "value"]
    filtered = coordinator.filter_args_for_script("test-script", all_args)

    assert "file.txt" in filtered
    assert "-v" in filtered
    assert "--custom" in filtered
    assert "42" in filtered
    assert "--unsupported" not in filtered
    assert "value" not in filtered  # Value for unsupported flag


def test_coordinator_run_scripts():
    """Test running multiple scripts."""

    @register_script(name="script-a", supports=["-v"])
    def create_parser_a():
        parser = BaseParser(description="Script A", standard_flags=["verbose"])
        parser.add_argument("files", nargs="+")
        return parser

    @register_script(name="script-b", supports=["--custom"])
    def create_parser_b():
        parser = BaseParser(description="Script B", standard_flags=[])
        parser.add_argument("files", nargs="+")
        parser.add_argument("--custom")
        return parser

    coordinator = Coordinator()

    results = coordinator.run(
        scripts=["script-a", "script-b"], args=["file.txt", "-v", "--custom", "value"]
    )

    assert len(results.results) == 2
    assert results.all_success
    assert results.success_count == 2
    assert results.failed_count == 0


def test_batch_results_summary():
    """Test batch results summary generation."""
    results = BatchResults()

    results.results.append(ExecutionResult("script-a", success=True))
    results.results.append(
        ExecutionResult("script-b", success=False, error_message="Failed to parse")
    )

    summary = results.summary()

    assert "Executed 2 script(s)" in summary
    assert "Success: 1" in summary
    assert "Failed: 1" in summary
    assert "script-b" in summary


def test_coordinator_unknown_script():
    """Test handling of unknown script."""
    coordinator = Coordinator()

    results = coordinator.run(scripts=["unknown-script"], args=["file.txt"])

    assert not results.all_success
    assert results.failed_count == 1
    assert "not found" in results.results[0].error_message
