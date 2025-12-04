"""
Batch runner example - runs multiple scripts with flag filtering.
"""
import sys
from cliparse import BaseParser, Coordinator


def main():
    # Parse batch-level arguments
    parser = BaseParser(
        description="Batch font processor - runs multiple scripts",
        epilog="Example: python runner.py --scripts all fonts/*.ttf -R -v"
    )

    parser.add_argument('--scripts', default='all',
                       help='Comma-separated script names or "all"')
    parser.add_argument('--list', action='store_true',
                       help='List available scripts and exit')

    # Parse known args, keep the rest for scripts
    args, remaining = parser.parse_known_args()

    # Create coordinator and load scripts
    coordinator = Coordinator()
    coordinator.load_scripts([
        'script_a',
        'script_b'
    ])

    # List scripts if requested
    if args.list:
        print("Available scripts:")
        for name in coordinator.list_scripts():
            info = coordinator.get_script_info(name)
            print(f"  {name}: {info.description}")
            print(f"    Supports: {', '.join(sorted(info.supported_flags))}")
        return

    # Determine which scripts to run
    if args.scripts == 'all':
        script_names = coordinator.list_scripts()
    else:
        script_names = [s.strip() for s in args.scripts.split(',')]

    if args.verbose:
        print(f"Running scripts: {', '.join(script_names)}")
        print(f"With arguments: {' '.join(remaining)}")
        print()

    # Execute scripts
    results = coordinator.run(
        scripts=script_names,
        args=remaining
    )

    # Print results
    print()
    print(results.summary())

    # Exit with appropriate code
    sys.exit(0 if results.all_success else 1)


if __name__ == '__main__':
    main()

