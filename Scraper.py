from selenium import webdriver


class Scraper:
    def __init__(self):
        self.webdriver = self.get_driver()

    @staticmethod
    def get_driver():
        return webdriver.Chrome()

    def quit_driver(self):
        self.webdriver.quit()

