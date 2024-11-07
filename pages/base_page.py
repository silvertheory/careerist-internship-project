from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def find_element(self, by, locator):
        try:
            return self.wait.until(EC.visibility_of_element_located((by, locator)))
        except TimeoutException:
            return None

    def click_element(self, by, locator):
        element = self.find_element(by, locator)
        if element:
            element.click()