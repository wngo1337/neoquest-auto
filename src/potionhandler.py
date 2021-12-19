from selenium.common.exceptions import NoSuchElementException
import seleniumobjectsandmethods

"""This class will take the current and max health values to find the potion
that best recovers the user's health without overhealing.

We let it function on its own by passing the WebDriver defined in seleniumobjectsandmethods.py"""

"""We want a list of potions so if the best potion isn't available, we use the next best one."""

class PotionHandler:
    # THESE WORK YOOOOO
    WEAK_POTION_XPATH = "//A[contains(.,'Use a Weak Healing Potion')]"
    STANDARD_POTION_XPATH = "//A[contains(.,'Use a Standard Healing Potion')]"
    STRONG_POTION_XPATH = "//A[contains(.,'Use a Strong Healing Potion')]"
    GREATER_POTION_XPATH = "//A[contains(.,'Use a Greater Healing Potion')]"
    SUPERIOR_POTION_XPATH = "//A[contains(.,'Use a Superior Healing Potion')]"
    SPIRIT_POTION_XPATH = "//A[contains(.,'Use a Spirit Healing Potion')]"
    
    # Don't want the program to use Spirit Healing Potions, so exclude those

    potionDictionary = {WEAK_POTION_XPATH: 10,
                        STANDARD_POTION_XPATH: 30,
                        STRONG_POTION_XPATH:60,
                        GREATER_POTION_XPATH: 90,
                        SUPERIOR_POTION_XPATH: 120}

    @staticmethod
    def getBestPotion(currentHealth, maxHealth):
        # This method returns the potion that heals the most health without going over the max.
        # IDEA: RETURN A LIST OF POTIONS IN DESCENDING ORDER INSTEAD
        currentPotionXpath = next(iter(PotionHandler.potionDictionary))
        for potionXpath in PotionHandler.potionDictionary:
            # This aims to get the best potion while minimizing the amount of healing wasted
            if abs(currentHealth + PotionHandler.potionDictionary[potionXpath] - maxHealth) < \
                    abs(currentHealth + PotionHandler.potionDictionary[currentPotionXpath] - maxHealth):
                currentPotionXpath = potionXpath

        # Want to get a full list of viable potions so we don't have to go back and forth between potion methods
        potionXpathList = []
        for potionXpath in reversed(list(PotionHandler.potionDictionary.keys())):
            if PotionHandler.potionDictionary[potionXpath] <= \
                    PotionHandler.potionDictionary[currentPotionXpath]:
                potionXpathList.append(potionXpath)

        return potionXpathList

    def usePotion(self, currentHealth, maxHealth):
        potionXpathList = self.getBestPotion(currentHealth, maxHealth)
        for potionXpath in potionXpathList:
            try:
                seleniumobjectsandmethods.clickLinkByXpath(potionXpath)
                break
                # break because we don't want to keep using potions if we found the one we want
            except NoSuchElementException:
                continue




