from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class SecondaryDealsPage(BasePage):
    def open(self):
        """Navigate to the Secondary Deals page."""
        secondary_deals_button = self.driver.find_element(By.XPATH, '//button[text()="Secondary Deals"]')
        secondary_deals_button.click()

    def go_to_last_page(self):
        """Navigate to the last page using pagination."""
        last_page_button = self.driver.find_element(By.XPATH, '//a[text()="Last"]')
        last_page_button.click()

    def go_to_first_page(self):
        """Navigate to the first page using pagination."""
        first_page_button = self.driver.find_element(By.XPATH, '//a[text()="First"]')
        first_page_button.click()