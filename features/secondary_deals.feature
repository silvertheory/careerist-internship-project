Feature: Secondary Deals Page

  Scenario: User can open the Secondary Deals page and go through the pagination
    Given the user navigates to the main page
    When the user logs in with valid credentials
    And the user navigates to the Secondary Deals page
    Then the Secondary Deals page should be displayed
    And the user can go to the last page using pagination
    And the user can go back to the first page using pagination