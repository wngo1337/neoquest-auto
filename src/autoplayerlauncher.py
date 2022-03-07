"""This class allows users to launch and use the program through a command line interface.
It automatically starts an autobattler instance and lets users choose from a number of options.

Users should read carefully to understand when to use each option."""

import experimentaltaskperformer
import sys
import logging

class AutoPlayerLauncher:

    # Would be nice to add options for grinding and stuff, but not necessary
    # Also might want to add option to complete entire game
    optionDictionary = {"1": "Initial Skill Setup + Levelling",
                        "2": "Dank Cave + Weapon/Armour upgrade",
                        "3": "Jungle Ruins (Kreai, Gors + Weapon Upgrade, Rollay)",
                        "4": "Techo Caves + Shiny Medallion",
                        "5": "Mountain Fortress (Final Weapon/Armour Upgrade)",
                        "6": "Kal Panning",
                        "7": "Two Rings Grind and Navigation",
                        "8": "Follow a Custom Path",
                        "9": "Train For a Bit (30 Battles because I am lazy to implement)",
                        "10": "Exit The Program"}

    myTaskPerformer = None

    def __init__(self):
        self.myTaskPerformer = experimentaltaskperformer.ExperimentalTaskPerformer()

    def printMenu(self):
        for key in self.optionDictionary:
            print("{}: {}".format(key, self.optionDictionary[key]))
        print()

    def option1(self):
        logging.info("Initial skillpoint spending and leveling in progress...")
        self.myTaskPerformer.completeInitialSetup()

    def option2(self):
        logging.info("Weapon upgrade and Dank Cave completion in progress...")
        self.myTaskPerformer.completeDankCaveF1()
        self.myTaskPerformer.completeDankCaveF2()
        self.myTaskPerformer.completeDankCaveF3()
        self.myTaskPerformer.completeDankCaveF4()
        self.myTaskPerformer.completeEleusAfterXantan()

    def option3(self):
        logging.info("Jungle Ruins completion in progress...")
        self.myTaskPerformer.completeJungleRuinsF1FromEleus()
        self.myTaskPerformer.completeJungleRuinsF2ToKreai()
        self.myTaskPerformer.completeJungleRuinsAfterKreaiToGors()
        self.myTaskPerformer.completeJungleRuinsWeaponUpgrade()
        self.myTaskPerformer.completeRollayFromDenethrir()
        self.myTaskPerformer.completeAfterRollayToTechoCaves()

    def option4(self):
        logging.info("Techo Caves and Kelladrian Medallion in progres...")
        self.myTaskPerformer.completeTechoCave1()
        self.myTaskPerformer.completeCave2And4Medallion()
        self.myTaskPerformer.completeSunnyCityToMountainFortress()

    def option5(self):
        logging.info("Mountain Fortress completion in progress...")
        self.myTaskPerformer.completeMountainFortress()

    def option6(self):
        logging.info("Kal Panning completion in progress...")
        self.myTaskPerformer.completeKalPanning()

    def option7(self):
        logging.info("Two Rings completion in progress...")
        self.myTaskPerformer.completeFaleinnToJahbal()

    def option8(self):
        print("CAREFUL: Do not use this method if you do not know what you are doing!")
        while True:
            mapPath = input("Enter a custom map path (numbers only) to follow, "
                            "or q to return to menu: ")
            if mapPath.casefold() == "q":
                return
            try:
                pathCheck = int(mapPath)
                self.myTaskPerformer.autobattler.followPath(mapPath)
                return
            except ValueError:
                print("You have entered an invalid path!")
                continue

    def option9(self):
        self.myTaskPerformer.autobattler.train(30)
        return

def main():
    myAutoPlayerLauncher = AutoPlayerLauncher()
    while True:
        # Make sure to catch invalid inputs or we will crash
        try:
            myAutoPlayerLauncher.printMenu()
            choice = input("Please enter a choice from the menu above: ")
            if choice not in myAutoPlayerLauncher.optionDictionary.keys():
                print("Please choose a valid option!")
            else:
                print("Option selected. We are going to perform: {}".format(
                    myAutoPlayerLauncher.optionDictionary[choice]))
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
                    myAutoPlayerLauncher.option8();
                if choice == "9":
                    myAutoPlayerLauncher.option9();
                if choice == "10":
                    # Exit the loop to terminate the program
                    break
        except SyntaxError as e:
            print("No input was detected. Please enter a valid option!")
            continue

    print("Goodbye, I hope the program served you well")
    myAutoPlayerLauncher.myTaskPerformer.autobattler.closeAutoBattler()

if __name__ == "__main__":
    main()
