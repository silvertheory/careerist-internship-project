import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.wait import WebDriverWait
from app.application import Application
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import allure

# BrowserStack Credentials
BROWSERSTACK_USERNAME = os.getenv("BROWSERSTACK_USERNAME", "davedriot_hkoi4e")
BROWSERSTACK_ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY", "STmAojL8ob4aP1GR4uqR")


def browserstack_remote(context, options):
    """
    Initialize a BrowserStack Remote WebDriver session using `options`.
    """
    browserstack_url = f"https://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"
    context.driver = webdriver.Remote(command_executor=browserstack_url, options=options)


def ios_capabilities(context, device_name="iPhone 14", os_version="16"):
    """
    Define capabilities for iOS devices on BrowserStack.
    """
    options = webdriver.ChromeOptions()
    options.set_capability("platformName", "iOS")
    options.set_capability("deviceName", device_name)
    options.set_capability("os_version", os_version)
    options.set_capability("browserName", "safari")
    options.set_capability(
        "bstack:options",
        {
            "projectName": "Internship Project",
            "buildName": os.getenv("BUILD_NAME", "iOS Browser Tests"),
            "sessionName": os.getenv("SESSION_NAME", f"iOS Test - {device_name} {os_version}"),
            "debug": True,
            "networkLogs": True,
        },
    )
    browserstack_remote(context, options)


def android_capabilities(context, device_name="Samsung Galaxy S22", os_version="12.0"):
    """
    Define capabilities for Android devices on BrowserStack.
    """
    options = webdriver.ChromeOptions()
    options.set_capability("platformName", "Android")
    options.set_capability("deviceName", device_name)
    options.set_capability("os_version", os_version)
    options.set_capability("browserName", "chrome")
    options.set_capability(
        "bstack:options",
        {
            "projectName": "Internship Project",
            "buildName": os.getenv("BUILD_NAME", "Android Browser Tests"),
            "sessionName": os.getenv("SESSION_NAME", f"Android Test - {device_name} {os_version}"),
            "debug": True,
            "networkLogs": True,
        },
    )
    browserstack_remote(context, options)


def browserstack_desktop_capabilities(context, browser="chrome", os="Windows", os_version="10"):
    """
    Define capabilities for desktop browsers on BrowserStack.
    """
    options = webdriver.ChromeOptions()
    options.set_capability("browserName", browser)
    options.set_capability("browserVersion", "latest")
    options.set_capability(
        "bstack:options",
        {
            "os": os,
            "osVersion": os_version,
            "projectName": "Internship Project",
            "buildName": os.getenv("BUILD_NAME", "Desktop Browser Tests"),
            "sessionName": os.getenv("SESSION_NAME", f"Desktop Test - {os} {os_version}"),
            "debug": True,
            "networkLogs": True,
        },
    )
    browserstack_remote(context, options)


def local_chrome(context, mobile_device=None):
    """
    Initialize local Chrome WebDriver.
    """
    chrome_options = ChromeOptions()
    if mobile_device:
        chrome_options.add_experimental_option("mobileEmulation", {"deviceName": mobile_device})
    service = ChromeService(ChromeDriverManager().install())
    context.driver = webdriver.Chrome(service=service, options=chrome_options)


def local_firefox(context):
    """
    Initialize local Firefox WebDriver.
    """
    firefox_options = FirefoxOptions()
    firefox_options.add_argument("--headless")
    firefox_options.add_argument("--no-sandbox")
    firefox_options.add_argument("--disable-dev-shm-usage")
    service = FirefoxService(GeckoDriverManager().install())
    context.driver = webdriver.Firefox(service=service, options=firefox_options)


def browser_init(context, browser="chrome", platform="desktop"):
    """
    Initializes WebDriver based on the platform and browser type.
    """
    try:
        if platform == "browserstack-ios":
            ios_capabilities(context)
        elif platform == "browserstack-android":
            android_capabilities(context)
        elif platform == "browserstack-desktop":
            browserstack_desktop_capabilities(context)
        elif platform == "local":
            if browser == "chrome":
                local_chrome(context)
            elif browser == "firefox":
                local_firefox(context)
            else:
                raise ValueError(f"Unsupported local browser '{browser}'.")
        else:
            raise ValueError(f"Unsupported platform '{platform}'.")

        context.driver.implicitly_wait(4)
        context.driver.wait = WebDriverWait(context.driver, 10)
        context.app = Application(context.driver)

    except Exception as e:
        raise RuntimeError(f"Failed to initialize browser: {e}")


def before_all(context):
    """
    Initialize environment before all tests.
    """
    print("Setting up Allure environment for reporting.")
    os.makedirs("allure-results", exist_ok=True)
    with open("allure-results/environment.properties", "w") as env_file:
        env_file.write(f"Browser={os.getenv('BROWSER', 'chrome')}\n")
        env_file.write("Platform=Cross-platform\n")
        env_file.write(f"Build Name={os.getenv('BUILD_NAME', 'Default Build')}\n")


def before_scenario(context, scenario):
    """
    Initialize the browser before each scenario.
    """
    print(f"\nStarting scenario: {scenario.name}")
    platform = os.getenv("PLATFORM", "local").lower()
    browser = os.getenv("BROWSER", "chrome").lower()
    try:
        browser_init(context, browser, platform)
    except Exception as e:
        print(f"Error initializing browser: {e}")
        raise


def before_step(context, step):
    """
    Attach step details to Allure report.
    """
    print(f"\nStarting step: {step.name}")
    allure.attach(name="Step Details", body=step.name, attachment_type=allure.attachment_type.TEXT)


def after_step(context, step):
    """
    Capture screenshots for failed steps.
    """
    if step.status == "failed" and hasattr(context, "driver"):
        screenshot_path = f"screenshots/{step.name.replace(' ', '_')}.png"
        try:
            context.driver.save_screenshot(screenshot_path)
            allure.attach.file(screenshot_path, name="Failed Step Screenshot",
                               attachment_type=allure.attachment_type.PNG)
        except Exception as e:
            print(f"Error capturing screenshot: {e}")


def after_scenario(context, scenario):
    """
    Quit browser after each scenario.
    """
    if hasattr(context, "driver"):
        try:
            context.driver.quit()
            print(f"Closed browser for scenario: {scenario.name}")
        except Exception as e:
            print(f"Error closing browser: {e}")

