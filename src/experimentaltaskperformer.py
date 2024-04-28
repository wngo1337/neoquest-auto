import autobattler
import gameinfo
import logging
import constants
import seleniumobjectsandmethods

class ExperimentalTaskPerformer:

    def __init__(self):
        self.autobattler = autobattler.AutoBattler()
        self.autobattler.login_manager.login_neopets()

    def split_path_by_last_step(self, movementPath):
        path_without_last_step = movementPath[:-1]
        last_step = movementPath[-1]
        return path_without_last_step, last_step

    def complete_initial_setup(self):
        self.autobattler.skill_point_spender.initial_skill_setup()

        current_health, max_health, level = self.autobattler.get_player_info()
        self.autobattler.follow_path("44")
        while level < 4:
            logging.info("Grinding to level 4 before continuing...")
            self.autobattler.train(1)
            current_health, max_health, level = self.autobattler.get_player_info()
            if current_health < 25:
                self.autobattler.follow_path("3")
                seleniumobjectsandmethods.go_to_url(
                    "http://www.neopets.com/games/neoquest/neoquest.phtml?action=talk&target=90010001")
                seleniumobjectsandmethods.go_to_url(constants.MAIN_GAME_URL)
                self.autobattler.follow_path("6")
        # Now go hunt plains lupes
        # Player should always get 5+ glowing stones by level 8
        self.autobattler.follow_path("1111")
        while level < 8:
            logging.info("Grinding to level 8 before continuing...")
            self.autobattler.train(5)
            current_health, max_health, level = self.autobattler.get_player_info()
        self.autobattler.change_movement_mode("s")
        self.autobattler.follow_path("888855")
        logging.info("Initial setup completed!")

    def complete_dank_cave_f1(self):
        # Go to Morax and get a new armour
        logging.info("Getting new armour from Morax Dorangis...")

        self.autobattler.follow_path("6")
        self.autobattler.equipment_maker.set_equipment_recipe("Energy Shield")
        self.autobattler.equipment_maker.make_equipment()
        self.autobattler.follow_path(self.autobattler.path_tracker.invert_path("6"))

        logging.info("Walking to the Dank Cave...")

        self.autobattler.follow_path(gameinfo.travel_locations_to_paths["eleusToDankCave"])
        # Want to stop right before floor 2 to grind cave lupe pelt

        logging.info("Walking from Dank Cave F1 to F2...")

        f1_to_f2_path = gameinfo.travel_locations_to_paths["dankCaveF1ToF2"]
        stop_before_f2_path, last_f2_step = self.split_path_by_last_step(f1_to_f2_path)
        self.autobattler.follow_path(stop_before_f2_path)
        self.autobattler.grind_for_items(("cave lupe pelt",))
        self.autobattler.follow_path(last_f2_step)

        logging.info("Dank Cave F1 completed!")

    def complete_dank_cave_f2(self):
        # Key items to grind: tiny beryl, tiny obsidian
        logging.info("Walking to Dank Cave F3...")

        f2_to_f3_path = gameinfo.travel_locations_to_paths["dankCaveF2ToF3"]
        stop_before_f3_path, last_f2_step = self.split_path_by_last_step(f2_to_f3_path)
        self.autobattler.follow_path(stop_before_f3_path)
        # Grind the ingredient for silver wand before going to next floor
        self.autobattler.grind_for_items(("tiny beryl", "tiny obsidian"))
        self.autobattler.follow_path(last_f2_step)

        logging.info("Dank Cave F2 completed!")

    def complete_dank_cave_f3(self):
        # Don't need any items. Just grind to 11 and move to last floor
        logging.info("Walking to dank Cave F4...")

        f3_to_f4_path = gameinfo.travel_locations_to_paths["dankCaveF3ToF4"]
        stop_before_f4_path, last_f3_step = self.split_path_by_last_step(f3_to_f4_path)
        current_health, max_health, level = self.autobattler.get_player_info()
        self.autobattler.follow_path(stop_before_f4_path)
        self.autobattler.train_to_desired_level(11)
        self.autobattler.change_movement_mode("s")
        self.autobattler.follow_path(last_f3_step)

        logging.info("Dank Cave F3 completed!")

    def complete_dank_cave_f4(self):
        # Need to grab aluminum rod and Xantan's Ring
        logging.info("Walking to Xantan...")

        f4_to_xantan_path = gameinfo.travel_locations_to_paths["dankCaveF4ToXantan"]
        stop_before_exit_path, last_f4_step = self.split_path_by_last_step(f4_to_xantan_path)
        self.autobattler.grind_for_items(("corroded aluminum rod",))
        self.autobattler.follow_path(stop_before_exit_path)
        # Will automatically fight Xantan here
        self.autobattler.grind_for_items(("stretch of rotted cloth",))
        self.autobattler.train_to_desired_level(14)
        self.autobattler.follow_path(last_f4_step)

        logging.info("Dank Cave F4 completed!")

    def complete_eleus_after_xantan(self):
        logging.info("Walking back to Eleus Batrin for weapon upgrade...")

        self.autobattler.follow_path(gameinfo.travel_locations_to_paths["afterDankCaveTeleporterToEleus"])
        # # Should be at Eleus now
        self.autobattler.equipment_maker.set_equipment_recipe("Silver Wand")
        self.autobattler.equipment_maker.make_equipment()
        # Must go to Choras Tillie now
        self.autobattler.follow_path("8")
        self.autobattler.equipment_maker.set_equipment_recipe("Magic Robe")
        self.autobattler.equipment_maker.make_equipment()
        # Reset position to Eleus for next movement script
        self.autobattler.follow_path("1")

        logging.info("Weapon and armour upgrade after Xantan completed!")

    def complete_jungle_ruins_f1_from_eleus(self):
        # Nothing to grind. Just walking to next location
        logging.info("Walking to Jungle Ruins F2...")
        self.autobattler.follow_path(gameinfo.travel_locations_to_paths["eleusToJungleRuins"])
        self.autobattler.follow_path(gameinfo.travel_locations_to_paths["jungleRuinsF1ToF2"])

    def complete_jungle_ruins_f2_to_kreai(self):
        # Need to grind jungle beast claw and noil's tooth. Don't leave without them!
        # Move forward to encounter jungle beasts
        logging.info("Walking to Kreai...")
        f1_to_kreai_path = gameinfo.travel_locations_to_paths["jungleRuinsF2ToKreai"]
        stop_before_kreai_path, last_kreai_step = self.split_path_by_last_step(f1_to_kreai_path)
        self.autobattler.follow_path("3555")
        # Get jungle beast claw before moving on
        self.autobattler.grind_for_items(("jungle beast claw",))
        self.autobattler.train_to_desired_level(16)
        # reset position to staircase for next movement script
        self.autobattler.follow_path(self.autobattler.path_tracker.invert_path("3555"))
        # This is dumb, but followPath automatically enters stairs, so must go back up
        self.autobattler.enter_or_exit_dungeon()
        # Path will now take us to one tile in front of Kreai. Grind for noil's tooth here
        self.autobattler.follow_path(stop_before_kreai_path)
        self.autobattler.grind_for_items(("noil's tooth",))
        currentHealth, maxHealth, level = self.autobattler.get_player_info()
        """Got the item, so grind to 18 and take the last step and beat Kreai's ass
         before taking the teleporter"""
        self.autobattler.train_to_desired_level(18)

        """Enemies at beginning of stage are not strong enough to grind to 18, so we have no choice
        but to end the right at Kreai and 'manually' enter the teleporter after"""
        self.autobattler.follow_path(last_kreai_step)
        self.autobattler.change_movement_mode("s")
        self.autobattler.follow_path("2")

        logging.info("Jungle Ruins F2 completed!")

    def complete_jungle_ruins_after_kreai_to_gors(self):
        # Just need to grind jungle pauldrons from here
        # Don't know where they show up though, so might need to split the path and not use dictionary
        logging.info("Walking to teleporter maze to grind...")

        self.autobattler.follow_path("55777778855553214122233214441144446777664412222222235555555555"
                                    "555555555877777777855558866")
        # Should take us to around the teleporter maze
        # Get the jungle pauldrons before moving on
        self.autobattler.grind_for_items(("jungle pauldrons",))
        self.autobattler.follow_path("446855553"
                                    "55876685532222214444")
        # Grind to maybe 20 here to be safe
        self.autobattler.train_to_desired_level(21)
        # If we are past 20, go grind two more levels after getting to Gors level
        self.autobattler.change_movement_mode("s")
        self.autobattler.follow_path("8322238852")
        self.autobattler.train_to_desired_level(23)
        # Should take us all the way to Gors and take the teleporter...
        self.autobattler.change_movement_mode("s")
        self.autobattler.follow_path("222222222222222222")

        logging.info("Gors level completed!")

    def complete_jungle_ruins_weapon_upgrade(self):
        # Start at place after Gor's teleporter
        logging.info("Walking to Denethrir for upgrade...")

        self.autobattler.follow_path(gameinfo.travel_locations_to_paths["jungleRuinsAfterGorsToDenethrir"])
        self.autobattler.equipment_maker.set_equipment_recipe("Nature Wand")
        self.autobattler.equipment_maker.make_equipment()

        logging.info("Weapon upgrade after Gors completed!")

    def complete_rollay_from_denethrir(self):
        # Navigate back from Denethrir all the way to Rollay
        # No items to grind, just levels
        logging.info("Walking from Denethrir to Jungle Ruins F3...")
        self.autobattler.follow_path(gameinfo.travel_locations_to_paths["jungleRuinsDenethrirToF3"])
        self.autobattler.train_to_desired_level(24)

        # Now we want to walk halfway to Rollay and grind WAY up, maybe to 27
        # This should already be true, but just in case. Want to hunt all the way to Rollay
        self.autobattler.follow_path("55558588788777788878888553333333353332233333555555558")
        self.autobattler.train_to_desired_level(27)

        # Walk near Rollay to encounter higher level enemies
        self.autobattler.follow_path(
            "777777777777666677888668767778877776776666644444444"
            "414441114466644111211446787676461221222333311232223"
            "355558883338886777883223233553588")

        # Train to 29 to prep for Techo Caves and then beat Rollay and enter teleporter
        self.autobattler.train_to_desired_level(29)
        self.autobattler.follow_path("777777777")

        logging.info("Jungle Ruins completed!")

    def complete_after_rollay_to_techo_caves(self):
        # Nothing special here, just a pure navigation function
        logging.info("Walking from after Rollay to Techo Cave 1...")

        rollay_to_techo_caves_path = gameinfo.travel_locations_to_paths["jungleRuinsAfterRollayToTechoCaves"]
        self.autobattler.follow_path(rollay_to_techo_caves_path)

    def complete_techo_cave1(self):
        # Remember to gather all three drakonid parts and make the armour
        logging.info("Walking to Techo Cave 1 exit to grind...")

        techo_cave1_to_exit_path = gameinfo.travel_locations_to_paths["techoCave1ToExit"]
        techo_cave1_to_2_transition_path = gameinfo.travel_locations_to_paths["techoCave1To2Transition"]
        stop_before_exit_path, cave1_last_step = self.split_path_by_last_step(techo_cave1_to_exit_path)

        # Need to level up, so grind to 30 before continuing
        self.autobattler.train_to_desired_level(30, "66444")

        # Go to the end of the cave and grind out the drakonid parts
        self.autobattler.follow_path(stop_before_exit_path)
        self.autobattler.grind_for_items(("drakonid eye", "drakonid hide", "drakonid heart",))
        # Go back out of the cave and come back in before visiting Mr. Irgo
        self.autobattler.follow_path(self.autobattler.path_tracker.invert_path(stop_before_exit_path))
        self.autobattler.enter_or_exit_dungeon()
        self.autobattler.follow_path("64")

        # Make the stuff and reset the starting point one more time
        self.autobattler.equipment_maker.set_equipment_recipe("Robe of Protection")
        self.autobattler.equipment_maker.make_equipment()
        self.autobattler.follow_path(self.autobattler.path_tracker.invert_path("64"))
        self.autobattler.enter_or_exit_dungeon()

        # Finally, grind to 33 and go to cave 2
        self.autobattler.follow_path(stop_before_exit_path)
        self.autobattler.train_to_desired_level(33)
        self.autobattler.follow_path(cave1_last_step)
        self.autobattler.follow_path(techo_cave1_to_2_transition_path)

        logging.info("Techo Cave 1 completed!")

    def complete_techo_cave2_and_4_medallion(self):
        # No longer need to grind any ingredients
        # This section only cares about navigating caves and polishing the medallion

        self.autobattler.train_to_desired_level(34, "66")

        logging.info("Walking to techo cave 2 exit to grind...")
        techoCave2ToExitPath = gameinfo.travel_locations_to_paths["techoCave2ToExit"]
        techoCave2To4TransitionPath = gameinfo.travel_locations_to_paths["techoCave2To4Transition"]
        stopBeforeCave2ExitPath, lastCave2Step = self.split_path_by_last_step(techoCave2ToExitPath)
        self.autobattler.follow_path(stopBeforeCave2ExitPath)

        # We are now at step before exit. Grind up to 37 to be safe
        self.autobattler.train_to_desired_level(37)

        # Finish cave 2 navigation and enter 4
        self.autobattler.follow_path(lastCave2Step)
        self.autobattler.follow_path(techoCave2To4TransitionPath)
        # Maybe want to go back to main navigation page, but idk if needed

        # Navigate all the way to Sunny City and clean the medallion
        logging.info("Walking to Sunny City...")
        self.autobattler.follow_path(gameinfo.travel_locations_to_paths["techoCave4ToSunnyCity"])
        self.autobattler.equipment_maker.set_equipment_recipe("Keladrian Medallion")
        # I don't know what will happen if you try to equip this since you can't, but uh...
        self.autobattler.equipment_maker.make_equipment()
        # WANT TO GO BACK INTO CAVE 4 AND GRIND TO LEVEL 40
        self.autobattler.train_to_desired_level(40, "55555")

        logging.info("Keladrian Medallion completed!")

    def complete_sunny_city_to_mountain_fortress(self):
        # Start at Sunny City. No need to grind. Just navigate all the way to Mountain Fortress
        # Remember to call enterOrExit after returning because it auto clicks the cave 2 exit
        logging.info("Walking from Sunny City to Mountain Fortress...")
        self.autobattler.follow_path(gameinfo.travel_locations_to_paths["sunnyCityToTechoCave2"])
        self.autobattler.follow_path(gameinfo.travel_locations_to_paths["techoCave2To6"])
        self.autobattler.follow_path(gameinfo.travel_locations_to_paths["techoCave6ToMountainFortress"])

        logging.info("Techo Caves completed!")

    def complete_mountain_fortress(self):
        # Will grind to level 42??? and circle the entire fortress, beating the guardians
        # Starts at the Ice Guardian and should equip the Iceheart Staff ideally
        # DON'T FORGET TO GRIND FOR INFERNO ROBE
        self.autobattler.train_to_desired_level(42, "777")

        # No way to easily grind Inferno Robe since tile zero has no encounters
        self.autobattler.follow_path("777")
        self.autobattler.grind_for_items("Inferno Robe")
        self.autobattler.equipment_maker.set_equipment_recipe("Inferno Robe")
        self.autobattler.equipment_maker.equip_equipment()
        self.autobattler.follow_path("222")
        self.autobattler.enter_or_exit_dungeon()

        logging.info("Final armour upgrade completed!")

        # Now beat all the guardians
        logging.info("Walking to all guardians and beating them...")
        self.autobattler.follow_path(gameinfo.travel_locations_to_paths["mountainFortressToIce"])
        self.autobattler.follow_path(gameinfo.travel_locations_to_paths["mountainFortressIceToLife"])
        # Might be nice to grind here to maybe 44, but no clue if you can find enemies on boss square
        # Also don't forget to equip the Moonstone Staff

        # followPath() ends right after taking the last step, so it doesn't battle
        # That's why our equipping gets skipped, so winBattle() should fix that
        # Have now added a fix to followPath(), but need to check if it works
        # self.autobattler.winBattle()

        self.autobattler.equipment_maker.set_equipment_recipe("Moonstone Staff")
        self.autobattler.equipment_maker.equip_equipment()

        logging.info("Final weapon upgrade completed!")

        self.autobattler.train_to_desired_level(44)

        self.autobattler.follow_path(gameinfo.travel_locations_to_paths["mountainFortressLifeToFire"])
        self.autobattler.follow_path(gameinfo.travel_locations_to_paths["mountainFortressFireToShock"])
        self.autobattler.follow_path(gameinfo.travel_locations_to_paths["mountainFortressShockToSpectral"])
        self.autobattler.follow_path(
            gameinfo.travel_locations_to_paths["mountainFortressSpectralToEntrance"])

        logging.info("Mountain Fortress completed!")

    def complete_kal_panning(self):
        # Starts from outside Mountain Fortress
        # Basically just walk to Kal Panning and stop before Faleinn to grind to 46

        # Try to equip Moonstone one more time for good measure...
        self.autobattler.equipment_maker.set_equipment_recipe("Moonstone Staff")
        self.autobattler.equipment_maker.equip_equipment()

        logging.info("Walking from Mountain Fortress to Kal Panning...")
        self.autobattler.follow_path(gameinfo.travel_locations_to_paths["mountainFortressToTechoCave6"])
        # We are outside cave 6 again, so just follow path to Faleinn
        self.autobattler.follow_path(gameinfo.travel_locations_to_paths["techoCave6ToKalPanning"])
        # We are now in front of Kal Panning. Stop before Faleinn now

        kal_panning_to_faleinn_path = gameinfo.travel_locations_to_paths["kalPanningToFaleinn"]
        stop_before_faleinn_path, last_faleinn_step = self.split_path_by_last_step(kal_panning_to_faleinn_path)
        self.autobattler.follow_path(stop_before_faleinn_path)

        self.autobattler.train_to_desired_level(47)

        self.autobattler.follow_path(last_faleinn_step)
        # self.autobattler.winBattle()
        # Now in battle with Faleinn. Should autoshow medallion

        logging.info("Kal Panning completed!")

    def complete_faleinn_to_jahbal(self):
        # Just want to walk all the way to the Two Rings, grind to 50, and walk to Jahbal
        logging.info("Walking from Faleinn to Two Rings Castle...")
        self.autobattler.follow_path(gameinfo.travel_locations_to_paths["faleinnToTwoRings"])
        # Should be inside Two Rings now. Walk in a few steps to grind
        self.autobattler.train_to_desired_level(50, "2222222222")
        logging.info("Final grind completed! Walking to Jahbal now...")
        self.autobattler.follow_path(gameinfo.travel_locations_to_paths["twoRingsToJahbal"])

        self.autobattler.follow_path("5")
        # Program will automatically fight Jahbal and move to Mastermind, then Xantan if on InSaNe

    def complete_jahbal_after_revive(self):
        # Jahbal fight has a lot of RNG because of 3-turn stuns. Dying is a distinct possibility
        # In that case, walk all the way back to him to fight again
        self.autobattler.follow_path(gameinfo.travel_locations_to_paths["reviveToJahbal"])

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