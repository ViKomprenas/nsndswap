#!/usr/bin/env python3
# nsndswap/viko_nsnd.py
# copyright 2017 ViKomprenas, 2-clause BSD license (LICENSE.md)

from nsndswap.util import Track

nsnd = {
    # A Shade of Two
    "criticalErr0r": ["Taureg"],
    "Exploreation": ["Explore", "Upward Movement (Dave Owns)"],
    "Taureg": ["Sburban Jungle", "Beatdown"],
    "HammertimeVsThatBlackDoggo": ["Beatdown", "Doctor", "Sburban Jungle", "Liquid Negrocity", "BeatVale", "Penumbra Phantasm"],
    "Saviour of the Dancing Demon": ["Doctor", "Penumbra Phantasm", "Beatdown", "Sburban Jungle"],
    "Player 2": ["Sburban Jungle", "Beatdown", "Liquid Negrocity", "Doctor", "Dance of Thorns"],
    "Cascadium Dioxide": ["Cascade (Beta)", "Flare", "Doctor", "Penumbra Phantasm", "Black Rose / Green Sun", "Black Hole / Green Sun", "Sburban Jungle"],
    "Unnamed Jungle Club Remix (Extra)": ["Sburban Jungle"],
    "Tales of an Unknown Universe": [],

    # M3l0m4ni4c soundcloud
    "At Shadow's Edge": ["Penumbra Phantasm", "Amen Break"],
    "Whirlwind (L8 for D8 Version)": ["Whirlwind", "Patient", "Penumbra Phantasm", "Doctor", "Showtime", "Crystalanthemums", "Crystamanthequins", "Spider's Claw", "Vriska's Theme"],
    "Wishful Thinking": ["Skies of Skaia", "Skaian Summoning", "Theme", "Rex Duodecim Angelus", "Penumbra Phantasm", "Upward Movement (Dave Owns)", "Lotus", "Homestuck Anthem", "Ruins", "Explore", "Skaian Skuffle", "Sburban Jungle", "Cascade (Beta)", "Overture (Canon Edit)", "Even in Death"],
    "\N{Dingbat Circled Sans-Serif Digit Eight}": ["Spider's Claw", "Vriska's Theme", "Rex Duodecim Angelus", "Amen Break"],
    "Blacker Than Licorice": ["Three in the Morning", "Liquid Negrocity", "Descend", "Umbral Ultimatum", "Walk-Stab-Walk", "Cascade (Beta)", "The Ballad of Jack Noir", "Lotus", "Non Compos Mentis", "Three's a Crowd", "Calamity", "Explore", "Flight of the White Wolf", "Amen Break", "Harlequin"],
    "Whirlwind": ["Showtime", "Doctor", "Patient", "Savior of the Waking World", "Penumbra Phantasm"],
    "Ignition": ["Flare (Cascade Cut)", "MeGaLoVania"],

    # M3l0m4ni4c Sins album
    "Temmie Sleuth": ["Problem Sleuth Title Screen", "Temmie Village"],
    "Midnight Temmie": ["I'm a Member of the Midnight Crew", "Temmie Village"],
    "Infinity Temmie": ["Infinity Mechanism", "Temmie Village"],
    "Lord Temmie": ["English", "Temmie Village"],
    "Temmie Served Cold": ["Eternity, Served Cold", "Temmie Village"],
    "Temmie on My Side": ["Time on My Side", "Temmie Village"],
    "Temmie Dreamers": ["Derse Dreamers", "Temmie Village"],
    "[S] Temmie: Ascend": ["Explore", "Temmie Village"],
    "Temmiesetter": ["Moonsetter", "Temmie Village"],
    "The Lost Temmie": ["The Lost Child", "Temmie Village"],
    "Beatdown (Temmie Style)": ["Beatdown", "Temmie Village"],
    "Temmieawesome": ["Revelawesome", "Temmie Village"],
    "Tems (With Temmies)": ["Ruins (With Strings)", "Temmie Village"],
    "Temmieslammer": ["Sunslammer", "Temmie Village"],
    "Temmie Aggrieves": ["Aggrieve", "Temmie Village"],
    "Endless Temmie": ["Endless Climb", "Temmie Village"],
    "Temmie8reath": ["Spider8reath", "Temmie Village"],
    "BL1ND T3MM13": ["BL1ND JUST1C3 : 1NV3ST1G4T1ON !!", "Temmie Village"],
    "Crystamanthetems": ["Crystamanthequins", "Temmie Village"],
    "Temmiedown": ["Showdown", "Temmie Village"],
    "Cascade of Unfortunate Temmies": ["Cascade (Beta)", "Temmie Village"],
    "Umbral Temmie": ["Umbral Ultimatum", "Temmie Village"],
    "[S] Temmie: Descend": ["Descend", "Temmie Village"],
    "Temmie's Claw": ["Spider's Claw", "Temmie Village"],
    "Atomyk Temmiepyre": ["Atomyk Ebonpyre", "Temmie Village"],
    "Liquid Temmiecity": ["Liquid Negrocity", "Temmie Village"],
    "Savior of the Waking Temmie": ["Savior of the Waking World", "Temmie Village"],
    "ShowTemmie": ["Showtime", "Temmie Village"],
    "Temmie Flares": ["Flare (Cascade Cut)", "Temmie Village"],

    # ViKomprenas clyp.it
    "Dentist": ["Doctor", "Ruins", "Patient", "Savior of the Waking Patient"],
    "Another Elevator": ["Another Jungle", "Sburban Elevator"],
    "Elevator #3": ["Jungle #3", "Sburban Elevator"],
    "Another Paradigm": ["Endless Climb", "Rhapsody in Green", "MeGaLoVania", "The Paradox Paradigm", "Maestro", "Sburban Jungle", "Penumbra Phantasm", "Beatdown", "Look Where We Are", "Crystalanthemums", "Heir of Grief", "Showtime (Piano Refrain)", "Revelawesome", "Three in the Morning", "Ruins", "Jungle #3", "Tock", "Unintentional Touhou", "Courser"],
    "Radiation Sickness": ["Gaster's Theme", "Penumbra Phantasm", "Heartache", "Earthsea Borealis", "the rose rap"],
    "unfinished medley for power464646": ["Carbon Nadsat / Cuestick Genius", "Rhapsody in Green", "Havoc", "Eternity, Served Cold", "Showdown", "Riches to Ruins Movements I & II", "Negastrife", "PPiSHWA", "Carne Vale"],

    # The Exquisite Corpse
    "Exquisite Corpse": ["Carne Vale", "A Taste for Adventure", "Endless Climb", "RCT Title Screen", "Sburban Jungle", "Courser", "Jungle #3", "MeGaLoVania"],

    # YUM!: The Vore Album
    "A Welcome to the Wonderful World of Vore": [],
    "Can't Keep a Good Man Down": [],
    "The Cannibal Cafe": ["Dinosaur Comics Theme"],
    "Voreska": ["MeGaLoVania", "Spider's Claw"],
    "Voriginal Content (feat. Mister Pumpkin)": [],
    "Stomach Is An Instrument / Vorejazz": [],
    "Vorintosh Plus": ["MACINTOSH PLUS - リサフランク420 / 現代のコンピュー"],
    "the eighth track is about vriska": ["Spider's Claw", "Jungle #3", "Death by Glamour"],
    "Dentist (Vore Cut)": ["Dentist"],
    "this story has about 300 pages of worldbuilding and then someone gets encased in latex and suffocates and it's generally agreed to be a real sexy affair": [],
    "A Farewell to the Wonderful World of Vore": ["A Welcome to the Wonderful World of Vore"],
    "[BONUS] The Voreing Experience": [],

    # Sealstuck Volume 1
    "Sealumbra Phantasm": ["Penumbra Phantasm"],
    "sealteamsixgoestotacobellfordinnerexcepteveryonesasealandwecheer": [],
    "Sealburban Jugnle": ["Sburban Jungle"],
    "it's an amusement park! it's a sealival!": ["le canrival"],
    "A seal related undertale pun": ["CORE"],
    "sealsleepytime.wav": [],
    "caseal": ["casin"],
    "Seal Who": ["Doctor Who Theme"],
    "the seal rap": [],
    "Necrosealfoxtasia": ["Necrofantasia"],
    "Pumpkin Party in Seal Hitler's Water Apocalypse": ["Pumpkin Party in Sea Hitler's Water Apocalypse"],
    "Dinoseal Comics": ["Dinosaur Comics Theme"],
    "Sealache": ["Heartache"],
    "Seal Intermission": [],
    "Moonsealer": ["Moonsetter"],
    "Seally Slippery Cave": ["Ice Path"],
    "sealsetter": ["Sunsetter"],
    "eriseals theme": ["Eridan's Theme"],
    "sealwave": [],
    "The Key of Seal": [],
    "just driving my seal to work officer": [],
    "Unintentionally Seal": ["Unintentionally Short"],
    "i put seal noises over an old abandoned project": [],
    #"アザラシ 赤ちゃん 420 / モダン樹皮": ["MACINTOSH PLUS - リサフランク420 / 現代のコンピュー",
    "This isn't an old song that I bullshitted over, no sir": [],
    "sealsounds.wav": [],
    "Troubled Seas": [],
    "Seal the Deal": [],
    "A Seal Legend - A Seal is 2": ["A Baby Legend"],
}


def parse():
    return [Track(x, y) for x, y in nsnd.items() if y is not NotImplementedError]
