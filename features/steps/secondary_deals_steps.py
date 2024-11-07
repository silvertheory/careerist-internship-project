from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.secondary_deals_page import SecondaryDealsPage

@given("the user is on the main page")
def step_given_user_on_main_page(context):
    context.driver = webdriver.Chrome()
    context.driver.maximize_window()
    context.login_page = LoginPage(context.driver)
    context.secondary_deals_page = SecondaryDealsPage(context.driver)
    context.driver.get("https://soft.reelly.io")

@when("the user logs into the page")
def step_when_user_logs_in(context):
    context.login_page.login("your_username", "your_password")  # Replace with valid credentials

@when("the user clicks on the Secondary option in the left side menu")
def step_when_user_clicks_secondary(context):
    context.secondary_deals_page.navigate_to_secondary_deals()

@then("the Secondary Deals page should be displayed")
def step_then_secondary_deals_page_displayed(context):
    # Wait for a unique element on the "Secondary Deals" page to confirm it is loaded
    WebDriverWait(context.driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//h1[text()='Secondary Deals']"))  # Adjust as needed
    )
    assert "Secondary Deals" in context.driver.title, "Secondary Deals page did not load as expected"

@when("the user navigates to the final page using the pagination button")
def step_when_user_goes_to_final_page(context):
    context.secondary_deals_page.go_to_final_page()

@when("the user navigates back to the first page using the pagination button")
def step_when_user_goes_to_first_page(context):
    context.secondary_deals_page.go_back_to_first_page()

@then("the user should be on the first page of the Secondary deals")
def step_then_user_on_first_page(context):
    # Verifies the user is on the first page by checking the 'Previous' button is disabled or hidden
    first_page_indicator = WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[@aria-disabled='true' and text()='Previous']"))
    )
    assert first_page_indicator is not None, "User is not on the first page of Secondary Deals"