"""This class allows users to launch and use the program through a command line interface.
It automatically starts an autobattler instance and lets users choose from a number of options.

Users should read carefully to understand when to use each option."""

import experimentaltaskperformer
import sys
import logging


class AutoPlayerController:

    # Would be nice to add options for grinding and stuff, but not necessary
    # Also might want to add option to complete entire game
    option_dictionary = {
        "1": "Initial Skill Setup + Levelling",
        "2": "Dank Cave + Weapon/Armour upgrade",
        "3": "Jungle Ruins (Kreai, Gors + Weapon Upgrade, Rollay)",
        "4": "Techo Caves + Shiny Medallion",
        "5": "Mountain Fortress (Final Weapon/Armour Upgrade)",
        "6": "Kal Panning",
        "7": "Two Rings Grind and Navigation",
        "8": "Follow a Custom Path",
        "9": "Train For a Bit (100 Battles because I am lazy to customize)",
        "10": "Return to Jahbal If You Died From Bad RNG",
        "11": "Exit The Program",
    }

    task_performer = None

    def __init__(self, use_neopass):
        self.task_performer = experimentaltaskperformer.ExperimentalTaskPerformer(
            use_neopass=use_neopass
        )

    def print_menu(self):
        for key in self.option_dictionary:
            print("{}: {}".format(key, self.option_dictionary[key]))
        print()

    def option1(self):
        logging.info("Initial skillpoint spending and leveling in progress...")
        self.task_performer.complete_initial_setup()

    def option2(self):
        logging.info("Weapon upgrade and Dank Cave completion in progress...")
        self.task_performer.complete_dank_cave_f1()
        self.task_performer.complete_dank_cave_f2()
        self.task_performer.complete_dank_cave_f3()
        self.task_performer.complete_dank_cave_f4()
        self.task_performer.complete_eleus_after_xantan()

    def option3(self):
        logging.info("Jungle Ruins completion in progress...")
        self.task_performer.complete_jungle_ruins_f1_from_eleus()
        self.task_performer.complete_jungle_ruins_f2_to_kreai()
        self.task_performer.complete_jungle_ruins_after_kreai_to_gors()
        self.task_performer.complete_jungle_ruins_weapon_upgrade()
        self.task_performer.complete_rollay_from_denethrir()
        self.task_performer.complete_after_rollay_to_techo_caves()

    def option4(self):
        logging.info("Techo Caves and Kelladrian Medallion in progres...")
        self.task_performer.complete_techo_cave1()
        self.task_performer.complete_techo_cave2_and_4_medallion()
        self.task_performer.complete_sunny_city_to_mountain_fortress()

    def option5(self):
        logging.info("Mountain Fortress completion in progress...")
        self.task_performer.complete_mountain_fortress()

    def option6(self):
        logging.info("Kal Panning completion in progress...")
        self.task_performer.complete_kal_panning()

    def option7(self):
        logging.info("Two Rings completion in progress...")
        self.task_performer.complete_faleinn_to_jahbal()

    def option8(self):
        print("CAREFUL: Do not use this method if you do not know what you are doing!")
        while True:
            mapPath = input(
                "Enter a custom map path (numbers only) to follow, "
                "or q to return to menu: "
            )
            if mapPath.casefold() == "q":
                return
            try:
                pathCheck = int(mapPath)
                self.task_performer.autobattler.follow_path(mapPath)
                return
            except ValueError:
                print("You have entered an invalid path!")
                continue

    def option9(self):
        self.task_performer.autobattler.train(100)

    def option10(self):
        self.task_performer.complete_jahbal_after_revive()
