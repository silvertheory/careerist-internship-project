from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.login_page import LoginPage
from pages.secondary_deals_page import SecondaryDealsPage

@given("the user is on the main page")
def step_given_user_on_main_page(context):
    context.app.main_page.open_main_page()

@when("the user logs into the page")
def step_when_user_logs_in(context):
    context.app.login_page.login("thoughtriot211@hotmail.com", "Marenostro182!@#")

@when("the user clicks on the Secondary option in the left side menu")
def step_when_user_clicks_secondary(context):
    context.app.secondary_deals_page.navigate_to_secondary_deals()

@then("the Secondary Deals page should be displayed")
def step_then_secondary_deals_page_displayed(context):
    context.app.secondary_deals_page.navigate_to_secondary_deals()

@when("the user navigates to the final page using the pagination button")
def step_when_user_goes_to_final_page(context):
    context.app.secondary_deals_page.go_to_final_page()

@when("the user navigates back to the first page using the pagination button")
def step_when_user_goes_to_first_page(context):
    context.app.secondary_deals_page.go_back_to_first_page()

@then("the user should be on the first page of the Secondary deals")
def step_then_user_on_first_page(context):
    context.app.secondary_deals_page.navigate_to_secondary_deals()