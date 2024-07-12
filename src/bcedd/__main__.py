import argparse
import os
try:
    import tkinter as tk
    from tkinter import filedialog
except Exception:
    tk = None
    filedialog = None

from typing import Optional

from bcedd import event_data, game_version, country_code


def save_file(name: str, data: bytes):
    """Saves a file to the user's computer using a dialog.

    Args:
        name (str): Name of the file.
        data (bytes): Data to save to the file.
    """
    if tk is None or filedialog is None:
        print("Error: Tkinter was not found!")
        return
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


def load_args() -> tuple[list[str], list[str], Optional[str], bool]:
    """Loads the arguments from the command line.

    Returns:
        tuple[list[str], list[str], Optional[str]]: Country code, files, and output folder.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--country-codes",
        nargs="+",
        help="Country codes to download",
        default=["en"],
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
    parser.add_argument(
        "--old",
        help="Use the old event data domain and method (aws)",
        action="store_true",
    )

    args = parser.parse_args()

    ccs: list[str] = args.country_codes
    files: list[str] = args.files
    output: Optional[str] = args.output
    use_old: bool = args.old

    return ccs, files, output, use_old


def download(ccs: list[str], files: list[str], output: Optional[str], use_old: bool):
    """Downloads the files.

    Args:
        country_code (list[str]): Country code to download the files for.
        files (list[str]): Files to download.
        output (Optional[str]): Output folder.
    """

    for cc in ccs:
        download_cc(cc, files, output, use_old)
   
def download_cc(cc: str, files: list[str], output: Optional[str], use_old: bool):
    gv = game_version.GameVersion.from_string("12.4.0")  # doesn't matter
    for file in files:
        file_name = cc + "_" + file
        print(f"Downloading {file_name}...")
        ed = event_data.EventData(
            file, country_code.CountryCode.from_code(cc), gv, use_old
        )
        if output is not None:
            save_file_no_dialog(file_name, ed.make_request().content, output)
        else:
            save_file(file_name, ed.make_request().content)


def main():
    """Main function."""
    ccs, files, output, use_old = load_args()
    download(ccs, files, output, use_old)


if __name__ == "__main__":
    main()
