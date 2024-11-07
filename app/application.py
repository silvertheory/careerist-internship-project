from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.secondary_deals_page import SecondaryDealsPage


class Application:
    def __init__(self, driver):
        # Page Objects
        self.secondary_deals_page = SecondaryDealsPage(driver)
        self.login_page = LoginPage(driver)
        self.main_page = MainPage(driver)
