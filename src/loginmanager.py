import seleniumobjectsandmethods
import constants
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import os
import logging
import sys


# This class handles logging in and navigating to the Neoquest game page
class LoginManager:

    DEFAULT_DELAY = 10

    def __init__(self, use_neopass):
        # TODO: REMOVE ALL MY LOGIN INFO FROM TEXT FILES AND METHODS
        logging.basicConfig(level=logging.INFO)
        logging.info("Reading login info...")

        """Input to the file should change depending on the login method
        specified.

        If using normal login, then username and password are required.

        If using neopass, then we need email, password, and username of account
        to locate buttons. In this case, we list them in the order they are
        used for login.
        """
        self.use_neopass = use_neopass

        base_dir = os.path.dirname(os.path.abspath(__file__))
        txtfiles_dir = os.path.join(base_dir, "txtfiles")
        if self.use_neopass:
            logging.info("Detected login method is: Neopass")
            with open(os.path.join(txtfiles_dir, "userinfo.txt"), "r") as login_file:
                self.email = login_file.readline().strip()
                self.password = login_file.readline().strip()
                self.username = login_file.readline().strip()
        else:

            logging.info("Detected login method is: Traditional login")
            with open(os.path.join(txtfiles_dir, "userinfo.txt"), "r") as login_file:
                self.username = login_file.readline().strip()
                self.password = login_file.readline().strip()

    def login_neopets(self):
        if self.use_neopass:
            self.login_neopets_neopass()
        else:
            self.login_neopets_traditional()

    def login_neopets_traditional(self):
        # Login to Neopets
        logging.info("Attempting to login via traditional login...")
        seleniumobjectsandmethods.go_to_url(constants.LOGIN_URL)

        """Below code implement an explicit wait for the login button element so that
        we don't try to submit any information before the page is ready"""

        try:
            my_element = seleniumobjectsandmethods.get_element_with_wait(
                seleniumobjectsandmethods.single_driver,
                LoginManager.DEFAULT_DELAY,
                (By.ID, "loginButton"),
            )

            seleniumobjectsandmethods.single_driver.find_element(
                By.ID, "loginUsername"
            ).send_keys(self.username)
            seleniumobjectsandmethods.single_driver.find_element(
                By.ID, "loginPassword"
            ).send_keys(self.password)

            seleniumobjectsandmethods.single_driver.find_element(
                By.ID, "loginButton"
            ).click()

        except TimeoutException:
            print("The login page took too long to load!")
            seleniumobjectsandmethods.single_driver.quit()
            sys.exit(1)

        try:
            logout_element = seleniumobjectsandmethods.get_element_with_wait(
                seleniumobjectsandmethods.single_driver,
                LoginManager.DEFAULT_DELAY,
                (By.CSS_SELECTOR, "a[href='/logout.phtml']"),
            )
            seleniumobjectsandmethods.single_driver.get(constants.MAIN_GAME_URL)

        except TimeoutException:
            print("We didn't find a logout button, so we probably aren't logged in")
            seleniumobjectsandmethods.single_driver.quit()
            sys.exit(1)

        logging.info("We have logged in via traditional login!")

    def login_neopets_neopass(self):

        logging.info("Attempting to login via Neopass...")
        seleniumobjectsandmethods.go_to_url(constants.NEOPASS_LOGIN_URL)

        login_button = seleniumobjectsandmethods.get_element_with_wait(
            seleniumobjectsandmethods.single_driver,
            LoginManager.DEFAULT_DELAY,
            (By.CSS_SELECTOR, "button[type='submit']"),
        )

        email_element = seleniumobjectsandmethods.get_element_with_wait(
            seleniumobjectsandmethods.single_driver,
            LoginManager.DEFAULT_DELAY,
            (By.NAME, "email"),
        )
        email_element.send_keys(self.email)

        password_element = seleniumobjectsandmethods.get_element_with_wait(
            seleniumobjectsandmethods.single_driver,
            LoginManager.DEFAULT_DELAY,
            (By.NAME, "password"),
        )
        password_element.send_keys(self.password)

        login_button.click()

        # At this point, we are logged in to the main Neopass launch page
        launch_button = seleniumobjectsandmethods.get_element_with_wait(
            seleniumobjectsandmethods.single_driver,
            LoginManager.DEFAULT_DELAY,
            (By.XPATH, "//button[text()='Launch']"),
        )
        launch_button.click()

        # After clicking, a new tab is opened that we have to navigate to
        # Otherwise, context is still on the old tab
        tabs = seleniumobjectsandmethods.single_driver.window_handles
        seleniumobjectsandmethods.single_driver.switch_to.window(
            seleniumobjectsandmethods.single_driver.window_handles[-1]
        )
        print(seleniumobjectsandmethods.single_driver.current_url)

        # Now click the button of corresponding username
        username_button = seleniumobjectsandmethods.get_element_with_wait(
            seleniumobjectsandmethods.single_driver,
            LoginManager.DEFAULT_DELAY,
            (By.XPATH, f"//button[.//h4[contains(text(), '{self.username}')]]"),
        )
        username_button.click()

        # Lastly, click the continue button and we are good
        continue_button = seleniumobjectsandmethods.get_element_with_wait(
            seleniumobjectsandmethods.single_driver,
            LoginManager.DEFAULT_DELAY,
            (By.XPATH, f"//button[contains(text(), 'Continue')]"),
        )
        continue_button.click()

        # At this point, we need to WAIT until we see a unique element that
        # identifies our login, and then we can safely start playing

        try:
            logout_element = seleniumobjectsandmethods.get_element_with_wait(
                seleniumobjectsandmethods.single_driver,
                LoginManager.DEFAULT_DELAY,
                (By.CSS_SELECTOR, "a[href='/logout.phtml']"),
            )
            seleniumobjectsandmethods.single_driver.get(constants.MAIN_GAME_URL)

        except TimeoutException:
            print("We didn't find a logout button, so we probably aren't logged in")
            seleniumobjectsandmethods.single_driver.quit()
            sys.exit()

        print("We have logged in via Neopass!")
