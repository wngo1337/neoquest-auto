"""This class allows users to launch and use the program through a command line interface.
It automatically starts an autobattler instance and lets users choose from a number of options.

Users should read carefully to understand when to use each option."""

import experimentaltaskperformer
import sys
import logging

class AutoPlayerLauncher:

    # Would be nice to add options for grinding and stuff, but not necessary
    # Also might want to add option to complete entire game
    option_dictionary = {"1": "Initial Skill Setup + Levelling",
                        "2": "Dank Cave + Weapon/Armour upgrade",
                        "3": "Jungle Ruins (Kreai, Gors + Weapon Upgrade, Rollay)",
                        "4": "Techo Caves + Shiny Medallion",
                        "5": "Mountain Fortress (Final Weapon/Armour Upgrade)",
                        "6": "Kal Panning",
                        "7": "Two Rings Grind and Navigation",
                        "8": "Follow a Custom Path",
                        "9": "Train For a Bit (100 Battles because I am lazy to customize)",
                        "10": "Return to Jahbal If You Died From Bad RNG",
                        "11": "Exit The Program"}

    task_performer = None

    def __init__(self):
        self.task_performer = experimentaltaskperformer.ExperimentalTaskPerformer()

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
            mapPath = input("Enter a custom map path (numbers only) to follow, "
                            "or q to return to menu: ")
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

def main():
    myAutoPlayerLauncher = AutoPlayerLauncher()
    while True:
        # Make sure to catch invalid inputs or we will crash
        try:
            myAutoPlayerLauncher.print_menu()
            choice = input("Please enter a choice from the menu above: ")
            if choice not in myAutoPlayerLauncher.option_dictionary.keys():
                print("Please choose a valid option!")
            else:
                print("Option selected. We are going to perform: {}".format(
                    myAutoPlayerLauncher.option_dictionary[choice]))
                print("DO NOT CLOSE THE PROGRAM UNTIL CURRENT FUNCTION EXECUTION IS COMPLETED!!!")
                if choice == "1":
                    myAutoPlayerLauncher.option1()
                if choice == "2":
                    myAutoPlayerLauncher.option2()
                if choice == "3":
                    myAutoPlayerLauncher.option3()
                if choice == "4":
                    myAutoPlayerLauncher.option4()
                if choice == "5":
                    myAutoPlayerLauncher.option5()
                if choice == "6":
                    myAutoPlayerLauncher.option6()
                if choice == "7":
                    myAutoPlayerLauncher.option7()
                if choice == "8":
                    myAutoPlayerLauncher.option8()
                if choice == "9":
                    myAutoPlayerLauncher.option9()
                if choice == "10":
                    myAutoPlayerLauncher.option10()
                if choice == "11":
                    # Exit the loop to terminate the program
                    break
        except SyntaxError as e:
            print("No input was detected. Please enter a valid option!")
            continue

    print("Goodbye, I hope the program served you well")
    myAutoPlayerLauncher.task_performer.autobattler.close_auto_battler()

if __name__ == "__main__":
    main()
