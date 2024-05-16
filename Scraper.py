from selenium import webdriver
from selenium.webdriver.chrome.options import ChromiumOptions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from urllib3.exceptions import MaxRetryError


class Scraper:
    def __init__(self, target_url: str, headless: bool):
        """
        Class responsible for the Selenium's API calls
        :param target_url: target web page url
        """
        self.target_url = target_url
        self.headless = headless

        # Web Driver (Chrome) setup
        self.webdriver = self.get_driver()

        # Web page setup
        self.get(target_url)

    def get_driver(self):
        """
        create Chrome webdriver instance
        :return: Chrome webdriver instance
        """
        if self.headless:
            options = webdriver.chrome.options.Options()
            options.add_argument(argument="--headless=new")
            driver = webdriver.Chrome(options=options)
            return driver

    def quit_driver(self):
        """
        Close webdriver instance
        :return:
        """
        self.webdriver.quit()

    def find_element_by_name(self, name: str):
        """
        find element in the page by name
        :param name: element`s name
        :return: instance of the element
        """
        try:
            return self.webdriver.find_element(By.NAME, name)
        except NoSuchElementException as e:
            self.quit_driver()
            raise e

    def find_elements_by_name(self, name: str):
        """
        find multiple elements in the page by name
        :param name: elements name
        :return: instances of the elements
        """
        try:
            return self.webdriver.find_elements(By.NAME, name)
        except NoSuchElementException as e:
            self.quit_driver()
            raise e

    def find_elements_by_class_name(self, class_name: str):
        """
        find multiple elements in the page by class name
        :param class_name: elements class name
        :return: instances of the elements
        """
        try:
            return self.webdriver.find_elements(By.CLASS_NAME, class_name)
        except NoSuchElementException as e:
            self.quit_driver()
            raise e

    def find_element_by_xpath(self, xpath: str, close_driver_on_fail=True):
        """
        fin element in the page by xpath
        :param close_driver_on_fail: use False when called by self.check_element_by_xpath
        :param xpath: element's xpath
        :return: instance of the element
        """
        try:
            return self.webdriver.find_element(By.XPATH, xpath)
        except NoSuchElementException as e:
            if close_driver_on_fail:
                self.quit_driver()
            raise e

    def check_element_by_xpath(self, xpath: str):
        """
        check if element exists within current page by xpath
        :param xpath: element's xpath
        :return: True if element exists else False
        """
        try:
            self.find_element_by_xpath(xpath, False)
            return True
        except NoSuchElementException:
            return False

    def get_current_page_source(self):
        """
        :return: source code of the current page
        """
        return self.webdriver.page_source

    def send_keys(self, element, keys: str):
        """
        Input string into text field
        :param element: element representing text field
        :param keys: string to be inputted
        :return:
        """
        try:
            element.send_keys(keys)
        except StaleElementReferenceException as e:
            self.quit_driver()
            raise e

    def click(self, element):
        """
        execute the click action of a button
        :param element: element representing button
        :return:
        """
        try:
            element.click()
        except StaleElementReferenceException as e:
            self.quit_driver()
            raise e

    def wait(self, time: float):
        """
        wait for a period of time in seconds. Used to synchronize web page to code
        :param time: time in seconds
        :return:
        """
        self.webdriver.implicitly_wait(time)

    def get_current_url(self):
        """
        :return: url of the current working page
        """
        return self.webdriver.current_url

    def get(self, url: str):
        try:
            self.webdriver.get(url)
        except MaxRetryError as e:
            self.quit_driver()
            raise e
