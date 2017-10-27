#!/usr/bin/env python
# -*- coding: utf-8 -*-

u"""UrlGetter
filename : PubMedURLGetter.py
Brief : Extract searched results(url)
Author : Naoki Kimoto
Usage : PubMedURLGetter.py -k keyword
"""
from argparse import ArgumentParser
import re
import os
import sys
# import time
from selenium import webdriver
from bs4 import BeautifulSoup
DRIVER_PATH = os.path.join(
    os.path.realpath(__file__).rsplit('/', 1)[0], 'phantomjs')


def GetSearchResultURL(keyword):
    PubHome = 'https://www.ncbi.nlm.nih.gov/pubmed/?'

    URL = PubHome + 'term=' + keyword
    return(URL)


def GetAllURL(SearchResultURL):
    PubHome = 'https://www.ncbi.nlm.nih.gov/pubmed'
    driver = webdriver.PhantomJS(DRIVER_PATH)
    driver.get(SearchResultURL)
    PaperURLList = []
    while True:
        Html = driver.page_source.encode('utf-8')
        Soup = BeautifulSoup(Html, 'html.parser')
        Tagdd = Soup.find_all('dd')
        TagRemovePatt = r'<.*?>'
        TagRemover = re.compile(TagRemovePatt)
        PaperID = [TagRemover.sub('', str(j)) for j in Tagdd]
        PaperURLs = [PubHome + '/' + i for i in PaperID]
        PaperURLList.extend(PaperURLs)
        try:
            next_page_links = driver.find_elements_by_css_selector(
                'div.pagination > a[class="active page_link next"]')
            next_page_links[0].click()
#            time.sleep(1)
        except:
            break
    return(PaperURLList)
    driver.quit()


if __name__ == '__main__':
    # import external arguments
    Parser = ArgumentParser(description='URLGetter')
    Parser.add_argument('-k', '--keyword',
                        nargs=1,
                        type=str,
                        dest='keyword',
                        required=True,
                        help='keyword is required.')
    Parser.add_argument('-o', '--output',
                        nargs='?',
                        type=str,
                        dest='output',
                        default='result.txt',
                        help='Output file name.<option>')
    Args = Parser.parse_args()
    # Start
    print('URLGetter start !')
    # Get Search Result URL
    SearchResultURL = GetSearchResultURL(Args.keyword[0])
    # Get All URL List
    try:
        PaperURLList = GetAllURL(SearchResultURL)
        print('%d papers hitted!' % len(PaperURLList))
    except:
        sys.exit('Referance was not detected...')
    # Output to result.txt
    with open(Args.output[0], 'w') as f:
        f.write('[' + Args.keyword[0] + ']' + '\n')
        for l in PaperURLList:
            f.write(l + '\n')
    print('URLGetter end !')
