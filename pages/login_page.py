from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver

        # Updated locators based on what you provided
        self.username_locator = (By.XPATH, '//input[@id="email-2"]')
        self.password_locator = (By.XPATH, '//input[@id="field"]')
        self.submit_locator = (By.XPATH, '//input[@class="login-button w-button"]')

    def enter_username(self, username):
        username_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.username_locator)
        )
        username_field.clear()  # Clears any existing text
        username_field.send_keys(username)  # Types the username

    def enter_password(self, password):
        password_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.password_locator)
        )
        password_field.clear()  # Clears any existing text
        password_field.send_keys(password)  # Types the password

    def click_login_button(self):
        login_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.submit_locator)
        )
        login_button.click()  # Click the login button

    def login(self, username, password):
        self.enter_username(username)  # Enter username
        self.enter_password(password)  # Enter password
        self.click_login_button()  # Click the login button