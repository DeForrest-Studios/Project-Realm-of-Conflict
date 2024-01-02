from Structures import ProductionFacility, Well, SandQuarry, GravelPit, CottonFarm, LimestoneQuarry, WheatFarm, TreeFarm, CoalMine, MyceliumFarm, CopperMine, IronMine, BauxiteMine, SilverMine, GoldMine, LithiumMine

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
                "Power": 0,
                "Level": 1,
                "Experience": 0.0,
                "Skill Points": 0,
                "Attack Power": 0,
                "Defensive Power": 0,
                "Production Power": 0,
                "Manufacturing Power": 0,
                "Energy Sapping": 0,
                "General Skill": 0, 
                "Offensive Skill": 0,
                "Defensive Skill": 0,
                "Counter Operations Skill": 0,
                "Maiden's Grace": 0, # 0 for False, 1 for True
                "Join TimeStamp": int(time()),
                "Time of Last Production Collection": "Never",
                "Time of Last Manufacturing Collection": "Never",
            }
        else:
            Self.Data:{str:...} = {
                "UUID": Member.id,
                "Member Object": Member,
                "Name": Member.name,
                "Team": "None",
                "Wallet": 0.00,
                "Power": 0,
                "Level": 1,
                "Experience": 0.0,
                "Skill Points": 0,
                "Offensive Power": 0,
                "Defensive Power": 0,
                "Production Power": 0,
                "Manufacturing Power": 0,
                "General Skill": 0, 
                "Offensive Skill": 0,
                "Defensive Skill": 0,
                "Counter Operations Skill": 0,
                "Maiden's Grace": 0, # 0 for False, 1 for True
                "Join TimeStamp": int(time()),
                "Time of Last Production Collection": "Never",
                "Time of Last Manufacturing Collection": "Never",
            }
        Self.Skills = {
            "Production":0,
            "Manufacturing":0,
            "Offensive":0,
            "Domination":0,
            "Defensive":0,
            "Healing":0,
            "Hacking":0,
            "Raiding":0,
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

    
    def Add_Skill_Point(Self, ChosenSkill):
        if Self.Data["Skill Points"] < 1:
            return False
        Self.Skills[ChosenSkill] += 1
        Self.Data["Skill Points"] -= 1
        Self.Refresh_Power()
        return True


    def Refresh_Power(Self):
        Self.Data["Offensive Power"] = Self.Skills["Offensive"] * 2500
        Self.Data["Defensive Power"] = Self.Skills["Defensive"] * 2500
        for Infantry in Self.Army.values():
            if hasattr(Infantry, "OffensivePower"):
                Self.Data["Offensive Power"] += Infantry.OffensivePower +  (Self.Skills["Offense"])
            if hasattr(Infantry, "DefensivePower"):
                Self.Data["Defensive Power"] += Infantry.DefensivePower
        Self.Data["Power"] = (Self.Data["Offensive Power"] + Self.Data["Defensive Power"] +
                              Self.Data["Production Power"] + Self.Data["Manufacturing Power"])


    def Refresh_Stats(Self) -> str:
        Self.ExperienceForNextLevel = Self.Data["Level"] * (325 + (135 * Self.Data["Level"]) - (Self.Data["Maiden's Grace"] * (5 * Self.Data["Level"])))
        if Self.Data["Experience"] >= Self.ExperienceForNextLevel:
            Self.Level_Up()
            return "Level Up"

    
    def Level_Up(Self):
        Self.Data["Level"] += 1
        Self.Data["Skill Points"] += 1
        Self.Refresh_Stats()