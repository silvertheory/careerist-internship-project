Feature: Secondary Deals Page Pagination

  Scenario: User can open the Secondary deals page and go through the pagination
    Given the user is on the main page
    When the user logs into the page
    And the user clicks on the Secondary option in the left side menu
    Then the Secondary deals page should be displayed
    When the user navigates to the final page using the pagination button
    And the user navigates back to the first page using the pagination button
    Then the user should be on the first page of the Secondary deals