from asyncio import run
from random import randrange
from Player import Player

FirstNames = [
    "Zara", "Nyx", "Xander", "Ari", "Nova", "Eli", "Luna", "Kai", "Cleo", "Jett",
    "Ava", "Orion", "Zoe", "Axel", "Lyra", "Finn", "Aria", "Cassian", "Mila", "Phoenix",
    "Atlas", "Athena", "Cyrus", "Dax", "Elara", "Gideon", "Haven", "Iris", "Jupiter", "Kira",
    "Leo", "Maeve", "Neo", "Ophelia", "Pax", "Quinn", "Rhea", "Soren", "Thalia", "Ulysses",
    "Vesper", "Wren", "Yara", "Zephyr", "Artemis", "Bastian", "Celeste", "Dorian", "Ember",
    "Faye", "Galaxy", "Hawk", "Ivy", "Jaxon", "Kaida", "Lazarus", "Mira", "Nash", "Olympia",
    "Piper", "Quest", "Rogue", "Sage", "Theia", "Ursa", "Venus", "Winter", "Yuri", "Zarael",
    "Adira", "Branwen", "Caius", "Dahlia", "Ezra", "Freyja", "Gaius", "Hera", "Inara", "Jareth",
    "Kael", "Lilith", "Mars", "Nia", "Octavia", "Perseus", "Quasar", "Raven", "Serafina", "Talon",
    "Umbra", "Valkyrie", "Wilder", "Yasmin", "Zephyra", "Apollo", "Belle", "Castor", "Delta", "Eos",
    "Felix", "Gemma", "Helios", "Indigo", "Juno", "Kale", "Lisbeth", "Maximus", "Nyxen", "Oriel",
    "Pandora", "Quill", "Rigel", "Seraphim", "Terra", "Umbriel", "Vespera", "Wynter", "Yarael",
    "Zed", "Aeris", "Briar", "Cosmo", "Dante", "Elowen", "Fawn", "Galen", "Hermes", "Ione",
    "Jaspar", "Kalliope", "Lysander", "Miraak", "Nebula", "Ozias", "Paisley", "Quinnlan", "Raiden",
    "Selene", "Tiberius", "Uma", "Veda", "Wynne", "Yasmina", "Zaraiah", "Andromeda", "Bellatrix",
    "Cassiopeia", "Draco", "Electra", "Fiero", "Gaia", "Hades", "Icarus", "Jupiter", "Keira",
    "Lysandra", "Morrigan", "Neptune", "Orpheus", "Pandora", "Quintessa", "Riordan", "Saffron",
    "Theon", "Uranus", "Vesperia", "Wynona", "Yseult", "Zephyrine", "Astra", "Borealis", "Calypso",
    "Draven", "Eclipse", "Faelan", "Galadriel", "Hypatia", "Io", "Kestrel", "Lunaire", "Mercury",
    "Nyxia", "Oberon", "Paxton", "Quasar", "Ravenna", "Seren", "Triton", "Ulyssia", "Vesperian",
    "Wynn", "Yvaine", "Zelenia", "Alaric", "Brynn", "Cyra", "Daxton", "Eirian", "Faela", "Gareth",
    "Hera", "Ivory", "Jorah", "Kairos", "Lyric", "Maia", "Nashira", "Oriana", "Peregrine", "Quinten",
    "Raine", "Sylvan", "Talon", "Umbria", "Vespera", "Wynston", "Yvette", "Zephyrine", "Ariadne",
    "Bellamy", "Cairo", "Dresden", "Elysia", "Ferris", "Gwendolyn", "Havoc", "Isolde", "Jasper",
    "Kieran", "Lyra", "Maverick", "Nia", "Orson", "Paisley", "Quinn", "Raina", "Sylvia", "Talon",
    "Ursa", "Vesper", "Wynn", "Yvonne", "Zephyr", "Ariella", "Beaumont", "Callista", "Daxton",
    "Elara", "Fiora", "Griffin", "Hazel", "Ivy", "Jace", "Kiera", "Lyric", "Meadow", "Nyx", "Orin",
    "Paxton", "Quincy", "Raine", "Sylvie", "Talon", "Ulysses", "Vada", "Winona", "Yasmin", "Zander",
]

LastNames = [
    "Nova", "Draco", "Williams", "Jones", "Brown", "Silvers", "Taylor", "Anderson", "Galactic", "Thompson",
    "Orion", "White", "Harris", "Tesla", "Martin", "Space", "Garcia", "Martinez", "Robinson", "Warp",
    "Astro", "Rodriguez", "Lewis", "Lee", "Walker", "Nebula", "Allen", "Stellar", "Hernandez", "Starlight", "Wright",
    "Lopez", "Hill", "Quantum", "Green", "Adams", "Baker", "Gonzalez", "Nelson", "Carter", "Mitchell",
    "Cosmos", "Roberts", "Turner", "Phillips", "Campbell", "Parker", "Evans", "Edwards", "Collins", "Stewart",
    "Nebula", "Morris", "Rogers", "Reed", "Cook", "Morgan", "Bell", "Murphy", "Bailey", "Rivera",
    "Cooper", "Stargazer", "Richardson", "Cox", "Howard", "Stellaris", "Torres", "Peterson", "Gray", "Ramirez",
    "James", "Watson", "Stellar", "Brooks", "Kelly", "Sanders", "Astronomos", "Bennett", "Wood", "Barnes",
    "Roswell", "Henderson", "Coleman", "Jenkins", "Perry", "Powell", "Long", "Patterson", "Hughes", "Galaxian",
    "Washington", "Butler", "Simmons", "Foster", "Gonzales", "Bryant", "Alexander", "Russell", "Griffin", "Diaz",
    "Vortex", "Myers", "Ford", "Hamilton", "Graham", "Sullivan", "Wallace", "Woods", "Cole", "West",
    "Jordan", "Stellaris", "Owens", "Reynolds", "Fisher", "Ellis", "Harrison", "Gibson", "McDonald", "Quasar",
    "Marshall", "Ortiz", "Gomez", "Murray", "Freeman", "Wells", "Webb", "Simpson", "Stevens", "Tucker",
    "Porter", "Hunter", "Hicks", "Crawford", "Starborn", "Boyd", "Mason", "Morales", "Kennedy", "Warren",
    "Stellaris", "Ramos", "Reyes", "Burns", "Gordon", "Shaw", "Holmes", "Rice", "Starlight", "Hunt", "Black",
    "Daniels", "Stargazer", "Mills", "Nichols", "Grant", "Knight", "Ferguson", "Rose", "Stone", "Lunar",
    "Thorne", "Cosmic", "Khan", "Warp", "Ryder", "Aldrin", "Venus", "Apollo", "Skywalker", "Xenon"
]


class Infantry:
    def __init__(Self, Level, Type, Owner, Name=None):
        if Name == None:
            Self.Name = Self.Generate_Name(Owner)
        else:
            Self.Name = Name
        Self.Level = Level
        Self.Type = Type
    
    def Generate_Name(Self, Owner):
        RandomFirstName = FirstNames[randrange(0, len(FirstNames))]
        RandomLastName = LastNames[randrange(0, len(LastNames))]
        Name = f"{RandomFirstName} {RandomLastName}"
        if Name not in Owner.Army.keys():
            return Name
        else:
            Self.Generate_Name(Owner)

class Marksman(Infantry):
    def __init__(Self, Level, Type, Owner, Name=None):
        if Name == None:
            super().__init__(Level, Type, Owner)
        else:
            super().__init__(Level, Type, Owner, Name)
        Self.OffensivePower = 15000 + (Level * 3500)
        Self.DefensivePower = 4500 + (Level * 1000)


class Soldier(Infantry):
    def __init__(Self, Level, Type, Owner, Name=None):
        if Name == None:
            super().__init__(Level, Type, Owner)
        else:
            super().__init__(Level, Type, Owner, Name)
        Self.OffensivePower = 7500 + (Level * 4500)
        Self.DefensivePower = 7500 + (Level * 4500)


class Medic(Infantry):
    def __init__(Self, Level, Type, Owner, Name=None):
        if Name == None:
            super().__init__(Level, Type, Owner)
        else:
            super().__init__(Level, Type, Owner, Name)
        Self.HealingPower = 15000 + (Level * 3500)
        Self.DefensivePower = 4500 + (Level * 1000)