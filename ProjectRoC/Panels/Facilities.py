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
        
        Self.PlayPanel = PlayPanel
        Self.Interaction = Interaction
        Self.Player = Ether.Data['Players'][InitialContext.author.id]

        if Interaction.data["custom_id"] == "FacilityUpgradeButton":
            if Self.Player.Data['Wallet'] < Self.FacilitySelected.UpgradeCost:
                Self.EmbedFrame.clear_fields()
                FacilityInfoString = (f"Level: {Self.FacilitySelected.Level}\n"+
                                    f"Capacity: {Self.FacilitySelected.Capacity}\n"+
                                    f"Units Per Second: {Self.FacilitySelected.UnitsPerTick}\n"+
                                    f"Upgrade Cost: {Self.FacilitySelected.UpgradeCost}")
                await Self._Generate_Info(Ether, InitialContext, Exclusions=["Team", "Power"])
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
                await Self._Generate_Info(Ether, InitialContext, Exclusions=["Team", "Power"])
                Self.EmbedFrame.add_field(name=f"{Self.FacilitySelected.Name} Info", value=FacilityInfoString)
        elif Interaction.data["custom_id"] == "ItemSelection":
            Self.FacilitySelected:ProductionFacility = Self.Player.ProductionFacilities[Interaction.data["values"][0]]
            Self.FacilitiesSelect.placeholder = Interaction.data["values"][0]
            Self.EmbedFrame.clear_fields()
            try: # This is fucking stupid. There has to be a better way I don't know about
                Self.FacilityUpgradeButton
            except AttributeError:
                Self.FacilityUpgradeButton = Button(label="Upgrade", style=ButtonStyle, custom_id="FacilityUpgradeButton", row=1)
                Self.BaseViewFrame.add_item(Self.FacilityUpgradeButton)
                Self.FacilityUpgradeButton.callback = lambda SelectInteraction: Self._Construct_Panel(Ether, InitialContext, ButtonStyle, SelectInteraction, PlayPanel)
            FacilityInfoString = (f"Level: {format(Self.FacilitySelected.Level, ',')}\n"+
                                  f"Capacity: {format(Self.FacilitySelected.Capacity, ',')}\n"+
                                  f"Units Per Second: {format(Self.FacilitySelected.UnitsPerTick, ',')}\n"+
                                  f"Upgrade Cost: {format(Self.FacilitySelected.UpgradeCost, ',')}")
            await Self._Generate_Info(Ether, InitialContext, Exclusions=["Team", "Power"])
            Self.EmbedFrame.add_field(name=f"{Self.FacilitySelected.Name} Info", value=FacilityInfoString)
        else:
            Self.FacilitiesSelected = None
            Self.BaseViewFrame = View(timeout=144000)
            Self.EmbedFrame = Embed(title=f"{InitialContext.author.name}'s Facilities Panel")

            Self.CollectProductionButton = Button(label="Collect Production", style=ButtonStyle, custom_id="CollectProductionButton")
            Self.CollectProductionButton.callback = lambda ButtonInteraction: Self._Collect_Production_Facilities(Ether, InitialContext, ButtonStyle, ButtonInteraction)
            Self.BaseViewFrame.add_item(Self.CollectProductionButton)

            Self.HomepageButton = Button(label="Home", style=DiscordButtonStyle.grey, row=3, custom_id="HomePageButton")
            # This is a bad callback. This is really bad, I'm well aware. But you know what, fuck it.
            Self.HomepageButton.callback = lambda ButtonInteraction: PlayPanel._Construct_Home(Ether, InitialContext, ButtonInteraction)
            Self.BaseViewFrame.add_item(Self.HomepageButton)

            Self.Options = [SelectOption(label=Name) for Name, Building in Self.Player.ProductionFacilities.items() if Building != "None"]
            Self.FacilitiesSelect = Select(options=Self.Options, custom_id=f"ItemSelection", row=2)
            Self.FacilitiesSelect.callback = lambda SelectInteraction: Self._Construct_Panel(Ether, InitialContext, ButtonStyle, SelectInteraction, PlayPanel)
            Self.BaseViewFrame.add_item(Self.FacilitiesSelect)

            await Self._Generate_Info(Ether, InitialContext, Exclusions=["Team", "Power"])

        Ether.Logger.info(f"Sent Facilities panel to {Self.Player}")
        await Self._Send_New_Panel(Interaction)


    async def _Collect_Production_Facilities(Self, Ether:RealmOfConflict, InitialContext:DiscordContext, ButtonStyle, Interaction:DiscordInteraction):
        if Interaction.user != InitialContext.author:
            return
        CollectionString = ""
        ProductionFacilityLength:int = len(Self.Player.ProductionFacilities.values()) - 1
        CollectionTime = int(Time())
        Index:int
        Facility:ProductionFacility
        for Index, Facility in enumerate(Self.Player.ProductionFacilities.values()):
            if Self.Player.Data["Time of Last Production Collection"] == "Never":
                EarnedAmount = round((Facility.UnitsPerTick * (CollectionTime - Self.Player.Data["Join TimeStamp"])) , 2)
                SkillBonus = ((Self.Player.Skills["Production"] + 1) * (5 * EarnedAmount)/100)
                print(SkillBonus)
            else:
                EarnedAmount = round(Facility.UnitsPerTick * (CollectionTime - Self.Player.Data["Time of Last Production Collection"]), 2)
                SkillBonus = ((Self.Player.Skills["Production"] + 1) * (5 * EarnedAmount)/100)
                print(SkillBonus)

            if Index == ProductionFacilityLength:
                CollectionString += f"{EarnedAmount} {Facility.OutputItem}"
            else:
                CollectionString += f"{EarnedAmount} {Facility.OutputItem}\n"

            Self.Player.Inventory[Facility.OutputItem] = round(Self.Player.Inventory[Facility.OutputItem] + EarnedAmount, 2)
        
        Self.Player.Data["Time of Last Production Collection"] = CollectionTime

        Self.EmbedFrame.clear_fields()

        await Self._Generate_Info(Ether, InitialContext, Exclusions=["Team", "Power"])

        Self.EmbedFrame.add_field(name="Collected:", value=CollectionString)

        await Self._Send_New_Panel(Interaction)