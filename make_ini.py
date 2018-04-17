#!usr/bin/env python

import os
import sys
import glob

def check_fastaq(f):
    _, ext = os.path.splitext(f)
    ok_ext_list = [".fa", ".fq", ".fasta", ".fastq"]
    return ext in ok_ext_list

def get_path(target_dir):
    path_list = [os.path.abspath(j) for j in glob.glob("{}/*".format(target_dir)) + glob.glob("{}/*/*".format(target_dir)) if check_fastaq(j) == True]
    return path_list

def get_name_list(path_list):
    name_list = [os.path.splitext(i.split('/')[-1])[0] for i in path_list]
    return name_list

def make_ini(output, name_list, path_list, filetype = 'fastq'):
    with open(output, 'w') as wf:
        wf.write('[{}]\n'.format(filetype))
        wf.write('\n'.join([i + '=' + j for i, j in zip(name_list, path_list)]))

if __name__ == '__main__':
    target_dir = sys.argv[1]
    path_list = get_path(target_dir)
    name_list = get_name_list(path_list)
    make_ini('output.ini', name_list, path_list)
