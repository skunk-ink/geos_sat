# AIRS Sources Compiler

This Python script extracts file URLs of specific types from a given web page and saves them to a text file. It is particularly useful for users who obtain satellite data from NOAA's Archive Information Request System (AIRS) and want to quickly organize and save the download links.

## Table of contents
- [Dependencies](#dependencies)
- [Usage](#usage)
- [Examples](#example)

## Dependencies
- Python 3.6+
- Required Python libraries:
  - requests
  - beautifulsoup4
  - tqdm

Install the required libraries using the following command:
   ```bash
   pip install requests beautifulsoup4 tqdm
   ```

## Usage

1. Run the script by providing the URL as a command-line argument or by following the prompts. If no URL is provided, the script will prompt you for one.
   ```bash
   python compile_airs_sources.py [URL]
   ```
2. The script will fetch the webpage content, extract the file URLs ending in `.nc`, and save them to a text file in the `data_sources/` folder. The output file name will be created based on the last parts of the URL provided.
3. You will find the generated text file in the `data_sources/` folder of the script's parent directory.

## Example
Once you've obtained a URL from [NOAA's Archive Information Request System (AIRS)](https://www.ncdc.noaa.gov/airs-web). The URL should be something like `https://download.avl.class.noaa.gov/download/0123456789/001`. Then run the script with this URL and it will parse the `.nc` files from the webpage and save them to a text file in the `data_sources/` directory.

```bash
python compile_airs_sources.py https://download.avl.class.noaa.gov/download/0123456789/001
```

Please note that this script doesn't access NOAA's Archive Information Request System (AIRS) directly; it expects the user to provide the URLs they obtained from the system.