import sys
sys.path.append('/Users/WilliamLaptop/PycharmProjects/neoquestAutoplayer/src')
from src import equipmentmaker
from src import autobattler
import pytest
import logging

logging.basicConfig(level=logging.INFO)

auto_battler = autobattler.AutoBattler()
auto_battler.login_manager.login_neopets()

def test_get_ingredient_id():
    test_ingredient = "chunk of metal"
    expectedID = "item230001"
    assert auto_battler.equipment_maker.get_ingredient_id(test_ingredient) == expectedID

def test_is_ingredients_present():
    # Tricky to test because ingredients won't always be present...
    auto_battler.equipment_maker.set_equipment_recipe("Energy Shield")
    assert auto_battler.equipment_maker.are_ingredients_present() == True

def test_set_equipment_recipe():
    auto_battler.equipment_maker.set_equipment_recipe("Magic Robe")
    assert auto_battler.equipment_maker.maker_id == 90010005
    assert auto_battler.equipment_maker.equipment_id == 210011
    assert auto_battler.equipment_maker.recipe == ("cave lupe pelt", "stretch of rotted cloth",
                                                "tiny obsidian", "glowing stone")

def test_set_equipment_recipe_no_items():
    # Testing no-crafting (a.k.a. dropped weapons) equipment recipe setting
    auto_battler.equipment_maker.set_equipment_recipe("Inferno Robe")
    assert auto_battler.equipment_maker.maker_id == -1
    assert auto_battler.equipment_maker.equipment_id == 210014
    assert auto_battler.equipment_maker.recipe == tuple()

def test_equip_equipment_weapon():
    # Ideally test a default wand
    auto_battler.equipment_maker.set_equipment_recipe("White Wand")
    auto_battler.equipment_maker.equip_equipment()
    assert "You equipped" in auto_battler.driver.page_source \
           and "as your weapon" in auto_battler.driver.page_source

def test_equip_equipment_armour():
    auto_battler.equipment_maker.set_equipment_recipe("Energy Shield")
    auto_battler.equipment_maker.equip_equipment()
    assert "You equipped" in auto_battler.driver.page_source \
           and "as your armour" in auto_battler.driver.page_source



