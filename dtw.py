import numpy as np
import matplotlib.pyplot as plt

arr1 = [2, 5, 5, 7, 9, 1, 6, 6, 8, 9, 1, 6, 6, 8, 9]
arr2 = [1, 1, 1, 1, 3, 3, 3, 3, 1, 1, 1, 1, 7, 7, 8, 7]
arr3 = [4, 2, 1, 4, 8, 8, 9, 3, 2, 3, 2, 2, 6, 9, 2, 1, 1, 6, 1]
arr4 = [1, 5, 7, 3, 7, 2, 8, 9, 9, 2, 2, 3, 7, 8]
arr5 = [3, 2, 2, 1, 1, 8, 3, 2, 6, 9, 1, 6, 1]
arr6 = [1, 1, 1, 3, 3, 2, 1, 1, 7, 7, 7]

arrays = [arr1, arr2, arr3, arr4, arr5, arr6]

def distance(a, b):
    return np.abs(a - b)

def DTWDistance(s, t):
    n = len(s)
    m = len(t)

    dtw = np.zeros((n+1, m+1))
    dtw[0, 1:] = np.inf
    dtw[1:, 0] = np.inf

    dtw[0, 0] = 0

    for i in range(1, n+1):
        for j in range(1, m+1):
            cost = distance(s[i-1], t[j-1])
            dtw[i, j] = cost + min([dtw[i-1, j], dtw[i, j-1], dtw[i-1, j-1]])

    return dtw[n, m], dtw

similartiy = np.zeros((6, 6))

#for i in range(6):
#	for j in range(6):
#		similartiy[i, j] = DTWDistance(arrays[i], arrays[j])
print(similartiy)

def find_alignments(dtw_matrix):
    i = dtw_matrix.shape[0] - 1
    j = dtw_matrix.shape[1] - 1
    
    alignments = {}
    
    while i > 0 and j > 0:
        neighbors = [(i, j-1),
                   (i-1, j),
                   (i-1,j-1)]
        
        chosen_idx = np.argmin([dtw_matrix[neighbor] for neighbor in neighbors])
        i, j = neighbors[chosen_idx]
        
        if i not in alignments:
            alignments[i] = []
        alignments[i].append(j)
        
    return alignments 

distance, DTW_matrix = DTWDistance(arr2, arr6)

offset = 4
offset_series_b = np.array(arr6) + offset

plt.figure(figsize=(15,8))
plt.axis('off')

plt.plot(arr2, label='Array 2')
plt.plot(offset_series_b, label='Array 6')

alignment_dict = find_alignments(DTW_matrix)

for timestep in list(alignment_dict.keys()):
    alignments = alignment_dict[timestep]
    
    for alignment in alignments:
        if timestep < len(arr2) and alignment < len(offset_series_b):
            x_vals = [timestep, alignment]
            y_vals = [arr2[timestep], offset_series_b[alignment]]

            plt.plot(x_vals, y_vals, c='#888888FF', linestyle='dashed', linewidth=1)
            plt.scatter(x_vals[0], y_vals[0], s=8, c='#558ABA')
            plt.scatter(x_vals[1], y_vals[1], s=8, c='orange')

plt.legend()
plt.show()