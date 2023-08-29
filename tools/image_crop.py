import os
import cv2
from tqdm import tqdm
import time
import shutil
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Image cropping and resizing script.")
    parser.add_argument("--input_image_dirs", nargs="*", default=None, help="List of input image directories.")
    parser.add_argument("--export_format", default="jpg", help="Export image format.")
    parser.add_argument("--resize_resolution", type=int, nargs=2, default=[2400, 2400], help="Resize resolution (width height).")
    parser.add_argument("--crop_area", type=int, nargs=4, default=[50, 450, 900, 1500], help="Crop area (top, bottom, left, right).")
    return parser.parse_args()

def get_script_directory():
    return os.path.dirname(os.path.abspath(__file__))

def create_directory(directory):
    os.makedirs(directory, exist_ok=True)

def select_channels(extracted_data_dir):
    selected_dirs = []
    available_dirs = os.listdir(extracted_data_dir)
    total_sub_dirs = 0
    
    print("Available image channel directories:\n")
    
    directory_index = 1
    
    for idx, directory in enumerate(available_dirs, start=1):
        sub_dir = os.path.join(extracted_data_dir, directory, "images")
        if os.path.isdir(sub_dir):
            sub_dirs = os.listdir(sub_dir)
            print(f"  - {directory}")
            for sub_idx, sub_dir_name in enumerate(sub_dirs, start=total_sub_dirs + 1):
                print(f"    {directory_index}. {sub_dir_name}")
                selected_dirs.append(os.path.join(sub_dir, sub_dir_name))
                directory_index += 1
        
            total_sub_dirs += len(sub_dirs)
            
    selected = input(f"\nEnter the channel directories you would like to crop (1, 2, ...), or press Enter to skip: ")
    if selected:
        selected_indices = [int(idx) for idx in selected.split(",")]
        selected_dirs.extend([os.path.join(sub_dir, sub_dirs[i - 1]) for i in selected_indices if i <= len(sub_dirs)])
    print()
    
    return selected_dirs

def create_output_subdirectories(output_base_dir, input_sub_dir):
    # Recreate the subdirectory structure under the output base directory.
    subdirs = os.path.relpath(input_sub_dir, extracted_data_dir)
    output_sub_dir = os.path.join(output_base_dir, subdirs)
    create_directory(output_sub_dir)
    return output_sub_dir

args = parse_args()

if args.input_image_dirs is None:
    script_dir = get_script_directory()
    extracted_data_dir = os.path.join(script_dir, "..", "extracted_data")
    # Get the relative paths from extracted_data_dir
    selected_dirs = select_channels(extracted_data_dir)
    cropped_channel_dir = [os.path.relpath(dir_path, extracted_data_dir) for dir_path in selected_dirs]
else:
    selected_dirs = args.input_image_dirs
    cropped_channel_dir = selected_dirs

output_channel_names = "_".join([os.path.basename(os.path.dirname(dir_path)) for dir_path in cropped_channel_dir])
export_format = args.export_format
resize_resolution = tuple(args.resize_resolution)
crop_area = tuple(args.crop_area)

output_dirs = []
cropped_images_dir = os.path.join(get_script_directory(), "..", "cropped_images")
create_directory(cropped_images_dir)

for dir_path in cropped_channel_dir:
    output_base_dir = os.path.join(cropped_images_dir, os.path.basename(dir_path))

    output_sub_dir = create_output_subdirectories(output_base_dir, dir_path)
    output_dirs.append(output_sub_dir)

num_images = int(sum(len(os.listdir(dir_path)) for dir_path in selected_dirs) / 2)

progress_bar = tqdm(total=num_images, desc="Resizing Images", unit="image")
start_time = time.time()

for dir_path, output_dir in zip(selected_dirs, output_dirs):
    for frame, image_file in enumerate(sorted(os.listdir(dir_path))):
        if image_file.endswith("." + export_format):
            image_path = os.path.join(dir_path, image_file)
            image = cv2.imread(image_path)
            if image is None:
                continue  # Skip non-image files
            resized_image = cv2.resize(image, resize_resolution)
            temp_image_path = os.path.join(output_dir, image_file)
            cv2.imwrite(temp_image_path, resized_image)
            progress_bar.update(1)

progress_bar.close()
resize_time = time.time() - start_time
print(f"Images resized in {resize_time:.2f} seconds.")

progress_bar = tqdm(total=num_images, desc="Cropping Images", unit="image")
start_time = time.time()

for output_dir in output_dirs:
    for frame, image_file in enumerate(sorted(os.listdir(output_dir))):
        if image_file.endswith("." + export_format):
            image_path = os.path.join(output_dir, image_file)
            image = cv2.imread(image_path)
            if image is None:
                continue  # Skip non-image files
            print(f"Cropping image {image_file} with shape {image.shape}, crop area {crop_area}")
            cropped_image = image[crop_area[0]:crop_area[1], crop_area[2]:crop_area[3]]
            cv2.imwrite(image_path, cropped_image)
            progress_bar.update(1)

progress_bar.close()
crop_time = time.time() - start_time
print(f"Images cropped in {crop_time:.2f} seconds.")

render_script_file = "tools/render_animation.py"
destination_folder = cropped_images_dir
destination_path = os.path.join(destination_folder, render_script_file)

if not os.path.exists(destination_path):
    shutil.copy(render_script_file, destination_folder)
    print(f"File '{render_script_file}' copied to '{destination_path}'.")
else:
    print(f"File '{render_script_file}' already exists in '{destination_path}'. No need to copy.")
