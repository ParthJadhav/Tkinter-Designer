"""Tkinter Designer command-line interface."""

import argparse
import json
import logging
import os
from pathlib import Path
import sys

from tkdesigner import __version__
from tkdesigner.designer import Designer
from tkdesigner.utils import parse_figma_url


LOGGER = logging.getLogger("tkdesigner")
TRUE_VALUES = {"1", "true", "yes", "on"}
FALSE_VALUES = {"", "0", "false", "no", "off"}


def environment_flag(name: str, default=False) -> bool:
    """Parse a human-friendly environment flag without crashing at import."""
    value = os.getenv(name)
    if value is None:
        return default
    normalized = value.strip().lower()
    if normalized in TRUE_VALUES:
        return True
    if normalized in FALSE_VALUES:
        return False
    LOGGER.warning(
        "Ignoring invalid %s=%r; use true/false or 1/0.", name, value)
    return default


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tkdesigner",
        description="Inspect Figma designs and generate maintainable Tkinter projects.",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument(
        "-o", "--output", default=".",
        help="Parent folder for the generated build directory (default: current folder).")
    parser.add_argument(
        "-f", "--force", action="store_true",
        help="Replace an existing non-empty build after generation succeeds.")
    parser.add_argument(
        "-t", "--template", choices=("script", "class", "pages"), default="script",
        help="Generated code style (default: script).")
    parser.add_argument(
        "--theme", default="",
        help="Optional ttk theme, such as clam, alt, or default.")
    parser.add_argument(
        "--inspect", "--dry-run", action="store_true", dest="inspect",
        help="Preview frames, elements, rasterization, and warnings without generating.")
    parser.add_argument(
        "--format", choices=("text", "json"), default="text",
        help="Output format for inspection or the generation result (default: text).")
    parser.add_argument(
        "--no-manifest", action="store_true",
        help="Do not write build/tkdesigner.json provenance metadata.")
    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help="Show diagnostic progress. TKDESIGNER_VERBOSE=true also enables this.")
    parser.add_argument(
        "-q", "--quiet", action="store_true",
        help="Only print errors (JSON output is still printed when requested).")
    parser.add_argument("file_url", help="Figma design URL or file key.")
    parser.add_argument(
        "token", nargs="?",
        help="Figma token. Prefer the FIGMA_TOKEN environment variable.")
    return parser


def _configure_logging(args):
    verbose = args.verbose or environment_flag("TKDESIGNER_VERBOSE")
    level = logging.ERROR if args.quiet else logging.INFO if verbose else logging.WARNING
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")


def _confirm_output(parser, output_path: Path, force: bool) -> bool:
    if output_path.exists() and not output_path.is_dir():
        parser.error(f"`{output_path}` already exists and is not a directory.")
    if not output_path.exists() or not any(output_path.iterdir()) or force:
        return force

    if not sys.stdin.isatty():
        parser.error(
            f"`{output_path}` is not empty; pass --force in non-interactive environments.")
    print(f"Directory `{output_path}` is not empty.")
    response = input("Replace it after generation succeeds? [y/N] ")
    if response.lower().strip() != "y":
        print("Aborted; the existing build was not changed.")
        raise SystemExit(1)
    return True


def _generation_payload(result) -> dict:
    return {
        "output_path": str(result.output_path),
        "code_files": [str(path) for path in result.code_files],
        "asset_files": len(result.asset_files),
        "manifest_path": (
            str(result.manifest_path) if result.manifest_path is not None else None
        ),
        "summary": (
            result.report.to_dict().get("summary")
            if result.report is not None else None
        ),
    }


def run(args, parser) -> int:
    _configure_logging(args)
    reference = parse_figma_url(args.file_url)
    token = (args.token or os.getenv("FIGMA_TOKEN", "")).strip()
    if not token:
        parser.error(
            "missing Figma token. Set FIGMA_TOKEN or pass the token after the URL. "
            "If the URL contains `?` or `&`, wrap the URL in quotes.")

    output_path = Path(args.output.strip()).expanduser().resolve() / "build"
    clean_output = False
    if not args.inspect:
        clean_output = _confirm_output(parser, output_path, args.force)

    designer = Designer(
        token,
        reference.file_key,
        output_path,
        node_id=reference.node_id,
        template_style=args.template,
        theme=args.theme.strip(),
    )

    if args.inspect:
        report = designer.inspect()
        print(report.to_json() if args.format == "json" else report.to_text())
        return 0

    result = designer.design(
        clean=clean_output,
        write_manifest=not args.no_manifest,
    )
    if args.format == "json":
        print(json.dumps(_generation_payload(result), indent=2, sort_keys=True))
    elif not args.quiet:
        print(
            f"\nGenerated {len(result.code_files)} app file(s) and "
            f"{len(result.asset_files)} asset(s) at {result.output_path}."
        )
        if result.manifest_path is not None:
            print(f"Manifest: {result.manifest_path}")
    return 0


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return run(args, parser)
    except (OSError, RuntimeError, ValueError) as exc:
        parser.exit(1, f"error: {exc}\n")


if __name__ == "__main__":
    main()
