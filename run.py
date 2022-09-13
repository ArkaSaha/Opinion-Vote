import sys
from os import system

def intake(message):
	if sys.version_info[0] >= 3:
		return input(message)
	else:
		return raw_input(message)

assert len(sys.argv) == 9, "Usage: python run.py <dataset> <number-of-seeds> <time-horizon> <number-of-candidates> <target-candidate> <score> <mode> <path-to-seeds>"
dataset = sys.argv[1]
k = sys.argv[2]
t = sys.argv[3]
r = int(sys.argv[4])
q = int(sys.argv[5])
score = sys.argv[6]
mode = sys.argv[7]
output = sys.argv[8]

command = "./vom -dataset {} -k {} -t {} -r {} -q {} -score {} -mode {} -output {}".format(dataset, k, t, r, q, score, mode, output)
if score == "Cumulative":
	if mode == "RW":
		delta = intake("Value of delta: ")
		rho = intake("Value of rho: ")
		command += (" -delta {} -rho {}".format(delta, rho))
	elif mode == "Sketch":
		epsilon = intake("Value of epsilon: ")
		command += (" -epsilon {}".format(epsilon))
	else:
		assert False, "Invalid method"
elif score == "Plurality" or score == "p-Approval" or score == "Positional-p-Approval" or score == "Copeland":
	for x in range(r):
		if x != q:
			system("python MM.py {} {} {}".format(dataset, x, t))
	rho = intake("Value of rho: ")
	command += (" -rho {}".format(rho))
	if mode == "Sketch":
		theta = intake("Value of theta: ")
		command += (" -theta {}".format(theta))
	else:
		assert mode == "RW", "Invalid method"
	if score == "p-Approval" or score == "Positional-p-Approval":
		p = intake("Value of p: ")
		command += (" -p {}".format(p))
		if score == "Positional-p-Approval":
			command += " -weights"
			for i in range(p):
				w = intake("Value of omega[{}]: ".format(i + 1))
				command += (" {}".format(w))
else:
	assert False, "Invalid scoring function"
system(command)
