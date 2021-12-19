from selenium import webdriver
import seleniumobjectsandmethods
import logging
import gameinfo
import constants

logging.basicConfig(level=logging.INFO)

class EquipmentMaker:
    # Defining the giga dictionary of items and their corresponding in-game IDs
    # Maybe we only need to track the ones that we need for our strategy
    # Items will have their name as an identifier, and their value will be a tuple
    # Looks like: "item name":(itemID (for equipping), makerID, (ingredient1, ingredient2, etc.))
    # Might actually be better to rework into a data class, but that seems overkill tbh
    # NOT SURE IF I WANT TO PUT THIS IN A SEPARATE GAMEINFO.PY MODULE OR WHAT

    # Energy Shield maker is Morax Dorangis, Magic Robe is Choras Tillie, Steel Wand is Eleus Batrin, etc.

    ITEM_MAKER_ADDRESS_TEMPLATE = \
        "http://www.neopets.com/games/neoquest/neoquest.phtml?action=talk&target={}&say=&give=1"
    EQUIP_ADDRESS_TEMPLATE = \
        "http://www.neopets.com/games/neoquest/neoquest.phtml?action=items&equipitemid={}&do=equip"

    def __init__(self):
        # Ideally, we read these in from a text file
        self.equipmentName = None
        self.equipmentID = None
        self.makerID = None
        self.recipe = None

    def getIngredientID(self, ingredientName):
        return gameinfo.itemIDDictionary[ingredientName]

    def setEquipmentRecipe(self, equipmentName):
        # This method consults the equipmentInfoDictionary for relevant info before using
        self.equipmentName = equipmentName
        self.equipmentID, self.makerID, self.recipe = gameinfo.equipmentInfoDictionary[equipmentName]

        logging.info(self.equipmentName)
        logging.info("equipID={}, makerID={}".format(self.equipmentID, self.makerID))
        logging.info("".join([str(ingredient) for ingredient in self.recipe]))

    def isIngredientsPresent(self):
        # Must use temporary driver reference here because need to access page source
        seleniumobjectsandmethods.goToURL(constants.ITEM_PAGE_URL)
        itemPageSource = seleniumobjectsandmethods.singleDriver.page_source
        for ingredient in self.recipe:
            if ingredient not in itemPageSource:
                logging.info("Don't have the necessary ingredients!")
                return False
        logging.info("We have all the necessary ingredients!")
        return True

    def makeEquipment(self):
        # This method consults the equipment dictionary for the relevant info before using it
        if self.isIngredientsPresent():
            seleniumobjectsandmethods.goToURL(
                self.ITEM_MAKER_ADDRESS_TEMPLATE.format(self.makerID)
            )
            for ingredient in self.recipe:
                # find the selection radio button and click it
                pathTemplate = "//INPUT[@TYPE='radio' and @NAME='{}']"
                seleniumobjectsandmethods.clickLinkByXpath(pathTemplate.format(
                    self.getIngredientID(ingredient)
                ))
            seleniumobjectsandmethods.clickLinkByXpath("//INPUT[contains(@VALUE, 'Give items to')]")
            # Should always equip after making, so just do it now
            self.equipEquipment()

    def equipEquipment(self):
        seleniumobjectsandmethods.goToURL(constants.ITEM_PAGE_URL)
        seleniumobjectsandmethods.goToURL(self.EQUIP_ADDRESS_TEMPLATE.format(self.equipmentID))
        
        logging.info("We have equipped the {}".format(self.equipmentName))
