from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        # Updated locators based on the attributes provided
        self.username_locator = (By.XPATH, '//input[@id="email-2"]')
        self.password_locator = (By.XPATH, '//input[@id="field"]')
        self.submit_locator = (By.XPATH, '//button[@id="login-button"]')

    def enter_username(self, username):
        username_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.username_locator)
        )
        username_field.clear()
        username_field.send_keys(username)

    def enter_password(self, password):
        password_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.password_locator)
        )
        password_field.clear()
        password_field.send_keys(password)

    def click_login_button(self):
        try:
            login_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.submit_locator)
            )
            login_button.click()
        except TimeoutException:
            print("Login button not clickable after waiting. Attempting JavaScript click.")
            # Attempt JavaScript click if standard click fails
            login_button = self.driver.find_element(*self.submit_locator)
            self.driver.execute_script("arguments[0].click();", login_button)

    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()