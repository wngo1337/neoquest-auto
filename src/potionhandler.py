from selenium.common.exceptions import NoSuchElementException
import seleniumobjectsandmethods

"""This class will take the current and max health values to find the potion
that best recovers the user's health without overhealing.

We let it function on its own by passing the WebDriver defined in seleniumobjectsandmethods.py"""

"""We want a list of potions so if the best potion isn't available, we use the next best one."""

class PotionHandler:
    WEAK_POTION_XPATH = "//A[contains(.,'Use a Weak Healing Potion')]"
    STANDARD_POTION_XPATH = "//A[contains(.,'Use a Standard Healing Potion')]"
    STRONG_POTION_XPATH = "//A[contains(.,'Use a Strong Healing Potion')]"
    GREATER_POTION_XPATH = "//A[contains(.,'Use a Greater Healing Potion')]"
    SUPERIOR_POTION_XPATH = "//A[contains(.,'Use a Superior Healing Potion')]"
    SPIRIT_POTION_XPATH = "//A[contains(.,'Use a Spirit Healing Potion')]"
    
    # Don't want the program to use Spirit Healing Potions, so exclude those

    potion_names_to_healing_values = {WEAK_POTION_XPATH: 10,
                        STANDARD_POTION_XPATH: 30,
                        STRONG_POTION_XPATH:60,
                        GREATER_POTION_XPATH: 90,
                        SUPERIOR_POTION_XPATH: 120}

    @staticmethod
    def get_best_potion(current_health, max_health):
        # This method returns the potion that heals the most health without going over the max.
        current_potion_xpath = next(iter(PotionHandler.potion_names_to_healing_values))
        for potion_xpath in PotionHandler.potion_names_to_healing_values:
            # This aims to get the best potion while minimizing the amount of healing wasted
            if abs(current_health + PotionHandler.potion_names_to_healing_values[potion_xpath] - max_health) < \
                    abs(current_health + PotionHandler.potion_names_to_healing_values[current_potion_xpath] - max_health):
                current_potion_xpath = potion_xpath

        # Want to get a full list of viable potions so we don't have to go back and forth between potion methods
        potion_xpaths = []
        for potion_xpath in reversed(list(PotionHandler.potion_names_to_healing_values.keys())):
            if PotionHandler.potion_names_to_healing_values[potion_xpath] <= \
                    PotionHandler.potion_names_to_healing_values[current_potion_xpath]:
                potion_xpaths.append(potion_xpath)

        return potion_xpaths

    def use_potion(self, current_health, max_health):
        potionXpathList = self.get_best_potion(current_health, max_health)
        for potionXpath in potionXpathList:
            try:
                seleniumobjectsandmethods.click_link_by_xpath(potionXpath)
                break
                # break because we don't want to keep using potions if we found the one we want
            except NoSuchElementException:
                continue




