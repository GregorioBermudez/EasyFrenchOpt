from collections import Counter
from typing import List, Dict


class Video:
    def __init__(self, index: int, title: str, transcript: str):
        self.index = index
        self.title = title
        self.word_counts = Counter(transcript.split())
        self.total_words = sum(self.word_counts.values())
        self.TTR = len(self.word_counts) / self.total_words
        self.profiling = None

    def __repr__(self):
        return f"Video({self.index}, '{self.title}', {self.total_words} words)"

class VideoCollection:
    def __init__(self):
        self.videos: List[Video] = []
        self.global_word_counts: Dict[str, int] = Counter()
        self.title_to_index: Dict[str, int] = {}

    def add_video(self, title: str, transcript: str):
        index = len(self.videos)
        video = Video(index, title, transcript)
        self.videos.append(video)
        self.global_word_counts.update(video.word_counts)
        self.title_to_index[title] = index

    def get_video(self, identifier) -> Video:
        if isinstance(identifier, int):
            return self.videos[identifier]
        elif isinstance(identifier, str):
            return self.videos[self.title_to_index[identifier]]
        else:
            raise ValueError("Identifier must be an integer index or string title")

    def total_videos(self) -> int:
        return len(self.videos)

# Example usage:
collection = VideoCollection()

# Add videos
collection.add_video("Introduction to Python", "Python is a programming language Hello world")
collection.add_video("Data Structures", "Lists and dictionaries are important data structures")

# Access video data
video_by_index = collection.get_video(0)
video_by_title = collection.get_video("Data Structures")
