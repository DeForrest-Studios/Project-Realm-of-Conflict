class ProductionFacility:
    def __init__(Self):
        Self.Name: str = None
        Self.Level: int = 1
        Self.OutputItem: str = None
        Self.UnitsPerTick:int = None
        Self.UnitsPerTickMultiplier: float = None
        Self.CapacityMultiplier: int = None
        Self.UpgradeCostMultiplier: int = None


    def Upgrade(Self):
        Self.Level += 1
        Self.Stat_Refresh()


    def Stat_Refresh(Self):
        Self.Capacity = Self.CapacityMultiplier * Self.Level
        Self.UnitsPerTick = round(((Self.UnitsPerTickMultiplier + (Self.UnitsPerTickMultiplier*Self.Level)) * Self.Level), 2)
        Self.UpgradeCost = Self.UpgradeCostMultiplier * Self.Level
        Self.ExperienceGainOnUpgrade = (Self.UpgradeCost * 1.5) * Self.Level


class Well(ProductionFacility):
    def __init__(Self):
        super().__init__()
        Self.Name: str = "Well"
        Self.OutputItem: str = "Water"
        Self.UnitsPerTickMultiplier: float = 0.480
        Self.CapacityMultiplier: int = 5000
        Self.UpgradeCostMultiplier: int = 800
        Self.Stat_Refresh()


class SandQuarry(ProductionFacility):
    def __init__(Self):
        super().__init__()
        Self.Name: str = "Sand Quarry"
        Self.OutputItem: str = "Sand"
        Self.UnitsPerTickMultiplier: float = 0.440
        Self.CapacityMultiplier: int = 5000
        Self.UpgradeCostMultiplier: int = 800
        Self.Stat_Refresh()


class GravelPit(ProductionFacility):
    def __init__(Self):
        super().__init__()
        Self.Name: str = "Gravel Pit"
        Self.OutputItem: str = "Gravel"
        Self.UnitsPerTickMultiplier: float = 0.440
        Self.CapacityMultiplier: int = 5000
        Self.UpgradeCostMultiplier: int = 800
        Self.Stat_Refresh()


class CottonFarm(ProductionFacility):
    def __init__(Self):
        super().__init__()
        Self.Name: str = "Cotton Farm"
        Self.OutputItem: str = "Cotton"
        Self.UnitsPerTickMultiplier: float = 0.400
        Self.CapacityMultiplier: int = 5000
        Self.UpgradeCostMultiplier: int = 800
        Self.Stat_Refresh()


class LimestoneQuarry(ProductionFacility):
    def __init__(Self):
        super().__init__()
        Self.Name: str = "Limestone Quarry"
        Self.OutputItem: str = "Limestone"
        Self.UnitsPerTickMultiplier: float = 0.360
        Self.CapacityMultiplier: int = 5000
        Self.UpgradeCostMultiplier: int = 800
        Self.Stat_Refresh()


class WheatFarm(ProductionFacility):
    def __init__(Self):
        super().__init__()
        Self.Name: str = "Wheat Farm"
        Self.OutputItem: str = "Wheat"
        Self.UnitsPerTickMultiplier: float = 0.300
        Self.CapacityMultiplier: int = 5000
        Self.UpgradeCostMultiplier: int = 800
        Self.Stat_Refresh()


class TreeFarm(ProductionFacility):
    def __init__(Self):
        super().__init__()
        Self.Name: str = "Tree Farm"
        Self.OutputItem: str = "Log"
        Self.UnitsPerTickMultiplier: float = 0.260
        Self.CapacityMultiplier: int = 5000
        Self.UpgradeCostMultiplier: int = 800
        Self.Stat_Refresh()


class CoalMine(ProductionFacility):
    def __init__(Self):
        super().__init__()
        Self.Name: str = "Coal Mine"
        Self.OutputItem: str = "Coal"
        Self.UnitsPerTickMultiplier: float = 0.200
        Self.CapacityMultiplier: int = 5000
        Self.UpgradeCostMultiplier: int = 800
        Self.Stat_Refresh()


class MyceliumFarm(ProductionFacility):
    def __init__(Self):
        super().__init__()
        Self.Name: str = "Mycelium Farm"
        Self.OutputItem: str = "Mycelium"
        Self.UnitsPerTickMultiplier: float = 0.160
        Self.CapacityMultiplier: int = 5000
        Self.UpgradeCostMultiplier: int = 800
        Self.Stat_Refresh()


class CopperMine(ProductionFacility):
    def __init__(Self):
        super().__init__()
        Self.Name: str = "Copper Mine"
        Self.OutputItem: str = "Copper Ore"
        Self.UnitsPerTickMultiplier: float = 0.100
        Self.CapacityMultiplier: int = 5000
        Self.UpgradeCostMultiplier: int = 800
        Self.Stat_Refresh()


class IronMine(ProductionFacility):
    def __init__(Self):
        super().__init__()
        Self.Name: str = "Iron Mine"
        Self.OutputItem: str = "Iron Ore"
        Self.UnitsPerTickMultiplier: float = 0.060
        Self.CapacityMultiplier: int = 5000
        Self.UpgradeCostMultiplier: int = 800
        Self.Stat_Refresh()


class BauxiteMine(ProductionFacility):
    def __init__(Self):
        super().__init__()
        Self.Name: str = "Bauxite Mine"
        Self.OutputItem: str = "Aluminum Ore"
        Self.UnitsPerTickMultiplier: float = 0.020
        Self.CapacityMultiplier: int = 5000
        Self.UpgradeCostMultiplier: int = 800
        Self.Stat_Refresh()


class SilverMine(ProductionFacility):
    def __init__(Self):
        super().__init__()
        Self.Name: str = "Silver Mine"
        Self.OutputItem: str = "Silver Ore"
        Self.UnitsPerTickMultiplier: float = 0.010
        Self.CapacityMultiplier: int = 5000
        Self.UpgradeCostMultiplier: int = 800
        Self.Stat_Refresh()


class GoldMine(ProductionFacility):
    def __init__(Self):
        super().__init__()
        Self.Name: str = "Gold Mine"
        Self.OutputItem: str = "Gold Ore"
        Self.UnitsPerTickMultiplier: float = 0.010
        Self.CapacityMultiplier: int = 5000
        Self.UpgradeCostMultiplier: int = 800
        Self.Stat_Refresh()


class LithiumMine(ProductionFacility):
    def __init__(Self):
        super().__init__()
        Self.Name: str = "Lithium Mine"
        Self.OutputItem: str = "Lithium Ore"
        Self.UnitsPerTickMultiplier: float = 0.004
        Self.CapacityMultiplier: int = 5000
        Self.UpgradeCostMultiplier: int = 800
        Self.Stat_Refresh()


class ManufacturingFacility:
    def __init__(Self):
        Self.Name: str = None
        Self.Level: int = 1


    def Upgrade(Self):
        Self.Level += 1
        Self.Stat_Refresh()
    
    
    def Stat_Refresh(Self):
        ...# This is where stats are multiplied by level, and reassigned