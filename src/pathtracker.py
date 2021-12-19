from selenium.common.exceptions import NoSuchElementException
import seleniumobjectsandmethods
import constants
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import logging


logging.basicConfig(level=logging.WARNING)

invertedDirectionDictionary = {URL: movementString for
                               movementString, URL in constants.directionDictionary.items()}

# Want to compile all entrance/exit links and just loop through until we find the one in page
entranceXPathDictionary = {"":""}

class PathTracker:
    def __init__(self):
        self.currentPath = ""
        self.driver = seleniumobjectsandmethods.singleDriver
        self.currentAddress = ""

    def trackPath(self):
        while True:
            userInput = input("Enter here if you have made a move, or enter c to clear path: ")
            if userInput.lower() == "c":
                self.currentPath = ""
            else:
                self.currentAddress = self.driver.current_url
                if self.currentAddress in invertedDirectionDictionary:
                    self.currentPath = self.currentPath + invertedDirectionDictionary[
                        self.currentAddress]
                    print("Current path is {}".format(self.currentPath))

    # WANT TO MAKE THIS A STATIC METHOD
    def invertPath(self, originalPath):
        tempReversedPath = originalPath[::-1]
        invertedPath = ""
        # Generates a path that leads back to the original location
        reverseDirectionDictionary = {"1":"8", "2":"7", "3":"6", "4":"5", "5":"4",
                                      "6":"3", "7":"2", "8":"1"}
        # We have to invert the directions in REVERSE order to backtrack on the same path
        # Otherwise, program creates a path that is mirrored across the x-axis
        # This path might not exist if there are obstacles in the way obviously, so yeah
        for direction in tempReversedPath:
            invertedPath = invertedPath + reverseDirectionDictionary[direction]
        return invertedPath

# if __name__ == "__main__":
#     for URL in invertedDirectionDictionary:
#         print("{} {}".format(URL, invertedDirectionDictionary[URL]))
