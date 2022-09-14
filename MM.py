from scipy import sparse
import sys
from os.path import join

assert len(sys.argv) in [4, 5], "Usage : python MM.py <path-to-dataset> <candidate> <time-horizon> [path-to-seeds]"
dataset = sys.argv[1]
x = sys.argv[2]
t = int(sys.argv[3])

N = 0
with open(join(dataset, x, "attribute.txt"), 'r') as f:
	N = int(f.readline()[2:-1])

index0 = [0 for _ in range(N)]
index = [i for i in range(N)]
i_val = [1 for _ in range(N)]

O_Val = [0 for _ in range(N)]
with open(join(dataset, x, "opinion.txt"), 'r') as f:
	for line in f:
		line = line.strip().split()
		O_Val[int(line[0])] = float(line[1])

S_Val = [0 for _ in range(N)]
with open(join(dataset, x, "stubbornness.txt"), 'r') as f:
	for line in f:
		line = line.strip().split()
		S_Val[int(line[0])] = float(line[1])

row_index = []
col_index = []
g_val = []
with open(join(dataset, x, "graph_vote.txt"), 'r') as f:
	for line in f:
		line = line.strip().split()
		row_index.append(int(line[0]))
		col_index.append(int(line[1]))
		g_val.append(float(line[2]))

seeds = []
if len(sys.argv) == 5:
	with open(sys.argv[4], 'r') as f:
		for line in f:
			seeds.append(int(line.strip()))
for v in seeds:
	O_Val[v] = 1
	S_Val[v] = 1

I = sparse.coo_matrix((i_val, (index, index)), shape=(N, N)).tocsr()
B0 = sparse.coo_matrix((O_Val, (index0, index)), shape=(1, N)).tocsr()
D = sparse.coo_matrix((S_Val, (index, index)), shape=(N, N)).tocsr()
W = sparse.coo_matrix((g_val, (row_index, col_index)), shape=(N, N)).tocsr()

B = B0
I = I - D
for i in range(t):
	B = B * W * I + B0 * D

with open(join(dataset, x, "opinion_{}_{}.txt".format(t, len(seeds))), 'w') as f:
	for i in range(N):
		f.write("{} {}\n".format(i, B[0, i]))
