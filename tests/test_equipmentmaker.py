import sys
sys.path.append('/Users/WilliamLaptop/PycharmProjects/neoquestAutoplayer/src')
from src import equipmentmaker
from src import autobattler
import pytest
import logging

logging.basicConfig(level=logging.INFO)

myAutoBattler = autobattler.AutoBattler()
myAutoBattler.loginManager.loginNeopets()

def test_getIngredientID():
    testIngredient = "chunk of metal"
    expectedID = "item230001"
    assert myAutoBattler.equipmentMaker.getIngredientID(testIngredient) == expectedID

def test_isIngredientsPresent():
    # Tricky to test because ingredients won't always be present...
    myAutoBattler.equipmentMaker.setEquipmentRecipe("Energy Shield")
    assert myAutoBattler.equipmentMaker.isIngredientsPresent() == True

def test_makeEquipment():
    # Currently can only do after setting a recipe
    # Also unrepeatable so uh...
    assert True

def test_setEquipmentRecipe():
    myAutoBattler.equipmentMaker.setEquipmentRecipe("Magic Robe")
    assert myAutoBattler.equipmentMaker.makerID == 90010005
    assert myAutoBattler.equipmentMaker.equipmentID == 210011
    assert myAutoBattler.equipmentMaker.recipe == ("cave lupe pelt", "stretch of rotted cloth",
                                                "tiny obsidian", "glowing stone")

def test_isIngredientsPresent():
    # Pretty hard to test since we only allow checking for the current recipe's ingredients
    assert True

def test_setEquipmentRecipe_noItems():
    # Testing no-crafting (a.k.a. dropped weapons) equipment recipe setting
    myAutoBattler.equipmentMaker.setEquipmentRecipe("Inferno Robe")
    assert myAutoBattler.equipmentMaker.makerID == -1
    assert myAutoBattler.equipmentMaker.equipmentID == 210014
    assert myAutoBattler.equipmentMaker.recipe == tuple()

def test_equipEquipment_weapon():
    # Ideally test a default wand
    myAutoBattler.equipmentMaker.setEquipmentRecipe("White Wand")
    myAutoBattler.equipmentMaker.equipEquipment()
    assert "You equipped" in myAutoBattler.driver.page_source \
           and "as your weapon" in myAutoBattler.driver.page_source

def test_equipEquipment_armour():
    myAutoBattler.equipmentMaker.setEquipmentRecipe("Energy Shield")
    myAutoBattler.equipmentMaker.equipEquipment()
    assert "You equipped" in myAutoBattler.driver.page_source \
           and "as your armour" in myAutoBattler.driver.page_source



