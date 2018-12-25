#!/usr/bin/python3.6
""" =================================== ~ Python3.6 Webcrawler - Mitterlabill, 02.08.2018 | 11:48 ~ =================================== """

""" [main.py]: Imports ================================================================================================================ """
import requests as req
from bs4 import BeautifulSoup
import urllib.parse
import json

from colorama import init
init()
from colorama import Fore, Back, Style

""" [main.py]: Main Code ============================================================================================================== """
class Set(set):
    def get(self, index):
        if index >= len(self):
            return None

        seti = iter(self)
        for i in range(index):
            next(seti)
        return next(seti)

def meta_info_tag_descriptor(tag):
    return tag.get('name') == 'description' or tag.get('name') == 'keywords' or tag.get('name') == 'author' or tag.name == 'title'

def crawl(urls, json_dict):
    i = 0
    try:
        while urls.get(i) != None:
            curl = urls.get(i)
            print(Fore.LIGHTYELLOW_EX, "[%05d/%05d] Current URL: " % (i+1, len(urls)), curl, Fore.RESET)
        
            try:
                html_doc = req.get(curl, timeout=10).text
            except Exception:
                print(Fore.LIGHTRED_EX + " [-] '" + curl + "' didn't respond ...")

                i += 1
                continue

            soup = BeautifulSoup(html_doc, "html.parser")
            
            descr_str = ''
            for descriptor in soup.find_all(meta_info_tag_descriptor):
                if len(descriptor.contents) > 0:
                    if descriptor.contents[0]:
                        descr_str += ' ' + descriptor.contents[0]
                else:
                    if descriptor.get('content'):
                        descr_str += ' ' + descriptor.get('content')
            json_dict[curl] = descr_str

            for a in soup.find_all('a'):
                url = str(a.get('href'))

                if not (url.startswith('http://') or url.startswith('https://')) and not ('://' in url):
                    urls.add(urllib.parse.urljoin(curl, url))
                else:
                    urls.add(url)
            print(Fore.LIGHTGREEN_EX + "\t[+] Found " + str(len(soup.find_all('a'))) + " URLs ... " + Fore.RESET)
            i += 1
    except KeyboardInterrupt:
        pass
    return urls

def main():
    urls = Set(['http://links.cncwebsite.com/']) 
    json_dict = {}
    crawl(urls, json_dict)

    with open("urls.json", "w") as f:
        json.dump(json_dict, f)
    with open("urls.dmp", "w") as f:
        f.write(str(urls))

""" [main.py]: Not imported =========================================================================================================== """
if __name__ == '__main__':
    main()

""" =================================================================================================================================== """
