import os
from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from app.application import Application  # Import the Application class

# Step to open the main page
@given('the user navigates to the main page')
def step_impl(context):
    context.app = Application()  # Initialize the Application class
    context.app.open_main_page()

# Step to log in with valid credentials
@when('the user logs in with valid credentials')
def step_impl(context):
    # Fetch credentials from environment variables
    email = os.getenv('LOGIN_EMAIL')
    password = os.getenv('LOGIN_PASSWORD')
    # Use the login method from the login_page in the Application
    context.app.login_page.login(email, password)

# Step to navigate to the Secondary Deals page
@when('the user navigates to the Secondary Deals page')
def step_impl(context):
    context.app.secondary_deals_page.open()

# Step to verify the Secondary Deals page is displayed
@then('the Secondary Deals page should be displayed')
def step_impl(context):
    assert "Secondary Deals" in context.app.driver.title

# Step to go to the last page using pagination
@then('the user can go to the last page using pagination')
def step_impl(context):
    context.app.secondary_deals_page.go_to_last_page()

# Step to go back to the first page using pagination
@then('the user can go back to the first page using pagination')
def step_impl(context):
    context.app.secondary_deals_page.go_to_first_page()