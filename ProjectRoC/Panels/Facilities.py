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

class FacilitiesPanel(Panel):
    def __init__(Self, Ether:RealmOfConflict, InitialContext:DiscordContext, ButtonStyle, Interaction:DiscordInteraction, PlayPanel):
        super().__init__()
        create_task(Self._Construct_Panel(Ether, InitialContext, ButtonStyle, Interaction, PlayPanel))

    async def _Construct_Panel(Self, Ether, InitialContext, ButtonStyle, Interaction:DiscordInteraction, PlayPanel):
        if Interaction.user != InitialContext.author:
            return
        Self.FacilitySelected = None
        if Interaction.data["custom_id"] == "ItemSelection":
            Self.FacilitySelected: ProductionFacility = Ether.Data["Players"][InitialContext.author.id].ProductionFacilities[Interaction.data["values"][0]]
            Self.FacilitiesSelect.placeholder = Interaction.data["values"][0]

        if Interaction.data["custom_id"] == "FacilityUpgradeButton":
            Self.FacilitySelected.Upgrade()
            # Do not refresh BaseViewFrame, and EmbedFrame
        else:
            Self.BaseViewFrame = View(timeout=144000)
            Self.EmbedFrame = Embed(title=f"{InitialContext.author.name}'s Facilities Panel")

            Self.CollectProductionButton = Button(label="Collect Production", style=ButtonStyle, custom_id="CollectProductionButton")
            Self.CollectProductionButton.callback = lambda Interaction: Self._Collect_Production_Facilities(Ether, InitialContext, ButtonStyle, Interaction)
            Self.BaseViewFrame.add_item(Self.CollectProductionButton)

            Self.HomepageButton = Button(label="Home", style=DiscordButtonStyle.grey, row=3, custom_id="HomePageButton")
            # This is a bad callback. This is really bad, I'm well aware. But you know what, fuck it.
            Self.HomepageButton.callback = lambda Interaction: PlayPanel._Construct_Home(Ether, InitialContext, Interaction)
            Self.BaseViewFrame.add_item(Self.HomepageButton)

            Self.Options = [SelectOption(label=Name) for Name, Building in Ether.Data["Players"][InitialContext.author.id].ProductionFacilities.items() if Building != "None"]
            Self.FacilitiesSelect = Select(options=Self.Options, custom_id=f"ItemSelection", row=2)
            Self.FacilitiesSelect.callback = lambda Interaction: Self._Construct_Panel(Ether, InitialContext, ButtonStyle, Interaction, PlayPanel)
            Self.BaseViewFrame.add_item(Self.FacilitiesSelect)

            await Self._Generate_Info(Ether, InitialContext, Exclusions=["Team", "Power"])
        
        if Self.FacilitySelected:
            Self.EmbedFrame.clear_fields()
            Self.FacilityUpgradeButton = Button(label="Upgrade", style=ButtonStyle, custom_id="FacilityUpgradeButton", row=1)
            Self.BaseViewFrame.add_item(Self.FacilityUpgradeButton)
            Self.FacilityUpgradeButton.callback = lambda SelectInteraction: Self._Construct_Facilities_Panel(SelectInteraction)
            FacilityInfoString = (f"Level: {Self.FacilitySelected.Level}\n"+
                                    f"Capacity: {Self.FacilitySelected.Capacity}\n"+
                                    f"Units Per Second: {Self.FacilitySelected.UnitsPerTick}\n"+
                                    f"Upgrade Cost: {Self.FacilitySelected.UpgradeCost}")
            Self.EmbedFrame.add_field(name=f"{Self.FacilitySelected.Name} Info", value=FacilityInfoString)

        Ether.Logger.info(f"Sent Facilities panel to {Ether.Data['Players'][InitialContext.author.id].Data['Name']}")
        await Self._Send_New_Panel(Interaction)


    async def _Collect_Production_Facilities(Self, Ether:RealmOfConflict, InitialContext:DiscordContext, ButtonStyle, Interaction:DiscordInteraction):
        if Interaction.user != InitialContext.author:
            return
        CollectionString = ""
        ProductionFacilityLength:int = len(Ether.Data["Players"][InitialContext.author.id].ProductionFacilities.values()) - 1
        CollectionTime = int(Time())
        Index:int
        Facility:ProductionFacility
        for Index, Facility in enumerate(Ether.Data["Players"][InitialContext.author.id].ProductionFacilities.values()):
            if Ether.Data["Players"][InitialContext.author.id].Data["Time of Last Production Collection"] == "Never":
                EarnedAmount = round(Facility.UnitsPerTick * (CollectionTime - Ether.Data["Players"][InitialContext.author.id].Data["Join TimeStamp"]), 2)
            else:
                EarnedAmount = round(Facility.UnitsPerTick * (CollectionTime - Ether.Data["Players"][InitialContext.author.id].Data["Time of Last Production Collection"]), 2)

            if Index == ProductionFacilityLength:
                CollectionString += f"{EarnedAmount} {Facility.OutputItem}"
            else:
                CollectionString += f"{EarnedAmount} {Facility.OutputItem}\n"

            Ether.Data["Players"][InitialContext.author.id].Inventory[Facility.OutputItem] = round(Ether.Data["Players"][InitialContext.author.id].Inventory[Facility.OutputItem] + EarnedAmount, 2)
        
        Ether.Data["Players"][InitialContext.author.id].Data["Time of Last Production Collection"] = CollectionTime

        Self.EmbedFrame.clear_fields()

        await Self._Generate_Info(Ether, InitialContext, Exclusions=["Team", "Power"])

        Self.EmbedFrame.add_field(name="Collected:", value=CollectionString)

        await Self._Send_New_Panel(Interaction)