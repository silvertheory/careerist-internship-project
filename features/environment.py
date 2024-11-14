import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.wait import WebDriverWait
from app.application import Application
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import allure

# Credentials
BROWSERSTACK_USERNAME = os.getenv("BROWSERSTACK_USERNAME", "davedriot_hkoi4e")
BROWSERSTACK_ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY", "STmAojL8ob4aP1GR4uqR")


def browser_init(context, browser="chrome"):
    """
    Initializes the WebDriver based on the browser type and environment.
    """
    try:
        if browser == "chrome":
            chrome_options = ChromeOptions()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--window-size=1920,1080")
            service = ChromeService(ChromeDriverManager().install())
            context.driver = webdriver.Chrome(service=service, options=chrome_options)

        elif browser == "firefox":
            firefox_options = FirefoxOptions()
            firefox_options.add_argument("--headless")
            firefox_options.add_argument("--no-sandbox")
            firefox_options.add_argument("--disable-dev-shm-usage")
            firefox_options.add_argument("--width=1920")
            firefox_options.add_argument("--height=1080")
            service = FirefoxService(GeckoDriverManager().install())
            context.driver = webdriver.Firefox(service=service, options=firefox_options)

        elif browser == "browserstack":
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
            browserstack_url = f"https://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"
            context.driver = webdriver.Remote(command_executor=browserstack_url, desired_capabilities=capabilities)
        else:
            raise ValueError(f"Browser '{browser}' is not supported. Use 'chrome', 'firefox', or 'browserstack'.")

        # WebDriver wait and Application
        context.driver.implicitly_wait(4)
        context.driver.wait = WebDriverWait(context.driver, timeout=10)
        context.app = Application(context.driver)

    except Exception as e:
        raise RuntimeError(f"Failed to initialize browser: {e}")


def before_all(context):
    """
    Initialize environment before all tests.
    Create environment.properties file for Allure.
    """
    print("Setting up Allure environment for reporting.")
    os.makedirs("allure-results", exist_ok=True)  # Ensure directory exists
    with open("allure-results/environment.properties", "w") as env_file:
        env_file.write("Browser={}\n".format(os.getenv("BROWSER", "chrome")))
        env_file.write("Platform=Cross-platform\n")
        env_file.write("Build Name={}\n".format(os.getenv("BUILD_NAME", "Default Build")))


def before_scenario(context, scenario):
    """
    Runs before each scenario to initialize the browser.
    """
    print('\nStarted scenario: ', scenario.name)
    try:
        browser = os.getenv("BROWSER", "chrome").lower()
        browser_init(context, browser)
    except Exception as e:
        print(f"Error during browser initialization: {e}")
        raise


def before_step(context, step):
    """
    Logs the step details in the Allure report.
    """
    print('\nStarted step: ', step)
    allure.attach(
        name="Step Description",
        body=step.name,
        attachment_type=allure.attachment_type.TEXT
    )


def after_step(context, step):
    """
    Logs failures and attaches screenshots on failure.
    """
    if step.status == 'failed':
        print('\nStep failed: ', step)
        if hasattr(context, "driver"):
            try:
                screenshot_path = f"screenshots/{step.name.replace(' ', '_')}.png"
                context.driver.save_screenshot(screenshot_path)
                allure.attach.file(
                    screenshot_path,
                    name="Screenshot on Failure",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                print(f"Error capturing screenshot: {e}")


def after_scenario(context, scenario):
    """
    Closes the browser after each scenario.
    """
    if hasattr(context, "driver"):
        try:
            context.driver.quit()
            print(f"Closed driver after scenario: {scenario.name}")
        except Exception as e:
            print(f"Error while quitting the driver: {e}")
