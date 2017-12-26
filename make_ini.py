#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
from collections import OrderedDict

def make_ini_dict(fastq_dir):
    sample_list = sorted(os.listdir(fastq_dir), key = lambda x: int(x[:2]) if x[:2].isdigit() else int(x[0]))
    sample_dict = OrderedDict()
    for n, i in enumerate(sample_list):
        prefix = i.split('_R')[0]
        for j in sample_list[n + 1:]:
            if prefix in j:
                sample_dict[prefix] = [fastq_dir + i, fastq_dir + j]
                break
    return sample_dict

def make_ini(sample_dict, ini):
    writelines =[]
    for sample, fq_list in sample_dict.items():
        writelines.append(sample + '=' + fq_list[0] + ',' + fq_list[1])
    with open(ini, 'w') as wf:
        wf.write('[fastq]\n' + '\n'.join(writelines))

if __name__ == '__main__':
    args = sys.argv
    sample_dict = make_ini_dict(args[1])
    make_ini(sample_dict, 'test.ini')
