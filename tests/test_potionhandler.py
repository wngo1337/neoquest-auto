from src import potionhandler
import logging
import pytest

logging.basicConfig(level=logging.DEBUG)

# I totally reworked the PotionHandler, so none of these tests are valid anymore... Oops

# weakPotionTestData = [(12, 25), (15, 30), (17, 35), (25, 50), (20, 40)]
# weakPotionTestData = [data + ((potionhandler.PotionHandler.WEAK_POTION_STRING),) for
#                       data in weakPotionTestData]
# @pytest.mark.parametrize("current, max, expectedPotion", weakPotionTestData)
# def test_getBestPotion_weak(current, max, expectedPotion):
#     assert potionhandler.PotionHandler.getBestPotion(current, max) == expectedPotion

    # 1/25 is failing because weak leaves 14 hp missing, standard overheals by 6 hp.
    # 25/50 should probably be standard potion, but only if we allow overheal.
    # Standard only overheals 5 hp but safer, weak leaves 15 hp missing. Could be dangerous.

# standardPotionTestData = [(1, 35), (30, 60), (34, 70), (40, 80)]
# standardPotionTestData = [data + ((potionhandler.PotionHandler.STANDARD_POTION_STRING),) for
#                           data in standardPotionTestData]
# @pytest.mark.parametrize("current, max, expectedPotion", standardPotionTestData)
# def test_getBestPotion_standard(current, max, expectedPotion):
#     assert potionhandler.PotionHandler.getBestPotion(current, max) == expectedPotion

# def test_getBestPotion_strong():
#
# def test_getBestPotion_greater():
#
# def test_getBestPotion_superior():






