from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def wait_for_element(self, locator, timeout=10):
        """Wait for an element to be visible."""
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )