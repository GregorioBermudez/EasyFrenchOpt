from load_videos import video_collection
from videos import VideoCollection
from typing import List
import random
import math
from collections import Counter
import nltk
from nltk.corpus import words as nltk_words
import matplotlib.pyplot as plt

# Set random seed
random.seed(0)

# Download the words corpus if not already downloaded
nltk.download('words', quiet=True)

# Create a set of English words for efficient lookup
english_words = set(word.lower() for word in nltk_words.words())

def is_polish_word(word: str) -> bool:
    # This is a simple check. You might want to refine this further.
    return word.lower() not in english_words


'''def evaluate_solution(video_collection: VideoCollection, solution: List[int]) -> int:
    learned_words = Counter()
    for index in solution:
        video = video_collection.get_video(index)
        learned_words.update(video.word_counts)
    return sum(1 for count in learned_words.values() if count >= 20)'''

def evaluate_solution(video_collection: VideoCollection, solution: List[int]) -> int:
    learned_words = {}
    for index in solution:
        video = video_collection.get_video(index)
        for word, count in video.word_counts.items():
            if is_polish_word(word):
                learned_words[word] = learned_words.get(word, 0) + count
    return sum(1 for count in learned_words.values() if count >= 20)

def get_neighbour(solution: List[int], video_collection: VideoCollection) -> List[int]:
    new_solution = solution.copy()
    index_to_remove = random.randint(0, len(new_solution) - 1)
    new_video = random.randint(0, video_collection.total_videos() - 1)
    while new_video == new_solution[index_to_remove]:
        new_video = random.randint(0, video_collection.total_videos() - 1)
    new_solution[index_to_remove] = new_video
    return new_solution

def simulated_annealing(video_collection: VideoCollection, num_videos: int, iterations: int, 
                        temperature: float, cooling_rate: float, t_min: float):
    # Initialize the current solution
    current_solution = list(range(num_videos))
    print(current_solution)
    current_score = evaluate_solution(video_collection, current_solution)
    best_solution = current_solution
    best_score = current_score
    temp = temperature

    score_history = [current_score]

    #for iteration in range(iterations):
    iteration = 0
    while temp > t_min:
        neighbour_solution = get_neighbour(current_solution, video_collection)
        neighbour_score = evaluate_solution(video_collection, neighbour_solution)

        if neighbour_score > current_score or random.random() < math.exp((neighbour_score - current_score) / temp):
            current_solution = neighbour_solution
            current_score = neighbour_score

            if current_score > best_score:
                best_solution = current_solution
                best_score = current_score
        if iteration % 500 == 0:
            print(f"Iteration {iteration}, Temperature: {temp:.2f}, Best Score: {best_score}")
        temp *= cooling_rate
        score_history.append(current_score)
        iteration += 1

    return best_solution, best_score, score_history

def plot_progress(score_history: List[int]):
    plt.figure(figsize=(10, 6))
    plt.plot(score_history)
    plt.title('Numero de palabras adquiridas sobre las iteraciónes')
    plt.xlabel('Iteración')
    plt.ylabel('Numero de palabras adquiridas')
    plt.grid(True)
    plt.show()

# Usage
num_videos_to_select = 90
initial_temp = 100000.0
t_min = 0.00001
cooling_rate = 0.995
num_iterations = 8000

best_solution, best_score, score_history = simulated_annealing(
    video_collection,
    num_videos_to_select,
    num_iterations,
    initial_temp,
    cooling_rate,   
    t_min
)

print("\nBest Solution:")
for index in best_solution:
    video = video_collection.get_video(index)
    print(f"- {video.title}")
print(f"\nTotal words learned: {best_score}")
plot_progress(score_history)