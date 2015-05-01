#!/usr/bin/python
import re
import subprocess
import os

headings = 'headings.{}.txt'

corpus ='../corpora/en_wiki.txt'
query_words = ['bank','desert','close']

# Opening file pointers for all query words.
query_heads = [open(headings.format(word),"a") for word in query_words]

def analyze(text,heading):
	global headings
	for i,word in enumerate(query_words):
		if word in re.split('[\. \t\n]',text.strip()):
			# Writing to relevant file
			query_heads[i].write(heading)

fp = open(corpus,'r')

text = ''
ctr = 0
heading = None
for line in fp:
	if re.match(r'\[\[\d+\]\]',line.strip()) is not None:
		ctr += 1
		if ctr%10000 == 0: print "Analyzing Wikipedia article ",ctr
		analyze(text,heading)
		text = ''
	else:
		if text == '':
			heading = str(ctr)+"\t"+line
		text += line

fp.close()

# Closing all file pointers
for fp in query_heads:
	fp.close()
