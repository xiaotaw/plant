#!/usr/bin/env python
# encoding=utf8
import re
import glob
import codecs
from collections import defaultdict
data_dir = "/data/DATASETS/nlp_data/parallel_corpus/en-zh/txt"

# english
en_r = re.compile("[^\s\w]")
en_counts = defaultdict(int)

en_files = glob.glob(data_dir + "/en_*.txt")
for en_file in en_files:
    print("process %s ..." % en_file)
    en_f = codecs.open(en_file, encoding="utf8", errors="ignore")
    for l in en_f:
        l = en_r.sub(" ", l).strip().split()
        for word in l:
            en_counts[word] += 1
    en_f.close()

en_f = codecs.open("en_vocab.txt", "w", encoding="utf8")
vocab = list(en_counts.items())
vocab.sort(key=lambda x: x[1], reverse=True)
for word, freq in vocab:
    _ = en_f.write("%s\t%d\n" % (word, freq))

en_f.close()



# chinese
zh_r_1 = re.compile("[^\s\w]")
zh_r_2 = re.compile(u"([\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff])")
zh_counts = defaultdict(int)

zh_files = glob.glob(data_dir + "/zh_*.txt")
for zh_file in zh_files:
    print("process %s ..." % zh_file)
    zh_f = codecs.open(zh_file, encoding="utf8", errors="ignore")
    for l in zh_f:
        l = zh_r_1.sub(" ", l)
        l = zh_r_2.sub(" \\1 ", l)
        l = l.strip().split()
        for word in l:
            zh_counts[word] += 1
    zh_f.close()

zh_f = codecs.open("zh_vocab.txt", "w", encoding="utf8")
vocab = list(zh_counts.items())
vocab.sort(key=lambda x: x[1], reverse=True)
for word, freq in vocab:
    _ = zh_f.write("%s\t%d\n" % (word, freq))

zh_f.close()
