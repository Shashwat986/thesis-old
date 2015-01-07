import codecs

fc = codecs.open("new_step33.dat","r","utf-8")
words = [k.split()[0] for k in fc.readlines() if len(k)>=1]
fc.close()

fm = codecs.open("new_step1.dat","r","utf-8")
fo = codecs.open("input_dataset1.dat","w","utf-8")

for line in fm:
    l = line.strip().split()
    if len(l) < 5:
        continue
    for i in xrange(len(l)-5):
        if all([l[i+k] in words for k in range(5)]):
            fo.write(" ".join(l[i:i+5])+"\n")

fo.close()
fm.close()