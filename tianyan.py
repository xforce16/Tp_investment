import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN",
    "Connection": "keep-alive",
    # "Cookie": "UOR=,finance.sina.com.cn,; ULV=1534845786251:1:1:1::; SINAGLOBAL=172.16.92.25_1534845786.467970; Apache=172.16.92.25_1534845786.467973; U_TRS1=000000a0.21c37a97.5b7be35a.2ed7630a; U_TRS2=000000a0.21cc7a97.5b7be35a.36e8f01d; lxlrttp=1532434326; hqEtagMode=0; WEB2_OTHER=f236fc0a92d2ce55e95e423abbb7978c; SSCSum=4",
    # "DNT": "1",
    "Host": "capi.tianyancha.com",
    "Referer": "https://dis.tianyancha.com/dis/tree?graphId=464491166&origin=https%3A%2F%2Fwww.tianyancha.com&mobile=&time=1535444089368e9f1",
    # "Referer": "https://search.sina.com.cn/?t=news",
    # "Cookie":"JSESSIONID=0000OuAYtrTD4hLpRX08ThiHSIJ:1923sla2v; wzwsconfirm=0bccd30c334adc75a2aee555f142c3c2; wzwstemplate=MTA=; ccpassport=15fa04d30ca7e6be6c088facd9c45adb; wzwschallenge=-1; wzwsvtime=1535426904",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36 Maxthon/5.2.1.6000",
    "X-DevTools-Emulate-Network-Conditions-Client-Id": "dcf30bce-afd2-4781-a4e2-c0d985ee5007",
}


browser = webdriver.Chrome()
wait = WebDriverWait(browser, 5)


url = 'https://www.tianyancha.com/login'
companyList=['准朔铁路有限责任公司']
usernames=["15310675140"]
passwords=['Taiping159']
ip_pool=['']
chromeOptions = webdriver.ChromeOptions()


def login():
    for proxy in ip_pool:
        # chromeOptions.add_argument("--proxy-server={}".format(proxy))
        # browser = webdriver.Chrome(chrome_options=chromeOptions)
        print('打开页面')
        browser.get(url)
        browser.maximize_window()
        # index = wait.until(EC.presence_of_element_located((By.XPATH, "//div[text()='请输入您的手机号码']")))
        for user in usernames:
            browser.find_element_by_xpath(".//*[@id='web-content']/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div[2]/input").send_keys(user)
            for password in passwords:
                browser.find_element_by_xpath(".//*[@id='web-content']/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div[3]/input").send_keys(password)
                browser.find_element_by_xpath(".//*[@id='web-content']/div/div/div/div[2]/div/div[2]/div[2]/div[2]/div[5]").click()
                # print(browser.page_source)
                c = browser.get_cookies()
                print("登陆成功")


def start_url():

    cookie = [item["name"] + ":" + item["value"] for item in browser.get_cookies()]
    # print(cookie)
    # cookiestr = ';'.join(item for item in cookie)
    cook_map = {}
    for item in cookie:
        str = item.split(':')
        cook_map[str[0]] = str[1]
    # print(cook_map)
    cookies = requests.utils.cookiejar_from_dict(cook_map, cookiejar=None, overwrite=True)
    s=requests.Session
    s.cookies= cookies


def start_page():
    browser.get("https://www.tianyancha.com/company/464491166")
    cookie = [item["name"] + ":" + item["value"] for item in browser.get_cookies()]
    # cookiestr = ';'.join(item for item in cookie)
    cook_map = {}
    for item in cookie:
        str = item.split(':')
        cook_map[str[0]] = str[1]
    print(cook_map)

def detail_page():
    browser.get(
        'https://dis.tianyancha.com/dis/tree?graphId=464491166&origin=https%3A%2F%2Fwww.tianyancha.com&mobile=&time=1535444089368e9f1')
    cookie = [item["name"] + ":" + item["value"] for item in browser.get_cookies()]
    cook_map = {}
    for item in cookie:
        str = item.split(':')
        cook_map[str[0]] = str[1]
    cookies = requests.utils.cookiejar_from_dict(cook_map, cookiejar=None, overwrite=True)
    options = webdriver.ChromeOptions()
    options.add_argument('Referer ="https://dis.tianyancha.com/dis/tree?graphId=464491166&origin=https%3A%2F%2Fwww.tianyancha.com&mobile=&time=1535444089368e9f1"')
    # options.add_argument('X-AUTH-TOKEN="eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxNTMxMDY3NTE0MCIsImlhdCI6MTUzNTQ0OTA4OSwiZXhwIjoxNTUxMDAxMDg5fQ.xKgibm9FUAJhoB7WJsI2Z029LJLJLNHa0lVL6INw4Y9m0JxJGRZu5puwmgQI-jjXQbqKZ_0fE4EM-TW20jseVA"')
    # browser.get('https://capi.tianyancha.com/cloud-equity-provider/v4/equity/indexnode.json?id=464491166')
    print(browser.page_source)
    # s = requests.Session()
    # s.cookies = cookies
    # r= s.get(url='https://capi.tianyancha.com/cloud-equity-provider/v4/equity/indexnode.json?id=464491166',headers=headers)
    # print(r.content.decode())

def run():
    login()
    start_url()
    start_page()
    detail_page()



if __name__ == '__main__':
    run()


