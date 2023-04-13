import argparse
import os
import tkinter as tk
from tkinter import filedialog
from typing import Optional

from bcedd import event_data


def save_file(name: str, data: bytes):
    """Saves a file to the user's computer using a dialog.

    Args:
        name (str): Name of the file.
        data (bytes): Data to save to the file.
    """
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)  # type: ignore
    file_path = filedialog.asksaveasfilename(initialfile=name, defaultextension=".tsv")
    if file_path:
        with open(file_path, "wb") as f:
            f.write(data)


def save_file_no_dialog(name: str, data: bytes, output: str):
    """Saves a file to the user's computer without using a dialog.

    Args:
        name (str): Name of the file.
        data (bytes): Data to save to the file.
        output (str): Output folder.
    """
    file_path = os.path.join(output, name)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(data)


def load_args() -> tuple[str, list[str], Optional[str]]:
    """Loads the arguments from the command line.

    Returns:
        tuple[str, list[str], Optional[str]]: Country code, files, and output folder.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--country-code",
        help="Country code to download",
        default="en",
        choices=["en", "jp", "kr", "tw"],
    )
    parser.add_argument(
        "-f",
        "--files",
        nargs="+",
        help="Files to download",
        choices=["sale.tsv", "gatya.tsv", "item.tsv"],
        default=["sale.tsv", "gatya.tsv", "item.tsv"],
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output folder",
        default=None,
    )

    args = parser.parse_args()

    country_code: str = args.country_code
    files: list[str] = args.files
    output: Optional[str] = args.output

    return country_code, files, output


def download(country_code: str, files: list[str], output: Optional[str]):
    """Downloads the files.

    Args:
        country_code (str): Country code to download the files for.
        files (list[str]): Files to download.
        output (Optional[str]): Output folder.
    """
    for file in files:
        file_name = country_code + "_" + file
        print(f"Downloading {file_name}...")
        ed = event_data.EventData(file, country_code)
        if output is not None:
            save_file_no_dialog(file_name, ed.make_request().content, output)
        else:
            save_file(file_name, ed.make_request().content)


def main():
    """Main function."""
    country_code, files, output = load_args()
    download(country_code, files, output)


if __name__ == "__main__":
    main()
