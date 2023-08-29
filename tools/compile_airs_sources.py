import sys
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin
from tqdm import tqdm  # Import tqdm for the progress bar

# Get user input URL from command line arguments or prompt
if len(sys.argv) > 1:
    url = sys.argv[1]
else:
    url = input("Enter the URL: ")

# Fetch the webpage content
response = requests.get(url)
html_content = response.text

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Extract file names and their URLs
file_urls = []
base_url = urljoin(url, '/')  # Ensure base URL ends with '/'
for link in soup.find_all('a', href=True):
    if link['href'].endswith('.nc'):
        file_urls.append(urljoin(base_url, link['href']))

# Create the output file name
output_file_name = url.split('/')[-2] + '-' + url.split('/')[-1] + '.txt'
output_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data_sources', output_file_name)

# Write the URLs to the output file with a progress bar
with open(output_file_path, 'w') as f, tqdm(total=len(file_urls), desc="Writing URLs") as pbar:
    for i, file_url in enumerate(file_urls):
        f.write(file_url)
        if i < len(file_urls) - 1:  # Don't add newline for the last URL
            f.write('\n')
        pbar.update(1)  # Update the progress bar

print(f"File URLs saved to: ..\\data_sources\\{output_file_name}")
