import codecs
import os
from collections import Counter

fc = codecs.open("new_step2.dat","r","utf-8")
c = Counter(fc)
fc.close()

fo = codecs.open("new_step33.dat","w","utf-8")
for i,j in c.most_common(30000):
    fo.write(i.strip()+"\t"+str(j)+"\n")

fo.close()