# Image Animation Tool

This tool blends and animates images from different channels. It takes input image directories, blending parameters, and output video settings to create an animation video.

You can use the [Image Cropping and Resizing Tool](./image-crop.md) to scale the extracted images to a more managable size.

## Table of contents
- [Dependencies](#dependencies)
- [Usage](#usage)
- [Command Line Options](#options)
- [Examples](#example)
- [Notes](#notes)

## Dependencies
- Python 3.6+
- Required Python libraries:
  - opencv-python
  - tqdm

Install the required libraries using the following command:
```shell
pip install opencv-python tqdm
```

## Usage

1. Prepare your input images by organizing them into subdirectories under the cropped_images directory. Each input image directory should contain subdirectories corresponding to different channels. You can use the [Image Crop and Resizing Tool](./image-crop.md)

2. Run the tool with the following command:
    ```shell
    python render_animation.py [options]
    ```

## Options
You can also provide command-line arguments to customize the process:
- `--input_image_dirs`: List of input image directories. If not provided, you will be prompted to select an input image directory and channels to use for blending and animation.
- `--video_fps`: Frames per second for the output video. If not provided, the default is 10.
- `--export_format`: Export format for images. If not provided, the default is 'jpg'.
- `--alpha`: Alpha value for image blending. If not provided, the default is 0.25.

## Example

To create an animation using specific input image directories, video FPS, export format, and alpha value:

```shell
python render_animation.py --input_image_dirs cropped_images/C01/images --video_fps 15 --export_format png --alpha 0.5
```

## Notes

- The tool will generate an animation video saved in the corresponding subfolder of the input image directory under the cropped_images directory.
- The animation is created by blending images from different channels using the specified alpha value.
- The tool uses the OpenCV library for image processing and video creation.
