#!/usr/bin/env python
# -*- coding: utf-8 -*-
Rice_IDs = []
f = open("result.txt" , mode = "a+")
with open("ListTop100.txt",mode = 'r') as imput:
 for a in imput:
  Rice_IDs.append(a)
#for Rice_ID in Rice_IDs:
 Rice_ID = Rice_IDs[0].strip()##
 orthologous_group_ID = []
 GO_ID = []
 for line in open("APK_ftp_file2.txt",'r'):
  itemList = line[:-1].split('\t')
  orthologs = itemList[4].split(' ')#List
  orthologs_conma = ','.join(orthologs)
  if orthologs_conma.find(Rice_ID) > -1:
   orthologous_group_ID.append(itemList[0])
   Arabidopsis_ID = [arg for arg in orthologs if arg[0] == 'A'] #List
   Arabidopsis_ID_joined = ','.join(Arabidopsis_ID)
   for Line in open("ATH_GO_GOSLIM.txt",'r'):
    itemlist = Line.strip('\n').split('\t')
    if Arabidopsis_ID_joined.find(itemlist[0].strip()) > -1:
     GO_ID.append(itemlist[5])
    else:
     continue

 if Arabidopsis_ID == []:
   orthologous_group_ID.append("Not found...")
 f.write(Rice_ID.rstrip('\r\n') + "\t" + \
	','.join(orthologous_group_ID) + "\t" + \
	','.join(Arabidopsis_ID) + "\t" +\
	','.join(GO_ID) + "\n")
f.close()
