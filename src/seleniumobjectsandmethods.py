from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
import logging

chromedriver_autoinstaller.install()

# Setting up logger for all files to use
logger = logging.getLogger(__name__)
logging.root.handlers = []
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("myTrainer.log"),
        logging.StreamHandler()
    ])

# Just pointing path to the location of Edge's driver and instantiating the driver

"""The following lines are EXTREMELY IMPORTANT because ads constitute the majority of page load time. 
Blocking them makes page loads and gameplay MUCH faster."""

# User will need to add their adblock folder path or make a copy and find that path
"""Uh... refer to this thread for details:
https://www.reddit.com/r/learnpython/comments/4zzn69/how_do_i_get_adblockplus_to_work_with_selenium/"""

with open("txtfiles/adblockpath.txt", "r") as adblockPathFile:
    adblockPath = adblockPathFile.readline()
adblockPath = r"{}".format(adblockPath)

my_chrome_options = Options()
my_chrome_options.add_argument("start-maximized")
my_chrome_options.add_argument("disable-infobars")
my_chrome_options.add_argument('--disable-application-cache')
my_chrome_options.add_argument('--disable-gpu')
my_chrome_options.add_argument("--disable-dev-shm-usage")

my_chrome_options.add_argument('load-extension=' + adblockPath)
# Silences the interpreter complaints about... uh, something
my_chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
# DO NOT use headless: at least for me, drastically INCREASES loading time
# Maybe because headless cannot run extensions, so must load ads
# myChromeOptions.add_argument("--headless")

# prefs = {"profile.managed_default_content_settings.images": 2}
# myChromeOptions.add_experimental_option("prefs", prefs)

single_driver = webdriver.Chrome(options=my_chrome_options)
# singleDriver.create_options()

# Want standardized methods for all classes to interact with pages through this module's singleDriver
# Only want to pass the driver around when necessary
def click_link_by_xpath(xpath):
    link = single_driver.find_element(By.XPATH, xpath)
    single_driver.execute_script("arguments[0].click();", link)
    return None

def go_to_url(address):
    single_driver.get(address)
    return None