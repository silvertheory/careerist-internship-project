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

# BrowserStack Credentials
BROWSERSTACK_USERNAME = os.getenv("BROWSERSTACK_USERNAME", "your_username")
BROWSERSTACK_ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY", "your_access_key")


def browserstack_mobile_android(context):
    """
    Initialize WebDriver for Android testing on BrowserStack.
    """
    capabilities = {
        "bstack:options": {
            "osVersion": "11.0",             # Android version
            "deviceName": "Google Pixel 5",  # Device
            "realMobile": "true",            # Use real devices
            "buildName": os.getenv("BUILD_NAME", "BrowserStack Mobile Test"),
            "sessionName": os.getenv("SESSION_NAME", "Mobile Android Test"),
        },
        "browserName": "Chrome",
        "browserVersion": "latest",
    }
    browserstack_url = f"https://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"
    context.driver = webdriver.Remote(command_executor=browserstack_url, desired_capabilities=capabilities)


def browserstack_mobile_ios(context):
    """
    Initialize WebDriver for iOS testing on BrowserStack.
    """
    capabilities = {
        "bstack:options": {
            "osVersion": "14.0",            # iOS version
            "deviceName": "iPhone 12",      # Device
            "realMobile": "true",           # Use real devices
            "buildName": os.getenv("BUILD_NAME", "BrowserStack Mobile Test"),
            "sessionName": os.getenv("SESSION_NAME", "Mobile iOS Test"),
        },
        "browserName": "Safari",
        "browserVersion": "latest",
    }
    browserstack_url = f"https://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"
    context.driver = webdriver.Remote(command_executor=browserstack_url, desired_capabilities=capabilities)


def browser_init(context, browser="chrome", platform="desktop", mobile_device=None):
    """
    Initialize WebDriver based on the platform and browser type.
    Supports:
    - Desktop browsers (Chrome, Firefox)
    - Mobile emulation (local Chrome)
    - BrowserStack (Android and iOS)
    """
    try:
        if platform == "browserstack-android":
            browserstack_mobile_android(context)

        elif platform == "browserstack-ios":
            browserstack_mobile_ios(context)

        elif browser == "chrome":
            chrome_options = ChromeOptions()

            # Local mobile emulation
            if mobile_device:
                mobile_emulation = {"deviceName": mobile_device}
                chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

            service = ChromeService(ChromeDriverManager().install())
            context.driver = webdriver.Chrome(service=service, options=chrome_options)

        elif browser == "firefox":
            firefox_options = FirefoxOptions()
            service = FirefoxService(GeckoDriverManager().install())
            context.driver = webdriver.Firefox(service=service, options=firefox_options)

        else:
            raise ValueError(f"Unsupported browser '{browser}'. Use 'chrome', 'firefox', or BrowserStack.")

        # Initialize Application and WebDriver waits
        context.driver.implicitly_wait(4)
        context.driver.wait = WebDriverWait(context.driver, timeout=10)
        context.app = Application(context.driver)

    except Exception as e:
        raise RuntimeError(f"Failed to initialize browser: {e}")


def before_all(context):
    """
    Setup environment before running all tests.
    """
    print("Setting up Allure environment for reporting.")
    os.makedirs("allure-results", exist_ok=True)
    with open("allure-results/environment.properties", "w") as env_file:
        env_file.write(f"Browser={os.getenv('BROWSER', 'chrome')}\n")
        env_file.write("Platform=Cross-platform\n")
        env_file.write(f"Build Name={os.getenv('BUILD_NAME', 'Default Build')}\n")


def before_scenario(context, scenario):
    """
    Initialize browser before running each scenario.
    """
    print(f'\nStarted scenario: {scenario.name}')
    try:
        browser = os.getenv("BROWSER", "chrome").lower()
        platform = os.getenv("PLATFORM", "desktop").lower()
        mobile_device = os.getenv("MOBILE_DEVICE")  # Optional for local mobile emulation
        browser_init(context, browser, platform, mobile_device)
    except Exception as e:
        print(f"Error initializing browser for scenario: {e}")
        raise


def before_step(context, step):
    """
    Log step details in the Allure report.
    """
    print(f'\nStarted step: {step.name}')
    allure.attach(
        name="Step Description",
        body=step.name,
        attachment_type=allure.attachment_type.TEXT
    )


def after_step(context, step):
    """
    Handle step failures and attach screenshots.
    """
    if step.status == 'failed':
        print(f'\nStep failed: {step.name}')
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
    Cleanup after each scenario by quitting the browser.
    """
    if hasattr(context, "driver"):
        try:
            context.driver.quit()
            print(f"Closed browser after scenario: {scenario.name}")
        except Exception as e:
            print(f"Error while quitting the browser: {e}")