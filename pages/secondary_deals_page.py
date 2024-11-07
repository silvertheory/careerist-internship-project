from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class SecondaryDealsPage(BasePage):
    def navigate_to_secondary_deals(self):
        self.click_element(By.XPATH, "//a[text()='Secondary']")

    def is_secondary_deals_page_opened(self):
        # Replace with the actual locator for confirmation
        return self.find_element(By.XPATH, "//h1[text()='Secondary Deals']") is not None

    def go_to_final_page(self):
        # Click until reaching the last page
        while True:
            next_button = self.find_element(By.XPATH, "//button[text()='Next']")
            if next_button and next_button.is_enabled():
                next_button.click()
            else:
                break  # Reached the final page

    def go_back_to_first_page(self):
        # Click until reaching the first page
        while True:
            previous_button = self.find_element(By.XPATH, "//button[text()='Previous']")
            if previous_button and previous_button.is_enabled():
                previous_button.click()
            else:
                break  # Reached the first page