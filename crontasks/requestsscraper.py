import requests
import urllib2
from bs4 import BeautifulSoup
import time
import random
import sys
import re
import datetime
import pandas as pd

hdr = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0"}

    
class scraper:
    def __init__(self,url,proxies=None):
        self.url = url 
        self.proxies = proxies
    def scrap(self):
        page = None
        number = 0
        while True:
            try:
                if self.proxies:
                    print "using proxies"
                    self.proxies = proxies
                    page = requests.get(self.url, proxies = self.proxies, verify=False,headers = hdr,timeout=10).text
                    time.sleep(random.uniform(0.5,1))
                    break
                else:
                    print "not using proxies"
                    page = requests.get(self.url,headers = hdr, verify=False,timeout=10).text
                    time.sleep(random.uniform(1.5,5))
                    break
            except Exception as e:
                print(e, "...retrying...")
                time.sleep(random.uniform(3.57,12.37))
                print(e)
                number += 1
                if number > 5:
                    print "waiting 10 minutes"
                    time.sleep(60*10)
                if number > 10:
                    print "Not working"
                    break
        return page 
