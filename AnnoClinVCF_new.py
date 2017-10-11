#!/usr/bin/env python
# -*- coding: utf-8 -*-

u"""AnoClinVCF
filename : AnnoClinVCF.py
Brief :  VCF -> SnpEff(classic) ->
         HGMD Annotation(HGMD_annotation.py) -> UniDB Annotation(SnpSift)
Author : Takuma Misawa, Amelieff Corporation
Usage : AnoClinVCF.py -i sample.ini -conf ConfigureFile.conf
"""
from argparse import ArgumentParser
import ConfigParser
import glob
import logging
import os
import subprocess
import sys


def ini_checker(ini, section):
    """
    if incorrect format ini file, this program is terminated.
    """
    init = ConfigParser.ConfigParser()
    init.optionxform = str
    init.readfp(open(ini))
    samples = init.items(section)
    for i in samples:
        print(i[0]+'\nfile path='+i[1])
        if len(i[1].split(',')) == 1:
            print('---> OK\n')
        else:
            print('invalid format...\n')
            sys.exit()
    return(samples)


def conf_checker(conf):
    """
    check and configure.
    """
    config = ConfigParser.ConfigParser()
    config.optionxform = str
    config.readfp(open(conf))
    section_name = config.sections()
    return(section_name, config)


def SectionNameAccesser(SettingsObject, SectionName, SearchWord):
    """
    get the run information from configure object derived from conf_checker
    """
    for i in SettingsObject.items(SectionName):
        if i[0] == SearchWord:
            return(i[1])


def ThrowShell(cmd):
    Tmp = subprocess.Popen(cmd, cwd=os.getcwd(), shell=True)
    Tmp.wait()
    return(Tmp)


def filter_vcf(vcf):
    """
    if the line have "AF = 0", eliminate the line
    output: header, mutation lines(list)
    """
    header = []
    mutation_lines = []
    for line in vcf.rstrip().split('\n'):
        try:
            if line.startswith("#"):
                header.append(line)
                continue
            else:
                comp = line.split('\t')
                AF_eq = comp[7].split(';')[0]
                AFs = AF_eq.lstrip('AF=').split(',')
                for AF in AFs:
                    if AF != '0':
                        mutation_lines.append(line)
        except:
            print("filter_vcf Error!")
            sys.exit()
    return header, mutation_lines


# ---- main ---- #


if __name__ == '__main__':
    print('AnoClinVCF was started !!')

    # create out put dir
    ResultDir = './AnoClinVCF'
    os.mkdir(ResultDir)

    # import external arguments
    parser = ArgumentParser(description='AnoClinVCF')
    parser.add_argument('-i', '--ini', nargs=1, type=str,
                        dest='ini', required=True,
                        help='ini file is required.')
    parser.add_argument('-c', '--conf', nargs=1, type=str,
                        dest='conf', required=True,
                        help='conf file is required.')
    args = parser.parse_args()
    logging.info('InputFiles: ' + args.ini[0] + '\t' + args.conf[0] + '\n')

    # Run ini_checker
    Samples = ini_checker(args.ini[0], 'vcf')
    print('# ---- TargetSample ---- #\n' +
          '\n'.join(['\n'.join(list(i)) for i in Samples]))

    # Run conf_checker
    SectionName, Settings = conf_checker(args.conf[0])

    # AnalysisStart
    os.chdir(ResultDir)

    # Parse VCF
    parsed_vcf = [k[0] + '_parsed.vcf' for k in Samples]
    for i, j in zip(Samples, parsed_vcf):
        parsecmd = 'vcf_parser {} --split > {}'.format(
            i[1], j)
        ThrowShell(parsecmd)
        print('vcf parser was performed: {}'.format(i[0] + '\n'))
        parsed_vcf.append(parsed_vcf)

    # Filter VCF
    filtered_vcf = [os.path.splittext(k) + '_filtered.vcf' for k in parsed_vcf]
    for i, j, k in zip(Samples, parsed_vcf, filtered_vcf):
        header, mutation_lines = filter_vcf(j)
        with open(k, "w") as wf:
            for line in header + mutation_lines:
                wf.write(line + '\n')
        print('filter vcf was performed: {}'.format(i[0] + '\n'))

    # SnpEff
    eff_vcf = [os.path.splittext(k) + '_eff.vcf' for k in filtered_vcf]
    for i, j, k in zip(Samples, filtered_vcf, eff_vcf):
        Effcmd = 'java -jar + \
            {} -s {}.html hg19 -formatEff {} > {}'.format(
                SectionNameAccesser(Settings, 'software', 'SnpEff'),
                i[0], j, k)
        ThrowShell(Effcmd)
        print('SnpEff was performed: {}'.format(i[0] + '\n'))

    # HGMD Annotation
    hgmd_vcf = [os.path.splittext(eff_vcf) + '_hgmd.vcf' for k in eff_vcf]
    for i, j, k in zip(Samples, eff_vcf, hgmd_vcf):
        HGMDcmd = 'python + \
            {} + -v + {} -o {} -s {}'.format(
                SectionNameAccesser(Settings, 'scripts', 'Python') +
                "/HGMD_annotation.py", j, k,
                SectionNameAccesser(Settings, 'files', 'hgmd'))
        ThrowShell(HGMDcmd)
        print('HGMD_annotation.py was performed: ' +
              i[0] + '\nCMD: ' + HGMDcmd)

    # SnpSift
    sift_vcf = [k[0] + 'full_annotation' for k in hgmd_vcf]
    for i, j, k in zip(Samples, hgmd_vcf, sift_vcf):
        Siftcmd = 'java -jar {} \
            annotate {} {} > {}'.format(
            SectionNameAccesser(Settings, 'software', 'SnpSift'),
            SectionNameAccesser(Settings, 'files', 'unidb'), j, k)
        ThrowShell(Siftcmd)
        print('SnpSift was performed: ' + i[0] + '\nCMD: ' + Siftcmd)

    # Delete Intermediate file
    [os.remove(i) for i in glob.glob("./*_parsed*.vcf")]
