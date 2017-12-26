#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
from Bio import SeqIO
from collections import OrderedDict


def GetFileName(genomes_dir):
    file_name_list = os.listdir(genomes_dir)
    return file_name_list


def GetFastaData(genomes_dir, file_name_list):
    id_list= []
    seq_parts_dict = {}
    for n, f in enumerate(file_name_list):
        if n == 0:
            with open(genomes_dir + '/' + f + '/genome.fa', 'r') as rf:
                for record in SeqIO.parse(rf, 'fasta'):
                    id_part = record.id
                    id_part_ = id_part.split('_')[1]
                    id_list.append(id_part_)
    for i in id_list:
        seq_parts_dict[i] = []
        for f in file_name_list:
            with open(genomes_dir + '/' + f + '/genome.fa', 'r') as rf:
                for record in SeqIO.parse(rf, 'fasta'):
                    if record.id.split('_')[1] == i:
                        seq = str(record.seq)
                        seq_parts_dict[i].append((f, seq))
    return id_list, seq_parts_dict


def JoinToFile(file_name_list, seq_parts_dict):
    contents = []
    for i, j in seq_parts_dict.items():
        with open(i, 'w') as wf:
            content = ''
            for k, l in j:
                content += '>' + k + '\n' + l + '\n'
            content.rstrip()
            wf.write(content)


def main():
    file_name_list = GetFileName(genomes_dir)
    id_list, seq_parts_dict = GetFastaData(genomes_dir, file_name_list)
    print(seq_parts_dict)
    JoinToFile(file_name_list, seq_parts_dict)


if __name__ == '__main__':
    genomes_dir = sys.argv[1]
    main()
