class ProductionFacility:
    def __init__(Self):
        Self.Data = {
            "Name":"None",
            "Level":1,
            "Output":"None",
            "Units Per Tick":0,
            "Units Per Tick Multiplier":0.0,
            "Capacity":0,
            "Upgrade Cost":0,
            "Experience On Upgrade":0,
            "Capacity Multiplier": 0,
            "Upgrade Cost Multiplier": 0,
            "Time of Last Collect": "Never",
        }


    def Upgrade(Self):
        Self.Data["Level"] += 1
        Self.Refresh_Stats()


    def Refresh_Stats(Self):
        Self.Data["Capacity"] = Self.Data["Capacity Multiplier"] * Self.Data["Level"]
        Self.Data["Units Per Tick"] = round(((Self.Data["Units Per Tick Multiplier"] + (Self.Data["Units Per Tick Multiplier"] * Self.Data["Level"])) * Self.Data["Level"]), 2)
        Self.Data["Upgrade Cost"] = Self.Data["Upgrade Cost Multiplier"] * Self.Data["Level"]
        Self.Data["Experience Gain On Upgrade"] = (Self.Data["Upgrade Cost"] * 1.5) * Self.Data["Level"]


class Well(ProductionFacility):
    def __init__(Self):
        super().__init__()
        Self.Data = {
            "Name":"Well",
            "Level":1,
            "Output":"Water",
            "Units Per Tick":0,
            "Units Per Tick Multiplier":0.480,
            "Capacity":0,
            "Upgrade Cost":0,
            "Experience On Upgrade":0,
            "Capacity Multiplier": 5000,
            "Upgrade Cost Multiplier": 800,
            "Time of Last Collect": "Never",
        }
        Self.Refresh_Stats()


class SandQuarry(ProductionFacility):
    def __init__(Self):
        super().__init__()
        Self.Data = {
            "Name":"Sand Quarry",
            "Level":1,
            "Output":"Sand",
            "Units Per Tick":0,
            "Units Per Tick Multiplier":0.440,
            "Capacity":0,
            "Upgrade Cost":0,
            "Experience On Upgrade":0,
            "Capacity Multiplier": 5000,
            "Upgrade Cost Multiplier": 800,
            "Time of Last Collect": "Never",
        }
        Self.Refresh_Stats()


class GravelPit(ProductionFacility):
    def __init__(Self):
        super().__init__()
        Self.Data = {
            "Name":"Gravel Pit",
            "Level":1,
            "Output":"Gravel",
            "Units Per Tick":0,
            "Units Per Tick Multiplier":0.440,
            "Capacity":0,
            "Upgrade Cost":0,
            "Experience On Upgrade":0,
            "Capacity Multiplier": 5000,
            "Upgrade Cost Multiplier": 800,
            "Time of Last Collect": "Never",
        }
        Self.Refresh_Stats()


class CottonFarm(ProductionFacility):
    def __init__(Self):
        super().__init__()
        Self.Data = {
            "Name":"Cotton Farm",
            "Level":1,
            "Output":"Cotton",
            "Units Per Tick":0,
            "Units Per Tick Multiplier":0.400,
            "Capacity":0,
            "Upgrade Cost":0,
            "Experience On Upgrade":0,
            "Capacity Multiplier": 5000,
            "Upgrade Cost Multiplier": 800,
            "Time of Last Collect": "Never",
        }
        Self.Refresh_Stats()


class LimestoneQuarry(ProductionFacility):
    def __init__(Self):
        super().__init__()
        Self.Data = {
            "Name":"Limestone Quarry",
            "Level":1,
            "Output":"Limestone",
            "Priority":0,
            "Units Per Tick":0,
            "Units Per Tick Multiplier":0.360,
            "Capacity":0,
            "Upgrade Cost":0,
            "Experience On Upgrade":0,
            "Capacity Multiplier": 5000,
            "Upgrade Cost Multiplier": 800,
            "Time of Last Collect": "Never",
        }
        Self.Refresh_Stats()


class WheatFarm(ProductionFacility):
    def __init__(Self):
        super().__init__()
        Self.Data = {
            "Name":"Wheat Farm",
            "Level":1,
            "Output":"Wheat",
            "Units Per Tick":0,
            "Units Per Tick Multiplier":0.300,
            "Capacity":0,
            "Upgrade Cost":0,
            "Experience On Upgrade":0,
            "Capacity Multiplier": 5000,
            "Upgrade Cost Multiplier": 800,
            "Time of Last Collect": "Never",
        }
        Self.Refresh_Stats()


class TreeFarm(ProductionFacility):
    def __init__(Self):
        super().__init__()
        Self.Data = {
            "Name":"Tree Farm",
            "Level":1,
            "Output":"Log",
            "Units Per Tick":0,
            "Units Per Tick Multiplier":0.260,
            "Capacity":0,
            "Upgrade Cost":0,
            "Experience On Upgrade":0,
            "Capacity Multiplier": 5000,
            "Upgrade Cost Multiplier": 800,
            "Time of Last Collect": "Never",
        }
        Self.Refresh_Stats()


class CoalMine(ProductionFacility):
    def __init__(Self):
        super().__init__()
        Self.Data = {
            "Name":"Coal Mine",
            "Level":1,
            "Output":"Coal",
            "Units Per Tick":0,
            "Units Per Tick Multiplier":0.200,
            "Capacity":0,
            "Upgrade Cost":0,
            "Experience On Upgrade":0,
            "Capacity Multiplier": 5000,
            "Upgrade Cost Multiplier": 800,
            "Time of Last Collect": "Never",
        }
        Self.Refresh_Stats()


class MyceliumFarm(ProductionFacility):
    def __init__(Self):
        super().__init__()
        Self.Data = {
            "Name":"Mycelium Farm",
            "Level":1,
            "Output":"Mycelium",
            "Units Per Tick":0,
            "Units Per Tick Multiplier":0.160,
            "Capacity":0,
            "Upgrade Cost":0,
            "Experience On Upgrade":0,
            "Capacity Multiplier": 5000,
            "Upgrade Cost Multiplier": 800,
            "Time of Last Collect": "Never",
        }
        Self.Refresh_Stats()


class CopperMine(ProductionFacility):
    def __init__(Self):
        super().__init__()
        Self.Data = {
            "Name":"Copper Mine",
            "Level":1,
            "Output":"Copper Ore",
            "Units Per Tick":0,
            "Units Per Tick Multiplier":0.100,
            "Capacity":0,
            "Upgrade Cost":0,
            "Experience On Upgrade":0,
            "Capacity Multiplier": 5000,
            "Upgrade Cost Multiplier": 800,
            "Time of Last Collect": "Never",
        }
        Self.Refresh_Stats()


class IronMine(ProductionFacility):
    def __init__(Self):
        super().__init__()
        Self.Data = {
            "Name":"Iron Mine",
            "Level":1,
            "Output":"Iron Ore",
            "Units Per Tick":0,
            "Units Per Tick Multiplier":0.060,
            "Capacity":0,
            "Upgrade Cost":0,
            "Experience On Upgrade":0,
            "Capacity Multiplier": 5000,
            "Upgrade Cost Multiplier": 800,
            "Time of Last Collect": "Never",
        }
        Self.Refresh_Stats()


class AluminumMine(ProductionFacility):
    def __init__(Self):
        super().__init__()
        Self.Data = {
            "Name":"Aluminum Mine",
            "Level":1,
            "Output":"Aluminum Ore",
            "Priority":0,
            "Units Per Tick":0,
            "Units Per Tick Multiplier":0.020,
            "Capacity":0,
            "Upgrade Cost":0,
            "Experience On Upgrade":0,
            "Capacity Multiplier": 5000,
            "Upgrade Cost Multiplier": 800,
            "Time of Last Collect": "Never",
        }
        Self.Refresh_Stats()


class SilverMine(ProductionFacility):
    def __init__(Self):
        super().__init__()
        Self.Data = {
            "Name":"Silver Mine",
            "Level":1,
            "Output":"Silver Ore",
            "Priority":0,
            "Units Per Tick":0,
            "Units Per Tick Multiplier":0.010,
            "Capacity":0,
            "Upgrade Cost":0,
            "Experience On Upgrade":0,
            "Capacity Multiplier": 5000,
            "Upgrade Cost Multiplier": 800,
            "Time of Last Collect": "Never",
        }
        Self.Refresh_Stats()


class GoldMine(ProductionFacility):
    def __init__(Self):
        super().__init__()
        Self.Data = {
            "Name":"Gold Mine",
            "Level":1,
            "Output":"Gold Ore",
            "Units Per Tick":0,
            "Units Per Tick Multiplier":0.010,
            "Capacity":0,
            "Upgrade Cost":0,
            "Experience On Upgrade":0,
            "Capacity Multiplier": 5000,
            "Upgrade Cost Multiplier": 800,
            "Time of Last Collect": "Never",
        }
        Self.Refresh_Stats()


class OilWell(ProductionFacility):
    def __init__(Self):
        super().__init__()
        Self.Data = {
            "Name":"Oil Well",
            "Level":1,
            "Output":"Oil",
            "Units Per Tick":0,
            "Units Per Tick Multiplier":0.008,
            "Capacity":0,
            "Upgrade Cost":0,
            "Experience On Upgrade":0,
            "Capacity Multiplier": 5000,
            "Upgrade Cost Multiplier": 800,
            "Time of Last Collect": "Never",
        }
        Self.Refresh_Stats()


class LithiumMine(ProductionFacility):
    def __init__(Self):
        super().__init__()
        Self.Data = {
            "Name":"Lithium Mine",
            "Level":1,
            "Output":"Lithium Ore",
            "Units Per Tick":0,
            "Units Per Tick Multiplier":0.004,
            "Capacity":0,
            "Upgrade Cost":0,
            "Experience On Upgrade":0,
            "Capacity Multiplier": 5000,
            "Upgrade Cost Multiplier": 800,
            "Time of Last Collect": "Never",
        }
        Self.Refresh_Stats()



class ManufacturingFacility:
    def __init__(Self, Name):
        Self.Data = {
            "Name":Name,
            "Level":1,
            "Recipe":"None",
            "Priority":1,
            "Units Per Tick":0,
            "Units Per Tick Multiplier":0.001,
            "Capacity":0,
            "Upgrade Cost":0,
            "Experience On Upgrade":0,
            "Capacity Multiplier": 5000,
            "Upgrade Cost Multiplier": 800,
            "Time of Last Collect": "Never",
        }

        Self.Refresh_Stats()


    def Upgrade(Self):
        Self.Data["Level"] += 1
        Self.Refresh_Stats()
    
    
    def Refresh_Stats(Self):
        Self.Data["Units Per Tick"] = Self.Data["Units Per Tick Multiplier"] * Self.Data["Level"]
        Self.Data["Capacity"] = Self.Data["Capacity Multiplier"] * Self.Data["Level"]
        Self.Data["Upgrade Cost"] = Self.Data["Upgrade Cost Multiplier"] * Self.Data["Level"]
        Self.Data["Experience On Upgrade"] = (Self.Data["Upgrade Cost"] * 1.5) * Self.Data["Level"]