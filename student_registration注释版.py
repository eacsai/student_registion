from selenium import webdriver
class student_registration:
    def __init__(self,username,password,path):
        options = webdriver.ChromeOptions()
        # ## 下面两行能让chrome在不弹出的情况下使用
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        self.username =  username#用户名
        self.password =  password#密码
        self.login_url = "https://ids.hit.edu.cn/authserver/login" #hit登陆url
        self.registration_url = path #上报的url
        self.driver = webdriver.Chrome(executable_path=path) 
    def login(self, url):   # 通过request_url来获取上报界面
        self.driver.get(url) #登陆
        self.driver.execute_script("const username = document.getElementById('username');username.value = " + self.username + ";const password = document.getElementById('password');password.value = "+ self.password)
        res3 = self.driver.find_element_by_id("login_submit")
        res3.click()
    def submit(self, url):
        self.driver.get(url) #登陆
        self.driver.execute_script("document.getElementById('txfscheckbox1').checked = true;document.getElementById('txfscheckbox2').checked = true;document.getElementById('txfscheckbox3').checked = true")
        self.driver.execute_script("kzl10 = '黑龙江省哈尔滨市南岗区';setTimeout(save,1000)")
    def run(self):
        self.login(self.login_url)
        self.submit(self.registration_url)
if __name__ == '__main__':
    #自行填入账号密码和chromedriver路径
    student_registration("'111'","'111'",'111').run()
