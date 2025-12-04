# Cliparse

Consistent argparse with smart flag pass-through for multi-script Python projects.

## Features

- **BaseParser**: argparse with standard flags (`-R`, `--dry-run`, `-y`, `-v`) built-in
- **@register_script**: Decorator for scripts to declare their capabilities
- **Coordinator**: Automatically filters and routes flags to appropriate scripts

## Installation

### Development Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/cliparse.git
cd cliparse

# Install in development mode
pip install -e .

# Or with dev dependencies
pip install -e ".[dev]"
```

### From PyPI (when published)

```bash
pip install cliparse
```

## Quick Start

### Single Script

```python
from cliparse import BaseParser

parser = BaseParser(description="Process files")
parser.add_argument('files', nargs='+')
parser.add_argument('--format', choices=['json', 'xml'])

args = parser.parse_args()

# Standard flags available automatically
if args.verbose:
    print(f"Processing {len(args.files)} files")

if not args.dry_run:
    # Do actual work
    pass
```

### Multi-Script Project

**Script A (script_a.py):**

```python
from cliparse import BaseParser, register_script

@register_script(
    name='process',
    supports=['-R', '--dry-run', '-v', '--format']
)
def create_parser():
    parser = BaseParser(description="Process files")
    parser.add_argument('files', nargs='+')
    parser.add_argument('--format')
    return parser
```

**Script B (script_b.py):**

```python
from cliparse import BaseParser, register_script

@register_script(
    name='validate',
    supports=['-R', '-v', '--strict']
)
def create_parser():
    parser = BaseParser(description="Validate files")
    parser.add_argument('files', nargs='+')
    parser.add_argument('--strict', action='store_true')
    return parser
```

**Runner (runner.py):**

```python
from cliparse import Coordinator

coordinator = Coordinator()
coordinator.load_scripts(['script_a', 'script_b'])

results = coordinator.run(
    scripts=['process', 'validate'],
    args=['files/*.txt', '-R', '-v', '--format', 'json', '--strict']
)

# Automatically filters flags:
# - 'process' gets: files/*.txt -R -v --format json
# - 'validate' gets: files/*.txt -R -v --strict

print(results.summary())
```

## Standard Flags

BaseParser includes these flags by default:

- `-h, --help`: Show help message
- `-R, --recursive`: Process directories recursively
- `-n, --dry-run`: Preview changes without executing
- `-y, --yes`: Skip confirmation prompts
- `-v, --verbose`: Enable verbose output

### Customizing Standard Flags

```python
# Include only specific flags
parser = BaseParser(
    description="My script",
    standard_flags=['verbose', 'dry-run']
)

# Exclude all standard flags
parser = BaseParser(
    description="My script",
    standard_flags=[]
)
```

## API Reference

### BaseParser

```python
BaseParser(
    description: str,
    epilog: Optional[str] = None,
    standard_flags: Optional[List[str]] = None,
    use_rich: bool = False,
    **kwargs
)
```

### @register_script

```python
@register_script(
    name: str,
    description: Optional[str] = None,
    supports: Optional[List[str]] = None
)
```

### Coordinator

```python
coordinator = Coordinator()
coordinator.load_scripts(module_paths: List[str])
results = coordinator.run(scripts: List[str], args: List[str])
```

## Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=cliparse --cov-report=html

# Run specific test
pytest tests/test_parser.py::test_base_parser_includes_standard_flags
```

## Examples

See the `examples/` directory for complete examples:

- `simple.py` - Basic single script usage
- `batch/` - Multi-script project with runner

## License

MIT License - see LICENSE file for details.

