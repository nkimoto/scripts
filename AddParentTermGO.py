#!/usr/bin/env python
# -*- coding: utf-8 -*-

u"""
filename : AddParentTermGO.py
Brief : add parent term of GO to the result of RAPIDAnnotator.py
Author : Takuma Misawa, Amelieff Corporation
Usage : python AddParentTermGO.py AllInformation.txt misawat mygo
"""

import os
import sys
import re
import MySQLdb

def MySQLConnector(SearchWord, USERname, DBname):
    connection = MySQLdb.connect(user = USERname, db = DBname)
    cursor = connection.cursor()
    sql = "SELECT child.term_type AS ontology, child.acc AS child_acc, child.name AS child_name, rel.acc AS rel_acc, parent.acc AS parent_acc, parent.name AS parent_name FROM term AS child INNER JOIN term2term ON (child.id=term2_id) INNER JOIN term AS parent ON (parent.id=term1_id) INNER JOIN term AS rel ON (rel.id=relationship_type_id) WHERE child.acc = '" + SearchWord + "'"
    cursor.execute(sql)
    SQLOut = cursor.fetchall()
    res = []
    for i in SQLOut:
        res.append('%'.join(i[4:]))
    return(res)

# -- main -- #
if __name__ == '__main__':

    args = sys.argv
    with open('ParentGO.txt', 'w') as Out:
        with open(args[1], 'r') as f:
            for i in f:
                TermResAll = []
                if i != 'Not found...\n' and not i.startswith('GeneChr'):
                    for Tr in range(1,11):
                        TermRes = []
                        try:
                            Attr = i.split('\t')[8 + 9*Tr].split(';')
                            Anno = 0
                            for j in Attr:
                                if j.startswith('GO='):
                                    regex = r'GO:.{7}'
                                    pattern = re.compile(regex)
                                    child = re.findall(pattern, j)
                                    for k in child:
                                        Parent = MySQLConnector(k, args[2], args[3])
                                        TermRes.append('ChildTerm:' + k)
                                        for l in Parent:
                                            TermRes.append('ParentTerm:' + l)
                                    Anno = 1
                                    TermResAll.append('^'.join(TermRes))
                            if Anno == 0:
                                TermResAll.append('Not found...') # test
                        except:
                            break
                    Out.write('\t'.join(TermResAll) + '\n')
                elif i.startswith('GeneChr'):
                    Out.write('Tr1GO\tTr2GO\tTr3GO\tTr4GO\tTr5GO\tTr6GO\tTr7GO\tTr8GO\tTr9GO\tTr10GO\n')
                else:
                    Out.write('Not found...\n')
