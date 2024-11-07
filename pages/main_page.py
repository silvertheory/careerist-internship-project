from pages.base_page import BasePage


class MainPage(BasePage):
    def open_main_page(self, url="https://soft.reelly.io"):
        """Open the main page of the application."""
        self.driver.get(url)