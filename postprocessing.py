# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import scipy
from sklearn.neighbors import KNeighborsClassifier
from scipy.cluster import hierarchy as hier
from scipy.spatial import distance
import json
import codecs

matplotlib.rc('font', **{'sans-serif' : 'Arial', 'family' : 'sans-serif'})

SIZE = 30000

print "Start"
fi = codecs.open("prog.dat","r","utf-8")
words = []
data = []
ctr = 0
for line in fi:
	if ctr > SIZE: break
	ctr += 1
	
	if not len(line.strip()): continue
	k = line.strip().split()
	words.append(k[0])
	data.append([float(i) for i in k[1:]])

fi.close()

vectors = np.array(data)

print "Pre-processing done"

# Calculate the distance matrix
def dist(x,y):
	return np.dot(x,y)
'''
links = hier.linkage(dist)

plt.figure(101)
hier.dendrogram(links, labels = words)
#plt.show()
#'''

knn = KNeighborsClassifier()
knn.fit(vectors,[0]*len(vectors))

fo = codecs.open("nn9m.dat","w","utf-8")
for i,word in enumerate(words):
	d,n = knn.kneighbors(vectors[i], n_neighbors = 5, return_distance = True)
	if i%1000==0: print d,n
	fo.write(word+"\t")
	for j in range(1,len(n[0])):
		fo.write(words[n[0][j]]+" ({:.6f}), ".format(d[0][j]))
	fo.write("\n")
fo.close()



'''
# -- K-Means --
from scipy.cluster.vq import kmeans2, vq, kmeans
nClust = 5
centroid, _ = kmeans(vects2,nClust)
idx, ds = vq(vects2, centroid)

fp = open('kmeans'+q+'.txt','w')
for i in range(nClust):
	for j,x in enumerate(idx):
		if i==x:
			fp.write("C"+str(x)+"\t")
			fp.write(str(j+1)+"\t")
			fp.write(titles[j]+"\n")
	fp.write('\n')
fp.close()

print idx

# --

hts = [l[2] for l in links]
alpha = int(SAMPLE_SIZE * 0.2)



# Display Graphs using Mathematica
fp = open("./array.nb","w")
# Convert to a format Mathematica understands
fp.write('Needs["HierarchicalClustering`"]'+'\n')

fp.write("vectlist = ")
fp.write(str(vects2_f.tolist()).replace('[','{').replace(']','}'))
fp.write('\n')

fp.write("labels = ")
fp.write('{')
fp.write(','.join(['"'+title.replace('"',"'")+'"' for title in titles]))
fp.write('}')
fp.write('\n')

fp.write("range = " + str(x_axis_f).replace('[','{').replace(']','}'))
fp.write('\n')

fp.write('diag=DendrogramPlot[vectlist, LeafLabels->range, PlotLabel->"'+q+'", ImageSize->1000,Linkage->Single]'+'\n')
fp.write(r'Export["'+q+r'.png",diag]'+'\n')

fp.write("height = " + str(hts).replace('[','{').replace(']','}'))
fp.write('\n')
fp.write('diag=ListPlot[height]\n')
fp.write(r'Export["'+q+r'_ht.png",diag]'+'\n')

fp.write("htdiff = " + str(htd).replace('[','{').replace(']','}'))
fp.write('\n')
fp.write('diag1=ListPlot[htdiff, ImageSize->1000, PlotRange->All]\n')
fp.write(r'Export["'+q+r'_htdiff.png",diag1]'+'\n')


fp.close()

#'''
