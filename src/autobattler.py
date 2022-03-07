from selenium.common.exceptions import NoSuchElementException
import seleniumobjectsandmethods
import constants
import re
import loginmanager
import potionhandler
import skillpointspender
import equipmentmaker
import pathtracker

import logging
import logging.handlers

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

"""This part of the program assumes that we are on a Neoquest page.
If not, then it doesn't do anything... Should be able to handle the following:

1. Moving back and forth to find enemies, or following a user-specified path
2. Basic attacking/casting spells on enemies.
3. Healing when below 50% HP
4. Exiting battle on win or loss.

The skill build is a fixed 10/10/10/0 Life and 7/7/6/6 Shock, which the program follows"""

# TODO: ENSURE ALL FUNCTIONS HAVE WEBDRIVER WAITS (EVEN LOGINMANAGER)
class AutoBattler:
    def __init__(self):
        self.loginManager = loginmanager.LoginManager()
        # THESE DON'T EVEN HAVE AN INIT METHOD LOL, JUST USING DEFAULT
        self.potionHandler = potionhandler.PotionHandler()
        self.skillPointSpender = skillpointspender.SkillPointSpender()
        self.equipmentMaker = equipmentmaker.EquipmentMaker()
        self.pathTracker = pathtracker.PathTracker()

    """This method walks back and forth on the world map on hunting mode.
    It automatically battles monsters, using attacks, skills, and potions as necessary.
    
    The basic prototype will just use basic attacks, which should be more than sufficient
    for any game mode. """

    def closeAutoBattler(self):
        seleniumobjectsandmethods.singleDriver.quit()

    def getPlayerInfo(self):
        # THIS GLITCHES SOMETIMES, I GUESS PAGE DOESN'T LOAD SOMETIMES AND BREAKS IT
        myInfoElement = WebDriverWait(seleniumobjectsandmethods.singleDriver, 30). \
            until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Name:')]")))
        playerInfo = myInfoElement.text

        # TODO: Fix the str parsing here. It works, but it is pretty dumb
        healthInfoObject = re.search("Health:(.*)", playerInfo)
        healthInfo = healthInfoObject.group(0).split(" ")[1]
        levelInfoObject = re.search("Level:(.*)", playerInfo)
        level = levelInfoObject.group(0).split(" ")[1]

        currentHealth, maxHealth = healthInfo.split("/")

        return int(currentHealth), int(maxHealth), int(level)

    # LOL this is dumb
    def refreshPage(self):
        seleniumobjectsandmethods.goToURL(constants.MAIN_GAME_URL)

    # Would be nice to be able to combine these three into one method
    def isBattle(self):
        pageSource = seleniumobjectsandmethods.singleDriver.page_source
        return constants.NAVIGATION_IMAGE_URL not in pageSource

    """
    Tricky: "Stuns you for" occurs on first turn you are stunned, while
    "You are stunned" can be on the page where you are able to act again, so need to check
    for presence of Attack button to see if you are really stunned...
    """
    def isStunned(self):
        pageSource = seleniumobjectsandmethods.singleDriver.page_source
        return "stuns you for" in pageSource \
               or ("You are stunned" in pageSource and "Attack" not in pageSource)

    # These are pretty weak conditions, but they do work...
    def isStartOrEndFight(self):
        pageSource = seleniumobjectsandmethods.singleDriver.page_source
        return "You defeated" in pageSource or "You are attacked by" in pageSource

    def hasPotions(self):
        # Can probably do this with a regex later...
        pageSource = seleniumobjectsandmethods.singleDriver.page_source
        return "Use a " in pageSource and "Healing Potion" in pageSource

    def isBossBattle(self):
        pageSource = seleniumobjectsandmethods.singleDriver.page_source
        for link in constants.bossImageList:
            if link in pageSource:
                return True
        return False

    def changeMovementMode(self, mode):
        if self.isBattle():
            self.winBattle()
            # Input can either be "s" for sneaking or "h" for hunting
        if mode.lower() == "s":
            seleniumobjectsandmethods.goToURL(constants.SNEAKING_MODE_URL)
        elif mode.lower() == "h":
            seleniumobjectsandmethods.goToURL(constants.HUNTING_MODE_URL)
        logging.info("Switched to {} movement mode".format(mode))

    def train(self, numBattles=1000):
        # Want function to halt eventually, but also want to be able to train x number of times
        self.changeMovementMode("h")
        while numBattles > 0:
            try:
                DELAY = 15
                infoElement = WebDriverWait(seleniumobjectsandmethods.singleDriver, DELAY).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//div[@ALIGN='center' and contains(.,'Experience')]")
                    )
                )
                # If we see the direction arrows, we want to "move" in place to encounter monsters
                if not self.isBattle():
                    if self.skillPointSpender.hasPoints():
                        currentHealth, maxHealth, level = self.getPlayerInfo()
                        self.skillPointSpender.spendPoints(level)
                    seleniumobjectsandmethods.goToURL(constants.MOVE_NOMOVE_URL)
                else:
                    self.winBattle()
                    numBattles -= 1
            except TimeoutException:
                logging.warning("The program ran into an error while training, refreshing page")
                self.refreshPage()
                continue

    def winBattle(self):
        # This function simply attacks and heals when necessary to win random encounters
        """Might be nice to implement a strategy pattern here, but not really necessary.
        Only two options: monsters and bosses"""

        # Determine whether is boss battle or regular encounter
        # DON'T FORGET TO ADD SPIRIT HEALING POTIONS TO POTIONHANDLER
        if self.isBossBattle():
            logging.info("We are in a boss battle! Increasing healing threshold for survival")
            HEALING_THRESHOLD = 0.65
        else:
            HEALING_THRESHOLD = 0.55

        # already checked this condition in train(), but double check to be sure
        while self.isBattle():
            try:
                DELAY = 15
                infoElement = WebDriverWait(seleniumobjectsandmethods.singleDriver, DELAY).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//div[@ALIGN='center' and contains(.,'Experience')]")
                    )
                )
                currentHealth, maxHealth, level = self.getPlayerInfo()
                # We need to heal, so use a potion

                if currentHealth < round(maxHealth * HEALING_THRESHOLD) \
                        and not self.isStunned() \
                        and not self.isStartOrEndFight() \
                        and self.hasPotions():
                    self.potionHandler.usePotion(currentHealth, maxHealth)
                    # Originally had a break statement here, was breaking the while loop
                    # WTF I HATE PYTHON
                else:
                    for BATTLE_MESSAGE in constants.battleXpathList:
                        try:
                            seleniumobjectsandmethods.clickLinkByXpath(BATTLE_MESSAGE)
                            break
                            # Early exit so we don't waste time when we find valid action
                        except NoSuchElementException:
                            # Keep going through the list until we find a valid button to click
                            continue

            except TimeoutException:
                logging.info("The page timed out in battle. Reloading")
                self.refreshPage()
                continue

        logging.info("We have completed a battle")

    def followPath(self, mapPath):
        """This method takes a string of ints where each one corresponds to one of 8
        directions on the directional map.

        It isn't really worth fleeing battles when following a path because you usually need the
        EXP and potions anyway. Only useful in Two Rings, but pretty unnecessary."""

        # TODO: FIGURE OUT HOW TO RECOVER FROM DISCONNECTIONS
        # Need WebDriverWait, but for what element?
        for direction in mapPath:
            hasMoved = False
            while not hasMoved:
                # TRY TO WAIT FOR AN ELEMENT
                # IF IT APPEARS, THEN CONTINUE
                # IF IT DOESN'T, GET TimeOutException, SO CONTINUE where hasMoved = False
                # Hopefully this fixes broken page loads
                try:
                    DELAY = 15
                    infoElement = WebDriverWait(seleniumobjectsandmethods.singleDriver, DELAY).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//div[@ALIGN='center' and contains(.,'Experience')]")
                        )
                    )

                    if not self.isBattle():
                        seleniumobjectsandmethods.goToURL(constants.directionDictionary[direction])
                        # if last step ends in battle, program will not loop again to click link
                        # so double check if last step entered a battle before clicking links
                        if (self.isBattle()):
                            self.winBattle();
                        # Try to enter or exit after each step. Really inefficient, but it works
                        self.enterOrExitDungeon()
                        hasMoved = True
                    else:
                        self.winBattle()
                except TimeoutException as e:
                    logging.warning("Failed to load page while moving across map. Reloading page...")
                    hasMoved = False
                    self.refreshPage()
                    # This should catch the unloaded page and try that direction again?
                    # But sometimes the page has already sent the data to server... Hard to know
                    continue

        # Rare scenario: last step of path ends on a battle, but this ends the loop
        # So win the battle and make one last check to see if we can enter/exit the floor

        logging.info("We have arrived at the destination!")

    def enterOrExitDungeon(self):
        # This class is going to go through a list of dictionary of links and try each one
        # Should be able to loop through until it finds the correct one, but that's a big should

        entranceOrExitTemplate = "//A[@HREF='neoquest.phtml?action=move&movelink={}']"
        # Maybe this magic number thing isn't so great... but it cuts down number of entries
        for pageIndex in range(31):
            try:
                seleniumobjectsandmethods.clickLinkByXpath(
                    constants.ENTRANCE_OR_EXIT_TEMPLATE.format(pageIndex)
                )
                logging.info("Successfully clicked link ending in {}".format(pageIndex))
                break
            except NoSuchElementException:
                continue
        # Should probably have a fail condition here, but uh...

    def areItemsPresent(self, itemList):
        """This method will perform an inventory check, and if required items aren't present,
        it will go and grind for x battles before checking to see if they are."""
        # Is kind of a ripoff of isIngredientsPresent() from equipmentmaker, might refactor later
        seleniumobjectsandmethods.goToURL(constants.ITEM_PAGE_URL)
        itemPageSource = seleniumobjectsandmethods.singleDriver.page_source
        for item in itemList:
            if item not in itemPageSource:
                logging.info("We are missing {}".format(item))
                return False
        logging.info("All items in {} are present".format(itemList))
        return True

    def grindForItems(self, itemList):
        haveAllItems = self.areItemsPresent(itemList)
        while not haveAllItems:
            logging.info("We are missing some items. Farming 5 battles and checking back...")
            self.train(5)
            haveAllItems = self.areItemsPresent(itemList)
        self.changeMovementMode("s")
        logging.info("We have all the items!")

    def trainToDesiredLevel(self, desiredLevel, optionalPath=None):
        currentHealth, maxHealth, level = self.getPlayerInfo()
        logging.info("We are trying to grind to level {}".format(desiredLevel))
        if level > desiredLevel:
            return
        # If we need to move somewhere to train, go there first
        if optionalPath is not None:
            self.followPath(optionalPath)
        # Now get the player information -> Gives current health, max health, and level
        while level < desiredLevel:
            self.train(5)
            currentHealth, maxHealth, level = self.getPlayerInfo()
        self.changeMovementMode("s")
        logging.info("We have reached level {}!".format(desiredLevel))
        # If there was a specified path, go back and then reenter the opening
        # THIS IS SO UGLY BUT WE CAN REWORK IT LATER
        if optionalPath is not None:
            logging.info("We had to move away to grind, so resetting our position for movement...")
            self.followPath(self.pathTracker.invertPath(optionalPath))
            self.enterOrExitDungeon()
