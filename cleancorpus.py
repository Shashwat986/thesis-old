#!python
# -*- coding: utf-8 -*-

import codecs

fp = codecs.open('hindi-wiki.xml','r','utf-8')
fo = codecs.open('new_step1.dat','w','utf-8')

newlist = []
flag = True
ctr=-1
for ln in fp:
    for lett in ln:
        ctr +=1
        if ctr%10000==0:
            print ctr
        
        # Hindi Unicode range (approximately)
        if (2300<=ord(lett)<=2420) or lett in [' ', '\n','\t']:
            if ord(lett) == 2404:
                fo.write('\n')
            else:
                fo.write(lett)
                flag = False
        elif flag==True:
            pass
        else:
            fo.write(" ")
            flag = True
    
fp.close()
fo.close()
