from selenium import webdriver
from app.application import Application

def before_all(context):
    # Initialize WebDriver
    context.driver = webdriver.Chrome()
    context.driver.maximize_window()
    context.app = Application(context.driver)  # Pass the driver to Application

def after_all(context):
    # Quit the WebDriver
    context.driver.quit()