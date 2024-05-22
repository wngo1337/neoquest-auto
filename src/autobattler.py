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

class AutoBattler:
    def __init__(self):
        self.login_manager = loginmanager.LoginManager()
        self.potion_handler = potionhandler.PotionHandler()
        self.skill_point_spender = skillpointspender.SkillPointSpender()
        self.equipment_maker = equipmentmaker.EquipmentMaker()
        self.path_tracker = pathtracker.PathTracker()

    """This method walks back and forth on the world map on hunting mode.
    It automatically battles monsters, using attacks, skills, and potions as necessary.
    
    The basic prototype will just use basic attacks, which should be more than sufficient
    for any game mode."""

    def close_auto_battler(self):
        seleniumobjectsandmethods.single_driver.quit()

    def get_player_info(self):
        my_info_element = WebDriverWait(seleniumobjectsandmethods.single_driver, 5). \
            until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Name:')]")))
        player_info = my_info_element.text

        # TODO: Fix the str parsing here. It works, but it is pretty dumb
        health_info_object = re.search("Health:(.*)", player_info)
        health_info = health_info_object.group(0).split(" ")[1]
        level_info_object = re.search("Level:(.*)", player_info)
        level = level_info_object.group(0).split(" ")[1]

        current_health, max_health = health_info.split("/")

        return int(current_health), int(max_health), int(level)

    def refresh_page(self):
        seleniumobjectsandmethods.go_to_url(constants.MAIN_GAME_URL)

    # Would be nice to be able to combine these three into one method
    def is_battle(self):
        page_source = seleniumobjectsandmethods.single_driver.page_source
        return constants.NAVIGATION_IMAGE_URL not in page_source

    """
    Tricky: "Stuns you for" occurs on first turn you are stunned, while
    "You are stunned" can be on the page where you are able to act again, so need to check
    for presence of Attack button to see if you are really stunned...
    """
    def is_stunned(self):
        page_source = seleniumobjectsandmethods.single_driver.page_source
        return ("stuns you for" in page_source) or ("You are stunned" in page_source and "Attack" not in page_source)

    # These are pretty weak conditions, but they do work...
    def is_start_or_end_of_fight(self):
        page_source = seleniumobjectsandmethods.single_driver.page_source
        return "You defeated" in page_source or "You are attacked by" in page_source

    def has_potions(self):
        # Can probably do this with a regex later...
        page_source = seleniumobjectsandmethods.single_driver.page_source
        return "Use a " in page_source and "Healing Potion" in page_source

    def is_boss_battle(self):
        page_source = seleniumobjectsandmethods.single_driver.page_source
        for link in constants.boss_images:
            if link in page_source:
                return True
        return False

    def change_movement_mode(self, mode):
        if self.is_battle():
            self.win_battle()
            # Input can either be "s" for sneaking or "h" for hunting
        if mode.lower() == "s":
            seleniumobjectsandmethods.go_to_url(constants.SNEAKING_MODE_URL)
        elif mode.lower() == "h":
            seleniumobjectsandmethods.go_to_url(constants.HUNTING_MODE_URL)
        logging.info("Switched to {} movement mode".format(mode))

    def train(self, num_battles=150):
        # Want function to halt eventually, but also want to be able to train x number of times
        self.change_movement_mode("h")
        while num_battles > 0:
            try:
                DELAY = 4
                info_element = WebDriverWait(seleniumobjectsandmethods.single_driver, DELAY).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//div[@ALIGN='center' and contains(.,'Experience')]")
                    )
                )
                # If we see the direction arrows, we want to "move" in place to encounter monsters
                if not self.is_battle():
                    if self.skill_point_spender.has_points():
                        current_health, max_health, level = self.get_player_info()
                        self.skill_point_spender.spendPoints(level)
                    seleniumobjectsandmethods.go_to_url(constants.MOVE_NOMOVE_URL)
                else:
                    self.win_battle()
                    num_battles -= 1
            except TimeoutException:
                logging.warning("The program ran into an error while training, refreshing page")
                self.refresh_page()
                continue

    def win_battle(self):
        # This function simply attacks and heals when necessary to win random encounters
        """Might be nice to implement a strategy pattern here, but not really necessary.
        Only two options: monsters and bosses"""

        # Determine whether is boss battle or regular encounter
        if self.is_boss_battle():
            logging.info("We are in a boss battle! Increasing healing threshold for survival")
            HEALING_THRESHOLD = 0.65
        else:
            HEALING_THRESHOLD = 0.55

        # already checked this condition in train(), but double check to be sure
        while self.is_battle():
            try:
                DELAY = 4
                info_element = WebDriverWait(seleniumobjectsandmethods.single_driver, DELAY).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//div[@ALIGN='center' and contains(.,'Experience')]")
                    )
                )
                current_health, max_health, level = self.get_player_info()
                # We need to heal, so use a potion

                if current_health < round(max_health * HEALING_THRESHOLD) \
                        and not self.is_stunned() \
                        and not self.is_start_or_end_of_fight() \
                        and self.has_potions():
                    self.potion_handler.use_potion(current_health, max_health)
                    # Originally had a break statement here, was breaking the while loop
                else:
                    for BATTLE_MESSAGE in constants.battle_options_xpaths:
                        try:
                            seleniumobjectsandmethods.click_link_by_xpath(BATTLE_MESSAGE)
                            break
                            # Early exit so we don't waste time when we find valid action
                        except NoSuchElementException:
                            # Keep going through the list until we find a valid button to click
                            continue

            except TimeoutException:
                logging.info("The page timed out in battle. Reloading")
                self.refresh_page()
                continue

        logging.info("We have completed a battle")

    def follow_path(self, map_path):
        """This method takes a string of ints where each one corresponds to one of 8
        directions on the directional map.

        It isn't really worth fleeing battles when following a path because you usually need the
        EXP and potions anyway. Only useful in Two Rings, but pretty unnecessary."""

        for direction in map_path:
            has_moved = False
            while not has_moved:
                # try to wait for an element
                # if it appears, then continue
                # if it doesn't, get timeoutexception, so continue where hasmoved = false
                # Hopefully this fixes broken page loads
                try:
                    DELAY = 4
                    info_element = WebDriverWait(seleniumobjectsandmethods.single_driver, DELAY).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//div[@ALIGN='center' and contains(.,'Experience')]")
                        )
                    )

                    if not self.is_battle():
                        seleniumobjectsandmethods.go_to_url(constants.numbers_to_direction_urls[direction])
                        # if last step ends in battle, program will not loop again to click link
                        # so double check if last step entered a battle before clicking links
                        if (self.is_battle()):
                            self.win_battle();
                        # Try to enter or exit after each step. Really inefficient, but it works
                        self.enter_or_exit_dungeon()
                        has_moved = True
                    else:
                        self.win_battle()
                except TimeoutException as e:
                    logging.warning("Failed to load page while moving across map. Reloading page...")
                    has_moved = False
                    self.refresh_page()
                    # This should catch the unloaded page and try that direction again?
                    # But sometimes the page has already sent the data to server... Hard to know
                    continue

        logging.info("We have arrived at the destination!")

    def enter_or_exit_dungeon(self):
        # Loop through a range of possible entrance/exit URLs until we find the valid one
        entranceOrExitTemplate = "//A[@HREF='neoquest.phtml?action=move&movelink={}']"
        # Maybe this magic number thing isn't so great... but it cuts down number of entries
        for page_index in range(31):
            try:
                seleniumobjectsandmethods.click_link_by_xpath(
                    constants.ENTRANCE_OR_EXIT_TEMPLATE.format(page_index)
                )
                logging.info("Successfully clicked link ending in {}".format(page_index))
                break
            except NoSuchElementException:
                continue
        # Should probably have a fail condition here, but uh...

    def are_items_present(self, item_list):
        """This method will perform an inventory check, and if required items aren't present,
        it will go and grind for x battles before checking to see if they are."""
        # Is kind of a ripoff of isIngredientsPresent() from equipmentmaker, might refactor later
        seleniumobjectsandmethods.go_to_url(constants.ITEM_PAGE_URL)
        item_page_source = seleniumobjectsandmethods.single_driver.page_source
        for item in item_list:
            if item not in item_page_source:
                logging.info("We are missing {}".format(item))
                return False
        logging.info("All items in {} are present".format(item_list))
        return True

    def grind_for_items(self, item_list):
        have_all_items = self.are_items_present(item_list)
        while not have_all_items:
            logging.info("We are missing some items. Farming 5 battles and checking back...")
            self.train(5)
            have_all_items = self.are_items_present(item_list)
        self.change_movement_mode("s")
        logging.info("We have all the items!")

    def train_to_desired_level(self, desired_level, optional_path=None):
        currentHealth, maxHealth, level = self.get_player_info()
        logging.info("We are trying to grind to level {}".format(desired_level))
        if level > desired_level:
            return
        # If we need to move somewhere to train, go there first
        if optional_path is not None:
            self.follow_path(optional_path)
        # Now get the player information -> Gives current health, max health, and level
        while level < desired_level:
            self.train(5)
            currentHealth, maxHealth, level = self.get_player_info()
        self.change_movement_mode("s")
        logging.info("We have reached level {}!".format(desired_level))
        # If there was a specified path, go back and then reenter the opening
        # THIS IS SO UGLY BUT WE CAN REWORK IT LATER
        if optional_path is not None:
            logging.info("We had to move away to grind, so resetting our position for movement...")
            self.follow_path(self.path_tracker.invert_path(optional_path))
            self.enter_or_exit_dungeon()
