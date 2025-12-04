"""
Simple example of using BaseParser.
"""

from cliparse import BaseParser


def main():
    parser = BaseParser(
        description="Process files with standard options",
        epilog="Example: python simple.py files/*.txt -R --dry-run",
    )

    # Add custom arguments
    parser.add_argument("files", nargs="+", help="Files to process")
    parser.add_argument(
        "--format", choices=["json", "xml"], default="json", help="Output format"
    )

    args = parser.parse_args()

    # Use standard flags
    if args.verbose:
        print(f"Processing {len(args.files)} files")
        print(f"Format: {args.format}")
        print(f"Recursive: {args.recursive}")
        print(f"Dry run: {args.dry_run}")

    # Process files
    for file in args.files:
        if args.verbose:
            print(f"  Processing: {file}")

        if not args.dry_run:
            # Do actual work here
            pass

    if args.dry_run:
        print("Dry run complete - no changes made")
    else:
        print("Processing complete")


if __name__ == "__main__":
    main()
