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
        self.equipment_name = None
        self.equipment_id = None
        self.maker_id = None
        self.recipe = None

    def get_ingredient_id(self, ingredient_name):
        return gameinfo.item_names_to_ids[ingredient_name]

    def set_equipment_recipe(self, equipment_name):
        # This method consults the equipmentInfoDictionary for relevant info before using
        self.equipment_name = equipment_name
        self.equipment_id, self.maker_id, self.recipe = gameinfo.equipment_names_to_recipes[equipment_name]

        logging.info(self.equipment_name)
        logging.info("equipID={}, makerID={}".format(self.equipment_id, self.maker_id))
        logging.info("".join([str(ingredient) for ingredient in self.recipe]))

    def are_ingredients_present(self):
        # Must use temporary driver reference here because need to access page source
        seleniumobjectsandmethods.go_to_url(constants.ITEM_PAGE_URL)
        item_page_source = seleniumobjectsandmethods.single_driver.page_source
        for ingredient in self.recipe:
            if ingredient not in item_page_source:
                logging.info("Don't have the necessary ingredients!")
                return False
        logging.info("We have all the necessary ingredients!")
        return True

    def make_equipment(self):
        # This method consults the equipment dictionary for the relevant info before using it
        if self.are_ingredients_present():
            seleniumobjectsandmethods.go_to_url(
                self.ITEM_MAKER_ADDRESS_TEMPLATE.format(self.maker_id)
            )
            for ingredient in self.recipe:
                # find the selection radio button and click it
                path_template = "//INPUT[@TYPE='radio' and @NAME='{}']"
                seleniumobjectsandmethods.click_link_by_xpath(path_template.format(
                    self.get_ingredient_id(ingredient)
                ))
            seleniumobjectsandmethods.click_link_by_xpath("//INPUT[contains(@VALUE, 'Give items to')]")
            # Should always equip after making, so just do it now
            self.equip_equipment()

    def equip_equipment(self):
        seleniumobjectsandmethods.go_to_url(constants.ITEM_PAGE_URL)
        seleniumobjectsandmethods.go_to_url(self.EQUIP_ADDRESS_TEMPLATE.format(self.equipment_id))
        
        logging.info("We have equipped the {}".format(self.equipment_name))
