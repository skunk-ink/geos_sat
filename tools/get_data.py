import os
import argparse
import requests
from tqdm import tqdm
import concurrent.futures
import time

def download_file(url, save_path):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    if os.path.exists(save_path):
        local_size = os.path.getsize(save_path)
        if local_size == total_size:
            print(f"Skipping {os.path.basename(url)} - already downloaded.")
            return
    
    with open(save_path, 'wb') as f:
        with tqdm(
            desc=os.path.basename(url),
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
            ncols=150,
            ascii=True,
        ) as pbar:
            for data in response.iter_content(chunk_size=8192):
                f.write(data)
                pbar.update(len(data))

def download_files(urls, save_folder, max_workers):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(download_file, url, os.path.join(save_folder, os.path.basename(url))): url for url in urls}
        
        with tqdm(total=len(future_to_url), desc="Overall Progress", ncols=100, ascii=True) as overall_pbar:
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    future.result()
                except Exception as e:
                    print(f"Error downloading {url}: {e}")
                finally:
                    overall_pbar.update(1)

def list_available_sources(source_folder):
    available_sources = []
    for filename in os.listdir(source_folder):
        if filename.endswith(".txt") and filename != "example_source_files.txt":
            available_sources.append(filename)
    return available_sources

def main():
    try:
        parser = argparse.ArgumentParser(description='Download files from a list of URLs.')
        parser.add_argument('input_file_path', nargs='?', default='', help='Path to the input file containing URLs. (default is ../data/)')
        parser.add_argument('--max_workers', type=int, default=20, help='Number of concurrent downloads.')
        args = parser.parse_args()
    
        if not args.input_file_path:
            script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script
            source_folder = os.path.join(script_dir, '..', 'data_sources')  # Navigate to the parent directory and then 'data_sources'
            available_sources = list_available_sources(source_folder)
            if available_sources:
                print("\nAvailable data source files:\n")
                for idx, source in enumerate(available_sources, start=1):
                    print(f"{idx}. {source}")
                source_index = int(input("\nSelect a source file (1, 2, ...): ")) - 1
                if source_index >= 0 and source_index < len(available_sources):
                    args.input_file_path = os.path.join(source_folder, available_sources[source_index])
                else:
                    print("Invalid selection. Exiting.")
                    return
            else:
                print("\nNo valid data source files found in the '../data_sources/' folder.")
                args.input_file_path = input("Enter the path to a data source file: ")
        
        with open(args.input_file_path, 'r', encoding='utf-8') as input_file:
            urls = [line.strip() for line in input_file]

        save_folder_name = os.path.splitext(os.path.basename(args.input_file_path))[0]
        data_folder = 'data'
        os.makedirs(data_folder, exist_ok=True)
        save_path = os.path.join(data_folder, save_folder_name)
        os.makedirs(save_path, exist_ok=True)
        
        start_time = time.time()

        download_files(urls, save_path, args.max_workers)
                
        total_size = sum(os.path.getsize(os.path.join(save_path, os.path.basename(url))) for url in urls)
        total_time = time.time() - start_time
        average_speed = total_size / total_time / (1024 * 1024)
        
        print(f"Total downloaded: {total_size / (1024 * 1024):.2f} MB")
        print(f"Average download speed: {average_speed:.2f} Mb/s")
        
    except KeyboardInterrupt:
        print("\nProgram interrupted. Exiting...")
        exit(1)

if __name__ == "__main__":
    main()
