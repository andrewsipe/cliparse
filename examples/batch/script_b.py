"""
Example script B - validates fonts.
"""
from cliparse import BaseParser, register_script


@register_script(
    name='validate-fonts',
    description='Validate font files',
    supports=['-R', '--recursive', '-v', '--verbose', '--strict']
)
def create_parser():
    parser = BaseParser(description="Validate font files")
    parser.add_argument('files', nargs='+', help='Font files to validate')
    parser.add_argument('--strict', action='store_true',
                       help='Enable strict validation')
    return parser


def main(args):
    """Main function for script B."""
    if args.verbose:
        print(f"[Script B] Validating {len(args.files)} fonts")
        if args.strict:
            print("[Script B] Strict mode enabled")

    for file in args.files:
        if args.verbose:
            print(f"[Script B]   Validating: {file}")

        # Do validation
        pass

    if args.verbose:
        print("[Script B] Validation complete")


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    main(args)

