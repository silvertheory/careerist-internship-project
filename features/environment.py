import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait
from app.application import Application
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

# Credentials
BROWSERSTACK_USERNAME = os.getenv("BROWSERSTACK_USERNAME", "davedriot_hkoi4e")
BROWSERSTACK_ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY", "STmAojL8ob4aP1GR4uqR")

def browser_init(context, browser="chrome"):
    """
    Initializes the WebDriver based on the browser type and environment.
    :param context: Behave context
    :param browser: Browser type ("chrome", "firefox", or "browserstack")
    """
    try:
        if browser == "chrome":
            # Local Chrome setup
            chrome_options = ChromeOptions()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--window-size=1920,1080")
            service = ChromeService(ChromeDriverManager().install())
            context.driver = webdriver.Chrome(service=service, options=chrome_options)

        elif browser == "firefox":
            # Local Firefox setup
            firefox_options = FirefoxOptions()
            firefox_options.add_argument("--headless")
            firefox_options.add_argument("--no-sandbox")
            firefox_options.add_argument("--disable-dev-shm-usage")
            firefox_options.add_argument("--width=1920")
            firefox_options.add_argument("--height=1080")
            service = FirefoxService(GeckoDriverManager().install())
            context.driver = webdriver.Firefox(service=service, options=firefox_options)

        elif browser == "browserstack":
            # BrowserStack setup
            capabilities = {
                "bstack:options": {
                    "os": "OS X",
                    "osVersion": "Big Sur",
                    "browserName": "Safari",
                    "browserVersion": "latest",
                    "buildName": os.getenv("BUILD_NAME", "Selenium BDD Tests - macOS"),
                    "sessionName": os.getenv("SESSION_NAME", "BrowserStack Test")
                }
            }

            # BrowserStack URL
            browserstack_url = f"https://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"

            # Initialize driver with options
            context.driver = webdriver.Remote(
                command_executor=browserstack_url,
                desired_capabilities=capabilities
            )
        else:
            raise ValueError(f"Browser '{browser}' is not supported. Use 'chrome', 'firefox', or 'browserstack'.")

        # WebDriver wait and Application
        context.driver.implicitly_wait(4)
        context.driver.wait = WebDriverWait(context.driver, timeout=10)
        context.app = Application(context.driver)

    except Exception as e:
        raise RuntimeError(f"Failed to initialize browser: {e}")

def before_scenario(context, scenario):
    print('\nStarted scenario: ', scenario.name)
    try:
        # Set the browser from an environment variable
        browser = os.getenv("BROWSER", "chrome").lower()
        browser_init(context, browser)
    except Exception as e:
        print(f"Error during browser initialization: {e}")
        raise

def before_step(context, step):
    print('\nStarted step: ', step)

def after_step(context, step):
    if step.status == 'failed':
        print('\nStep failed: ', step)

def after_scenario(context, feature):
    if hasattr(context, "driver"):
        try:
            context.driver.quit()
            print(f"Closed driver after scenario: {feature.name}")
        except Exception as e:
            print(f"Error while quitting the driver: {e}")