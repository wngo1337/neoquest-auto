from selenium.common.exceptions import NoSuchElementException
import seleniumobjectsandmethods
import constants
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import logging


logging.basicConfig(level=logging.WARNING)

direction_urls_to_numbers = {
    URL: movementString
    for movementString, URL in constants.numbers_to_direction_urls.items()
}

# Want to compile all entrance/exit links and just loop through until we find the one in page
entrance_xpath_dictionary = {"": ""}


class PathTracker:
    def __init__(self):
        self.current_path = ""
        self.driver = seleniumobjectsandmethods.single_driver
        self.current_address = ""

    def trackPath(self):
        while True:
            userInput = input(
                "Enter here if you have made a move, or enter c to clear path: "
            )
            if userInput.lower() == "c":
                self.current_path = ""
            else:
                self.current_address = self.driver.current_url
                if self.current_address in direction_urls_to_numbers:
                    self.current_path = (
                        self.current_path
                        + direction_urls_to_numbers[self.current_address]
                    )
                    print("Current path is {}".format(self.current_path))

    def invert_path(self, original_path):
        temp_reversed_path = original_path[::-1]
        inverted_path = ""
        # Generates a path that leads back to the original location
        original_directions_to_inverted = {
            "1": "8",
            "2": "7",
            "3": "6",
            "4": "5",
            "5": "4",
            "6": "3",
            "7": "2",
            "8": "1",
        }
        # We have to invert the directions in REVERSE order to backtrack on the same path
        # Otherwise, program creates a path that is mirrored across the x-axis
        # This path might not exist if there are obstacles in the way obviously, so yeah
        for direction in temp_reversed_path:
            inverted_path = inverted_path + original_directions_to_inverted[direction]
        return inverted_path
