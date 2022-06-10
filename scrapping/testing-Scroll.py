from jmespath import search
import selenium 
from selenium import webdriver
from selenium.webdriver.common.by import By 

DRIVER_PATH = '../driver/geckodriver'

driver = webdriver.Firefox(executable_path=DRIVER_PATH)

driver.get('https://google.com')
search_bok = driver.find_element(by=By.CSS_SELECTOR, value='input.gLFyf')
search_bok.send_keys('Buku')
driver.execute_script('winwod')