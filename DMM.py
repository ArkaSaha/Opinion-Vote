from scipy import sparse
from time import time
import sys
import numpy as np
from os.path import join
from heapq import heappush,heappop

def intake(message):
	if sys.version_info[0] >= 3:
		return input(message)
	else:
		return raw_input(message)

assert len(sys.argv) == 8, "Usage : python DMM.py <path-to-dataset> <r> <q> <t> <k> <score> <path-to-seeds>"
dataset = sys.argv[1]
r = int(sys.argv[2])
x = int(sys.argv[3])
time_stamp = int(sys.argv[4])
numOfSeeds = int(sys.argv[5])
model = sys.argv[6]
file = sys.argv[7]
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
index = [i for i in range(N)]
I = sparse.coo_matrix(([1 for _ in range(N)], (index, index)), shape=(N, N)).tocsr()

O_Val = [0 for _ in range(N)]
with open(join(dataset, str(x), "opinion.inf"), 'r') as f:
	for line in f:
		line = line.strip().split()
		O_Val[int(line[0])] = float(line[1])
B0 = sparse.coo_matrix((O_Val, ([0 for _ in range(N)], index)), shape=(1, N)).tocsr()

S_Val = [0 for _ in range(N)]
with open(join(dataset, str(x), "stubbornness.inf"), 'r') as f:
	for line in f:
		line = line.strip().split()
		S_Val[int(line[0])] = float(line[1])
D = sparse.coo_matrix((S_Val, (index, index)), shape=(N, N)).tocsr()

All_Val = []
row_index = []
col_index = []
M_Val = [0 for _ in range(N)]
if model == "Plurality" or model == "Copeland":
	for i in range(r):
		with open(join(dataset, str(i), "opinion_"+str(time_stamp)+"_0.txt"), 'r') as f:
			for line in f:
				line = line.strip().split()
				v = int(line[0])
				o = float(line[1])
				row_index.append(i)
				col_index.append(v)
				All_Val.append(o)
				if model == "Plurality" and i != x and M_Val[v] < o:
					M_Val[v] = o
Bx = sparse.coo_matrix((All_Val, (row_index, col_index)), shape=(r, N)).tocsr()
Bmax = sparse.coo_matrix((M_Val, ([0 for _ in range(N)], index)), shape=(1, N)).tocsr()

row_index = []
col_index = []
deg = np.zeros(N)
prob = np.zeros(N)
g_val = []
with open(join(dataset, str(x), "graph_vote.inf"), 'r') as f:
	for line in f:
		line = line.strip().split()
		row_index.append(int(line[0]))
		col_index.append(int(line[1]))
		g_val.append(float(line[2]))
		deg[int(line[0])] += 1
		prob[int(line[0])] += float(line[2])
W = sparse.coo_matrix((g_val, (row_index, col_index)), shape=(N, N)).tocsr()

nodes = set(range(N))
# nodes.update(deg.argsort()[-int(5 * numOfSeeds):])
# nodes.update(prob.argsort()[-int(5 * numOfSeeds):])
seeds = []
gainRecords = []

start = time()
for k in range(numOfSeeds):
	if k == 0:
		for i in nodes:
			temp_s = D[i, i]
			temp_o = B0[0, i]
			D[i, i] = 1
			B0[0, i] = 1
			B = B0
			S = I - D
			for j in range(time_stamp):
				B = B * W * S + B0 * D
			score = 0
			score1 = 0
			if model == "Cumulative":
				score = B.sum()
			elif model == "Plurality":
				score = (B > Bmax).nnz
			elif model == "p-Approval" or model == "Positional-p-Approval":
				for v in range(N):
					num = 0
					for j in range(r):
						if j != x and B[0, v] <= Bx[j, v]:
							num += 1
					score += (pos_wt[num] if num < p else 0)
			elif model == "Copeland":
				for cand in range(r):
					if cand != x:
						s1 = (B[0] > Bx[cand]).nnz
						s2 = (B[0] < Bx[cand]).nnz
						if s1 > s2:
							score += 1
						else:
							score1 += s1
			else:
				assert False, "Invalid scoring function"
			if model == "Copeland":
				heappush(gainRecords, (N - score, N - score1, i))
			else:
				heappush(gainRecords, (N - score, i))
			D[i, i] = temp_s
			B0[0, i] = temp_o
		seed_this_round = heappop(gainRecords)
	else:
		temp0 = -1
		temp1_details = heappop(gainRecords)
		temp1 = temp1_details[-1]
		while (temp0 != temp1):
			temp_s = D[temp1, temp1]
			temp_o = B0[0, temp1]
			D[temp1, temp1] = 1
			B0[0, temp1] = 1
			B = B0
			S = I - D
			for j in range(time_stamp):
				B = B * W * S + B0 * D
			score = 0
			score1 = 0
			if model == "Cumulative":
				score = B.sum()
			elif model == "Plurality":
				score = (B > Bmax).nnz
			elif model == "p-Approval" or model == "Positional-p-Approval":
				for v in range(N):
					num = 0
					for j in range(r):
						if j != x and B[0, v] <= Bx[j, v]:
							num += 1
					score += (pos_wt[num] if num < p else 0)
			elif model == "Copeland":
				for cand in range(r):
					if cand != x:
						s1 = (B > Bx[cand]).nnz
						s2 = (B < Bx[cand]).nnz
						if s1 > s2:
							score += 1
						else:
							score1 += s1
			else:
				assert False, "Invalid scoring function"
			if model == "Copeland":
				heappush(gainRecords, (N - score, N - score1, temp1))
			else:
				heappush(gainRecords, (N - score, temp1))
			D[temp1, temp1] = temp_s
			B0[0, temp1] = temp_o
			temp0 = temp1
			temp1_details = heappop(gainRecords)
			temp1 = temp1_details[-1]
		seed_this_round = temp1_details
	max_score = N - seed_this_round[0]
	seed = seed_this_round[-1]
	seeds.append(seed)
	D[seed, seed] = 1
	B0[0, seed] = 1
end = time()

print("Time used: {} seconds".format(end - start))
with open(file, 'w') as f:
	for v in seeds:
		f.write("{}\n".format(v))
