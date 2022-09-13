from scipy import sparse
import sys
from os.path import join

def intake(message):
	if sys.version_info[0] >= 3:
		return input(message)
	else:
		return raw_input(message)

assert len(sys.argv) in [6, 7], "Usage: python score.py <dataset> <r> <x> <t> <score> [<path-to-seeds>]"
dataset = sys.argv[1]
r = int(sys.argv[2])
x = int(sys.argv[3])
time_stamp = int(sys.argv[4])
model = sys.argv[5]
p = 1
pos_wt = [1 for _ in range(r)]
if model == "p-Approval" or model == "Positional-p-Approval":
	p = int(intake("Value of p: "))
	assert p >= 1 and p <= r, "p should be between 1 and r"
	if model == "Positional-p-Approval":
		for i in range(p):
			pos_wt[i] = float(intake("Value of omega[{}]: ".format(i + 1)))
			assert pos_wt[i] >= 0 and pos_wt[i] <= 1, "Weights should be between 0 and 1"
			assert i == 0 or pos_wt[i] <= pos_wt[i - 1], "Weights should be non-increasing"

N = 0
with open(join(dataset, str(x), "attribute.txt"), 'r') as f:
	N = int(f.readline()[2:-1])
O_Val = [0 for _ in range(N)]
S_Val = [0 for _ in range(N)]

with open(join(dataset, str(x), "opinion.txt"), 'r') as f:
	for line in f:
		line = line.strip().split()
		O_Val[int(line[0])] = float(line[1])
with open(join(dataset, str(x), "stubbornness.txt"), 'r') as f:
	for line in f:
		line = line.strip().split()
		S_Val[int(line[0])] = float(line[1])

All_Val = [[0 for _ in range(r)] for _ in range(N)]
if model != "Cumulative":
	for i in range(r):
		if i != x:
			with open(join(dataset, str(i), "opinion_"+str(time_stamp)+"_0.txt"), 'r') as f:
				for line in f:
					line = line.split()
					All_Val[int(line[0])][i] = float(line[1])

seeds = []
if len(sys.argv) == 7:
	with open(sys.argv[6], 'r') as f:
		for line in f:
			seeds.append(int(line.strip()))
for v in seeds:
	O_Val[v] = 1
	S_Val[v] = 1

index = [i for i in range(N)]
I = sparse.coo_matrix(([1 for _ in range(N)], (index, index)), shape=(N, N)).tocsr()
D = sparse.coo_matrix((S_Val, (index, index)), shape=(N, N)).tocsr()
B0 = sparse.coo_matrix((O_Val, ([0 for _ in range(N)], index)), shape=(1, N)).tocsr()

row_index = []
col_index = []
g_val = []
with open(join(dataset, str(x), "graph_vote.txt"), 'r') as f:
	for line in f:
		line = line.strip().split()
		row_index.append(int(line[0]))
		col_index.append(int(line[1]))
		g_val.append(float(line[2]))
W = sparse.coo_matrix((g_val, (row_index, col_index)), shape=(N, N)).tocsr()

B = B0
I = I - D
for j in range(time_stamp):
	B = B * W * I + B0 * D

score = 0
if model == 'Cumulative':
	score = B.sum()
elif model == 'Plurality' or model == 'p-Approval' or model == 'Positional-p-Approval':
	for node in range(N):
		num = 0
		for i in range(r):
			if i != x and B[0, node] <= All_Val[node][i]:
				num += 1
		score += (pos_wt[num] if num < p else 0)
elif model == 'Copeland':
	for cand in range(r):
		if cand != x:
			s1 = 0
			s2 = 0
			for node in range(N):
				if B[0, node] > All_Val[node][cand]:
					s1 += 1
				elif B[0, node] < All_Val[node][cand]:
					s2 += 1
			score += (s1 > s2)
else:
	assert False, "Invalid scoring function"
print("Score : {}".format(score))
