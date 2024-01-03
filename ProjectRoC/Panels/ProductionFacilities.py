from asyncio import create_task
from RealmOfConflict import RealmOfConflict
from discord.ext.commands import Context as DiscordContext
from discord import Interaction as DiscordInteraction
from discord import ButtonStyle as DiscordButtonStyle
from discord import SelectOption, Embed
from discord.ui import View, Select, Button
from Panels.Panel import Panel
from Structures import ProductionFacility
from time import time as Time
from Player import Player

class ProductionFacilitiesPanel(Panel):
    def __init__(Self, Ether:RealmOfConflict, InitialContext:DiscordContext, ButtonStyle, Interaction:DiscordInteraction, PlayPanel):
        super().__init__(Ether, InitialContext,
                         PlayPanel, "Production",
                         Interaction=Interaction, ButtonStyle=ButtonStyle)

    async def _Construct_Panel(Self, FacilitySelected=None, FacilityUpgraded=False):
        if Self.Interaction.user != Self.InitialContext.author:
            return

        if FacilityUpgraded == True:
            if Self.Player.Data['Wallet'] < Self.FacilitySelected.UpgradeCost:
                Self.EmbedFrame.clear_fields()
                FacilityInfoString = (f"Level: {Self.FacilitySelected.Level}\n"+
                                    f"Capacity: {Self.FacilitySelected.Capacity}\n"+
                                    f"Units Per Second: {Self.FacilitySelected.UnitsPerTick}\n"+
                                    f"Upgrade Cost: {Self.FacilitySelected.UpgradeCost}")
                await Self._Generate_Info(Self.Ether, Self.InitialContext, Exclusions=["Team", "Power"])
                Self.EmbedFrame.add_field(name=f"{Self.FacilitySelected.Name} Info", value=FacilityInfoString)
                Self.EmbedFrame.add_field(name="Insufficient Funds", value="\u200b", inline=False)
            else:
                Self.FacilitySelected.Upgrade()
                Self.Player.Data['Wallet'] = round(Self.Player.Data['Wallet'] - Self.FacilitySelected.UpgradeCost, 2)
                Self.EmbedFrame.clear_fields()
                FacilityInfoString = (f"Level: {format(Self.FacilitySelected.Level, ',')}\n"+
                                      f"Capacity: {format(Self.FacilitySelected.Capacity, ',')}\n"+
                                      f"Units Per Second: {format(Self.FacilitySelected.UnitsPerTick, ',')}\n"+
                                      f"Upgrade Cost: {format(Self.FacilitySelected.UpgradeCost, ',')}")
                await Self._Generate_Info(Self.Ether, Self.InitialContext, Exclusions=["Team", "Power"])
                Self.EmbedFrame.add_field(name=f"{Self.FacilitySelected.Name} Info", value=FacilityInfoString)

        if FacilitySelected is not None:
            Self.FacilitySelected:ProductionFacility = Self.Player.ProductionFacilities[Self.Interaction.data["values"][0]]
            Self.FacilitiesSelect.placeholder = Self.Interaction.data["values"][0]
            Self.EmbedFrame.clear_fields()

            try:
                Self.FacilityUpgradeButton
            except AttributeError:
                Self.FacilityUpgradeButton = Button(label="Upgrade", style=Self.ButtonStyle, custom_id="FacilityUpgradeButton", row=1)
                Self.BaseViewFrame.add_item(Self.FacilityUpgradeButton)
                Self.FacilityUpgradeButton.callback = lambda SelectInteraction: Self._Construct_Panel(SelectInteraction)

            await Self._Generate_Info(Self.Ether, Self.InitialContext, Exclusions=["Team", "Power"])

            FacilityInfoString = (f"Level: {format(Self.FacilitySelected.Level, ',')}\n"+
                                  f"Capacity: {format(Self.FacilitySelected.Capacity, ',')}\n"+
                                  f"Units Per Second: {format(Self.FacilitySelected.UnitsPerTick, ',')}\n"+
                                  f"Upgrade Cost: {format(Self.FacilitySelected.UpgradeCost, ',')}")
            Self.EmbedFrame.add_field(name=f"{Self.FacilitySelected.Name} Info", value=FacilityInfoString)
        else:
            await Self._Generate_Info(Self.Ether, Self.InitialContext, Exclusions=["Team", "Power"])
            Self.FacilitiesSelected = None
            Self.CollectProductionButton = Button(label="Collect Production", style=Self.ButtonStyle, custom_id="CollectProductionButton")
            Self.CollectProductionButton.callback = lambda ButtonInteraction: Self._Collect_Production_Facilities(Self.Ether, Self.InitialContext, Self.ButtonStyle, ButtonInteraction)
            Self.BaseViewFrame.add_item(Self.CollectProductionButton)

            Self.HomepageButton = Button(label="Home", style=DiscordButtonStyle.grey, row=3, custom_id="HomePageButton")
            Self.HomepageButton.callback = lambda ButtonInteraction: Self.PlayPanel._Construct_Home(Self.Ether, Self.InitialContext, ButtonInteraction)
            Self.BaseViewFrame.add_item(Self.HomepageButton)

            Self.Options = [SelectOption(label=Name) for Name, Building in Self.Player.ProductionFacilities.items() if Building != "None"]
            Self.FacilitiesSelect = Select(options=Self.Options, custom_id=f"ItemSelection", row=2)
            Self.FacilitiesSelect.callback = lambda SelectInteraction: Self._Construct_Panel(FacilitySelected=SelectInteraction.data["values"][0])
            Self.BaseViewFrame.add_item(Self.FacilitiesSelect)

            await Self._Generate_Info(Self.Ether, Self.InitialContext, Exclusions=["Team", "Power"])

        Self.Ether.Logger.info(f"Sent Facilities panel to {Self.Player}")
        await Self._Send_New_Panel(Self.Interaction)


    async def _Collect_Production_Facilities(Self, Interaction:DiscordInteraction):
        if Interaction.user != Self.InitialContext.author:
            return
        CollectionString = ""
        ProductionFacilityLength:int = len(Self.Player.ProductionFacilities.values()) - 1
        
        CollectionTime = int(Time())

        Index:int
        Facility:ProductionFacility
        for Index, Facility in enumerate(Self.Player.ProductionFacilities.values()):
            if Self.Player.Data["Time of Last Production Collection"] == "Never":
                EarnedAmount = round((Facility.UnitsPerTick * (CollectionTime - Self.Player.Data["Join TimeStamp"])) , 2)
            else:
                EarnedAmount = round(Facility.UnitsPerTick * (CollectionTime - Self.Player.Data["Time of Last Production Collection"]), 2)

            if Index == ProductionFacilityLength:
                CollectionString += f"{EarnedAmount} {Facility.OutputItem}"
            else:
                CollectionString += f"{EarnedAmount} {Facility.OutputItem}\n"

            SkillBonus = ((Self.Player.Skills["Production"] + 1) * (5 * EarnedAmount)/100)
            EarnedAmount = round(EarnedAmount + SkillBonus, 2)
            Self.Player.Inventory[Facility.OutputItem] = round(Self.Player.Inventory[Facility.OutputItem] + EarnedAmount, 2)
        
        Self.Player.Data["Time of Last Production Collection"] = CollectionTime

        Self.EmbedFrame.clear_fields()

        await Self._Generate_Info(Self.Ether, Self.InitialContext, Exclusions=["Team", "Power"])

        Self.EmbedFrame.add_field(name="Collected:", value=CollectionString)

        Self.Ether.Logger.info(f"{Self.Player} collected from production facilities")
        await Self._Send_New_Panel(Interaction)