#!/usr/bin/python
import re
import subprocess
import os
from glove import Corpus, Glove

NUM_EPOCHS = 15
NUM_THREADS = 4

corpus ='../corpora/en_wiki.txt'
query_words = ['bank','desert','close']

out_fp = [open('vectors/vectors.{}.txt'.format(word),"w") for word in query_words]
head_fp = [open('vectors/headings.{}.txt'.format(word), "w") for word in query_words]

def analyze(text,heading):
	# Analyze corpus
	corpus_model = Corpus()
	corpus_model.fit([line.strip().split() for line in re.split('[\.\n]',text) if len(line.strip().split())!=0], window = 10)
	corpus_model.save('corpus.model')

	# Train GloVe model.
	glove = Glove(no_components = 100, learning_rate = 0.05)
	glove.fit(corpus_model.matrix, epochs = NUM_EPOCHS, no_threads = NUM_THREADS, verbose = False)
	glove.add_dictionary(corpus_model.dictionary)
	glove.save('glove.model')
	
	for i,word in enumerate(query_words):
		try:
			_ = glove.dictionary[word]
		except KeyError:
			continue
		else:
			#vec = " ".join(map(str,glove.word_vectors[glove.dictionary[word]]))
			vec = " ".join([w[0] for w in glove.most_similar(word, number = 10)])
			out_fp[i].write(vec + "\n")
			occurrences = re.findall(".{0,10}"+word+".{0,10}",text)
			head_fp[i].write(heading.strip() + "\t[" + "|".join([" ".join(c.split()) for c in occurrences]) + "]\n")

print "Analyzing text"

fp = open(corpus,'r')

text = ''
vectors = []
ctr = 0
heading = ''
for line in fp:
	if re.match(r'\[\[\d+\]\]',line.strip()) is not None:
		ctr += 1
		if ctr % 100 == 0: print "Analyzing Wikipedia article ",ctr
		analyze(text,heading)
		text = ''
	else:
		if text == '':
			heading = str(ctr) + "\t" + line
		text += line

fp.close()

for fp in out_fp:
	fp.close()

for fp in head_fp:
	fp.close()
