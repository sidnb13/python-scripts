import configparser, os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

cfg = configparser.ConfigParser()
# fix if script is not run from CWD
cfg.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

username = cfg.get('login_info', 'username')
password = cfg.get('login_info', 'password')

options = Options()
options.add_argument('debuggerAddress')
options.add_argument('localhost:<remote-port>')

driver = webdriver.Chrome(options=options)
driver.get('https://my.austinisd.org/LoginPolicy.jsp')

# send username, then password in order
driver.find_element_by_xpath('//*[@id="loginForm"]/table/tbody/tr[1]/td[2]/div/input').send_keys(username)
driver.find_element_by_xpath('//*[@id="loginForm"]/table/tbody/tr[2]/td[2]/div/input').send_keys(password)
# click login button
driver.find_element_by_xpath('//*[@id="LoginButton"]').click()
# click on self-serve TEAMS button
driver.find_element_by_xpath('//*[@id="desktop0"]/table/tbody/tr/td/table/tbody/tr[2]/td[2]/div/div[1]/a').click()