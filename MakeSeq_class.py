# /usr/bin/env python

import os
from Bio import SeqIO

class MakeSeq():
    def __init__(self, input_dir, output_dir, ref):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.ref = ref

    def read_filtered_files(self, fdir):
        tmp_list = []
        files_list = os.listdir(fdir)
        for i in [f for f in files_list if 'freqfiltered' in f]:
            with open(fdir + '/' + i, 'r') as rf:
                for line in rf.readlines():
                    comp = line.split('\t')
                    tmp = (comp[0], int(comp[1]), comp[3], comp[4])
                    tmp_list.append(tmp)
        tmp_list = list(set(tmp_list))
        return sorted(tmp_list, key = lambda snp : snp[1])

    def insert(self, snp_list, reference):
        res = []
        for record in SeqIO.parse(reference, 'fasta'):
            ref = record.seq
            pos_add = 0
            for snp in [s for s in snp_list if s[0] == record.id]:
                ref_pref = ref[:snp[1] - 1 + pos_add]
                if len(snp[2]) > len(snp[3]):
                    pos_add -= len(snp[3]) - len(snp[2])
                    ref_suff = ref[len(ref_pref) + len(snp[3]) + 1:]
                elif len(snp[2]) == len(snp[3]):
                    pass
                else:
                    pos_add += len(snp[3]) - len(snp[2])
                    ref_suff = ref[len(ref_pref) + len(snp[3]) + 1:]
                ref = str(ref_pref) + snp[3] + str(ref_suff)
            res.append('>' + record.id)
            res.append(ref)
        return res

    def write_to_file(self, output, res_list):
        file_path = os.path.dirname(output)
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        with open(output, 'w') as wf:
            wf.write('\n'.join(res_list))

    def main(self):
        input_list = self.read_filtered_files(self.input_dir)
        res_list = self.insert(input_list, self.ref)
        self.write_to_file(self.output_dir, res_list)
