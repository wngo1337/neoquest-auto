import autobattler
import gameinfo
import logging
import constants
import seleniumobjectsandmethods

class ExperimentalTaskPerformer:

    def __init__(self):
        self.autobattler = autobattler.AutoBattler()
        self.autobattler.loginManager.loginNeopets()

# This class doesn't really have any instance variables... Just a list of methods that perform tasks

    def splitPathByLastStep(self, movementPath):
        pathWithoutLastStep = movementPath[:-1]
        lastStep = movementPath[-1]
        return pathWithoutLastStep, lastStep

    def completeInitialSetup(self):
        self.autobattler.skillPointSpender.initialSkillSetup()

        currentHealth, maxHealth, level = self.autobattler.getPlayerInfo()
        self.autobattler.followPath("44")
        while level < 4:
            logging.info("Grinding to level 4 before continuing...")
            self.autobattler.train(1)
            currentHealth, maxHealth, level = self.autobattler.getPlayerInfo()
            if currentHealth < 25:
                self.autobattler.followPath("3")
                seleniumobjectsandmethods.goToURL(
                    "http://www.neopets.com/games/neoquest/neoquest.phtml?action=talk&target=90010001")
                seleniumobjectsandmethods.goToURL(constants.MAIN_GAME_URL)
                self.autobattler.followPath("6")
        # Now go hunt plains lupes
        self.autobattler.followPath("1111")
        while level < 8:
            logging.info("Grinding to level 8 before continuing...")
            self.autobattler.train(5)
            currentHealth, maxHealth, level = self.autobattler.getPlayerInfo()
        self.autobattler.changeMovementMode("s")
        self.autobattler.followPath("888855")
        logging.info("Initial setup completed!")

    def completeDankCaveF1(self):
        # PLAYER SHOULD GO GRIND 5 GLOWING STONES I THINK BEFORE RUNNING THIS
        # Honestly, chance is so low that it doesn't happen by level 8, who cares
        # Go to Morax and get a new armour
        logging.info("Getting new armour from Morax Dorangis...")

        self.autobattler.followPath("6")
        self.autobattler.equipmentMaker.setEquipmentRecipe("Energy Shield")
        self.autobattler.equipmentMaker.makeEquipment()
        self.autobattler.followPath(self.autobattler.pathTracker.invertPath("6"))

        logging.info("Walking to the Dank Cave...")

        self.autobattler.followPath(gameinfo.movementPathDictionary["eleusToDankCave"])
        # Want to stop right before floor 2 to grind cave lupe pelt

        logging.info("Walking from Dank Cave F1 to F2...")

        F1ToF2Path = gameinfo.movementPathDictionary["dankCaveF1ToF2"]
        stopBeforeF2Path, lastF2Step = self.splitPathByLastStep(F1ToF2Path)
        self.autobattler.followPath(stopBeforeF2Path)
        self.autobattler.grindForItems(("cave lupe pelt",))
        self.autobattler.followPath(lastF2Step)

        logging.info("Dank Cave F1 completed!")

    def completeDankCaveF2(self):
        # Key items to grind: tiny beryl, tiny obsidian
        logging.info("Walking to Dank Cave F3...")

        f2ToF3Path = gameinfo.movementPathDictionary["dankCaveF2ToF3"]
        stopBeforeF3Path, lastF2Step = self.splitPathByLastStep(f2ToF3Path)
        self.autobattler.followPath(stopBeforeF3Path)
        # Grind the ingredient for silver wand before going to next floor
        self.autobattler.grindForItems(("tiny beryl", "tiny obsidian"))
        self.autobattler.followPath(lastF2Step)

        logging.info("Dank Cave F2 completed!")

    def completeDankCaveF3(self):
        # Don't need any items. Just grind to 11 and move to last floor
        logging.info("Walking to dank Cave F4...")

        f3ToF4Path = gameinfo.movementPathDictionary["dankCaveF3ToF4"]
        stopBeforeF4Path, lastF3Step = self.splitPathByLastStep(f3ToF4Path)
        currentHealth, maxHealth, level = self.autobattler.getPlayerInfo()
        self.autobattler.followPath(stopBeforeF4Path)
        self.autobattler.trainToDesiredLevel(11)
        self.autobattler.changeMovementMode("s")
        self.autobattler.followPath(lastF3Step)

        logging.info("Dank Cave F3 completed!")

    def completeDankCaveF4(self):
        # Need to grab aluminum rod and Xantan's Ring
        logging.info("Walking to Xantan...")

        f4ToXantanPath = gameinfo.movementPathDictionary["dankCaveF4ToXantan"]
        stopBeforeExitPath, lastF4Step = self.splitPathByLastStep(f4ToXantanPath)
        self.autobattler.grindForItems(("corroded aluminum rod",))
        self.autobattler.followPath(stopBeforeExitPath)
        # Will automatically fight Xantan here
        self.autobattler.grindForItems(("stretch of rotted cloth",))
        self.autobattler.trainToDesiredLevel(14)
        self.autobattler.followPath(lastF4Step)

        logging.info("Dank Cave F4 completed!")

    def completeEleusAfterXantan(self):
        logging.info("Walking back to Eleus Batrin for weapon upgrade...")

        self.autobattler.followPath(gameinfo.movementPathDictionary["afterDankCaveTeleporterToEleus"])
        # # Should be at Eleus now
        self.autobattler.equipmentMaker.setEquipmentRecipe("Silver Wand")
        self.autobattler.equipmentMaker.makeEquipment()
        # Must go to Choras Tillie now
        self.autobattler.followPath("8")
        self.autobattler.equipmentMaker.setEquipmentRecipe("Magic Robe")
        self.autobattler.equipmentMaker.makeEquipment()
        # Reset position to Eleus for next movement script
        self.autobattler.followPath("1")

        logging.info("Weapon and armour upgrade completed!")

    def completeJungleRuinsF1FromEleus(self):
        # Nothing to grind. Just walking to next location
        logging.info("Walking to Jungle Ruins F2...")
        self.autobattler.followPath(gameinfo.movementPathDictionary["eleusToJungleRuins"])
        self.autobattler.followPath(gameinfo.movementPathDictionary["jungleRuinsF1ToF2"])

    def completeJungleRuinsF2ToKreai(self):
        # Need to grind jungle beast claw and noil's tooth. Don't leave without them!
        # Move forward to encounter jungle beasts
        logging.info("Walking to Kreai...")
        f1ToKreaiPath = gameinfo.movementPathDictionary["jungleRuinsF2ToKreai"]
        stopBeforeKreaiPath, lastKreaiStep = self.splitPathByLastStep(f1ToKreaiPath)
        self.autobattler.followPath("3555")
        # Get jungle beast claw before moving on
        self.autobattler.grindForItems(("jungle beast claw",))
        self.autobattler.trainToDesiredLevel(16)
        # reset position to staircase for next movement script
        self.autobattler.followPath(self.autobattler.pathTracker.invertPath("3555"))
        # This is dumb, but followPath automatically enters stairs, so must go back up
        self.autobattler.enterOrExitDungeon()
        # Path will now take us to one tile in front of Kreai. Grind for noil's tooth here
        self.autobattler.followPath(stopBeforeKreaiPath)
        self.autobattler.grindForItems(("noil's tooth",))
        currentHealth, maxHealth, level = self.autobattler.getPlayerInfo()
        """Got the item, so grind to 18 and take the last step and beat Kreai's ass
         before taking the teleporter"""
        self.autobattler.trainToDesiredLevel(18)

        """Enemies at beginning of stage are not strong enough to grind to 18, so we have no choice
        but to end the right at Kreai and 'manually' enter the teleporter after"""
        self.autobattler.followPath(lastKreaiStep)
        self.autobattler.changeMovementMode("s")
        self.autobattler.followPath("2")

        logging.info("Jungle Ruins F2 completed!")

    def completeJungleRuinsAfterKreaiToGors(self):
        # Just need to grind jungle pauldrons from here
        # Don't know where they show up though, so might need to split the path and not use dictionary
        logging.info("Walking to teleporter maze to grind...")

        self.autobattler.followPath("55777778855553214122233214441144446777664412222222235555555555"
                                    "555555555877777777855558866")
        # Should take us to around the teleporter maze
        # Get the jungle pauldrons before moving on
        self.autobattler.grindForItems(("jungle pauldrons",))
        self.autobattler.followPath("446855553"
                                    "55876685532222214444")
        # Grind to maybe 20 here to be safe
        self.autobattler.trainToDesiredLevel(21)
        # If we are past 20, go grind two more levels after getting to Gors level
        self.autobattler.changeMovementMode("s")
        self.autobattler.followPath("8322238852")
        self.autobattler.trainToDesiredLevel(23)
        # Should take us all the way to Gors and take the teleporter...
        self.autobattler.changeMovementMode("s")
        self.autobattler.followPath("222222222222222222")

        logging.info("Gors level completed!")

    def completeJungleRuinsWeaponUpgrade(self):
        # Start at place after Gor's teleporter
        # Works pretty well, straightforward
        logging.info("Walking to Denethrir for upgrade...")

        self.autobattler.followPath(gameinfo.movementPathDictionary["jungleRuinsAfterGorsToDenethrir"])
        self.autobattler.equipmentMaker.setEquipmentRecipe("Nature Wand")
        self.autobattler.equipmentMaker.makeEquipment()

        logging.info("Weapon upgrade completed!")

    def completeRollayFromDenethrir(self):
        # Navigate back from Denethrir all the way to Rollay
        # No items to grind, just levels
        logging.info("Walking from Denethrir to Jungle Ruins F3...")
        self.autobattler.followPath(gameinfo.movementPathDictionary["jungleRuinsDenethrirToF3"])
        self.autobattler.trainToDesiredLevel(24)

        # Now we want to walk halfway to Rollay and grind WAY up, maybe to 27
        # This should already be true, but just in case. Want to hunt all the way to Rollay
        self.autobattler.followPath("55558588788777788878888553333333353332233333555555558")
        self.autobattler.trainToDesiredLevel(27)

        # Walk near Rollay to encounter higher level enemies
        self.autobattler.followPath(
            "777777777777666677888668767778877776776666644444444"
            "414441114466644111211446787676461221222333311232223"
            "355558883338886777883223233553588")

        # Train to 29 to prep for Techo Caves and then beat Rollay and enter teleporter
        self.autobattler.trainToDesiredLevel(29)
        self.autobattler.followPath("777777777")

        logging.info("Jungle Ruins completed!")

    def completeAfterRollayToTechoCaves(self):
        # Nothing special here, just a pure navigation function
        logging.info("Walking from after Rollay to Techo Cave 1...")

        rollayToTechoCavesPath = gameinfo.movementPathDictionary["jungleRuinsAfterRollayToTechoCaves"]
        self.autobattler.followPath(rollayToTechoCavesPath)

    def completeTechoCave1(self):
        # Remember to gather all three drakonid parts and make the armour
        logging.info("Walking to Techo Cave 1 exit to grind...")

        techoCave1ToExitPath = gameinfo.movementPathDictionary["techoCave1ToExit"]
        techoCave1To2TransitionPath = gameinfo.movementPathDictionary["techoCave1To2Transition"]
        stopBeforeExitPath, cave1LastStep = self.splitPathByLastStep(techoCave1ToExitPath)

        # Need to level up, so grind to 30 before continuing
        self.autobattler.trainToDesiredLevel(30, "66444")

        # Go to the end of the cave and grind out the drakonid parts
        self.autobattler.followPath(stopBeforeExitPath)
        self.autobattler.grindForItems(("drakonid eye", "drakonid hide", "drakonid heart",))
        # Go back out of the cave and come back in before visiting Mr. Irgo
        self.autobattler.followPath(self.autobattler.pathTracker.invertPath(stopBeforeExitPath))
        self.autobattler.enterOrExitDungeon()
        self.autobattler.followPath("64")

        # Make the stuff and reset the starting point one more time
        self.autobattler.equipmentMaker.setEquipmentRecipe("Robe of Protection")
        self.autobattler.equipmentMaker.makeEquipment()
        self.autobattler.followPath(self.autobattler.pathTracker.invertPath("64"))
        self.autobattler.enterOrExitDungeon()

        # Finally, grind to 33 and go to cave 2
        # THIS HASN'T BEEN TESTED, MIGHT BREAK SOMETHING
        self.autobattler.followPath(stopBeforeExitPath)
        self.autobattler.trainToDesiredLevel(33)
        self.autobattler.followPath(cave1LastStep)
        self.autobattler.followPath(techoCave1To2TransitionPath)

        logging.info("Techo Cave 1 completed!")

    def completeCave2And4Medallion(self):
        # No longer need to grind any ingredients
        # This section only cares about navigating caves and polishing the medallion

        self.autobattler.trainToDesiredLevel(34, "66")

        logging.info("Walking to techo cave 2 exit to grind...")
        techoCave2ToExitPath = gameinfo.movementPathDictionary["techoCave2ToExit"]
        techoCave2To4TransitionPath = gameinfo.movementPathDictionary["techoCave2To4Transition"]
        stopBeforeCave2ExitPath, lastCave2Step = self.splitPathByLastStep(techoCave2ToExitPath)
        self.autobattler.followPath(stopBeforeCave2ExitPath)

        # We are now at step before exit. Grind up to 37 to be safe
        self.autobattler.trainToDesiredLevel(37)

        # Finish cave 2 navigation and enter 4
        self.autobattler.followPath(lastCave2Step)
        self.autobattler.followPath(techoCave2To4TransitionPath)
        # Maybe want to go back to main navigation page, but idk if needed

        # Navigate all the way to Sunny City and clean the medallion
        logging.info("Walking to Sunny City...")
        self.autobattler.followPath(gameinfo.movementPathDictionary["techoCave4ToSunnyCity"])
        self.autobattler.equipmentMaker.setEquipmentRecipe("Keladrian Medallion")
        # I don't know what will happen if you try to equip this since you can't, but uh...
        self.autobattler.equipmentMaker.makeEquipment()
        # WANT TO GO BACK INTO CAVE 4 AND GRIND TO LEVEL 40
        self.autobattler.trainToDesiredLevel(40, "55555")

        logging.info("Keladrian Medallion completed!")

    def completeSunnyCityToMountainFortress(self):
        # Start at Sunny City. No need to grind. Just navigate all the way to Mountain Fortress
        # Remember to call enterOrExit after returning because it auto clicks the cave 2 exit
        logging.info("Walking from Sunny City to Mountain Fortress...")
        self.autobattler.followPath(gameinfo.movementPathDictionary["sunnyCityToTechoCave2"])
        self.autobattler.followPath(gameinfo.movementPathDictionary["techoCave2To6"])
        self.autobattler.followPath(gameinfo.movementPathDictionary["techoCave6ToMountainFortress"])

        logging.info("Techo Caves completed!")

    def completeMountainFortress(self):
        # Will grind to level 42??? and circle the entire fortress, beating the guardians
        # Starts at the Ice Guardian and should equip the Iceheart Staff ideally
        # DON'T FORGET TO GRIND FOR INFERNO ROBE
        self.autobattler.trainToDesiredLevel(42, "777")

        # No way to easily grind Inferno Robe since tile zero has no encounters
        self.autobattler.followPath("777")
        self.autobattler.grindForItems("Inferno Robe")
        self.autobattler.equipmentMaker.setEquipmentRecipe("Inferno Robe")
        self.autobattler.equipmentMaker.equipEquipment()
        self.autobattler.followPath("222")
        self.autobattler.enterOrExitDungeon()

        logging.info("Final armour upgrade completed!")

        # Now beat all the guardians
        logging.info("Walking to all guardians and beating them...")
        self.autobattler.followPath(gameinfo.movementPathDictionary["mountainFortressToIce"])
        self.autobattler.followPath(gameinfo.movementPathDictionary["mountainFortressIceToLife"])
        # Might be nice to grind here to maybe 44, but no clue if you can find enemies on boss square
        # Also don't forget to equip the Moonstone Staff

        # followPath() ends right after taking the last step, so it doesn't battle
        # That's why our equipping gets skipped, so winBattle() should fix that
        # Have now added a fix to followPath(), but need to check if it works
        # self.autobattler.winBattle()

        self.autobattler.equipmentMaker.setEquipmentRecipe("Moonstone Staff")
        self.autobattler.equipmentMaker.equipEquipment()

        logging.info("Final weapon upgrade completed!")

        self.autobattler.trainToDesiredLevel(44)

        self.autobattler.followPath(gameinfo.movementPathDictionary["mountainFortressLifeToFire"])
        self.autobattler.followPath(gameinfo.movementPathDictionary["mountainFortressFireToShock"])
        self.autobattler.followPath(gameinfo.movementPathDictionary["mountainFortressShockToSpectral"])
        self.autobattler.followPath(
            gameinfo.movementPathDictionary["mountainFortressSpectralToEntrance"])

        logging.info("Mountain Fortress completed!")

    def completeKalPanning(self):
        # Starts from outside Mountain Fortress
        # Basically just walk to Kal Panning and stop before Faleinn to grind to 46
        # Show her the Medallion if you can figure out how...

        # Try to equip Moonstone one more time for good measure...
        self.autobattler.equipmentMaker.setEquipmentRecipe("Moonstone Staff")
        self.autobattler.equipmentMaker.equipEquipment()

        logging.info("Walking from Mountain Fortress to Kal Panning...")
        self.autobattler.followPath(gameinfo.movementPathDictionary["mountainFortressToTechoCave6"])
        # We are outside cave 6 again, so just follow path to Faleinn
        self.autobattler.followPath(gameinfo.movementPathDictionary["techoCave6ToKalPanning"])
        # We are now in front of Kal Panning. Stop before Faleinn now

        kalPanningToFaleinnPath = gameinfo.movementPathDictionary["kalPanningToFaleinn"]
        stopBeforeFaleinnPath, lastFaleinnStep = self.splitPathByLastStep(kalPanningToFaleinnPath)
        self.autobattler.followPath(stopBeforeFaleinnPath)

        self.autobattler.trainToDesiredLevel(47)

        self.autobattler.followPath(lastFaleinnStep)
        # self.autobattler.winBattle()
        # Now in battle with Faleinn. Should autoshow medallion

        logging.info("Kal Panning completed!")
    def completeFaleinnToJahbal(self):
        # Just want to walk all the way to the Two Rings, grind to 50, and walk to Jahbal
        logging.info("Walking from Faleinn to Two Rings Castle...")
        self.autobattler.followPath(gameinfo.movementPathDictionary["faleinnToTwoRings"])
        # Should be inside Two Rings now. Walk in a few steps to grind
        # AWW FRICK FORGOT TO GET ALL MY SPIRIT HEALING POTIONS...
        self.autobattler.trainToDesiredLevel(50, "2222222222")
        logging.info("Final grind completed! Walking to Jahbal now...")
        self.autobattler.followPath(gameinfo.movementPathDictionary["twoRingsToJahbal"])

        self.autobattler.followPath("5")
        # Program will automatically fight Jahbal and move to Mastermind, then Xantan if on InSaNe


# if __name__ == "__main__":
#     myTaskPerformer = ExperimentalTaskPerformer()
    # myTaskPerformer.completeInitialSetup()
    # myTaskPerformer.completeDankCaveF1()
    # myTaskPerformer.completeDankCaveF2()
    # myTaskPerformer.completeDankCaveF3()
    # myTaskPerformer.completeDankCaveF4()
    # myTaskPerformer.completeEleusAfterXantan()
    # myTaskPerformer.completeJungleRuinsF1FromEleus()
    # myTaskPerformer.completeJungleRuinsF2ToKreai()
    # myTaskPerformer.completeJungleRuinsAfterKreaiToGors()
    # myTaskPerformer.completeJungleRuinsWeaponUpgrade()
    # myTaskPerformer.completeRollayFromDenethrir()
    # myTaskPerformer.completeAfterRollayToTechoCaves()
    # myTaskPerformer.completeTechoCave1()
    # myTaskPerformer.completeCave2And4Medallion()
    # myTaskPerformer.completeSunnyCityToMountainFortress()
    # myTaskPerformer.completeMountainFortress()
    # myTaskPerformer.completeKalPanning()
    # myTaskPerformer.completeFaleinnToJahbal()