"""
TKinter Designer command-line interface.
"""

import re
import os
import logging
import argparse

from tkdesigner.constants import ASSETS_PATH
from tkdesigner.designer import Designer

from pathlib import Path


if int(os.getenv("TKDESIGNER_VERBOSE", 0)) == 1:
    log_level = logging.INFO
else:
    log_level = logging.WARN

logging.basicConfig(level=log_level)


def main():
    # TODO: Add support for `--force`. Be careful while deleting files.
    parser = argparse.ArgumentParser(
        description="Generate TKinter GUI code from Figma design.")
    parser.add_argument(
        "file_url", type=str, help="File url of the Figma design.")
    parser.add_argument("token", type=str, help="Figma token.")
    parser.add_argument(
        "-o", "--output", type=str, default="build/",
        help="Folder to output code and image assets to. Defaults to build/.")
    parser.add_argument(
        "-f", "--force", action="store_true",
        help=(
            "If this flag is passed in, the output directory given "
            "will be overwritten if it exists."))

    args = parser.parse_args()

    logging.basicConfig()
    logging.info(f"args: {args}")

    output_path = Path(args.output)
    assets_path = output_path / ASSETS_PATH

    output_path.mkdir(exist_ok=True)
    assets_path.mkdir(exist_ok=True)

    match = re.search(r'https://www.figma.com/file/([^/]+)', args.file_url)
    if match is None:
        raise ValueError("Invalid file URL.")

    file_key = match.group(1)

    designer = Designer(args.token, file_key, Path(args.output))
    designer.design()


if __name__ == "__main__":
    main()
