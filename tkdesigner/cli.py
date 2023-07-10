"""
TKinter Designer command-line interface.
"""

from tkdesigner.designer import Designer

import re
import os
import logging
import argparse

from pathlib import Path


if int(os.getenv("TKDESIGNER_VERBOSE", 0)) == 1:
    log_level = logging.INFO
else:
    log_level = logging.WARN

logging.basicConfig(level=log_level)


def main():
    parser = argparse.ArgumentParser(
        description="Generate TKinter GUI code from Figma design.")

    parser.add_argument(
        "-o", "--output", type=str, default=".",
        help=(
            "Folder to output code and image assets to. "
            "Defaults to current working directory."))
    parser.add_argument(
        "-f", "--force", action="store_true",
        help=(
            "If this flag is passed in, the output directory given "
            "will be overwritten if it exists."))

    parser.add_argument(
        "file_url", type=str, help="File url of the Figma design.")
    parser.add_argument("token", type=str, help="Figma token.")

    args = parser.parse_args()

    logging.basicConfig()
    logging.info(f"args: {args}")

    match = re.search(
        r'https://www.figma.com/file/([0-9A-Za-z]+)', args.file_url.split("?")[0])
    if match is None:
        raise ValueError("Invalid file URL.")

    file_key = match[1].strip()
    token = args.token.strip()
    output_path = Path(args.output.strip()).expanduser().resolve() / "build"

    if output_path.exists() and not output_path.is_dir():
        raise RuntimeError(
            f"`{output_path}` already exists and is not a directory.\n"
            "Hints: Input a different output directory "
            "or remove that existing file.")
    elif output_path.exists() and output_path.is_dir():
        if tuple(output_path.glob('*')) and not args.force:
            print(f"Directory `{output_path}` already exists.")
            response = input("Do you want to continue and overwrite? [N/y] ")
            if response.lower().strip() != "y":
                print("Aborting!")
                exit(-1)

    designer = Designer(token, file_key, output_path)
    designer.design()
    print(f"\nProject successfully generated at {output_path}.\n")


if __name__ == "__main__":
    main()