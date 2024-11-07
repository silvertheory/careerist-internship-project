from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def before_scenario(context, scenario):
    context.driver = webdriver.Chrome()

def after_scenario(context, scenario):
    context.driver.quit()