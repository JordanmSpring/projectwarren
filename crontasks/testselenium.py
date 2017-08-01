from seleniumscraper import scraperSelenium
from bs4 import BeautifulSoup
import time

url = r"https://www.theguardian.com/international"
url = r"https://finance.yahoo.com/quote/msft/key-statistics?ltr=1"
selenium_obj = scraperSelenium(url,False)
driver,display = selenium_obj.scrap()

time.sleep(3)
soup = BeautifulSoup(driver.page_source,"html.parser")
print len(soup)
#print soup
soup.find("div",{"id":"Main"}).text
