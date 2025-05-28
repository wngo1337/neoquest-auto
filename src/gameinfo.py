"""This module will probably contain a relevant list of game information like
equipment recipes, IDs, movement paths, etc."""

item_names_to_ids = {
    "glowing stone": "item230000",
    "chunk of metal": "item230001",
    "small yellow gem": "item230002",
    "plains lupe pelt": "item230003",
    "blue thread": "item230004",
    "cave lupe pelt": "item230005",
    "tiny garnet": "item230006",
    "tiny lapis": "item230007",
    "tiny amber": "item230008",
    "tiny obsidian": "item230009",
    "tiny beryl": "item230010",
    "corroded pyrite rod": "item230011",
    "corroded pewter rod": "item230012",
    "corroded copper rod": "item230013",
    "corroded ore rod": "item230014",
    "corroded aluminum rod": "item230015",
    "Xantan's Ring": "item230016",
    "grey lupe fang": "item230017",
    "black bearog paw": "item230018",
    "grizzly bearog tooth": "item230019",
    "dire lupe pelt": "item230020",
    "piece of smooth glass": "item230022",
    "lodestone": "item230023",
    "stretch of rotted cloth": "item230024",
    "armored stinger": "item230029",
    "noil's mane": "item230030",
    "shamanistic totem": "item230031",
    "skeith fang": "item230032",
    "buzz wing": "item230033",
    "wadjet skin": "item230034",
    "scorpion carapace": "item230035",
    "wooden shield": "item230036",
    "jungle beast claw": "item230037",
    "noil's tooth": "item230038",
    "jungle gauntlet": "item230039",
    "jungle vambrace": "item230040",
    "jungle breastplate": "item230041",
    "jungle helm": "item230042",
    "jungle pauldrons": "item230043",
    "the Staff of Ni-tas": "item230044",
    "rusty medallion": "item230045",
    "drakonid eye": "item230078",
    "drakonid hide": "item230079",
    "drakonid heart": "item230080",
}

equipment_names_to_recipes = {
    "Energy Shield": (
        210000,
        90010003,
        ("small yellow gem", "chunk of metal", "glowing stone"),
    ),
    # MAGIC ROBE ID IS MADE UP BECAUSE I DON'T KNOW IT YET
    "Magic Robe": (
        210011,
        90010005,
        ("cave lupe pelt", "stretch of rotted cloth", "tiny obsidian", "glowing stone"),
    ),
    "Steel Wand": (
        200006,
        90010004,
        ("tiny lapis", "corroded pewter rod", "glowing stone", "Xantan's Ring"),
    ),
    "Glacier Wand": (
        200011,
        90030001,
        (
            "shamanistic totem",
            "skeith fang",
            "jungle vambrace",
            "glowing stone",
            "the Staff of Ni-tas",
        ),
    ),
    "Robe of Protection": (
        210013,
        90070001,
        ("drakonid eye", "drakonid hide", "drakonid heart"),
    ),
    # TRIES TO ITERATE OVER THE STRING IF YOU ONLY HAVE ONE INGREDIENT
    "Keladrian Medallion": (230074, 90010008, ("rusty medallion",)),
    # -1 MEANS NO MAKER, empty tuple means no ingredients
    "Iceheart Staff": (200021, -1, tuple()),
    "White Wand": (200004, -1, tuple()),
    # NOTE: THESE ARE PLACEHOLDER IDS FOR EQUIPPING B/C DON'T KNOW THEM YET
    "Silver Wand": (
        200009,
        90010004,
        ("tiny beryl", "corroded aluminum rod", "glowing stone", "Xantan's Ring"),
    ),
    # THIS IS STILL A FILLER ID BTW
    "Nature Wand": (
        200014,
        90030001,
        (
            "jungle beast claw",
            "jungle pauldrons",
            "noil's tooth",
            "glowing stone",
            "the Staff of Ni-tas",
        ),
    ),
    "Moonstone Staff": (200024, -1, tuple()),
    "Inferno Robe": (210014, -1, tuple()),
}

travel_locations_to_paths = {
    "eleusToDankCave": "4444444444411112",
    "dankCaveF1ToF2": "878785555555555588587776664644446778855555555",
    "dankCaveF2ToF3": "555555558777777777777777777855555555532222222222222222211",
    "dankCaveF3ToF4": "555877778532222358777785322223558777677778766785877764444"
    "41441441441114122222223",
    # Takes us ONE SHORT of teleporter to grind
    "dankCaveF4ToXantan": "22146777787855558853222222112214444444466677777777"
    "858855555555555322323222222211221441144644444444444",
    "afterDankCaveTeleporterToEleus": "17888855555555555",
    "eleusToJungleRuins": "6777766677777888888555",
    "jungleRuinsF1ToF2": "22353555322335",
    "jungleRuinsF2ToKreai": "35555555555555555555555555555555877777777777777777"
    "8555555555555322233355532223555555555555878532222"
    "111164414641",
    "jungleRuinsAfterKreaiToGors": "5577777885555321412223321444114444677766"
    "44122222222355555555555555555558777777778"
    "5555886644685555355876685532222214444"
    "8322238852222222222222222222",
    "jungleRuinsAfterGorsToDenethrir": "224446467761111112277644446777777776444",
    "jungleRuinsDenethrirToF3": "555322222222355553227788888832235355577" "77788555555",
    # NEED TO ADD EXTRA 7 IF YOU WANT TO TAKE THE TELEPORTER AUTOMATICALLY
    "jungleRuinsF3ToRollay": "55558588788777788878888553333333353332233333555555558"
    "777777777777666677888668767778877776776666644444444"
    "414441114466644111211446787676461221222333311232223"
    "355558883338886777883223233553588777777777",
    "jungleRuinsAfterRollayToTechoCaves": "144444444122222244464677646444677"
    "44114111122212111121111111114444444444"
    "464444446466664677888677687887777778"
    "8878877777777666646",
    "techoCave1ToExit": "66444414444467776666777787877764444",
    "techoCave1To2Transition": "5864",
    "techoCave2ToExit": "64646666876676778888885555",
    "techoCave2To4Transition": "444",
    "techoCave4ToSunnyCity": "6676677877668887778876464644464688666444441141144"
    "644444678587666446444",
    "sunnyCityToTechoCave2": "55535533321412355555355885885555533311353555"
    "3535321122211133221223323355544441111112232"
    "332133335353",
    "techoCave2To6": "5555888558535555335553558558858776687668885855553555555"
    "355355888585535355558555888857641",
    "techoCave6ToMountainFortress": "885555555586887768764641466411111141111"
    "141467766677777777777767",
    "mountainFortressToIce": "77777777777777777777777777777777777766664",
    "mountainFortressIceToLife": "33333322222222222222235555888888877788777",
    "mountainFortressLifeToFire": "111112212222111444444444444466666777777667",
    "mountainFortressFireToShock": "332222233323335555555112222222222144446666666",
    "mountainFortressShockToSpectral": "3333333555555555555888885877",
    "mountainFortressSpectralToEntrance": "221141111444411222",
    "mountainFortressToTechoCave6": "23222222222222333223585888885888888533585"
    "3532132211314444444411",
    "techoCave6ToKalPanning": "8558887888888877777888558555558555555558558588"
    "5587876776687776666677555355558855855555585"
    "55585555558555555555335533333333332222",
    "kalPanningToFaleinn": "2222222222222231222222222222232233555555533333555" "333322",
    "faleinnToTwoRings": "77677766664446444444444446677777777777777777777777777777777"
    "7766666766666444464441"
    "22232212222222312222"
    "2222212222222211122",
    "twoRingsToJahbal": "2222222222222222222222222222222233222122222222232333333"
    "22222235555555555555555555555555555555553222114"
    "858777644444444444444412221467777776122221144444444677"
    "7777886441221"
    "144446414444641146464441144444444445864444444444444444"
    "555555555555555555",
    "reviveToJahbal": "44111114444411446444464444444444446464466646877886677"
    "887777777888887777777777766646"
    # Arrive at cave 1
    "66444414444467776666777787877764444" "5885"
    # Now at cave 3?
    "888558535555335553558558858776687668885855553555555"
    "35535588858553535555855588885"
    "778"
    # Now at cave 6
    "887888888877777888558555558555555558558588"
    "5587876776687776666677"
    "555355555555555555555588885555558553"
    # Now in the cave to Two Rings
    "22232212222222312222" "2222212222222211122"
    # Now in the Two Rings
    "2222222222222222222222222222222233222122222222232333333"
    "22222235555555555555555555555555555555553222114"
    "858777644444444444444412221467777776122221144444444677"
    "7777886441221"
    "144446414444641146464441144444444445864444444444444444"
    "5555555555555555555",
}
