import os

folder_path = "../data/8335455739-001"
text_file_path = "../data_sources/8335455739-001.txt"

# Get the list of file names in the folder
folder_files = os.listdir(folder_path)

# Read the list of file names from the text file
with open(text_file_path, "r") as file:
    text_file_names = file.read().splitlines()

# Find missing names
missing_names = set(text_file_names) - set(folder_files)

# Print missing names
for name in missing_names:
    print(name)

