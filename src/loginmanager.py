import seleniumobjectsandmethods
import constants
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import logging

# This class handles logging in and navigating to the Neoquest game page
class LoginManager:

    def __init__(self):
        # TODO: REMOVE ALL MY LOGIN INFO FROM TEXT FILES AND METHODS
        logging.basicConfig(level=logging.INFO)
        logging.info("Reading login info...")

        loginFile = open("txtfiles/userinfo.txt", "r")
        self.username = loginFile.readline()
        self.password = loginFile.readline()

        loginFile.close()

    def loginNeopets(self):
        # Login to Neopets
        seleniumobjectsandmethods.goToURL(constants.LOGIN_URL)
        """Below code implement an explicit wait for the login button element so that
        we don't try to submit any information before the page is ready"""
        try:
            DELAY = 15
            myElement = WebDriverWait(seleniumobjectsandmethods.singleDriver, DELAY).\
                until(EC.presence_of_element_located((By.ID, "loginButton")))
            # Wait until the login button appears before submitting any information
            seleniumobjectsandmethods.singleDriver.find_element_by_name("username").send_keys(self.username)
            seleniumobjectsandmethods.singleDriver.find_element_by_id("loginPassword").send_keys(self.password)
            seleniumobjectsandmethods.singleDriver.find_element_by_class_name("login-button").click()
        except TimeoutException:
            print("The page took too long to load!")
            seleniumobjectsandmethods.singleDriver.quit()

        try:
            DELAY = 15
            # This CSS selector is pretty inflexible, but it works for now
            welcomeElement = WebDriverWait(seleniumobjectsandmethods.singleDriver, DELAY).\
                until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/logout.phtml']")))
            seleniumobjectsandmethods.singleDriver.get(constants.MAIN_GAME_URL)
        except TimeoutException:
            print("We didn't find a logout button, so we probably aren't logged in")
            seleniumobjectsandmethods.singleDriver.quit()

        logging.info("We have logged in!")

