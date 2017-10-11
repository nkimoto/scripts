#!/usr/bin/env python
# -*- coding: utf-8 -*-
def rap_msu_converter(rap_msu_database,rap_input):
  msu_list = []
  with open(rap_input,'r') as rap_lines:
    rap_list = [rap_line.strip() for rap_line in rap_lines]
  for rap in rap_list:
    with open(rap_msu_database,'r') as rap_msu_datas:
      for rap_msu_data in rap_msu_datas:
        rap_msu_list = rap_msu_data.split('\t')
        if rap_msu_list[0] == 'None':
          continue
        if rap_msu_list[0] == rap:
          if rap_msu_list[1].strip() == 'None':
            msu_list.append(rap_msu_list[1].strip())
            break
          else:
            msu_list.append(rap_msu_list[1][:14])
            break
      else:
        msu_list.append('Not found...')
  return(msu_list)

def msu_ortho(msu_list,rice_ortho_database):

  '''
  イネのID(Os##g#####)からオーソロガス遺伝子を辞書にして返す。
  '''

  ortho_list = []
  for msu in msu_list:
    if msu == 'None' or msu =='Not found...':
      ortho_list.append('.')
      continue
    with open(rice_ortho_database,'r') as ortho_datas:
      for ortho_data in ortho_datas:
        ortho_data_list = ortho_data[:-1].split('\t')
        ortho_genes_list = ortho_data_list[4].split(' ')
        ortho_genes_comma = ','.join(ortho_genes_list)
        if ortho_genes_comma.find(msu.strip()) > -1:
          ortho_list.append(ortho_data_list[0])
          break
      else:
        ortho_list.append('Not found...')
  return(ortho_list)

def ortho_arabi(ortho_list,rice_ortho_database):
  '''
  オーソロガス遺伝子(APK_ORTHOMCL####)のリストからNot found...のものを除いてシロイヌナズナのホモログを辞書にして返す。
  '''
  arabi_list = []
  for ortho in ortho_list:
    if ortho == '.' or ortho == 'Not found...':
      arabi_list.append('.')
      continue
    arabi_in_list = []
    with open (rice_ortho_database,'r') as ortho_datas:
      for ortho_data in ortho_datas:
        ortho_data_list = ortho_data[:-1].split('\t')
        ortho_search_word = ortho_data_list[0] + '\n'
        if ortho_search_word.find(ortho + "\n") > -1:#検索のため改行を含める
          ortho_genes_list = ortho_data_list[4].split(' ')
          extend_list = [arg for arg in ortho_genes_list if arg[:2] == 'AT']
          arabi_in_list.extend(extend_list)
          break
      if arabi_in_list == []:
        arabi_in_list.append('Not found...')
    arabi_list.append(arabi_in_list)
  return(arabi_list)

def arabi_GO(arabi_list,arabi_GO_database):
  '''
  シロイヌナズナのAGIコード(AT#G#####)のリストinリストからGOをリストinリストinリストにして返す。
  '''
#  arabi_GO = {}
  GO_list = []
#  with open(arabi_lists,'r') as arabis:
  for arabi_in_list in arabi_list:
    if arabi_in_list == '.':
      GO_list.append('.')
      continue
    if arabi_in_list == ['Not found...']:
      GO_list.append('Not found...')
      continue
    GO_in_list = []
    for arabi in arabi_in_list:
      GO_in_in_list = []
      with open(arabi_GO_database,'r') as arabi_datas:
        for arabi_data in arabi_datas:
          arabi_data_list = arabi_data[:-1].split('\t')
          arabi_serch_word = arabi_data_list[0] + '\n'
          if arabi_serch_word.find(arabi + '\n') > -1:
            GO_in_in_list.append(arabi_data_list[5] + '-' + arabi_data_list[8])
            continue
      if GO_in_in_list == []:
        GO_in_in_list.append('GO:Not found...')
      GO_in_list.append(GO_in_in_list)
    GO_list.append(GO_in_list)
  return (GO_list)

def writer(output):
  '''
  outputファイルへの書き込みを行う。
  '''
  with open(output,'w') as result:
    result.write('RAPID\t' + 'MSUID\t' + 'OrthologousID\t' + 'ArabiGO\n')
    write_terms_list = []
    for output_arabis,output_GOs_list in zip(arabi_list,GO_list):
      if output_GOs_list == '.' or output_GOs_list == 'Not found...':
        write_terms_list.append(output_GOs_list)
        continue
      write_terms_in_list = []
      for output_arabi,output_GOs in zip(output_arabis,output_GOs_list):
        write_terms_in_list.append(output_arabi + '=' + ';'.join(output_GOs))
      write_terms_list.append('^'.join(write_terms_in_list))
    for input_rap,output_msu,output_ortho,write_term in zip(rap_list,msu_list,ortho_list,write_terms_list):
      result.write(input_rap + '\t' + output_msu + '\t' + output_ortho + '\t' + write_term + '\n')
if __name__ == '__main__':
  import sys
  args = sys.argv
  rap_msu_DATABASE = args[1]
  rap_LIST = args[2]
  rice_ortho_DATABASE = args[3]
  arabi_GO_DATABASE = args[4]
  output_file = args[5]
#  rap_msu_dic = rap_msu_converter(rap_msu_DATABASE,rap_LIST)
#  rice_ortho_dic = riceID_ortho(rap_msu_dic.values(),rice_ortho_DATABASE)
#  ortho_arabi_dic = ortho_arabi(rice_ortho_dic.values(),rice_ortho_DATABASE)
#  arabi_GO_dic = arabi_GO(ortho_arabi_dic.values(),arabi_GO_DATABASE)
  with open(rap_LIST,'r') as rap_lines:
    rap_list = [rap_line.strip() for rap_line in rap_lines]
  msu_list = rap_msu_converter(rap_msu_DATABASE,rap_LIST)
  ortho_list = msu_ortho(msu_list,rice_ortho_DATABASE)
  arabi_list = ortho_arabi(ortho_list,rice_ortho_DATABASE)
  GO_list = arabi_GO(arabi_list,arabi_GO_DATABASE)
  arabi_list = ortho_arabi(ortho_list,rice_ortho_DATABASE)
  GO_list = arabi_GO(arabi_list,arabi_GO_DATABASE)
  GO_list = arabi_GO(arabi_list,arabi_GO_DATABASE)


#  for input_rice in rice_ortho_dic.keys():
#    print(input_rice.strip(),end = '\t')
#    output_ortho = rice_ortho_dic[input_rice]
#    print(output_ortho.strip(),end = '\t')
#    if output_ortho != 'Not found...':
#      output_arabis = ortho_arabi_dic[output_ortho]
#      print(output_arabis,end = '\t')
#      for output_arabi in output_arabis:
#        output_GO = arabi_GO_dic[output_arabi]
#        print(output_arabi + '=' + ';'.join(output_GO) + '^',end = '')
#    else :
#      print('')
  writer(output_file)
"""
Usage : rap_to_arabiGO.py riceID_LIST rice_ortho_DATABASE arabi_GO_DATABASE outp                                                                                                             ut_file
"""
