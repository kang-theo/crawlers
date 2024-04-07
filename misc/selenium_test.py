"""
selenium will use chromedriver to open a chrome instance and execute the request defined
if a chrome browser is opened, the basic functionality of selenium and chromedriver is fine.
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome('chromedriver')
driver.get("https://www.python.org")
print(driver.title)
# input()
search_bar = driver.find_element_by_name("q")
search_bar.clear()
search_bar.send_keys("getting started with python")
search_bar.send_keys(Keys.RETURN)
print(driver.current_url)
driver.close()