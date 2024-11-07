from pulp import *
from typing import Dict
from videos import *
from load_videos import video_collection

# Assuming video_collection is already created using load_videos_from_folder
# and contains all the videos from the 'Polish Transcripts' folder.

# Prepare data for the optimization model
num_videos = video_collection.total_videos()
num_days = 90  # Total number of days
num_words = video_collection.total_words()
P = 9 # Number of periods

# Create the 'a_{i,j}' matrix: occurrences of word i in video j
a = {}
for i in range(num_words):
    for j in range(num_videos):
        word = video_collection.index_to_word[i]
        video = video_collection.get_video(j)
        a[(i, j)] = video.word_counts.get(word, 0)

d_aux = []
for j in range(num_videos):
    difficulty  = 0.33*video_collection.get_video(j).profiling + 0.67*video_collection.get_video(j).TTR
    d_aux += [difficulty]

d_aux = [5 if int(((x-min(d_aux))/(max(d_aux)-min(d_aux)))*5) == 5 else int(((x-min(d_aux))/(max(d_aux)-min(d_aux)))*5)+1 for x in d_aux]
print(d_aux)

print(len(d_aux))
# Create the 'd_{j}' vector: difficulty of video j
dif = {j: d_aux[j] for j in range(num_videos)}

# Establish min and max difficulty for each period
bounds = {1: (1, 3), 2: (1, 3), 3: (1, 3), 4: (1, 4), 5: (1, 4), 6: (1, 4), 7: (1, 5), 8: (1, 5), 9: (1, 5)}


# Initialize the PuLP problem
prob = LpProblem("Vocabulary_Acquisition", LpMaximize)

# Decision variables
x = {}  # x_{j,d}: 1 if video j is watched on day d
for j in range(num_videos):
    for d in range(num_days):
        x[(j, d)] = LpVariable(f"x_{j}_{d}", cat="Binary")

w = {}  # w_i: 1 if word i is learned
for i in range(num_words):
    w[i] = LpVariable(f"w_{i}", cat="Binary")

# Objective function: Maximize the number of words learned
prob += lpSum(w[i] for i in range(num_words)), "Total_Words_Learned"

# Constraint 1: Each day, exactly one video is watched
for d in range(num_days):
    prob += lpSum(x[(j, d)] for j in range(num_videos)) == 1, f"One_Video_Per_Day_{d}"

# Constraint 2: Each video can be watched at most 3 times
for j in range(num_videos):
    prob += lpSum(x[(j, d)] for d in range(num_days)) <= 3, f"Video_Max_3_Times_{j}"

# Constraint 3: Word is learned if it appears at least 10 times in selected videos
for i in range(num_words):
    prob += lpSum(a[(i, j)] * lpSum(x[(j, d)] for d in range(num_days)) for j in range(num_videos)) >= 10 * w[i], f"Word_Learning_{i}"

# Constraint 4: Difficulty of selected videos must be within bounds
for d in range(num_days):
    # prob += lpSum(d[j] * x[(j, d)] for j in range(num_videos)) >= bounds[int(d/(num_days/P))+1][0], f"Min_Difficulty_{d}"
    prob += lpSum(dif[j] * x[(j, d)] for j in range(num_videos)) <= bounds[int(d/(num_days/P))+1][1], f"Max_Difficulty_{d}"

# Constraint 5: Each video can be watched at most once per period
for j in range(num_videos):
    for p in range(P):
        prob += lpSum(x[(j, d)] for d in range(p*num_days//P, (p+1)*num_days//P)) <= 1, f"Video_Max_Once_Per_Period_{j}_{p}"

# Solve the optimization problem
prob.solve(GUROBI_CMD())	

# Output the results
print("Status:", LpStatus[prob.status])
print("Total words learned:", value(prob.objective))

# List the learned words
learned_words = []
for i in range(num_words):
    if value(w[i]) == 1:
        learned_words.append(video_collection.index_to_word[i])

print("Learned Words:")
print(learned_words)

# Schedule of videos to watch each day
print("\nVideo Schedule:")
for d in range(num_days):
    for j in range(num_videos):
        if value(x[(j, d)]) == 1:
            video = video_collection.get_video(j)
            print(f"Day {d+1}: Watch '{video.title}'")
            break
