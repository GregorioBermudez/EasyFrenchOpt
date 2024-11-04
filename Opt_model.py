import pulp
from typing import Dict
from videos import *
from load_videos import video_collection

# Assuming video_collection is already created using load_videos_from_folder
# and contains all the videos from the 'Polish Transcripts' folder.

# Prepare data for the optimization model
num_videos = video_collection.total_videos()
num_days = 90  # Total number of days

# Create a set of all unique words in the video collection
video_collection.finalize()  # Ensure word indices are prepared
num_words = video_collection.total_words()

# Create the 'a_{i,j}' matrix: occurrences of word i in video j
a = {}
for i in range(num_words):
    for j in range(num_videos):
        word = video_collection.index_to_word[i]
        video = video_collection.get_video(j)
        a[(i, j)] = video.word_counts.get(word, 0)

# Initialize the PuLP problem
prob = pulp.LpProblem("Vocabulary_Acquisition", pulp.LpMaximize)

# Decision variables
x = {}  # x_{j,d}: 1 if video j is watched on day d
for j in range(num_videos):
    for d in range(num_days):
        x[(j, d)] = pulp.LpVariable(f"x_{j}_{d}", cat="Binary")

w = {}  # w_i: 1 if word i is learned
for i in range(num_words):
    w[i] = pulp.LpVariable(f"w_{i}", cat="Binary")

# Objective function: Maximize the number of words learned
prob += pulp.lpSum(w[i] for i in range(num_words)), "Total_Words_Learned"

# Constraint 1: Each day, exactly one video is watched
for d in range(num_days):
    prob += pulp.lpSum(x[(j, d)] for j in range(num_videos)) == 1, f"One_Video_Per_Day_{d}"

# Constraint 2: Each video can be watched at most 3 times
for j in range(num_videos):
    prob += pulp.lpSum(x[(j, d)] for d in range(num_days)) <= 3, f"Video_Max_3_Times_{j}"

# Constraint 3: Word is learned if it appears at least 10 times in selected videos
for i in range(num_words):
    prob += pulp.lpSum(a[(i, j)] * pulp.lpSum(x[(j, d)] for d in range(num_days)) for j in range(num_videos)) >= 10 * w[i], f"Word_Learning_{i}"

# Solve the optimization problem
prob.solve()

# Output the results
print("Status:", pulp.LpStatus[prob.status])
print("Total words learned:", pulp.value(prob.objective))

# List the learned words
learned_words = []
for i in range(num_words):
    if pulp.value(w[i]) == 1:
        learned_words.append(video_collection.index_to_word[i])

print("Learned Words:")
print(learned_words)

# Schedule of videos to watch each day
print("\nVideo Schedule:")
for d in range(num_days):
    for j in range(num_videos):
        if pulp.value(x[(j, d)]) == 1:
            video = video_collection.get_video(j)
            print(f"Day {d+1}: Watch '{video.title}'")
            break
