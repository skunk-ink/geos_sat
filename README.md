# NOAA GEOS Satellite Data Tools

Tools to download, extract and analyze GOES-R (ABI/GLM) Terrestrial Weather satellite data. Data can be obtained through [NOAA's Archive Information Request System (AIRS)](https://www.ncdc.noaa.gov/airs-web).

## Tools

- [AIRS Sources Compiler](./docs/airs-sources-compiler.md)
- [NOAA Data Downloader](./docs/noaa-data-downloader.md)
- [Imagery Extraction Tool](./docs/imagery-extraction-tool.md)
- [Image Crop and Resizing Tool](./docs/image-crop.md)
- [Image Animation Tool](./docs/image-animation-tool.md)

## Dependencies
- Python 3.6+
- Required Python libraries:
  - requests
  - beautifulsoup4
  - tqdm
  - numpy
  - netCDF4
  - PIL
  - matplotlib
  - opencv-python
  - opencv-python-headless

Install the required libraries using the following command:
   ```bash
   pip install requests beautifulsoup4 tqdm numpy netCDF4 Pillow matplotlib opencv-python opencv-python-headless
   ```