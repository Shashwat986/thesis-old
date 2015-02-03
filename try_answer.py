import sys
import os
import codecs
import random
import numpy as np
import cPickle as pickle

PERC = 2 # Number of 0 values for every 1 value (target)
ELEMS = None #100000

fc = codecs.open("new_step33.dat","r","utf-8")
words = [k.split()[0] for k in fc.readlines() if len(k)>=1]
fc.close()
print "Read wordlist"

os.system("shuf -o input_datasetN.dat input_dataset1.dat")
print "Shuffled."

NUM_WORDS = 5
NUM_PARAMS = 30000
NUM_HID = 40

def sigmoid(x):
	return 1.0/(1.0+np.exp(-x))

if len(sys.argv)>1:
	pkf = open(sys.argv[1],'rb')
	w_ih = pickle.load(pkf)
	w_ho = pickle.load(pkf)
	pkf.close()
else:
	# Creating NN
	print "Creating NN"
	w_ih = [np.array([random.random()-0.5 for _ in xrange(NUM_PARAMS + 1)]) for __ in xrange(NUM_HID)]
	w_ho = np.array([random.random()-0.5 for _ in xrange(NUM_HID * NUM_WORDS + 1)])


def save(fn):
	global w_ih
	global w_ho
	print "Saving progress...",
	fo = open(fn,"wb")
	pickle.dump(w_ih,fo)
	pickle.dump(w_ho,fo)
	fo.close()
	print "done"

def train(ln, target):
	global w_ih
	global w_ho
	global words
	
	out_ih = []
	in_ih = []
	for i,word in enumerate(ln):
		in_tmp_ih = [0.0]*NUM_PARAMS
		in_tmp_ih[words.index(word)] = 1.0
		
		in_tmp_ih += [1] #Bias
		in_tmp_ih = np.array(in_tmp_ih)
		
		in_ih.append(in_tmp_ih)
		
		out_tmp_ih = [np.dot(in_tmp_ih,w_ih[i]) for i in xrange(NUM_HID)]
		out_tmp_ih = [sigmoid(x) for x in out_tmp_ih]
		out_ih += list(out_tmp_ih)
	
	out_ih += [1] # Bias
	out_ih = np.array(out_ih)
	out_ho = np.dot(out_ih,w_ho)
	out_ho = sigmoid(out_ho)
	
	delta_o = out_ho * (1.0 - out_ho) * (target - out_ho)	
	w_ho = np.add(w_ho, eta * delta_o * out_ih)
	
	delta_h = np.multiply(np.multiply(out_ih, (1.0 - out_ih)), w_ho * delta_o)
	delta_h = delta_h[:-1] # Removing Bias
	
	for i in xrange(NUM_WORDS):
		for j in xrange(NUM_HID):
			w_ih[j] = np.add(w_ih[j], eta * delta_h[j + i*NUM_WORDS] * in_ih[i])
	
	#print in_ih
	#print w_ih
	#print out_ih
	#print w_ho
	#print out_ho

eta = 0.01
print "Training"
ctr = 1
fi = codecs.open("input_datasetN.dat","r","utf-8")
try:
  for line in fi:
	if ctr%50 == 0: print "Input #{} of {}".format(ctr, ELEMS)
	if ctr%100000 == 0: save("save_state_{}".format(ctr))

	ctr += 1
	if ELEMS is not None and ctr > ELEMS: break
	
	ln = line.strip().split()
	# Input Validation
	if len(ln)!=NUM_WORDS: continue
	if any([k not in words for k in ln]): continue	

	
	train(ln, 1.0)
	for i in range(PERC):
		ln[NUM_WORDS // 2] = random.choice(words)
		train(ln, 0.0)
	
except KeyboardInterrupt:
  print "Saving Data"
  save("savedata_t.pkl")
  pass

fi.close()


save("savedata.pkl")
sys.exit(0)
