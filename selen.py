from selenium import webdriver
import time,zhengz,os
from bs4 import BeautifulSoup
import csv
import random
from openpyxl import load_workbook
from selenium.webdriver.common.action_chains import ActionChains

# 输入信息
username = '15310675140'
password = 'Taiping159'
# 打开并存储相关表数据
csvfile = open('D:\\User Desktop\\ZHANGZHI\\桌面\\爬虫\\主要人员股东.csv', 'a+', newline='', encoding='gb18030')
csvfile2 = open('D:\\User Desktop\\ZHANGZHI\\桌面\\爬虫\\风险数量总览.csv', 'a+', newline='', encoding='gb18030')
csvfile3 = open('D:\\User Desktop\\ZHANGZHI\\桌面\\爬虫\\风险文件内容.csv', 'a+', newline='', encoding='gb18030')
csvfile4 = open('D:\\User Desktop\\ZHANGZHI\\桌面\\爬虫\\公司基本内容.csv', 'a+', newline='', encoding='gb18030')
csvfile5 = open('D:\\User Desktop\\ZHANGZHI\\桌面\\爬虫\\人员股东详情.csv', 'a+', newline='', encoding='gb18030')

writer_people= csv.writer(csvfile)
writer_risknum= csv.writer(csvfile2)
writer_riskcontent= csv.writer(csvfile3)
writer_baseinfo= csv.writer(csvfile4)
writer_personinfo= csv.writer(csvfile5)

#存储人员链接列表
person_list=[]

def get_company_info(file_name):
    target_company_name=[]
    open_target = load_workbook(file_name)
    read_content = open_target.get_sheet_by_name('target')
    for row in read_content.rows:
        for col in row:
            target_company_name.append(col.value)
    return (target_company_name)

def open_browser(url):
    driver = webdriver.Chrome(executable_path='D:\\爬虫\\chromedriver_win32\\chromedriver.exe')
    driver.get(url)
    driver.maximize_window()
    return driver

def log_in(driver):
    # 模拟登陆
    driver.find_element_by_xpath(
        ".//*[@id='web-content']/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/input"). \
        send_keys(username)
    driver.find_element_by_xpath(
        ".//*[@id='web-content']/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div[3]/input"). \
        send_keys(password)
    driver.find_element_by_xpath(
        ".//*[@id='web-content']/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div[5]").click()
    time.sleep(3)
    return driver

def search_company(driver, url1, keyword):
    print(url1)
    driver.get(url1)
    content = driver.page_source.encode('utf-8')
    soup1 = BeautifulSoup(content, 'lxml')
    companylist_source = soup1.findAll("div", {"class": "search-result-single"})
    length= len(companylist_source)
    for i in range(0, length):
        historyname = ''
        sp = BeautifulSoup(str(companylist_source[i]), "html.parser")
        text_re = zhengz.search(r'(历史名称：)[^\x00-\xff]+', sp.text)
        if text_re:
            content01 = text_re.group()
            historyname = content01[5:]
        company_title = sp.find("a", {"class": "name "})
        if (company_title.text == keyword) or (historyname == keyword):
            href = BeautifulSoup(str(company_title), "html.parser")
            link = href.a['href']
            driver.get(link)
    return driver

def get_base_info(driver,keyword):
    base_table =[]
    base_info = driver.find_element_by_xpath('//*[@id="company_web_top"]/div[2]/div[2]/div[5]')
    phone= base_info.text.split('电话：')[1].split('邮箱')[0]
    email= base_info.text.split('邮箱：')[1].split('\n')[0]
    http= base_info.text.split('网址：')[1].split('地址')[0]
    address= base_info.text.split('地址：')[1].split('\n')[0]
    script= base_info.text.split('简介：')[1].split('\n')[0]
    baseInfo=driver.find_element_by_id('_container_baseInfo')
    tabs = baseInfo.find_elements_by_tag_name('table')

    rows1 = tabs[0].find_elements_by_tag_name('tr')
    corporation= rows1[1].find_elements_by_tag_name('td')[0].text.split('\n')[0]
    capital= rows1[1].find_elements_by_tag_name('td')[1].text.split('\n')[1]
    time_zhuce= rows1[2].find_elements_by_tag_name('td')[0].text.split('\n')[1]
    state= rows1[3].find_elements_by_tag_name('td')[0].text.split('\n')[1]

    rows2 = tabs[1].find_elements_by_tag_name('tr')
    registration = rows2[0].find_elements_by_tag_name('td')[1].text
    credit_code= rows2[1].find_elements_by_tag_name('td')[1].text
    identification_number= rows2[2].find_elements_by_tag_name('td')[1].text
    business_term = rows2[3].find_elements_by_tag_name('td')[1].text
    Taxpayer_qualification= rows2[4].find_elements_by_tag_name('td')[1].text
    Paid_capital = rows2[5].find_elements_by_tag_name('td')[1].text
    Insured_number = rows2[6].find_elements_by_tag_name('td')[1].text

    Organization_code= rows2[0].find_elements_by_tag_name('td')[3].text
    Type_of_company= rows2[1].find_elements_by_tag_name('td')[3].text
    industry= rows2[2].find_elements_by_tag_name('td')[3].text
    Date_of_approval = rows2[3].find_elements_by_tag_name('td')[3].text
    Personnel_scale= rows2[4].find_elements_by_tag_name('td')[3].text
    registration_authority= rows2[5].find_elements_by_tag_name('td')[3].text
    English_name= rows2[6].find_elements_by_tag_name('td')[3].text

    Registered_address= rows2[7].find_elements_by_tag_name('td')[1].text.split('附近公司')[0]
    Scope_of_operation= rows2[8].find_elements_by_tag_name('td')[1].text

    base_table.append(keyword);base_table.append(phone);base_table.append(email);base_table.append(http);base_table.append(address)
    base_table.append(script);base_table.append(corporation);base_table.append(capital);base_table.append(time_zhuce);base_table.append(state)
    base_table.append(registration);base_table.append(credit_code);base_table.append(identification_number);base_table.append(business_term)
    base_table.append(Taxpayer_qualification);base_table.append(Paid_capital);base_table.append(Insured_number);base_table.append(Organization_code)
    base_table.append(Type_of_company);base_table.append(industry);base_table.append(Date_of_approval);base_table.append(Personnel_scale)
    base_table.append(registration_authority);base_table.append(English_name);base_table.append(Registered_address);base_table.append(Scope_of_operation)

    writer_baseinfo.writerow(base_table)

def get_riskcontent_info(driver,keyword):
    bsobj=BeautifulSoup(driver.page_source, "html.parser")

    content_xzcf = bsobj.find("div", {"id": "_container_punish"})  # _container_punish 行政处罚
    ct02 = BeautifulSoup(str(content_xzcf), "html.parser")
    content22 = ct02.findAll("tr")
    length = len(content22)
    for i in range(1, length + 1):
        contenlist = []
        contenlist.append(keyword)
        contenlist.append('行政处罚')
        sp = BeautifulSoup(str(content22[i - 1]), "html.parser")
        content02 = sp.find_all('td')
        for j in content02:
            contenlist.append(j.text)
        writer_riskcontent.writerow(contenlist)  # 将处罚信息按行存入

    content_jyyc = bsobj.find("div", {"id": "_container_abnormal"})  # _container_abnormal 经营异常
    ct03 = BeautifulSoup(str(content_jyyc), "html.parser")
    content33 = ct03.findAll("tr")
    length03 = len(content33)
    for i in range(1, length03 + 1):
        contenlist = []
        contenlist.append(keyword)
        contenlist.append('经营异常')
        sp = BeautifulSoup(str(content33[i - 1]), "html.parser")
        content02 = sp.find_all('td')
        for j in content02:
            contenlist.append(j.text)
        writer_riskcontent.writerow(contenlist)  # 将经营异常信息按行存入

    content_dcdy = bsobj.find("div", {"id": "_container_mortgage"})  # _container_mortgage 动产抵押
    ct04 = BeautifulSoup(str(content_dcdy), "html.parser")
    content44 = ct04.findAll("tr")
    length04 = len(content44)
    for i in range(1, length04 + 1):
        contenlist = []
        contenlist.append(keyword)
        contenlist.append('动产抵押')
        sp = BeautifulSoup(str(content44[i - 1]), "html.parser")
        content02 = sp.find_all('td')
        for j in content02:
            contenlist.append(j.text)
        writer_riskcontent.writerow(contenlist)  # 将经营异常信息按行存入

    content_gccz = bsobj.find("div", {"id": "_container_equity"})  # _container_equity 股权出质
    ct05 = BeautifulSoup(str(content_gccz), "html.parser")
    content55 = ct05.findAll("tr")
    length5 = len(content55)
    for i in range(1, length5 + 1):
        contenlist = []
        contenlist.append(keyword)
        contenlist.append('股权出质')
        sp = BeautifulSoup(str(content55[i - 1]), "html.parser")
        content02 = sp.find_all('td')
        for j in content02:
            contenlist.append(j.text)
        writer_riskcontent.writerow(contenlist)  # 将经营异常信息按行存入

    content_sfpm = bsobj.find("div", {"id": "_container_judicialSale"})  # _container_judicialSale 司法拍卖
    ct06 = BeautifulSoup(str(content_sfpm), "html.parser")
    content66 = ct06.findAll("tr")
    length6 = len(content66)
    for i in range(1, length6 + 1):
        contenlist = []
        contenlist.append(keyword)
        contenlist.append('司法拍卖')
        sp = BeautifulSoup(str(content66[i - 1]), "html.parser")
        content02 = sp.find_all('td')
        for j in content02:
            contenlist.append(j.text)
        writer_riskcontent.writerow(contenlist)  # 将经营异常信息按行存入

    content_qsgg = bsobj.find("div", {"id": "_container_towntax"})  # _container_towntax 欠税公告
    ct07 = BeautifulSoup(str(content_qsgg), "html.parser")
    content77 = ct07.findAll("tr")
    length7 = len(content77)
    for i in range(1, length7 + 1):
        contenlist = []
        contenlist.append(keyword)
        contenlist.append('欠税公告')
        sp = BeautifulSoup(str(content77[i - 1]), "html.parser")
        content02 = sp.find_all('td')
        for j in content02:
            contenlist.append(j.text)
        writer_riskcontent.writerow(contenlist)  # 将经营异常信息按行存入

    content_touzhi = bsobj.find("div", {"id": "_container_invest"})  # _container_invest 对外投资
    ct08 = BeautifulSoup(str(content_touzhi), "html.parser")
    content88 = ct08.findAll("tr")
    length8 = len(content88)
    for i in range(1, length8 + 1):
        contenlist = []
        contenlist.append(keyword)
        contenlist.append('对外投资')
        sp = BeautifulSoup(str(content88[i - 1]), "html.parser")
        content02 = sp.find_all('td')
        for j in content02:
            contenlist.append(j.text)
        writer_riskcontent.writerow(contenlist)  # 将投资信息按行存入

def get_risk_info(driver,keyword):
    a=0
    b=2
    # 识别需要悬停的元素
    ele = driver.find_element_by_xpath('//*[@id="web-content"]/div/div[2]/div[1]/div[2]/div[1]/div/div/div[2]/div[1]')
    # 鼠标移到悬停元素上
    ActionChains(driver).move_to_element(ele).perform()
    time.sleep(random.randint(3,10))
    bsobj = BeautifulSoup(driver.page_source, "html.parser")
    risk = bsobj.findAll('div', {'class': 'itemcontent -no-border '})
    #判断是否有上市信息栏
    if 'nav-main-shangshiitem' in str(driver.page_source):
        a=1
        b=3
    risk_num = []
    risk_num.append(keyword)
    for i in range(a, b):
        bsobj01 = BeautifulSoup(str(risk[i]), "html.parser")
        risk_list = bsobj01.findAll('div')
        for j in range(1, len(risk_list)):
            total = zhengz.findall(r"\d+\.?\d*", str(risk_list[j].text))
            if len(total) == 0:
                total01 = 0
            else:
                total01 = int(total[0])
                if total01 == 99:
                    count = BeautifulSoup(driver.page_source, "html.parser")
                    try:
                        if '开庭公告' in str(risk_list[j].text):
                            content_text = count.select('#nav-main-announcementCount')[0].get_text()
                            total01= zhengz.findall(r"\d+\.?\d*", str(content_text))[0]
                        elif '法律诉讼' in str(risk_list[j].text):
                            content_text = count.select('#nav-main-lawsuitCount')[0].get_text()
                            total01= zhengz.findall(r"\d+\.?\d*", str(content_text))[0]
                        elif '法院公告' in str(risk_list[j].text):
                            content_text = count.select('#nav-main-courtCount')[0].get_text()
                            total01= zhengz.findall(r"\d+\.?\d*", str(content_text))[0]
                    except:
                        total01=99
            risk_num.append(total01)
    writer_risknum.writerow(risk_num)

def get_staff_info(driver,keyword):
    humancompany=driver.find_elements_by_xpath('//*[@class="humancompany"]/div[1]/a')  #获取法人信息
    human=[]
    human.append(keyword)
    human.append(humancompany[0].get_attribute('href'))
    human.append(humancompany[0].text)
    writer_people.writerow(human)  # 将企业信息按行存入
    #存入人名链接
    staff_link = []
    staff_link.append(humancompany[0].get_attribute('href')) #存入法人链接

    staff_info = driver.find_elements_by_xpath('//*[@id="_container_staff"]/div[1]/table/tbody/tr/td[2]/div/a[1]')
    for i in range(len(staff_info)):
        staff_list = []
        href = driver.find_elements_by_xpath('//*[@id="_container_staff"]/div[1]/table/tbody/tr/td[2]/div/a[1]')[i].\
            get_attribute('href')
        person = driver.find_elements_by_xpath('//*[@id="_container_staff"]/div[1]/table/tbody/tr/td[2]/div/a[1]')[i].text
        staff_list.append(keyword)
        staff_list.append(href)
        staff_link.append(href)  #存入主要人员链接
        staff_list.append(person)
        print(staff_list)
        writer_people.writerow(staff_list)  # 将企业信息按行存入

    return staff_link

def get_gudong_info(driver,keyword):
    gudong_link=[]
    gudong_info = driver.find_elements_by_xpath('//*[@id="_container_holder"]/table/tbody/tr/td[2]/div/div[2]/a')
    for i in range(len(gudong_info)):
        gudong_list = []
        href = driver.find_elements_by_xpath('//*[@id="_container_holder"]/table/tbody/tr/td[2]/div/div[2]/a')[i].\
            get_attribute('href')
        person = driver.find_elements_by_xpath('//*[@id="_container_holder"]/table/tbody/tr/td[2]/div/div[2]/a')[i].text
        gudong_list.append(keyword)
        gudong_list.append(href)
        gudong_link.append(href)
        gudong_list.append(person)
        print(gudong_list)
        writer_people.writerow(gudong_list)  # 将企业信息按行存入
    return gudong_link

def get_person_info(driver,keyword,person_link):
    for list in set(person_link):
        if len(zhengz.findall(r"[\s\S]*human[\s\S]*", str(list))) > 0:
            driver.get(list)
            time.sleep(random.randint(3, 10))
            bsobj = BeautifulSoup(driver.page_source, "html.parser")
            a = bsobj.find("span", {"id": "humanName"})
            bbb = bsobj.find("div", {"id": "_container_sygs"})
            bsobj2 = BeautifulSoup(str(bbb), "html.parser")
            content01 = bsobj2.find("table", {"class": "table"}).tbody
            ct = BeautifulSoup(str(content01), "html.parser")
            content = ct.findAll("tr")
            length = len(content)
            for i in range(1, length + 1):
                contenlist = []
                contenlist.append(keyword)
                contenlist.append(a.get_text())
                sp = BeautifulSoup(str(content[i - 1]), "html.parser")
                content02 = sp.find_all('td')
                for j in content02:
                    contenlist.append(j.text)
                writer_personinfo.writerow(contenlist)  # 将企业信息按行存入
                print('正在爬取法人信息--' + a.get_text())

def tryonclick(table):
    # 测试是否有翻页
    try:
        # 找到有翻页标记
        table.find_element_by_tag_name('ul')
        onclickflag = 1
    except Exception:
        print("没有翻页")
        onclickflag = 0
    return onclickflag

def change_page(table,driver,keyword):
    for i in range(30):
        if table.find_element_by_xpath(".//a[@class='num -next']"):
            button = table.find_element_by_xpath(".//a[@class='num -next']")
            driver.execute_script("arguments[0].click();", button)
            time.sleep(3)
            if '主要人员' in table.text:
                get_staff_info(driver,keyword)
            if '股东' in table.text:
                get_gudong_info(driver,keyword)

def scrapy(driver,keyword):
    get_base_info(driver,keyword)
    get_risk_info(driver, keyword)
    get_riskcontent_info(driver, keyword)
    #翻页获取主要人员信息
    table_staff= driver.find_elements_by_xpath("//div[contains(@id,'_container_staff')]")
    staff_link2=get_staff_info(driver,keyword)
    # 判断此表格是否有翻页功能
    onclickflag = tryonclick(table_staff)
    if onclickflag == 1:
       change_page(table_staff,driver,keyword)
    #翻页获取股东信息
    table_gudong= driver.find_elements_by_xpath("//div[contains(@id,'_container_holder')]")
    gudong_link2=get_gudong_info(driver, keyword)
    # 判断此表格是否有翻页功能
    onclickflag = tryonclick(table_gudong)
    if onclickflag == 1:
        change_page(table_gudong, driver, keyword)
    #获取人名对应的详细信息
    staff_link2.extend(gudong_link2)
    get_person_info(driver, keyword, person_link=staff_link2)



if __name__ == "__main__":
    file_name = "D:\\User Desktop\\ZHANGZHI\\桌面\\target.xlsx"
    keyword_list=get_company_info(file_name=file_name)
    url = 'https://www.tianyancha.com/login'
    driver = open_browser(url)
    driver = log_in(driver)
    for keyword in keyword_list:
        url1 = 'http://www.tianyancha.com/search?key=%s' % keyword
        driver = search_company(driver, url1, keyword)
        if '相关搜索结果' in driver.title:
            continue
        scrapy(driver,keyword)
        time.sleep(random.randint(3, 10))

