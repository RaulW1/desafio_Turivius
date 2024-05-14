from selenium import webdriver
from selenium.webdriver.common.by import By


class Scraper:
    def __init__(self, target_url: str):
        self.target_url = target_url

        # Web Driver (Chrome) setup
        self.webdriver = self.get_driver()

        # Web page setup
        self.webdriver.get(self.target_url)

    @staticmethod
    def get_driver():
        """
        create Chrome webdriver instance
        :return: Chrome webdriver instance
        """
        return webdriver.Chrome()

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
        return self.webdriver.find_element(By.NAME, name)

    def find_elements_by_name(self, name: str):
        """
        find multiple elements in the page by name
        :param name: elements name
        :return: instances of the elements
        """
        return self.webdriver.find_elements(By.NAME, name)

    def find_elements_by_class_name(self, class_name: str):
        """
        find multiple elements in the page by class name
        :param class_name: elements class name
        :return: instances of the elements
        """
        return self.webdriver.find_elements(By.CLASS_NAME, class_name)

    @staticmethod
    def send_keys(element, keys: str):
        """
        Input string into text field
        :param element: element representing text field
        :param keys: string to be inputted
        :return:
        """
        element.send_keys(keys)

    @staticmethod
    def click(element):
        """
        execute the click action of a button
        :param element: element representing button
        :return:
        """
        element.click()

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
