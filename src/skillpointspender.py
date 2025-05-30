from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import seleniumobjectsandmethods
import constants

"""Maybe want to make a dictionary of what skill to spend on depending on level"""


class SkillPointSpender:

    levels_to_skill_investments = {}
    SKILL_PAGE_ADDRESS = (
        "http://www.neopets.com/games/neoquest/neoquest.phtml?action=skill"
    )
    SKILL_SELECT_ADDRESS_TEMPLATE = (
        "http://www.neopets.com/games/neoquest/"
        "neoquest.phtml?skill_choice={}&action=skill"
    )
    SKILL_CONFIRM_ADDRESS_TEMPLATE = (
        "http://www.neopets.com/games/neoquest/"
        "neoquest.phtml?action=skill&skill_choice={}&confirm=1"
    )
    SPEND_POINTS_XPATH = "//A[contains(.,'Spend Skill Points')]"

    # IMPORTANT!!! EITHER CONVERT ZERO-BASED LEVELS TO REAL, OR ADD 1 TO THE LEVEL FROM PAGE SOURCE
    # Setting up the dictionary for use
    for level in range(2, 51):
        #         # These are the numbers that correspond with Life Weapons, Field Medic, and Lifesteal
        # Negative values are a quick fix for initial skill setup
        # Idea is seven initial points, so seven values before level 1 lol
        levels_to_skill_investments.update(
            dict.fromkeys([-7, -4, -1, 4, 7, 10, 13, 16, 19, 22], 5001)
        )
        levels_to_skill_investments.update(
            dict.fromkeys([-6, -3, 2, 5, 8, 11, 14, 17, 20, 23], 5002)
        )
        levels_to_skill_investments.update(
            dict.fromkeys([-5, -2, 3, 6, 9, 12, 15, 18, 21, 24], 5003)
        )
    #
    #     # TODO: There has to be a better way to build the dictionary...
    levels_to_skill_investments.update(
        dict.fromkeys([25, 29, 33, 37, 41, 45, 49], "3001")
    )
    levels_to_skill_investments.update(
        dict.fromkeys([26, 30, 34, 38, 42, 46, 50], "3002")
    )
    levels_to_skill_investments.update(dict.fromkeys([27, 31, 35, 39, 43, 47], "3003"))
    levels_to_skill_investments.update(dict.fromkeys([28, 32, 36, 40, 44, 48], "3004"))

    # THESE ARE THE EXPERIMENTAL ICE BUILD
    #     if level >= 2 and level <= 4:
    #         skillDictionary[level] = "2001"
    #     if level >= 5 and level <= 14:
    #         skillDictionary[level] = "2002"
    #
    #     skillDictionary.update(dict.fromkeys([15, 19, 23, 27, 31, 35, 39, 43, 47], "3001"))
    #     skillDictionary.update(dict.fromkeys([16, 20, 24, 28, 32, 36, 40, 44, 48], "3002"))
    #     skillDictionary.update(dict.fromkeys([17, 21, 25, 29, 33, 37, 41, 45, 49], "3003"))
    #     skillDictionary.update(dict.fromkeys([18, 22, 26, 30, 34, 38, 42, 46, 50], "3004"))

    @staticmethod
    def get_skill_id(level):
        return SkillPointSpender.levels_to_skill_investments[level]

    def initial_skill_setup(self):
        # Maybe a misplaced method. CALL THIS AFTER YOU NAVIGATE TO INITIAL SKILL SELECTION PAGE
        # Start the game with 7 skill points.
        # Life build requires 3/3/2/0 split
        # Generally, better to work with URLs than Xpaths

        for i in range(-7, 0):
            seleniumobjectsandmethods.go_to_url(
                self.SKILL_SELECT_ADDRESS_TEMPLATE.format(
                    self.levels_to_skill_investments[i]
                )
            )
        # Really don't want to bother putting these in a file since they are only used here...
        seleniumobjectsandmethods.go_to_url(
            "http://www.neopets.com/games/neoquest/neoquest.phtml?cc_accept=1"
        )
        seleniumobjectsandmethods.go_to_url(
            "http://www.neopets.com/games/neoquest/neoquest.phtml?weapon_choice=5"
        )
        seleniumobjectsandmethods.go_to_url(
            "http://www.neopets.com/games/neoquest/neoquest.phtml?cc_accept=1"
        )
        seleniumobjectsandmethods.go_to_url(
            "http://www.neopets.com/games/neoquest/neoquest.phtml?cc_accept=1"
        )
        seleniumobjectsandmethods.go_to_url(
            "http://www.neopets.com/games/neoquest/neoquest.phtml"
        )

    def has_points(self):
        try:
            seleniumobjectsandmethods.single_driver.find_element(
                By.XPATH, self.SPEND_POINTS_XPATH
            )
        except NoSuchElementException:
            return False
        return True

    def spendPoints(self, level):
        # Go to the skill page
        seleniumobjectsandmethods.go_to_url(self.SKILL_PAGE_ADDRESS)

        skill_id = self.get_skill_id(level)
        # Finally select the skill address
        seleniumobjectsandmethods.go_to_url(
            self.SKILL_SELECT_ADDRESS_TEMPLATE.format(skill_id)
        )
        seleniumobjectsandmethods.go_to_url(
            self.SKILL_CONFIRM_ADDRESS_TEMPLATE.format(skill_id)
        )
        seleniumobjectsandmethods.go_to_url(constants.MAIN_GAME_URL)

        # Not going to bother implementing a method for multiple skill point spending


# if __name__ == "__main__":
#     for level in sorted(SkillPointSpender.skillDictionary):
#         print("{} {}".format(level, SkillPointSpender.skillDictionary[level]))
