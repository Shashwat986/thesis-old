#!/usr/bin/python
import re
import pickle
from copy import deepcopy
import os
import sys
import numpy as np

# Max number of articles to cluster
ARTICLE_LIMIT = 1000

# Similarity threshold for merging clusters
CLUSTER_THRESH = 0.2

def set_similarity(set1,set2):
	intersection = len(set1 & set2)
	union = len(set1 | set2)
	return 1.0*intersection/union

if len(sys.argv) < 3:
	print ("""Usage:
	$ analysis.py filename headings
	""")
	sys.exit(0)

if len(sys.argv) > 3:
	pkl_name = sys.argv[2]
	if not os.path.isfile(pkl_name):
		raise Exception("File Not Found")
	fp = open(pkl_name,"r")
	score = pickle.load(fp)
	fp.close()
	flag = True
else:
	# False flag means we need to calculate score.
	flag = False

fname = sys.argv[1]
hname = sys.argv[2]
if not os.path.isfile(fname) or not os.path.isfile(hname):
	raise Exception("File Not Found")

fp = open(fname)
if ARTICLE_LIMIT is not None:
	lines = []
	heads = []
	fp = open(fname)
	fh = open(hname)
	for i in range(ARTICLE_LIMIT):
		l = fp.readline()
		h = fh.readline()
		if l == '' or h == '':
			# If EOF
			break
		lines.append(l.strip())
		heads.append(h.strip())
else:
	lines = fp.readlines()
	heads = fh.readlines()

L = len(lines)

words = [0]*L
if not flag: score = np.zeros((L,L))

for i,line in enumerate(lines):
	if i % 1000 == 0: print "%d of %d lines parsed"%(i,L)
	if not flag: score[i,i] = -1.0

	words[i]  = set(line.strip().split())
	if not flag:
		for j in range(i):
			score[i,j] = set_similarity(words[i],words[j])
			score[j,i] = score[i,j]
	
fp.close()

print "Parsing done."

if not flag:
	print "Saving to score.pkl"
	fp = open("score.pkl","wb")
	pickle.dump(score, fp)
	fp.close()
	print "Saved."

print "Starting clustering"

# dist = deepcopy(score)
# Hierarchical Clustering. Will stop at k clusters.
k = 2

clusters = [[i] for i in range(L)]
cluster_map = range(L)
num_clusters = L

while num_clusters > k:
	if num_clusters % 100 == 0: print "%d clusters remaining. Reaching %d" % (num_clusters, k)
	i,j = np.unravel_index(score.argmax(), score.shape)

	#print "Point (%d,%d) is max with value %f" % (i,j,score[i,j])

	if CLUSTER_THRESH is not None and score[i,j] < CLUSTER_THRESH:
		print "Cluster threshold hit. Finishing"
		break

	score[i,j] = -1.0 # To find next cluster
	score[j,i] = -1.0

	if i > j:
		i,j = j,i
	# So i is smaller than j

	ci = cluster_map[i]
	cj = cluster_map[j]
	
	# Getting the latest cluster index
	while clusters[ci] is None and cluster_map[ci] != ci:
		#print ci, "is a None cluster (CI)."
		t = cluster_map[ci]
		cluster_map[ci] = cluster_map[t]
		ci = t
	while clusters[cj] is None and cluster_map[cj] != cj:
		#print cj, "is a None cluster (CJ)."
		t = cluster_map[cj]
		cluster_map[cj] = cluster_map[t]
		cj = t
	
	#print "Cluster maps to:",ci,cj
	
	if ci != cj:
		cluster_map[j] = ci

		# Just in case.
		if clusters[ci] is None and clusters[cj] is None:
			continue
		elif clusters[ci] is None:
			clusters[ci] = clusters[cj]
			clusters[cj] = None
		elif clusters[cj] is None:
			pass
		else:
			clusters[ci].extend(clusters[cj])
			clusters[cj] = None
			num_clusters -= 1

clusters = [c for c in clusters if c is not None]
print clusters
print "Clustering done."

'''
for i in range(L):
	ind = score[i].argmax()
	print words[i]
	print words[ind]
	print
'''
