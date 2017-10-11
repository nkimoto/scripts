#!/usr/bin/env python
# -*- coding: utf-8 -*-

u"""RAPIDAnnotator
filename : RAPIDAnnotator.py
Brief : Annotate the input ID list. Source: RAP-DB
Author : Takuma Misawa, Amelieff Corporation
Usage : python RAPIDAnnotator.py -i IDList.txt -l locus.gff -t transcripts.gff -e transcripts_exon.gff
"""

from argparse import ArgumentParser
import datetime
import logging
import os
import subprocess
import sys
import time

def ApplyLocusID(input_file, lc_gff):
    logging.info('Now processing by using locus.gff as reference')
    ALIDres = []
    with open(input_file, 'r') as f:
        for i in f:
            found = 0
            with open(lc_gff, 'r') as lc:
                for j in lc:
                    if j.find('ID=' + i.strip() + ';') >= 0:
                        ALIDres.append(j)
                        found = 1
            if found == 0:
                ALIDres.append('Not found...\n')
    return(ALIDres)



def ApplyTransVariant(ALIDres, tr_gff, te_gff):
    logging.info('Creating target transcriptome list...')
    with open('AllInformation.txt', 'w') as f:
        header = ['GeneChr', 'GeneSource', 'GeneType', 'GeneStart', 'GeneEnd', 'GeneScore', 'GeneStrand', 'GeneFrame', 'GeneAttr', 'Tr1Chr', 'Tr1Source', 'Tr1Type', 'Tr1Start', 'Tr1End', 'Tr1Score', 'Tr1Strand', 'Tr1Frame', 'Tr1Attr', 'Tr2Chr', 'Tr2Source', 'Tr2Type', 'Tr2Start', 'Tr2End', 'Tr2Score', 'Tr2Strand', 'Tr2Frame', 'Tr2Attr', 'Tr3Chr', 'Tr3Source', 'Tr3Type', 'Tr3Start', 'Tr3End', 'Tr3Score', 'Tr3Strand', 'Tr3Frame', 'Tr3Attr', 'Tr4Chr', 'Tr4Source', 'Tr4Type', 'Tr4Start', 'Tr4End', 'Tr4Score', 'Tr4Strand', 'Tr4Frame', 'Tr4Attr', 'Tr5Chr', 'Tr5Source', 'Tr5Type', 'Tr5Start', 'Tr5End', 'Tr5Score', 'Tr5Strand', 'Tr5Frame', 'Tr5Attr', 'Tr6Chr', 'Tr6Source', 'Tr6Type', 'Tr6Start', 'Tr6End', 'Tr6Score', 'Tr6Strand', 'Tr6Frame', 'Tr6Attr', 'Tr7Chr', 'Tr7Source', 'Tr7Type', 'Tr7Start', 'Tr7End', 'Tr7Score', 'Tr7Strand', 'Tr7Frame', 'Tr7Attr', 'Tr8Chr', 'Tr8Source', 'Tr8Type', 'Tr8Start', 'Tr8End', 'Tr8Score', 'Tr8Strand', 'Tr8Frame', 'Tr8Attr', '\n']
        f.write('\t'.join(header))
    for i in ALIDres:
        ATVres = []
        if i.strip() != 'Not found...':
            Attr = i.strip().split('\t')[8].split(';')
            for j in Attr:
                if j.startswith('Transcript variants='):
                    Tv = str(j)
                    Targetid = Tv.split('=')[1:]
                    for tg in Targetid:
                        if len(tg.split(',')) != 1:
                            for k in tg.split(','):
                                tg = k
                                ATVres.append(tg)
                        else:
                            ATVres.append(tg)
        else:
            ATVres.append('Not found...\n')

        LocRes = i.split('\n')[:-1]
        with open('AllInformation.txt', 'a') as ATVRES:
            logging.info('Now processing by using transcripts.gff')
            for ii in ATVres:
                with open(tr_gff, 'r') as r:
                    for jj in r:
                        if jj.find('ID=' + ii.strip() + ';') >= 0:
                            LocRes.append(jj.strip())

            logging.info('Now processing by using transcripts_exon.gff')
            for ii in ATVres:
                with open(te_gff, 'r') as r:
                    for jj in r:
                        if jj.find('ID=' + ii.strip() + ';') >= 0:
                            LocRes.append(jj.strip())
            ATVRES.write('\t'.join(LocRes) + '\n')

# -- main -- #
if __name__ == '__main__':

    # create result directory
    ResultDir = 'RAPIDAnnotator_' + \
        datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    os.mkdir(ResultDir)
    os.mkdir(ResultDir + '/log')
    logging.basicConfig(level = logging.INFO, \
                        filename = ResultDir + '/log/' + \
                        ResultDir + '.log')
    logging.info('function start at ' + \
                datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '\n')

    # ---- settings argparse ---- #
    usage = 'python RAPIDAnnotator.py -i IDList.txt -l locus.gff -t transcripts.gff -e transcripts_exon.gff'
    parser = ArgumentParser(description='RAPIDAnnotator')
    parser.add_argument('-i', '--input_file', nargs = 1, type = str, \
                        dest = 'input_file', required = True, \
                        help = 'ID_List file is required.')
    parser.add_argument('-l', '--locus_gff', nargs = 1, type = str, \
                        dest = 'lc_gff', required = True, \
                        help = 'locus.gff is required.')
    parser.add_argument('-t', '--transcripts_gff', nargs = 1, type = str, \
                        dest = 'tr_gff', required = True, \
                        help = 'transcripts.gff is required.')
    parser.add_argument('-e', '--transcripts_exon_gff', nargs = 1, type = str, \
                        dest = 'te_gff', required = True, \
                        help = 'transcripts_exon.gff is required.')


    args = parser.parse_args()

    os.chdir(ResultDir)
    ALIDres = ApplyLocusID(args.input_file[0], args.lc_gff[0])
    ApplyTransVariant(ALIDres, args.tr_gff[0], args.te_gff[0])
    # ResultFormatter()
    os.chdir('../')

    sys.exit('All process was done !!')
