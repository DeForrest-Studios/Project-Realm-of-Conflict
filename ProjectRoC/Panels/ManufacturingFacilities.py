from RealmOfConflict import RealmOfConflict
from discord.ext.commands import Context as DiscordContext
from discord import Interaction as DiscordInteraction
from discord import ButtonStyle as DiscordButtonStyle
from discord import SelectOption, Embed
from discord.ui import Button, Select, View
from Panels.Panel import Panel
from Structures import ManufacturingFacility

class ManufacturingFacilitiesPanel(Panel):
    def __init__(Self, Ether:RealmOfConflict, InitialContext:DiscordContext, ButtonStyle, Interaction:DiscordInteraction, PlayPanel):
        super().__init__(Ether, InitialContext,
                         PlayPanel, "Manufacturing Facilities",
                         Interaction=Interaction, ButtonStyle=ButtonStyle)

    async def _Construct_Panel(Self, Interaction=None, FacilitySelected=None,
                               GroupSelected=None, BoughtFacility=False,
                               BoughtLandPlot=False):
        if Self.Interaction.user != Self.InitialContext.author: return

        if Interaction is not None:
            Self.BaseViewFrame = View(timeout=144000)
            Self.EmbedFrame = Embed(title=f"{Self.Player.Data['Name']}'s Manufacturing Facilities Panel")
            Self.Interaction = Interaction

        await Self._Generate_Info(Self.Ether, Self.InitialContext)
        Self.BuyFacility = Button(label="Buy Facility ~ $35,000", style=Self.ButtonStyle, row=0, custom_id="BuyFacilityButton")
        Self.BuyFacility.callback = lambda Interaction: Self._Construct_Panel(Interaction, BoughtFacility=True)
        Self.BaseViewFrame.add_item(Self.BuyFacility)

        Self.BuyLandPlot = Button(label="Buy Land Plot ~ $1,750,000", style=Self.ButtonStyle, row=0, custom_id="BuyLandPlotButton")
        Self.BuyLandPlot.callback = lambda Interaction: Self._Construct_Panel(Interaction, BoughtLandPlot=True)
        Self.BaseViewFrame.add_item(Self.BuyLandPlot)

        if BoughtFacility:
            if Self.Player.Data["Wallet"] >= 35000:
                Self.EmbedFrame.description += "Bought a facility"
                Self.Player.Data["Wallet"] = round(Self.Player.Data["Wallet"] - 35000, 2)
                Self.Player.ManufacturingFacilities.update({f"Facility {len(Self.Player.ManufacturingFacilities)}":ManufacturingFacility(f"Facility {len(Self.Player.ManufacturingFacilities)}")})
            else:
                Self.EmbedFrame.description += "Insufficient Funds"

        if BoughtLandPlot:
            if Self.Player.Data["Wallet"] >= 1750000:
                Self.EmbedFrame.description += "Bought a facility"
                Self.Player.Data["Wallet"] = round(Self.Player.Data["Wallet"] - 1750000, 2)
                Self.Player.Data["Land Plots"] += 1
            else:
                Self.EmbedFrame.description += "Insufficient Funds"

        if GroupSelected is not None:
            Self.GroupSelected = GroupSelected
            Self.GroupSelection.placeholder = GroupSelected

        if FacilitySelected is not None:
            Self.FacilitySelected = FacilitySelected
            Self.FacilitySelection.placeholder = FacilitySelected
            Self.EmbedFrame.description += f"{Self.Player.ManufacturingFacilities[Self.FacilitySelected].Data['Name']}\n"
            Self.EmbedFrame.description += f"**Level:** {Self.Player.ManufacturingFacilities[Self.FacilitySelected].Data['Level']}\n"
            Self.EmbedFrame.description += f"**Recipe:** {Self.Player.ManufacturingFacilities[Self.FacilitySelected].Data['Recipe']}\n"

            Self.ChangeFacilityName = Button(label="Change Facility Name (WIP)", style=Self.ButtonStyle, row=1, custom_id="ChangeFacilityNameButton")
            if hasattr(Self, "GroupSelected"):
                Self.ChangeFacilityName.callback = lambda Interaction: Self._Send_Change_Name_Modal((Interaction, Self.GroupSelected, Self.FacilitySelected))
            else:
                Self.ChangeFacilityName.callback = lambda Interaction: Self._Send_Change_Name_Modal((Interaction, Self.FacilitySelected))
            Self.BaseViewFrame.add_item(Self.ChangeFacilityName)

        if Self.Player.Data["Land Plots"] > 1 or Interaction is not None and Self.Player.Data["Land Plots"] > 1:
            Self.GroupSelectionChoices = [SelectOption(label=str(Index)) for Index in Self.Player.Data["Land Plots"]]
            Self.GroupSelection = Select(placeholder="Select a Plot", options=Self.GroupSelectionChoices, row=2, custom_id=f"GroupSelection")
            Self.BaseViewFrame.add_item(Self.GroupSelection)
            Self.GroupSelection.callback = lambda SelectInteraction: Self._Construct_Panel(SelectInteraction, GroupSelected=SelectInteraction.data["values"][0])

        if len(Self.Player.ManufacturingFacilities) > 0 or Interaction is not None and len(Self.Player.ManufacturingFacilities) > 0:
            Self.FacilitySelectionChoices = [SelectOption(label=FacilityName) for FacilityName in Self.Player.ManufacturingFacilities.keys()]
            Self.FacilitySelection = Select(placeholder="Select a Facility", options=Self.FacilitySelectionChoices, row=3, custom_id=f"FacilitySelection")
            Self.BaseViewFrame.add_item(Self.FacilitySelection)
            Self.FacilitySelection.callback = lambda SelectInteraction: Self._Construct_Panel(SelectInteraction, FacilitySelected=SelectInteraction.data["values"][0])

        Self.HomepageButton = Button(label="Home", style=DiscordButtonStyle.grey, row=4, custom_id="HomePageButton")
        Self.HomepageButton.callback = lambda Interaction: Self.PlayPanel._Construct_Home(Self.Ether, Self.InitialContext, Interaction)
        Self.BaseViewFrame.add_item(Self.HomepageButton)

        Self.Ether.Logger.info(f"Sent Manufacturing Facilities panel to {Self.Player.Data['Name']}")
        await Self._Send_New_Panel(Self.Interaction)


    async def _Send_Change_Name_Modal(Self, Data):
        await Self._Construct_Panel(*Data)