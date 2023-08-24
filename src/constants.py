# Common URLs for navigation

LOGIN_URL = "https://www.neopets.com/login/?destination=/home/"
# Multi-purpose page that mainly navigates to the overworld map
MAIN_GAME_URL = "http://www.neopets.com/games/neoquest/neoquest.phtml"
# Used to "move" in place for random encounters
MAP_MOVEMENT_URL = "http://www.neopets.com/games/neoquest/neoquest.phtml?action=move&movedir="

# # Key button/link strings that determine the program's next choice of action
# RETURN_MAP_STRING = "Click here to return to the map"
# BEGIN_BATTLE_STRING = "Click here to begin the fight!"
# END_BATTLE_STRING = "Click here to see what you found!"
# # This option is always available in battle, so...
# ICEHEART_ABILITY_STRING = "Cast Ice Wind from your Iceheart Staff"
# IN_BATTLE_STRING = "Attack"
# STUNNED_IN_BATTLE_STRING = "Do nothing"

# ORDER IS VERY IMPORTANT. e.g. Don't do nothing before checking if we can attack
# Might redo this later because that seems like a bad idea, but I dunno
battleXpathList = [
    # We only use this option once in the entire game... oh well
    "//A[contains(.,'Show the Keladrian Medallion to Faleinn')]",
    "//A[contains(.,'Cast Ice Wind from your Iceheart Staff')]",
    "//A[@HREF='javascript:;' and text()='Attack']",
    "//A[contains(.,'Do nothing')]",
    "//a[contains(.,'Click here to see what you found!')]",
    "//INPUT[@TYPE='submit' and "
    "@VALUE='Click here to return to the map']",
    "//INPUT[@TYPE='submit' and @VALUE='Click here to see what happens...']",
    "//INPUT[@TYPE='submit' and "
    "@VALUE='Click here to begin the fight!']"
]

# Static image URLs for identifying presence of boss
bossImageList = ["images.neopets.com/nq/m/400198_VRhlK_Jahbal.gif",
                 "http://images.neopets.com/nq/m/400199_GWcxJ_Mastermind.gif"]

# MAYBE DO DIRECTIONS FOR THE MOVEMENT SYSTEM NEXT
NAVIGATION_IMAGE_URL = "images.neopets.com/nq/n/navarrows.gif"

MOVE_NOMOVE_URL = "http://www.neopets.com/games/neoquest/neoquest.phtml?action=move&movedir="
MOVE_NORTHWEST_URL = "http://www.neopets.com/games/neoquest/neoquest.phtml?action=move&movedir=1"
MOVE_NORTH_URL = "http://www.neopets.com/games/neoquest/neoquest.phtml?action=move&movedir=2"
MOVE_NORTHEAST_URL = "http://www.neopets.com/games/neoquest/neoquest.phtml?action=move&movedir=3"
MOVE_WEST_URL = "http://www.neopets.com/games/neoquest/neoquest.phtml?action=move&movedir=4"
MOVE_EAST_URL = "http://www.neopets.com/games/neoquest/neoquest.phtml?action=move&movedir=5"
MOVE_SOUTHWEST_URL = "http://www.neopets.com/games/neoquest/neoquest.phtml?action=move&movedir=6"
MOVE_SOUTH_URL = "http://www.neopets.com/games/neoquest/neoquest.phtml?action=move&movedir=7"
MOVE_SOUTHEAST_URL = "http://www.neopets.com/games/neoquest/neoquest.phtml?action=move&movedir=8"

directionDictionary = {"1": MOVE_NORTHWEST_URL,
                       "2": MOVE_NORTH_URL,
                       "3": MOVE_NORTHEAST_URL,
                       "4": MOVE_WEST_URL,
                       "5": MOVE_EAST_URL,
                       "6": MOVE_SOUTHWEST_URL,
                       "7": MOVE_SOUTH_URL,
                       "8": MOVE_SOUTHEAST_URL
                       }

SNEAKING_MODE_URL = "http://www.neopets.com/games/neoquest/neoquest.phtml?movetype=3"
HUNTING_MODE_URL = "http://www.neopets.com/games/neoquest/neoquest.phtml?movetype=2"

ITEM_PAGE_URL = "http://www.neopets.com/games/neoquest/neoquest.phtml?action=items"

ENTRANCE_OR_EXIT_TEMPLATE = "//A[@HREF='neoquest.phtml?action=move&movelink={}']"

# Xpaths can break easily but not here I think, plus they are needed
# dungeonXPathDictionary = {"dankCaveEntranceExit": "//A[@HREF='neoquest.phtml?action=move&movelink=1']",
#                           "dankCaveF1ToF2": "//A[@HREF='neoquest.phtml?action=move&movelink=2']",
#                           "dankCaveF2ToF1": "//A[@HREF='neoquest.phtml?action=move&movelink=3']",
#                           "dankCaveF2ToF3": "//A[@HREF='neoquest.phtml?action=move&movelink=4']",
#                           "dankCaveF3ToF2": "//A[@HREF='neoquest.phtml?action=move&movelink=5']",
#                           "dankCaveF3ToF4": "//A[@HREF='neoquest.phtml?action=move&movelink=6']",
#                           "dankCaveF4ToF3": "//A[@HREF='neoquest.phtml?action=move&movelink=7']",
#                           "dankCaveTeleporter": "//A[@HREF='neoquest.phtml?action=move&movelink=8']",
#                           # This is kind of dumb... Same as Dank Cave one???
#                           "eleusToJungleRuins": "//A[@HREF='neoquest.phtml?action=move&movelink=2']",
#                           # wtf same as dank cave exit... Also same "You see an exit here" text
#                           "jungleRuinsExit": "//A[@HREF='neoquest.phtml?action=move&movelink=1']",
#                           "kreaiTeleporterToF2": "//A[@HREF='neoquest.phtml?action=move&movelink=3']",
#                           # You see a magic teleporter here for all the following
#                           "jungleRuinsMazeT1ToT2": "//A[@HREF='neoquest.phtml?action=move&movelink=14']",
#                           "jungleRuinsMazeT2ToT1": "//A[@HREF='neoquest.phtml?action=move&movelink=15']",
#                           "jungleRuinsMazeT3": "//A[@HREF='neoquest.phtml?action=move&movelink=16']",
#                           "jungleRuinsMazeT4ToT3": "//A[@HREF='neoquest.phtml?action=move&movelink=17']",
#                           "jungleRuinsMazeT5": "//A[@HREF='neoquest.phtml?action=move&movelink=10']",
#                           "jungleRuinsMazeT5ToT4": "//A[@HREF='neoquest.phtml?action=move&movelink=11']",
#                           "jungleRuinsMazeT6": "//A[@HREF='neoquest.phtml?action=move&movelink=12']",
#                           "jungleRuinsMazeT7ToT6": "//A[@HREF='neoquest.phtml?action=move&movelink=13']",
#                           # "You see a staircase leading up here"
#                           "jungleRuinsF1ToUpstairs": "//A[@HREF='neoquest.phtml?action=move&movelink=2']",
#                           "jungleRuinsUpstairsToF1": "//A[@HREF='neoquest.phtml?action=move&movelink=4']",
#                           "jungleRuinsRollayTeleporter": "//A[@HREF='neoquest.phtml?action=move&movelink=30']",
#                           # "You see a cave entrance here" is same as all other cave entrances???
#                           "techoCave1Entrance": "//A[@HREF='neoquest.phtml?action=move&movelink=4']",
#                           # "You see a cave exit here" same as other cave exits...
#                           "techoCave1Leave": "//A[@HREF='neoquest.phtml?action=move&movelink=1']",
#                           "techoCave1Exit": "//A[@HREF='neoquest.phtml?action=move&movelink=2']",
#                           "techoCave1ReEnter": "//A[@HREF='neoquest.phtml?action=move&movelink=5']",
#                           "techoCave2Entrance": "//A[@HREF='neoquest.phtml?action=move&movelink=7']",
#                           "techoCave2Leave": "//A[@HREF='neoquest.phtml?action=move&movelink=4']",
#                           "techoCave2Exit": "//A[@HREF='neoquest.phtml?action=move&movelink=12']",
#                           "techoCave2ReEnter": "//A[@HREF='neoquest.phtml?action=move&movelink=15']",
#                           "techoCave4Entrance": "//A[@HREF='neoquest.phtml?action=move&movelink=14']",
#                           "techoCave4Leave": "//A[@HREF='neoquest.phtml?action=move&movelink=11']",
#                           "techoCave4Exit": "//A[@HREF='neoquest.phtml?action=move&movelink=15']",
#                           "techoCave4ReEnter": "//A[@HREF='neoquest.phtml?action=move&movelink=18']",
#                           "techoCave3Entrance": "//A[@HREF='neoquest.phtml?action=move&movelink=6']",
#                           "techoCave3Leave": "//A[@HREF='neoquest.phtml?action=move&movelink=3']",
#                           "techoCave3Exit": "//A[@HREF='neoquest.phtml?action=move&movelink=5']",
#                           "techoCave3ReEnter": "//A[@HREF='neoquest.phtml?action=move&movelink=8']",
#                           "techoCave6Entrance": "//A[@HREF='neoquest.phtml?action=move&movelink=9']",
#                           "techoCave6Leave": "//A[@HREF='neoquest.phtml?action=move&movelink=6']",
#                           "techoCave6Exit": "//A[@HREF='neoquest.phtml?action=move&movelink=14']",
#                           "techoCave6ReEnter": "//A[@HREF='neoquest.phtml?action=move&movelink=17']",
#                           "mountainFortressEntrance": "//A[@HREF='neoquest.phtml?action=move&movelink=20']",
#                           "mountainFortressLeave": "//A[@HREF='neoquest.phtml?action=move&movelink=1']",
#                           "techoCave7Entrance": "//A[@HREF='neoquest.phtml?action=move&movelink=10']",
#                           "techoCave7Leave": "//A[@HREF='neoquest.phtml?action=move&movelink=7']",
#                           "techoCave7Exit": "//A[@HREF='neoquest.phtml?action=move&movelink=16']",
#                           "techoCave7ReEnter": "//A[@HREF='neoquest.phtml?action=move&movelink=19']",
#                           "kalPanningEntrance": "//A[@HREF='neoquest.phtml?action=move&movelink=22']",
#                           "kalPanningLeave": "//A[@HREF='neoquest.phtml?action=move&movelink=2']",
#                           "twoRingsCaveEntrance": "//A[@HREF='neoquest.phtml?action=move&movelink=25']",
#                           "twoRingsCaveLeave": "//A[@HREF='neoquest.phtml?action=move&movelink=2']",
#                           "twoRingsCaveExit": "//A[@HREF='neoquest.phtml?action=move&movelink=1']",
#                           "twoRingsPalaceEntrance": "//A[@HREF='neoquest.phtml?action=move&movelink=26']",
#                           "twoRingsPalaceLeave": "//A[@HREF='neoquest.phtml?action=move&movelink=1']",
#                           "twoRingsF2Enter": "//A[@HREF='neoquest.phtml?action=move&movelink=2']",
#                           "twoRingsF2Leave": "//A[@HREF='neoquest.phtml?action=move&movelink=3']",
#                           "twoRingsF3Enter": "//A[@HREF='neoquest.phtml?action=move&movelink=4']",
#                           "twoRingsF3Leave": "//A[@HREF='neoquest.phtml?action=move&movelink=5']"}
