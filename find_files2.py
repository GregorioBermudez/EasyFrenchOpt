import os
import glob
import shutil
import re

def find_and_copy_polish_files(root_folder, destination_folder):
    polish_files = []
    pattern = re.compile(r'^EP(\d+)')  # Pattern to match directories starting with 'EP' followed by digits
    
    # Walk through all directories and subdirectories
    for dirpath, dirnames, filenames in os.walk(root_folder):
        # Extract the directory name
        dir_name = os.path.basename(dirpath)
        print(f'Dir name: {dir_name}')
        match = pattern.match(dir_name)
        print(f' Match: {match}')
        
        if match:
            # Extract the number from the directory name
            dir_number = int(match.group(1))
            # Check if the number is less than or equal to 139
            if dir_number <= 139:
                # Use glob to find files with "(Polish only)" in the name and ending with ".txt"
                matching_files = glob.glob(os.path.join(dirpath, "*.txt"))
                print(f'Matching files: {matching_files}')
                polish_files.extend(matching_files)
                
                # Copy each matching file to the destination folder
                for file in matching_files:
                    # Make sure the file is a text file
                    if file.endswith(".txt"):
                        # Make sure the destination folder exists
                        os.makedirs(destination_folder, exist_ok=True)
                        # Construct the full path for the destination file
                        destination_file = os.path.join(destination_folder, os.path.basename(file))
                        # Copy the file
                        shutil.copy(file, destination_file)
                        #print(f"Copied: {file}")
    
    return polish_files

# Example usage
root_folder = "Easy-Polish Drive"  # Replace with the path to your root folder
destination_folder = "Polish Transcripts"  # Replace with your destination folder path

polish_files = find_and_copy_polish_files(root_folder, destination_folder)