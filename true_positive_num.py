#!/usr/bin/env python
# -*- coding: utf-8 -*-
ans_list = []
check_list = []
matched_list =[]

for line in open('new_ans_sample'):
	ans_list.append(line)
for line in open('new_check_sample'):
	ans_list.append(line)

for i in check_list:
	matched_list += filter(lambda j: i == j,ans_list)
print len(matched_list)
