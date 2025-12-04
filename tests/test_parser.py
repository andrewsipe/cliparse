"""Tests for BaseParser."""
import pytest
from cliparse.parser import BaseParser


def test_base_parser_includes_standard_flags():
    """Test that standard flags are included by default."""
    parser = BaseParser(description="Test parser")

    # Parse with standard flags
    args = parser.parse_args(['-R', '--dry-run', '-y', '-v'])

    assert args.recursive is True
    assert args.dry_run is True
    assert args.yes is True
    assert args.verbose is True


def test_base_parser_selective_flags():
    """Test including only specific standard flags."""
    parser = BaseParser(
        description="Test parser",
        standard_flags=['verbose', 'dry-run']
    )

    args = parser.parse_args(['--verbose'])
    assert args.verbose is True

    # Should not have recursive flag
    assert not hasattr(args, 'recursive')


def test_base_parser_with_custom_args():
    """Test adding custom arguments."""
    parser = BaseParser(description="Test parser")
    parser.add_argument('--custom', type=int, default=42)

    args = parser.parse_args(['--custom', '100', '-v'])

    assert args.custom == 100
    assert args.verbose is True


def test_base_parser_no_standard_flags():
    """Test parser with no standard flags."""
    parser = BaseParser(
        description="Test parser",
        standard_flags=[]
    )

    args = parser.parse_args([])

    # Should not have any standard flags
    assert not hasattr(args, 'verbose')
    assert not hasattr(args, 'recursive')


def test_invalid_standard_flag():
    """Test that invalid flag names raise error."""
    with pytest.raises(ValueError, match="Unknown standard flag"):
        BaseParser(
            description="Test parser",
            standard_flags=['invalid_flag']
        )


def test_get_standard_flags():
    """Test retrieving list of standard flags."""
    parser = BaseParser(
        description="Test",
        standard_flags=['verbose', 'dry-run']
    )

    flags = parser.get_standard_flags()
    assert flags == ['verbose', 'dry-run']

