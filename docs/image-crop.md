# Image Cropping and Resizing Tool

This Python script allows you to crop and resize images in multiple input directories. The cropped and resized images are then saved in corresponding subdirectories under the 'cropped_images' folder.

To extract images from data obtained through [NOAA's Archive Information Request System (AIRS)](https://www.ncdc.noaa.gov/airs-web), you can use the [Imagery Extraction Tool](./imagery-extraction-tool.md).

## Table of contents
- [Dependencies](#dependencies)
- [Usage](#usage)
- [Command Line Options](#options)

## Dependencies
- Python 3.6+
- Required Python libraries:
  - opencv-python-headless
  - tqdm

Install the required libraries using the following command:
   ```bash
   pip install opencv-python-headless tqdm
   ```

## Usage

1. Clone this repository to your local machine.

2. Navigate to the repository directory using the command line.

3. To crop and resize images using the default options:
    ```shell
    python image_crop.py
    ```

    This will guide you through selecting the channel directories and perform cropping and resizing using default settings.

4. The cropped and resized images are saved in the `cropped_images` directory.

## Options
You can also provide command-line arguments to customize the process:

```shell
python image_crop.py --input_image_dirs path/to/input/dir --export_format png --resize_resolution 1800 1800 --crop_area 100 500 800 1400
```

- `--input_image_dirs`: List of input image directories. (Optional)
- `--export_format`: Export image format. (Default: jpg)
- `--resize_resolution`: Resize resolution in pixels (width height). (Default: 2400 2400)
- `--crop_area`: Crop area in pixels (top, bottom, left, right). (Default: 50 450 900 1500)