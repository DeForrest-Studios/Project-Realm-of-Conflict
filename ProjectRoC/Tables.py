from Infantry import Soldier, Medic

ScavengeTable = {
    "Wallet": 65,
    "Material": 65,
    "Bonus Material": 25,
    "Component": 35,
    "Bonus Component": 10,
    "Soldier": 5
}

MaterialTable = {
    "Water": (25, 30),
    "Sand": (17, 22),
    "Gravel": (17, 22),
    "Cotton": (15, 20),
    "Limestone": (14, 19),
    "Wheat": (13, 18),
    "Log": (12, 17),
    "Coal": (10, 15),
    "Mycelium": (9, 15),
    "Copper Ore": (7, 12),
    "Iron Ore": (7, 12),
    "Aluminum Ore": (5, 10),
    "Silver Ore": (3, 8),
    "Gold Ore": (1, 5),
    "Lithium Ore": (1, 3),
}

MaterialWorthTable = {
    "Water": 0.02,
    "Sand": 0.10,
    "Gravel": 0.10,
    "Cotton": 0.60,
    "Limestone": 0.65,
    "Wheat": 1.0,
    "Log": 1.2,
    "Coal": 3,
    "Mycelium": 5,
    "Copper Ore": 9,
    "Iron Ore": 9,
    "Aluminum Ore": 17,
    "Silver Ore": 28,
    "Gold Ore": 40,
    "Lithium Ore": 62,
}

InfantryToObject = {
    "Soldier":Soldier,
    "Medic":Medic,
}

InfantryTable = {
    "Level 1 ~ Soldier": 8500,
    "Level 2 ~ Soldier": 21500,
    "Level 3 ~ Soldier": 47300,
    "Level 1 ~ Medic": 8500,
    "Level 2 ~ Medic": 21500,
    "Level 3 ~ Medic": 47300,
}