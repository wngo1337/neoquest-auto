from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import sys
sys.path.append('../src')
from src import autobattler
from src import constants
import logging
import pytest

logging.basicConfig(level=logging.INFO)

myAutobattler = autobattler.AutoBattler()
myAutobattler.login_manager.login_neopets()

# CURRENTLY DON'T DO ANYTHING RIGHT NOW...
# def setup_function():
#     print("Setting up testing environment")
#
# def teardown_function():
#     print("Tearing down testing environment")

def test_get_player_info():
    # Should be able to get player info on any page, so...
    testInfo = myAutobattler.get_player_info()
    assert type(testInfo) is tuple

def test_change_movement_mode_hunting():
    # Should probably put the URL in the constants file lol
    myAutobattler.change_movement_mode("h")
    # SHOULD NOT be able to find the element if we change to hunting mode
    with pytest.raises(NoSuchElementException) as eInfo:
        myWebElement = myAutobattler.driver.find_element(By.XPATH,
            "//A[@HREF='neoquest.phtml?movetype=2']")

def test_change_movement_mode_sneaking():
    myAutobattler.change_movement_mode("s")
    # SHOULD NOT be able to find the element if we change to sneaking mode
    with pytest.raises(NoSuchElementException) as eInfo:
        myWebElement = myAutobattler.driver.find_element(By.XPATH,
            "//A[@HREF='neoquest.phtml?movetype=3']")