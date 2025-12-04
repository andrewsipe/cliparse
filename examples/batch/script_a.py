"""
Example script A - processes fonts.
"""

from cliparse import BaseParser, register_script


@register_script(
    name="process-fonts",
    description="Process font metadata",
    supports=["-R", "--recursive", "-v", "--verbose", "--dry-run", "--format"],
)
def create_parser():
    parser = BaseParser(description="Process font files")
    parser.add_argument("files", nargs="+", help="Font files to process")
    parser.add_argument("--format", choices=["otf", "ttf"], help="Font format filter")
    return parser


def main(args):
    """Main function for script A."""
    if args.verbose:
        print(f"[Script A] Processing {len(args.files)} fonts")
        if args.format:
            print(f"[Script A] Format filter: {args.format}")

    for file in args.files:
        if args.verbose:
            print(f"[Script A]   Processing: {file}")

        if not args.dry_run:
            # Do actual work
            pass

    if args.verbose:
        print("[Script A] Complete")


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    main(args)
