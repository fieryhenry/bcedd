# Battle Cats Event Data Downloader

The Battle Cats Event Data Downloader (BCEDD) is a tool made for downloading battle cats event data such as gatya data and sale data.

[PyPI](https://pypi.org/project/bcedd)

## Credits

- The [PackPack Discord Bot](https://github.com/battlecatsultimate/PackPack) for the general cryptography algorithm needed

## How To Use

### Prerequisites

- [Python](https://www.python.org/downloads/) for running and installing the tool

Run the following commands in command prompt or another terminal to install the tool - If you are not using windows you will need to use `python` or `python3` instead of `py`

### Installation

```bash
py -m pip install -U bcedd
```

If you get an error saying `No module named pip` then run

```bash
py -m ensurepip --upgrade
```

### Run

By default the tool will download `sale.tsv`, `gatya.tsv` and `item.tsv` for `en` and it will ask you where you want to save it:

```bash
py -m bcedd
```

If you want to download files for a different version use `-c <version>` Supported versions are `en`, `jp`, `kr`, `tw`.

```bash
py -m bcedd -c jp
```

This will download jp data instead

If you only want to download specific files then use `-f <file1> <file2> etc`. Supported files are `sale.tsv`, `gatya.tsv`, `item.tsv`.

```bash
py -m bcedd -f gatya.tsv item.tsv
```

This will download files `gatya.tsv` and `item.tsv` but not `sale.tsv`

If you don't want a file save dialog then use `-o <output_folder>` to save the files to a specific folder.

```bash
py -m bcedd -o "Event Data"
```

This will save all 3 en files to a folder called "Event Data" in the current working directory (use the `cd` command to change that)

## Install From Source

If you want the latest features and don't want to wait for a release then you can install the tool from the github directly.

1. Download [Git](https://git-scm.com/downloads)
2. Run the following commands: (You may have to replace `py` with `python` or `python3`)

```bash
git clone https://github.com/fieryhenry/bcedd.git
py -m pip install -e bcedd/
py -m bcedd
```

If you want to use the tool again all you need to do is run the `py -m bcedd` command

Then if you want the latest changes you only need to run `git pull` in the downloaded `bcedd` folder. (use `cd` to change the folder)
