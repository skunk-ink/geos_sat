# NOAA Data Downloader

This is a Python script that allows you to download files from a list of URLs concurrently using multithreading.

Use the [AIRS Sources Compiler](./airs-sources-compiler.md) to create some valid source files.

## Table of contents
- [Dependencies](#dependencies)
- [Usage](#usage)
- [Command Line Options](#options)
- [Examples](#examples)

## Dependencies
- Python 3.6+
- Required Python libraries:
  - requests
  - tqdm

Install the required libraries using the following command:
   ```bash
   pip install requests tqdm
   ```

## Usage

1. Clone this repository to your local machine.
2. Open a terminal and navigate to the repository's directory.
3. Run the script with the following command:

```shell
python get_data.py
```

The downloaded files will be saved in the `data/` folder.

## Options
You can also provide command-line arguments to customize the process:

- `input_file_path`: Path to the input file containing URLs.
- `--max_workers`: Number of concurrent downloads (default is 20).

## Examples

Suppose you have a file named `data_sources/example_source_files.txt` containing a list of URLs you want to download. To run the script with this input file, use the following command:

```shell
python get_files.py data_sources/example_source_files.txt
```

The downloaded files will be saved in the `data/example_source_files` folder.