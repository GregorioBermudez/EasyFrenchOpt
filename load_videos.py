import os
from typing import List
from utils import *
from videos import VideoCollection  # Assuming this is the module where we defined our classes

def load_videos_from_folder(folder_path: str) -> VideoCollection:
    collection = VideoCollection()
    
    # Ensure the folder path exists
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"The folder {folder_path} does not exist.")
    
    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            
            # The title is the filename without the .txt extension
            title = os.path.splitext(filename)[0]
            
            # Read the content of the file
            with open(file_path, encoding='latin-1') as file:
                transcript = file.read()
                transcript = clean(transcript)
            
            # Add the video to our collection
            collection.add_video(title, transcript)
    
    return collection

def create_frequency_rank(video_collection):
    # Calculate the overall frequency of each word
    word_frequencies = video_collection.global_word_counts

    # Sort words by frequency in descending order
    sorted_words = sorted(word_frequencies.items(), key=lambda item: item[1], reverse=True)

    # Create a dictionary to map each word to its rank
    frequency_rank = {word: rank + 1 for rank, (word, _) in enumerate(sorted_words)}

    return frequency_rank

folder_path = 'French Transcripts'
video_collection = load_videos_from_folder(folder_path)
video_collection.finalize()
frequency_rank = create_frequency_rank(video_collection)
highest_ranked_words = list(frequency_rank.keys())[:int(len(frequency_rank)*0.01)]

for video in video_collection.videos:
    video.profiling = sum(video.word_counts[word] for word in highest_ranked_words)/video.total_words

print(f'Amount of videos: {video_collection.total_videos()}')