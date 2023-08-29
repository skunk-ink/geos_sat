import os
import argparse
import numpy as np
from netCDF4 import Dataset
from PIL import Image
import matplotlib.pyplot as plt
from tqdm import tqdm
import signal

# Function to handle ctrl-c interruption
def signal_handler(sig, frame):
    print("\nProgram interrupted. Exiting.")
    exit(0)

# Function to select data directory interactively
def select_data_directory():
    parent_data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
    data_folders = [d for d in os.listdir(parent_data_dir) if os.path.isdir(os.path.join(parent_data_dir, d))]
    if not data_folders:
        print("No data folders found in '../data/' directory. Please specify the 'data_dir' flag.")
        exit(1)
    
    print("Available data folders:")
    for i, folder in enumerate(data_folders):
        print(f"{i + 1}. {folder}")
    
    try:
        selection = int(input("\nSelect a data folder by entering its index: "))
        if 1 <= selection <= len(data_folders):
            return os.path.join(parent_data_dir, data_folders[selection - 1])
        else:
            print("Invalid selection. Exiting.")
            exit(1)
    except ValueError:
        print("Invalid input. Exiting.")
        exit(1)

# Register ctrl-c handler
signal.signal(signal.SIGINT, signal_handler)

# Parse command line arguments
parser = argparse.ArgumentParser(description='Extract and process imagery data from netCDF files.')
parser.add_argument('data_dir', nargs='?', help='Directory containing netCDF files or network address')
parser.add_argument('selected_channel_band_ids', nargs='+', help='Selected channel identifiers (e.g., C01 C02 C03)')
parser.add_argument('--export_format', default='jpg', help='Export image format')
parser.add_argument('--gray_scale', action='store_true', help='Convert images to grayscale')
parser.add_argument('--apply_scaling', action='store_true', help='Apply scaling to images')
args = parser.parse_args()

# If data_dir is not specified, prompt the user to select a data folder
if not args.data_dir:
    args.data_dir = select_data_directory()

# List all netCDF files in the directory
try:
    file_list = [f for f in os.listdir(args.data_dir) if f.endswith('.nc')]
except FileNotFoundError:
    print(f"Data directory '{args.data_dir}' not found. Please make sure it exists.")
    exit(1)

# Extract the parent folder name from the data_dir
parent_folder_name = os.path.basename(os.path.normpath(args.data_dir))

# Create a directory to store extracted data
output_data_dir = os.path.join('extracted_data', parent_folder_name)
os.makedirs(output_data_dir, exist_ok=True)

# Create a directory to store extracted images
output_images_dir = os.path.join(output_data_dir, 'images')
os.makedirs(output_images_dir, exist_ok=True)

# Extract images from netCDF files and save them
for selected_channel_band_id in args.selected_channel_band_ids:
    channel_output_dir = os.path.join(output_images_dir, selected_channel_band_id)
    os.makedirs(channel_output_dir, exist_ok=True)

    for frame, nc_file in enumerate(tqdm(file_list, desc=f'Extracting {selected_channel_band_id} Images', unit='file')):
        if f'M6{selected_channel_band_id}' in nc_file:
            dataset = Dataset(os.path.join(args.data_dir, nc_file), 'r')
            imagery_data = dataset.variables['CMI'][:]
            
            # Apply scaling if specified
            if args.apply_scaling:
                scaled_imagery_data = np.array(Image.fromarray(imagery_data).resize((imagery_data.shape[1], imagery_data.shape[0])))
            else:
                scaled_imagery_data = imagery_data
            
            # Get the original filename without extension
            original_filename = os.path.splitext(nc_file)[0]
            
            # Save the scaled image
            image_filename = os.path.join(channel_output_dir, f'image_{original_filename}.{args.export_format}')
            
            if args.gray_scale:
                plt.imsave(image_filename, scaled_imagery_data, cmap='gray', format=args.export_format)
            else:
                plt.imsave(image_filename, scaled_imagery_data, format=args.export_format)

print('Extracted images saved successfully.')
