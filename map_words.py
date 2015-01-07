import sys
import pickle
import codecs
import numpy as np

NUM_PARAMS = 30000
NUM_HID = 40

if len(sys.argv)<=1:
	sys.exit(1)

pkl = open(sys.argv[1],"rb")
w_ih = pickle.load(pkl)
w_ho = pickle.load(pkl)
pkl.close()

fc = codecs.open("new_step33.dat","r",encoding = "utf-8")
words = [k.split()[0] for k in fc.readlines() if len(k)>=1]
fc.close()

print "Creating current status..."
fo = codecs.open("prog.dat","w",encoding="utf-8")
for i,word in enumerate(words):
	if i%100 == 0: print "Word #{} of {}".format(i+1,len(words))
	fo.write(word + "\t")
	inp = [0.0]*NUM_PARAMS
	inp[i] = 1.0
	inp.append(1.0) # Bias
	inp = np.array(inp)
	
	out = [np.dot(inp,w_ih[j]) for j in xrange(NUM_HID)]

	fo.write(" ".join([str(j) for j in out]))
	fo.write("\n")
fo.close()
print "done"

