# Imagery Extraction Tool

This Python script extracts and processes imagery data from netCDF files. It allows you to specify various options through command line arguments to customize the extraction process.

Use the [NOAA Data Downloader](./noaa-data-downloader.md) to obtain satellite data from [NOAA's Archive Information Request System (AIRS)](https://www.ncdc.noaa.gov/airs-web).

## Table of contents
- [Dependencies](#dependencies)
- [Usage](#usage)
- [Command Line Options](#options)
- [Examples](#examples)

## Dependencies
- Python 3.6+
- Required Python libraries:
  - numpy
  - netCDF4
  - PIL
  - matplotlib
  - tqdm

Install the required libraries using the following command:
   ```bash
   pip install numpy netCDF4 Pillow matplotlib tqdm
   ```

## Usage

```shell
python extract_images.py [data_dir] selected_channel_band_ids [options]
```

- 'data_dir': Directory containing netCDF files or network address.
- 'selected_channel_band_ids': Selected channel identifiers, e.g., C01 C02 C03.

## Options
You can also provide command-line arguments to customize the process:

- '--output_image_dir': Directory to save extracted images (default: 'extracted_images/').
- '--export_format': Export image format (default: 'jpg').
- '--gray_scale': Convert images to grayscale (flag, no value needed).
- '--apply_scaling': Apply scaling to images (flag, no value needed).

## Examples

1. Extract images from local directory:
   ```shell
   python extract_images.py local/data_folder C01 C02 --output_image_dir extracted_images/ --export_format png --gray_scale
   ```
2. Extract images from network address:
   ```shell
   python extract_images.py \\127.0.0.1\SharedFolder\data_folder C03 --output_image_dir extracted_images/
   ```