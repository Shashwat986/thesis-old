import os
import random
from math import sqrt

lines = None
outs = None

def _initialize(spc):
	global lines
	global outs
	# Prevent repitition.
	if lines is not None and outs is not None:
		return lines, outs
	
	if not os.path.exists("phrase2word.{}.input.tsv".format(spc)):
		raise IOError("File type incorrect")
	fd = open("phrase2word.{}.input.tsv".format(spc),"r")
	lines = [line.strip().split('\t') for line in fd.readlines()]
	fd.close()
	
	fo = open("phrase2word.{}.gs.tsv".format(spc),"r")
	outs = [float(line.strip()) for line in fo.readlines()]
	fo.close()

	if len(lines) != len(outs):
		raise IOError("Wrong file lengths")

	return lines, outs

def test_cases():
	lines,outs = _initialize("test")
	for i in range(len(outs)):
		yield (lines[i], outs[i])

def train_cases():
	lines,outs = _initialize("train")
	for i in range(len(outs)):
		yield (lines[i], outs[i])

def score(f):
	lines, outs = _initialize("test")
	calcouts = []
	l = len(outs)
	for i in range(l):
		calcouts.append(f(lines[i][0], lines[i][1]))
	
	return pearson(outs,calcouts)

def pearson(r1,r2):
	l = len(r1)
	mean_1 = 1.0*sum(r1)/l
	mean_2 = 1.0*sum(r2)/l
	
	pearson = 0.0
	s_xy = 0.0
	s_xx = 0.0
	s_yy = 0.0
	for i in range(l):
		s_xy += (r1[i] - mean_1) * (r2[i] - mean_2)
		s_xx += (r1[i] - mean_1) ** 2
		s_yy += (r2[i] - mean_2) ** 2
	
	if s_xx == 0 or s_yy == 0:
		return None
	
	pearson = 1.0 * s_xy / (sqrt(s_xx) * sqrt(s_yy))
	
	return pearson

if __name__ == '__main__':
	def f(w1,w2):
		return random.random()*4
	
	'''
	SOTA is 0.457 correlation. http://alt.qcri.org/semeval2014/task3/index.php?id=results
	'''
	
	print score(f)