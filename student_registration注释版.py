from selenium import webdriver
import requests
import json

class student_registration:
    def __init__(self):
        self.login_url = "http://ids.hit.edu.cn/authserver/login?service=http%3A%2F%2Fxg.hit.edu.cn%2Fzhxy-xgzs%2Fcommon%2FcasLogin%3Fparams%3DL3hnX21vYmlsZS94c0hvbWU%3D" #hit登陆url
        self.check_url = "http://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xs/getYqxxList" #发送post请求可以得到上报的日期和地点
        self.registration_url = "http://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xs/yqxx" #上报的url
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
        }

    def request_url(self, url1, url2):   # 通过request_url来获取上报界面
        driver_path = r"/Users/wqw/PycharmProjects/scrapy/chromedriver" # 本地的chromedriver绝对路径
        options = webdriver.ChromeOptions()
        # ## 下面两行能让chrome在不弹出的情况下使用
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        ## 给seleniuim添加headers
        options.add_argument('User-Agent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"')

        driver = webdriver.Chrome(executable_path=driver_path,options=options)
        driver.get(url1) #登陆
        driver.find_element_by_id("username").send_keys('') #填写学号
        driver.find_element_by_id("password").send_keys('') #填写密码

        driver.find_element_by_xpath("//button[@type='submit']").click()


        driver.get(url2) #进入上报列表界面 为什么要get两次呢 有一天我发现只get一次会被识别为机器登陆 但是get两次就好了。。。
        driver.get(url2)
        cookie = driver.get_cookies()
        Cookies = {i["name"]: i["value"] for i in cookie} #获取cookies，为后续操作准备
        # print(Cookies)
        driver.find_element_by_xpath("//div[@class='right_btn']").click()  #点击上报列表的上报按钮，这里不会直接进入上报界面，而是会向网页的json中添加一段数据
        response = requests.post("https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xs/csh", headers=self.headers, cookies=Cookies) #上报界面的url的一部分是由一串json中的数据组成，所以我们在这里发送post的请求来获取json数据
        # print(response)
        ret = json.loads(response.text) #获取json数据转为python字典
        # print(ret)
        ret1 = ret['module'] #这是我们上面提到的上报界面的url中的数据，我们把它从字典中取出
        ret2 = ret['msg'] #这里会反馈今日是否上报
        url3 = "http://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xs/editYqxx?id={}&zt=00".format(ret1)
        print('情况:',ret2)
        # print(url3)
        return Cookies,url3

    def registration(self,url1,url2):  #获取完url后来实现上报填写
        driver_path = r"/Users/wqw/PycharmProjects/scrapy/chromedriver"
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(executable_path=driver_path,options=options)

        driver.get(url1)  #我试了下用带入上一个函数获取的cookies来操作，发现不行，所以再次登陆账号
        driver.find_element_by_id("username").send_keys('') #填写学号
        driver.find_element_by_id("password").send_keys('') #填写密码
        driver.find_element_by_xpath("//button[@type='submit']").click()

        driver.get(url2) #和之前的同理，get一次会被认为是机器登陆
        driver.get(url2)
        driver.find_element_by_xpath("//input[@type='checkbox']").click() #点击我已阅读
        driver.find_element_by_xpath("//div[@onclick='save()']").click() #点击上报


    def check(self, url, Cookies): #最后，访问上报列表网页中的另一个json,来获取上报日期和地点，这里的post请求直接携带cookies就可以得到
        response = requests.post(url=url, headers=self.headers, cookies=Cookies)
        ret = json.loads(response.text)
        ret1 = ret['module']['data'][0]
        ret11 = ret1['rq']
        ret12 = ret1['dqztmc']
        print('check:')
        print({'登记后的日期': ret11, '登记后的地点': ret12})

    def run(self):
        Cookies,url3 = self.request_url(self.login_url,self.registration_url)
        reg = self.registration(self.login_url,url3)
        check_str = self.check(self.check_url, Cookies)

if __name__ == '__main__':
    CS=student_registration()
    CS.run()

