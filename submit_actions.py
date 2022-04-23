import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

class student_registration:
    def __init__(self,username,password,address,path):
        options = webdriver.ChromeOptions()
        # ## 下面两行能让chrome在不弹出的情况下使用
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        self.username =  username#用户名
        self.password =  password#密码
        self.address = address#地址
        self.login_url = "https://ids.hit.edu.cn/authserver/login" #hit登陆url
        self.registration_url = "https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xsMrsbNew/edit" #上报的url
        s = Service(path)
        self.driver = webdriver.Chrome(service = s,options=options)
    def login(self, url):   # 通过request_url来获取上报界面
        self.driver.get(url) #登陆
        self.driver.execute_script("const username = document.getElementById('username');username.value = " + self.username + ";const password = document.getElementById('password');password.value = "+ self.password)
        res3 = self.driver.find_element(By.ID,"login_submit")
        res3.click()
    def submit(self, url):
        self.driver.get(url) #登陆
        self.driver.execute_script("document.getElementById('txfscheckbox1').checked = true;document.getElementById('txfscheckbox2').checked = true;document.getElementById('txfscheckbox3').checked = true")
        self.driver.execute_script("kzl10 = "+self.address+";setTimeout(save,1000)")
    def run(self):
        try:
            self.login(self.login_url)
            self.submit(self.registration_url)
            print(self.username,'已上报成功')
        finally:
            self.driver.quit()
if __name__ == '__main__':
    #自行填入账号密码和chromedriver路径
    cpath = "/usr/bin/chromedriver"
    student_registration(sys.argv[1],sys.argv[2],sys.argv[3],'/Users/wqw/Documents/submit/chromedriver').run()