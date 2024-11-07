from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from app.application import Application


def browser_init(context):
    """
    :param context: Behave context
    """
    # Set up Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    # Initialize the ChromeDriver service with ChromeDriverManager
    service = Service(ChromeDriverManager().install())  # Changed to explicitly use `service=service`
    context.driver = webdriver.Chrome(service=service, options=chrome_options)  # Ensure `options` passed as keyword

    # Set up WebDriver wait and Application
    context.driver.implicitly_wait(4)
    context.driver.wait = WebDriverWait(context.driver, timeout=10)
    context.app = Application(context.driver)


def before_scenario(context, scenario):
    print('\nStarted scenario: ', scenario.name)
    try:
        browser_init(context)
    except Exception as e:
        print(f"Error during browser initialization: {e}")


def before_step(context, step):
    print('\nStarted step: ', step)


def after_step(context, step):
    if step.status == 'failed':
        print('\nStep failed: ', step)


def after_scenario(context, feature):
    if hasattr(context, "driver"):
        context.driver.quit()  # Ensure quit() only if `context.driver` exists