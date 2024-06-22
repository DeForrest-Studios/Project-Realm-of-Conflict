from RealmOfConflict import RealmOfConflict
from discord.ext.commands import Context as DiscordContext
from discord import Interaction as DiscordInteraction
from discord import ButtonStyle as DiscordButtonStyle
from discord import SelectOption
from discord.ui import Select, Button
from Panels.Panel import Panel
from Structures import ProductionFacility
from time import time as Time
from discord import Embed
from discord.ui import View

class ProductionFacilitiesPanel(Panel):
    def __init__(Self, Ether:RealmOfConflict, InitialContext:DiscordContext, ButtonStyle, Interaction:DiscordInteraction, PlayPanel, Emoji):
        super().__init__(Ether, InitialContext,
                         PlayPanel, "Production",
                         Interaction=Interaction, ButtonStyle=ButtonStyle, Emoji=Emoji)

    async def _Construct_Panel(Self, Interaction:DiscordInteraction=None, FacilitySelected=None, FacilityUpgraded=False):
        if Self.Interaction.user.id in Self.Ether.Whitelist: pass
        elif Self.Interaction.user != Self.InitialContext.author: return
        
        Self.BaseViewFrame = View(timeout=144000)
        Self.PanelTitle = f"{Self.Player.Data['Name']}'s Production Panel"
        Self.EmbedFrame = Embed(title=Self.Emoji*2 + Self.PanelTitle + Self.Emoji*2)

        # if Interaction is not None:
        #     await Self._Generate_Info(Self.Ether, Self.InitialContext, Exclusions=["Team", "Power"])
        #     Self.Ether.Logger.info(f"Sent Facilities panel to {Self.Player}")
        #     await Self._Send_New_Panel(Interaction)


        if FacilityUpgraded == True:
            if Self.Player.Data['Wallet'] < Self.FacilitySelected.Data['Upgrade Cost']:
                Self.EmbedFrame.clear_fields()
                FacilityInfoString = (f"Level: {Self.FacilitySelected.Data['Level']}\n"+
                                    f"Capacity: {Self.FacilitySelected.Data['Capacity']}\n"+
                                    f"Units Per Second: {Self.FacilitySelected.Data['Units Per Tick']}\n"+
                                    f"Upgrade Cost: {Self.FacilitySelected.Data['Upgrade Cost']}")
                await Self._Generate_Info(Self.Ether, Self.InitialContext, Exclusions=["Team", "Power"])
                Self.EmbedFrame.add_field(name=f"{Self.FacilitySelected.Data['Name']} Info", value=FacilityInfoString)
                Self.EmbedFrame.add_field(name="Insufficient Funds", value="\u200b", inline=False)
                await Self._Send_New_Panel(Interaction)
            else:
                Self.Player.Data['Wallet'] = round(Self.Player.Data['Wallet'] - Self.FacilitySelected.Data['Upgrade Cost'], 2)
                Self.FacilitySelected.Upgrade()
                Self.EmbedFrame.clear_fields()
                FacilityInfoString = (f"Level: {format(Self.FacilitySelected.Data['Level'], ',')}\n"+
                                      f"Capacity: {format(Self.FacilitySelected.Data['Capacity'], ',')}\n"+
                                      f"Units Per Second: {format(Self.FacilitySelected.Data['Units Per Tick'], ',')}\n"+
                                      f"Upgrade Cost: {format(Self.FacilitySelected.Data['Upgrade Cost'], ',')}")
                await Self._Generate_Info(Self.Ether, Self.InitialContext, Exclusions=["Team", "Power"])
                Self.EmbedFrame.add_field(name=f"{Self.FacilitySelected.Data['Name']} Info", value=FacilityInfoString)
                await Self._Send_New_Panel(Interaction)
        elif FacilitySelected is not None:
            Self.FacilitySelected:ProductionFacility = Self.Player.ProductionFacilities[FacilitySelected]
            Self.FacilitiesSelect.placeholder = FacilitySelected
            Self.EmbedFrame.clear_fields()

            try:
                Self.FacilityUpgradeButton
            except AttributeError:
                Self.FacilityUpgradeButton = Button(label="Upgrade", style=Self.ButtonStyle, custom_id="FacilityUpgradeButton", row=1)
                Self.BaseViewFrame.add_item(Self.FacilityUpgradeButton)
                Self.FacilityUpgradeButton.callback = lambda SelectInteraction: Self._Construct_Panel(Interaction=SelectInteraction, FacilityUpgraded=True)

            await Self._Generate_Info(Self.Ether, Self.InitialContext, Exclusions=["Team", "Power"])

            FacilityInfoString = (f"Level: {format(Self.FacilitySelected.Data['Level'], ',')}\n"+
                                  f"Capacity: {format(Self.FacilitySelected.Data['Capacity'], ',')}\n"+
                                  f"Units Per Second: {format(Self.FacilitySelected.Data['Units Per Tick'], ',')}\n"+
                                  f"Upgrade Cost: {format(Self.FacilitySelected.Data['Upgrade Cost'], ',')}")
            Self.EmbedFrame.add_field(name=f"{Self.FacilitySelected.Data['Name']} Info", value=FacilityInfoString)
            await Self._Send_New_Panel(Interaction)
        else:
            await Self._Generate_Info(Self.Ether, Self.InitialContext, Exclusions=["Team", "Power"])
            Self.FacilitiesSelected = None
            Self.CollectProductionButton = Button(label="Collect Production", style=Self.ButtonStyle, custom_id="CollectProductionButton")
            Self.CollectProductionButton.callback = lambda ButtonInteraction: Self._Collect_Production_Facilities(ButtonInteraction)
            Self.BaseViewFrame.add_item(Self.CollectProductionButton)

            Self.HomepageButton = Button(label="Home", style=DiscordButtonStyle.grey, row=3, custom_id="HomePageButton")
            Self.HomepageButton.callback = lambda ButtonInteraction: Self.PlayPanel._Construct_Home(Self.Ether, Self.InitialContext, ButtonInteraction)
            Self.BaseViewFrame.add_item(Self.HomepageButton)

            Self.Options = [SelectOption(label=Name) for Name, Building in Self.Player.ProductionFacilities.items() if Building != "None"]
            Self.FacilitiesSelect = Select(options=Self.Options, custom_id=f"ItemSelection", row=2)
            Self.FacilitiesSelect.callback = lambda SelectInteraction: Self._Construct_Panel(FacilitySelected=SelectInteraction.data["values"][0], Interaction=SelectInteraction)
            Self.BaseViewFrame.add_item(Self.FacilitiesSelect)

            await Self._Generate_Info(Self.Ether, Self.InitialContext, Exclusions=["Team", "Power"])
            await Self._Send_New_Panel(Self.Interaction)

        Self.Ether.Logger.info(f"Sent Facilities panel to {Self.Player}")


    async def _Collect_Production_Facilities(Self, Interaction:DiscordInteraction):
        if Interaction.user.id in Self.Ether.Whitelist: pass
        elif Interaction.user != Self.InitialContext.author: return
        CollectionString = ""
        ProductionFacilityLength:int = len(Self.Player.ProductionFacilities.values()) - 1
        
        CollectionTime = int(Time())

        Index:int
        Facility:ProductionFacility
        for Index, Facility in enumerate(Self.Player.ProductionFacilities.values()):
            print(Facility, " ", Facility.Data["Time of Last Collect"])
            if Facility.Data["Time of Last Collect"] == "Never":
                EarnedAmount = round((Facility.Data['Units Per Tick'] * (CollectionTime - Self.Player.Data["Join TimeStamp"])) , 2)
            else:
                EarnedAmount = round(Facility.Data['Units Per Tick'] * (CollectionTime - Facility.Data["Time of Last Collect"]), 2)

            if Index == ProductionFacilityLength:
                CollectionString += f"{EarnedAmount} {Facility.Data['Output']}"
            else:
                CollectionString += f"{EarnedAmount} {Facility.Data['Output']}\n"

            SkillBonus = ((Self.Player.Skills["Production"] + 1) * (5 * EarnedAmount)/100)
            EarnedAmount = round(EarnedAmount + SkillBonus, 2)
            Self.Player.Inventory[Facility.Data['Output']] = round(Self.Player.Inventory[Facility.Data['Output']] + EarnedAmount, 2)
            Facility.Data["Time of Last Collect"] = CollectionTime

        Self.EmbedFrame.clear_fields()

        await Self._Generate_Info(Self.Ether, Self.InitialContext, Exclusions=["Team", "Power"])

        Self.EmbedFrame.add_field(name="Collected:", value=CollectionString)

        Self.Ether.Logger.info(f"{Self.Player} collected from production facilities")
        await Self._Send_New_Panel(Interaction)