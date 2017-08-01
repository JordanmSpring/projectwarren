# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/ubuntu/venv/lib/python2.7/site-packages')
from selenium import webdriver
from bs4 import BeautifulSoup
import random
import time,datetime
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
from selenium.webdriver.common.proxy import *
VERBOSE = True
LOGGING = False

def log(message):
    message = str(message)
    if VERBOSE:
        print datetime.datetime.now().strftime('[%d-%m-%y %H:%M:%S] ') + message
    if LOGGING:
        pass

class scraperSelenium:
    def __init__(self,url,using_profile=False):
        self.url = url
        self.using_profile = using_profile
    def scrap(self):
        number = 0
        while True:
            try:
                self.display = Display(visible=0, size=(1024, 768))
                self.display.start()                
                if self.using_profile:
                    log("Using Firefox Profile")
                    fp = webdriver.FirefoxProfile()
                    fp.set_preference('network.proxy.ssl_port', int(proxy_port))
                    fp.set_preference('network.proxy.ssl', proxy_dir)
                    fp.set_preference('network.proxy.http_port', int(proxy_port))
                    fp.set_preference('network.proxy.http', proxy_dir)
                    fp.set_preference('network.proxy.type', 1)
                    self.driver = webdriver.Firefox(firefox_profile=fp)
                else:
                    log("Using Chrome")
                    self.driver = webdriver.Chrome()
                #self.driver.set_window_size(1120,550)
                #self.driver.set_page_load_timeout(25)
                self.driver.implicitly_wait(25)
                self.driver.get(self.url)
                time.sleep(random.uniform(1.3,2.27))
                break
            except Exception as e:
                log(e)
                number += 1
                if number > 5:
                    log(e, "...retrying...")
                    time.sleep(random.uniform(1.9,5.8))
                    log(e)
        return self.driver,self.display
    def soup(self):
        self.driver = self.scrap()
        soup = BeautifulSoup(self.driver.page_source,"html.parser")
        return soup
    def closeTools(self):
        try:
            log("closing Phantomjs")
            self.driver.quit()
            self.driver.close()

        except Exception as e:
            log(e)
        try:
            log("Closing Display")
            self.display.stop()
        except Exception as e:
            log(e)
            
def closetools(driver,display):
    try:
        log("closing Phantomjs")
        driver.quit()
        driver.close()
    except Exception as e:
        log(e)
    try:
        log("Closing Display")
        display.stop()
    except Exception as e:
        log(e)
