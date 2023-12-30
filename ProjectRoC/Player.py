from Facilities import ProductionFacility, Well, SandQuarry, GravelPit, CottonFarm, LimestoneQuarry, WheatFarm, TreeFarm, CoalMine, MyceliumFarm, CopperMine, IronMine, BauxiteMine, SilverMine, GoldMine, LithiumMine

from time import time

class Player:
    def __init__(Self, Member):
        Self.ExperienceForNextLevel:int = 0
        if Member == "Test":
            Self.Data:{str:...} = {
                "UUID": 42069,
                "Member Object": None,
                "Name": "TestPlayer",
                "Team": "None",
                "Wallet": 0.00,
                "Experience": 0.0,
                "Level": 1,
                "Power": 0,
                "Attack Power": 0,
                "Defensive Power": 0,
                "Production Power": 0,
                "Manufacturing Power": 0,
                "Energy Sapping": 0,
                "General Skill": 0, 
                "Offensive Skill": 0,
                "Defensive Skill": 0,
                "Counter Operations Skill": 0,
            }
        else:
            Self.Data:{str:...} = {
                "UUID": Member.id,
                "Member Object": Member,
                "Name": Member.name,
                "Team": "None",
                "Wallet": 0.00,
                "Experience": 0.0,
                "Level": 1,
                "Power": 0,
                "Offensive Power": 0,
                "Defensive Power": 0,
                "Healing Power": 0,
                "Production Power": 0,
                "Manufacturing Power": 0,
                "Energy Sapping": 0,
                "General Skill": 0, 
                "Offensive Skill": 0,
                "Defensive Skill": 0,
                "Counter Operations Skill": 0,
                "Maiden's Grace": False,
                "Join TimeStamp": int(time()),
                "Time of Last Production Collection": "Never",
                "Time of Last Manufacturing Collection": "Never",
            }
        Self.Inventory:{str:float} = {
            "Water": 0.0,
            "Sand": 0.0,
            "Gravel": 0.0,
            "Cotton": 0.0,
            "Limestone": 0.0,
            "Wheat": 0.0,
            "Log": 0.0,
            "Coal": 0.0,
            "Mycelium": 0.0,
            "Copper Ore": 0.0,
            "Iron Ore": 0.0,
            "Aluminum Ore": 0.0,
            "Silver Ore": 0.0,
            "Gold Ore": 0.0,
            "Lithium Ore": 0.0,
            "Refined Copper": 0.0,
            "Refined Iron": 0.0,
            "Refined Aluminum": 0.0,
            "Refined Silver": 0.0,
            "Refined Gold": 0.0,
            "Refined Lithium": 0.0,
        }
        Self.ProductionFacilities:{str:ProductionFacility} = {
            "Well": Well(),
            "Sand Quarry": SandQuarry(),
            "Gravel Pit": GravelPit(),
            "Cotton Farm": CottonFarm(),
            "Limestone Quarry": LimestoneQuarry(),
            "Wheat Farm": WheatFarm(),
            "Tree Farm": TreeFarm(),
            "Coal Mine": CoalMine(),
            "Mycelium Farm": MyceliumFarm(),
            "Copper Mine": CopperMine(),
            "Iron Mine": IronMine(),
            "Bauxite Mine": BauxiteMine(),
            "Silver Mine": SilverMine(),
            "Gold Mine": GoldMine(),
            "Lithium Mine": LithiumMine(),
        }
        Self.ManufacturingFacilities = {}
        Self.Army = {}
        Self.Refresh_Stats()


    def Refresh_Power(Self):
        Self.Data["Offensive Power"] = 0
        Self.Data["Defensive Power"] = 0
        Self.Data["Healing Power"] = 0
        for Infantry in Self.Army.values():
            if hasattr(Infantry, "OffensivePower"):
                Self.Data["Offensive Power"] += Infantry.OffensivePower
            if hasattr(Infantry, "DefensivePower"):
                Self.Data["Defensive Power"] += Infantry.DefensivePower
            if hasattr(Infantry, "HealingPower"):
                Self.Data["Healing Power"] += Infantry.HealingPower
        Self.Data["Power"] = Self.Data["Offensive Power"] + Self.Data["Defensive Power"] + Self.Data["Healing Power"]



    def Refresh_Stats(Self):
        Self.ExperienceForNextLevel = Self.Data["Level"] * (325 + (135 * Self.Data["Level"]))
        if Self.Data["Experience"] >= Self.ExperienceForNextLevel:
            Self.Data["Level"] += 1
            Self.Refresh_Stats()