fname = "glove.6B.300d.txt"
li = 400000	# Lines in glove.6B.300d.txt

import random
import numpy as np

def getvec(n):
	ans = [int(random.random()*li) for _ in range(n)]
	ans_vals = [0]*n
	fi = open(fname)
	for i,line in enumerate(fi):
		if i%50000 == 0: print i
		while i in ans:
			ans_vals[ans.index(i)] = np.array([float(x) for x in line.strip().split()[1:]])
			ans[ans.index(i)] = -1
	fi.close()
	return ans_vals

inputs = 50000

avgd = 0.0
minval = np.inf
maxval = -np.inf
rws = getvec(inputs*2)
for i in range(inputs):
	rw1 = rws.pop()
	rw2 = rws.pop()
	
	#d = float(np.dot(rw1,rw2)/(np.linalg.norm(rw1)*np.linalg.norm(rw)))
	d = np.linalg.norm(rw1-rw2)
	avgd += d
	minval = min(minval,d)
	maxval = max(maxval,d)

avgd /= inputs

# Average distance seems to be 4.9
# Maximum distance seems to be ~25
print avgd
print minval
print maxval
