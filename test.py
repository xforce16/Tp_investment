import json
import re
import pymongo
import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from urllib import parse
from lxml import etree
from bs4 import BeautifulSoup
from pymongo import MongoClient

url='https://www.qichacha.com/user_login'
MONGO_URI = '10.225.12.11'
client = MongoClient(host='10.225.12.11', port=27017)
collection = client["Qichacha"]["Sharehold"]
browser = webdriver.Chrome()
wait = WebDriverWait(browser, 5)



browser.get(url=url)
login = browser.find_element_by_xpath('//*[@id="normalLogin"]')
login.click()
browser.find_element_by_id("nameNormal").send_keys("13530988300")
time.sleep(0.7)
browser.find_element_by_id("pwdNormal").send_keys("lf8551")
time.sleep(0.7)

# bar = browser.find_element_by_xpath('//*[@id="nc_1_n1z"]')
# ActionChains(browser).move_to_element(bar).perform()
# ActionChains(browser).click_and_hold(bar).perform()
# # ActionChains(browser).move_by_offset(290,0).perform()
# # for x in range(290):
# #     ActionChains(browser).move_by_offset(x,0).perform()
# #     time.sleep(0.1)
# # time.sleep(0.5)
# # ActionChains(browser).move_by_offset(300,0).perform()
# # ActionChains(browser).release().perform()
# # wait.until(EC.presence_of_element_located((By.XPATH,"//span[text()='验证通过']")))
time.sleep(8)


# brower.get(url='https://www.qichacha.com/search?key={}#index:2&'.format(parse.quote("腾讯".encode('utf-8'))))
# index = brower.find_element_by_xpath('//*[@id="searchlist"]/table/tbody/tr[1]/td[2]/a')
# href = index.get_attribute("href")
# href1 = re.search("_(.*)\.", href).group(0)
# href2 = href1.replace("_","").replace(".","")
# text = index.text
# print(href2)
# relationship = brower.get(url='https://www.qichacha.com/company_muhou3?keyNo={}&name={}'.format(href2,parse.quote("text".encode('utf-8'))))
browser.get(url='https://www.qichacha.com/cms_guquanmap2?keyNo=4d89b310d346f0341e759e92eca34a2b')
html=browser.page_source
print(html)
# data1 = re.search('>{(.*?)}<',html).group(0)
# d =data1.replace(">","").replace("<","")
# data = json.loads(d,encoding='utf-8')
# collection.insert_one(data)





