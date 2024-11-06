from selenium import webdriver
from pages.secondary_deals_page import SecondaryDealsPage
from pages.login_page import LoginPage

class Application:
    def __init__(self):
        # Initialize the WebDriver
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

        # Page Objects
        self.secondary_deals_page = SecondaryDealsPage(self.driver)
        self.login_page = LoginPage(self.driver)

    def open_main_page(self, url="https://soft.reelly.io"):
        """Open the main page of the application."""
        self.driver.get(url)

    def quit(self):
        """Close the browser and quit the WebDriver."""
        self.driver.quit()