from autoplayercontroller import AutoPlayerController
import argparse


def main(use_neopass: bool):
    # We pass the use_neopass argument all the way down the constructor chain
    # I can't think of another way to get it to login_manager instance right now
    my_auto_player_controller = AutoPlayerController(use_neopass=use_neopass)
    my_auto_player_controller.task_performer.autobattler.login_manager.login_neopets()
    while True:
        # Make sure to catch invalid inputs or we will crash
        try:
            my_auto_player_controller.print_menu()
            choice = input("Please enter a choice from the menu above: ")
            if choice not in my_auto_player_controller.option_dictionary.keys():
                print("Please choose a valid option!")
            else:
                print(
                    "Option selected. We are going to perform: {}".format(
                        my_auto_player_controller.option_dictionary[choice]
                    )
                )
                print(
                    "DO NOT CLOSE THE PROGRAM UNTIL CURRENT FUNCTION EXECUTION IS COMPLETED!!!"
                )
                if choice == "1":
                    my_auto_player_controller.option1()
                if choice == "2":
                    my_auto_player_controller.option2()
                if choice == "3":
                    my_auto_player_controller.option3()
                if choice == "4":
                    my_auto_player_controller.option4()
                if choice == "5":
                    my_auto_player_controller.option5()
                if choice == "6":
                    my_auto_player_controller.option6()
                if choice == "7":
                    my_auto_player_controller.option7()
                if choice == "8":
                    my_auto_player_controller.option8()
                if choice == "9":
                    my_auto_player_controller.option9()
                if choice == "10":
                    my_auto_player_controller.option10()
                if choice == "11":
                    # Exit the loop to terminate the program
                    break
        except SyntaxError as e:
            print("No input was detected. Please enter a valid option!")
            continue

    print("Goodbye, I hope the program served you well")
    my_auto_player_controller.task_performer.autobattler.close_auto_battler()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--use-neopass",
        action="store_true",
        help="Set this flag if authenticating with Neopass",
    )
    args = parser.parse_args()

    main(use_neopass=args.use_neopass)
