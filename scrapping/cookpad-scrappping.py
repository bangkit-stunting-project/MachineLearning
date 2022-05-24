import selenium 
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent 
from fp.fp import FreeProxy

from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class Spoofer(object):

    def __init__(self, country_id=['US'], rand=True, anonym=True):
        self.country_id = country_id
        self.rand = rand
        self.anonym = anonym
        self.userAgent, self.ip = self.get()

    def get(self):
        ua = UserAgent()
        proxy = FreeProxy(country_id=self.country_id, rand=self.rand, anonym=self.anonym).get()
        ip = proxy.split("://")[1]
        return ua.random, ip

class DriverOptions(object):

    def __init__(self):

        self.options = Options()
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--start-maximized')
        self.options.add_argument('--start-fullscreen')
        self.options.add_argument('--single-process')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument("--incognito")
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        # self.options.set_preference('useAutomationExtension', False)
        # self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_argument("disable-infobars")

        self.helperSpoofer = Spoofer()

        self.options.add_argument('user-agent={}'.format(self.helperSpoofer.userAgent))
        self.options.add_argument('--proxy-server=%s' % self.helperSpoofer.ip)

class WebDriver(DriverOptions):

    def __init__(self, path=''):
        DriverOptions.__init__(self)
        self.driver_instance = self.get_driver()

    def get_driver(self):

        print("""
        IP:{}
        UserAgent: {}
        """.format(self.helperSpoofer.ip, self.helperSpoofer.userAgent))

        PROXY = self.helperSpoofer.ip
        webdriver.DesiredCapabilities.CHROME['proxy'] = {
            "httpProxy":PROXY,
            "ftpProxy":PROXY,
            "sslProxy":PROXY,
            "noProxy":None,
            "proxyType":"MANUAL",
            "autodetect":False
        }
        webdriver.DesiredCapabilities.CHROME['acceptSslCerts'] = True

        # path = os.path.join(os.getcwd(), '../windowsDriver/chromedriver.exe')

        driver = webdriver.Firefox(executable_path='../driver/geckodriver', options=self.options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        # driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        #     "source":
        #         "const newProto = navigator.__proto__;"
        #         "delete newProto.webdriver;"
        #         "navigator.__proto__ = newProto;"
        # })

        return driver

def main() :
    driver = WebDriver()
    driver_instance = driver.driver_instance
    driver_instance.get('https://cookpad.com/id/')

# driver = webdriver.Firefox(executable_path='../driver/geckodriver')

    class_list = ['Kalio Ayam', 'Ketoprak', 'Mie Ayam', 'Mie Bakso' , 'Bubur Ayam', 'Beef Teriyaki', 'Martabak Mesir', 'Mie Pangsit Basah', 'Beef Burger', 'Soto Padang', 'Mie Aceh Rebus', 'Rendang Sapi', 'Soto Betawi', 'Ayam Taliwang', 'Chicken Teriyaki', 'Pempek Telur', 'Sop Daging Sapi', 'Karedok', 'Gado-Gado', 'Nasi Rames' ]  

# driver.get('https://cookpad.com/id/')
    close_btn = driver_instance.find_element(By.XPATH, "/html/body/div[3]/div/div[1]/div[1]/a")
    close_btn.click()

    time.sleep(5)

    login_btn = driver_instance.find_element(By.XPATH, '/html/body/div[1]/header/div[1]/div[2]/div/a')
    login_btn.click()

    time.sleep(5)

if __name__ == "__main__" : 
    main()