import json
import random
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
from openpyxl import load_workbook

class QichachaCrawler():
    def __init__(self):
        self.login_url='https://www.qichacha.com/user_login'
        self.MONGO_URI = 'localhost'
        self.client = MongoClient(host='localhost', port=27017)
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 5)


    def login(self):
        self.browser.get(url=self.login_url)
        login = self.browser.find_element_by_xpath('//*[@id="normalLogin"]')
        login.click()
        self.browser.find_element_by_id("nameNormal").send_keys("13530988300")
        time.sleep(0.7)
        self.browser.find_element_by_id("pwdNormal").send_keys("lf8551")
        time.sleep(0.7)
        time.sleep(8)

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
        # # wait.until(EC.presence_of_element_located((By.XPATH,"//span[text()='验证通过']"))


    def get_company_info(self):
        # with open('d:\\touzhi2.txt','r',encoding='utf-8') as f:
        #     keywords = f.readlines()
        target_company_name = []
        file_name = "d:\\target.xlsx"
        open_target = load_workbook(file_name)
        read_content = open_target.get_sheet_by_name('target')
        for row in read_content.rows:
            for col in row:
                target_company_name.append(col.value)
        return (target_company_name)
        # return keywords


    def search_company(self,keywords):
        keyword = keywords.replace("\n","").replace("\r","")
        print(keyword)
        # keyword = '山西交院大成高速公路有限公司'
        self.browser.get(
            url='https://www.qichacha.com/search?key={}#index:2&'.format(parse.quote(keyword.encode('utf-8'))))

        # self.browser.set_page_load_timeout(5)
        #
        # index = self.browser.find_element_by_xpath('//*[@id="searchlist"]/table/tbody/tr[1]/td[2]/a')
        # href = index.get_attribute("href")
        # href1 = re.search("_(.*)\.", href).group(0)
        # href2 = href1.replace("_", "").replace(".", "")
        content = self.browser.page_source
        soup1 = BeautifulSoup(content, "html.parser")
        soup2 = soup1.find("table", {"class": "m_srchList"})
        try:
            companylist_source = soup2.findAll('tr')
            if companylist_source is not None:
                length = len(companylist_source)
                print(length)
                for i in range(0, length):
                    historyname = ''
                    sp = BeautifulSoup(str(companylist_source[i]), "html.parser")
                    title = sp.find("a", {"class": "ma_h1"})
                    text_re = re.search(r'(曾用名：)[^\x00-\xff]+', sp.text)
                    if text_re:
                        content01 = text_re.group()
                        historyname = content01[5:]
                    try:
                        company_title = title.text
                        print(title.text)
                    except:
                        company_title = ''
                    if (company_title == keyword) or (historyname == keyword):
                        print(1111)
                        href = BeautifulSoup(str(title), "html.parser")
                        link = href.a['href']
                        href2 = link.replace("/firm_", "").replace(".html", "")
                        print(href2)
                        return href2
                    else:
                        print("找不到相应的名称")
                        with open("D:\\touzhi_failure\\list.txt","w") as f:
                            f.write(keyword)
        except:
            companylist_source = None
            with open("D:\\touzhi_failure\\list.txt", "w") as f:
                f.write(keyword)




    def shareholder_map(self,href):
        self.browser.get(url='https://www.qichacha.com/cms_guquanmap2?keyNo={}'.format(href))
        html = self.browser.page_source
        data1 = re.search('>{(.*?)}<', html).group(0)
        d = data1.replace(">", "").replace("<", "")
        data = json.loads(d, encoding='utf-8')
        print(data)
        collection =self.client["touzhi"]["Sharehold"]
        collection.insert_one(data)

    def relationship_map(self,href):
        self.browser.get(url='https://www.qichacha.com/company_muhouAction?keyNo={}'.format(href))
        html = self.browser.page_source
        data1 = re.search('>{(.*?)}<', html).group(0)
        d = data1.replace(">", "").replace("<", "")
        data = json.loads(d, encoding='utf-8')
        collection = self.client["touzhi"]["Relationship"]
        collection.insert_one(data)
        print(data)


    def investment_map(self,href):
        try:
            self.browser.get(url='https://www.qichacha.com/cms_map?keyNo={}'.format(href))
        except Exception as e:
            print("Exception found", format(e))
        html = self.browser.page_source

        if html is not None:
            data1 = re.search('>{(.*?)}<', html).group(0)
            d = data1.replace(">", "").replace("<", "")
            data = json.loads(d, encoding='utf-8')
            collection = self.client["touzhi"]["Investment"]
            collection.insert_one(data)
            print(data)

    def run(self):
        self.login()
        keywords = self.get_company_info()
        for keyword in keywords:
            href = self.search_company(keyword)
            self.shareholder_map(href)
            time.sleep(random.randint(3,5))
            self.relationship_map(href)
            time.sleep(random.randint(3,5))
            self.investment_map(href)
            time.sleep(random.randint(3,7))






qiachacha = QichachaCrawler()
qiachacha.run()



