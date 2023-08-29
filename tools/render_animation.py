import os
import cv2
import argparse
from tqdm import tqdm

# Parse command line arguments
parser = argparse.ArgumentParser(description='Blend and animate images.')
parser.add_argument('--input_image_dirs', nargs='*', help='List of input image directories')
parser.add_argument('--video_fps', type=int, help='Frames per second for the output video')
parser.add_argument('--export_format', default='jpg', help='Export format for images')
parser.add_argument('--alpha', type=float, help='Alpha value for image blending')
args = parser.parse_args()

# Prompt for input image directory if not provided
if args.input_image_dirs is None:
    selected_dirs = []
    available_dirs = os.listdir('cropped_images')

    valid_directory = False
    valid_channel = False
    
    while valid_directory is False or valid_channel is False:
        print("Available input image directories:")
        for i, dir_name in enumerate(available_dirs):
            print(f"{i + 1}. {dir_name}")
        
        selected_dir_index = int(input("Select an input image directory (0 to finish): ")) - 1
        
        if selected_dir_index == -1:
            break
        else:
            valid_directory = True
        
        selected_dir = available_dirs[selected_dir_index]
        
        channel_dirs = os.listdir(f'cropped_images/{selected_dir}/images')
        print("Available channel directories:")
        for i, channel_name in enumerate(channel_dirs):
            print(f"{i + 1}. {channel_name}")
        
        selected_channel_indices = [int(idx) - 1 for idx in input("Select channel indices (comma-separated): ").split(',')]
        
        if -1 in selected_channel_indices:
            break
        else:
            valid_channel = True
        
        selected_dirs.extend([f'cropped_images/{selected_dir}/images/{channel_dirs[i]}' for i in selected_channel_indices])
    
    args.input_image_dirs = selected_dirs

# Prompt for video FPS if not provided
if args.video_fps is None:
    args.video_fps = int(input("Enter video FPS (default 10): ") or 10)

# Prompt for alpha value if not provided
if args.alpha is None:
    args.alpha = float(input("Enter alpha value (default 0.25): ") or 0.25)

# Ensure there is at least one input directory provided
if not args.input_image_dirs:
    print("No input image directories provided.")
    exit(1)

# Create output video filename based on input directories
output_channel_names = '_'.join([os.path.basename(dir_path) for dir_path in args.input_image_dirs])
output_video_filename = f'{selected_dir}_{output_channel_names}_animation.mp4'

# Create a list to store image filenames in alphabetical order for each channel
image_files_lists = []

# Iterate through input image directories and store sorted image filenames
for dir_path in args.input_image_dirs:
    image_files = [f for f in os.listdir(dir_path) if f.endswith('.' + args.export_format)]
    sorted_image_files = sorted(image_files)
    image_files_lists.append(sorted_image_files)

# Determine the number of frames based on the shortest image list
num_frames = min(len(image_files) for image_files in image_files_lists)

# Get the dimensions of the first image to determine video resolution
first_image_path = os.path.join(args.input_image_dirs[0], image_files_lists[0][0])
first_image = cv2.imread(first_image_path)
resize_resolution = (first_image.shape[1], first_image.shape[0])

# Create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter('cropped_images/' + selected_dir + "/images/" + output_video_filename, fourcc, args.video_fps, resize_resolution)

# Iterate through frames and blend images from different channels
for frame in tqdm(range(num_frames), desc='Creating Video', unit='frame'):
    try:
        blended_image = None
        
        for image_files in image_files_lists:
            image_file = image_files[frame]
            image_path = os.path.join(args.input_image_dirs[image_files_lists.index(image_files)], image_file)
            image = cv2.imread(image_path)
            
            # Resize the image to match the dimensions of the first image
            resized_image = cv2.resize(image, resize_resolution)
            
            if blended_image is None:
                blended_image = resized_image
            else:
                blended_image = cv2.addWeighted(blended_image, 1 - args.alpha, resized_image, args.alpha, 0)
        
        if blended_image is not None:
            video_writer.write(blended_image)
    except Exception as e:
        print(f"Error processing frame {frame}: {e}")

# Release the video writer
video_writer.release()

print(f'Video "cropped_images/{selected_dir}/images/{output_video_filename}" created successfully.')
