import os
import glob
import shutil

def find_and_copy_polish_files(root_folder, destination_folder):
    polish_files = []
    
    # Walk through all directories and subdirectories
    for dirpath, dirnames, filenames in os.walk(root_folder):
        # Use glob to find files with "(Polish only)" in the name and ending with ".txt"
        matching_files = glob.glob(os.path.join(dirpath, "*(Polish only).txt"))
        polish_files.extend(matching_files)
        
        # Copy each matching file to the destination folder
        for file in matching_files:
            # Make sure the file is a text file
            if file.endswith(".txt"):
                if file.endswith(".pdf"):
                    print("PDF FILE------------------------------")
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
