from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import sys

import seleniumobjectsandmethods

sys.path.append("../src")
from src import autobattler
from src import constants
import logging
import pytest

logging.basicConfig(level=logging.INFO)

my_autobattler = autobattler.AutoBattler(use_neopass=True)
my_autobattler.login_manager.login_neopets()

# CURRENTLY DON'T DO ANYTHING RIGHT NOW...
# def setup_function():
#     print("Setting up testing environment")
#
# def teardown_function():
#     print("Tearing down testing environment")


def test_get_player_info():
    # Should be able to get player info on any page, so...
    testInfo = my_autobattler.get_player_info()
    assert type(testInfo) is tuple


def test_change_movement_mode_hunting():
    # Should probably put the URL in the constants file lol
    my_autobattler.change_movement_mode("h")
    # SHOULD NOT be able to find the element if we change to hunting mode
    with pytest.raises(NoSuchElementException) as eInfo:
        myWebElement = seleniumobjectsandmethods.single_driver.find_element(
            By.XPATH, "//A[@HREF='neoquest.phtml?movetype=2']"
        )


def test_change_movement_mode_sneaking():
    my_autobattler.change_movement_mode("s")
    # SHOULD NOT be able to find the element if we change to sneaking mode
    with pytest.raises(NoSuchElementException) as eInfo:
        myWebElement = seleniumobjectsandmethods.single_driver.find_element(
            By.XPATH, "//A[@HREF='neoquest.phtml?movetype=3']"
        )
