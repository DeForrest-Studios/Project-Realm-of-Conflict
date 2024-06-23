from RealmOfConflict import RealmOfConflict
from discord.ext.commands import Context as DiscordContext
from discord import Interaction as DiscordInteraction
from discord import ButtonStyle as DiscordButtonStyle
from discord import SelectOption, Embed
from discord.ui import Button, Select, View, Modal, TextInput
from Panels.Panel import Panel
from Structures import ManufacturingFacility
from Tables import Components, FacilityMapping
from time import time as Time

class ManufacturingFacilitiesPanel(Panel):
    def __init__(Self, Ether:RealmOfConflict, InitialContext:DiscordContext, ButtonStyle, Interaction:DiscordInteraction, PlayPanel, Emoji):
        super().__init__(Ether, InitialContext,
                         PlayPanel, "Manufacturing Facilities",
                         Interaction=Interaction, ButtonStyle=ButtonStyle, Emoji=Emoji)
        Self.SelectedPlot = 1

    async def _Construct_Panel(Self, Interaction=None, FacilitySelected=None,
                               SelectedPlot=None, BoughtFacility=False,
                               BoughtLandPlot=False):
        if Self.Interaction.user.id in Self.Ether.Whitelist: pass
        elif Self.Interaction.user != Self.InitialContext.author: return

        Self.BaseViewFrame = View(timeout=144000)
        Self.PanelTitle = f"{Self.Player.Data['Name']}'s Manufacturing Panel"
        Self.EmbedFrame = Embed(title=Self.Emoji*2 + Self.PanelTitle + Self.Emoji*2)

        if Interaction is not None:
            Self.Interaction = Interaction

        await Self._Generate_Info(Self.Ether, Self.InitialContext)
        Self.CollectButton = Button(label="Collect from Facilities", style=Self.ButtonStyle, row=0, custom_id="CollectButton")
        Self.CollectButton.callback = lambda Interaction: Self._Collect(Interaction)
        Self.BaseViewFrame.add_item(Self.CollectButton)

        Self.BuyFacilityButton = Button(label="Buy Facility ~ $35,000", style=Self.ButtonStyle, row=0, custom_id="BuyFacilityButton")
        Self.BuyFacilityButton.callback = lambda Interaction: Self._Construct_Panel(Interaction, BoughtFacility=True)
        Self.BaseViewFrame.add_item(Self.BuyFacilityButton)

        Self.BuyLandPlotButton = Button(label="Buy Land Plot ~ $1,750,000", style=Self.ButtonStyle, row=0, custom_id="BuyLandPlotButton")
        Self.BuyLandPlotButton.callback = lambda Interaction: Self._Construct_Panel(Interaction, BoughtLandPlot=True)
        Self.BaseViewFrame.add_item(Self.BuyLandPlotButton)

        if BoughtFacility:
            if len(Self.Player.ManufacturingFacilities.values()) + 1 > Self.Player.Data["Land Plots"] * 5:
                Self.EmbedFrame.description += f"**Not Enough Land Plots**\n"
                pass
            elif Self.Player.Data["Wallet"] >= 35000:
                Self.EmbedFrame.description += "Bought a facility"
                Self.Player.Data["Wallet"] = round(Self.Player.Data["Wallet"] - 35000, 2)
                Self.Player.ManufacturingFacilities.update({f"Facility {len(Self.Player.ManufacturingFacilities)}":ManufacturingFacility(f"Facility {len(Self.Player.ManufacturingFacilities)}")})
            else:
                Self.EmbedFrame.description += "Insufficient Funds"

        if BoughtLandPlot:
            if Self.Player.Data["Land Plots"] + 1 > 10:
                Self.EmbedFrame.description += f"**You have the maximum land plots allowed of 10**\n"
                pass
            elif Self.Player.Data["Wallet"] >= 1750000:
                Self.EmbedFrame.description += "Bought a land plot"
                Self.Player.Data["Wallet"] = round(Self.Player.Data["Wallet"] - 1750000, 2)
                Self.Player.Data["Land Plots"] += 1
            else:
                Self.EmbedFrame.description += "Insufficient Funds"

        if FacilitySelected is not None:
            Self.FacilitySelected = FacilitySelected
            Self.FacilitySelection.placeholder = FacilitySelected
            Self.EmbedFrame.description += f"**{Self.Player.ManufacturingFacilities[Self.FacilitySelected].Data['Name']}**\n"
            Self.EmbedFrame.description += f"**Level:** {Self.Player.ManufacturingFacilities[Self.FacilitySelected].Data['Level']}\n"
            Self.EmbedFrame.description += f"**Recipe:** {Self.Player.ManufacturingFacilities[Self.FacilitySelected].Data['Recipe']}\n"

            Self.EditFacilityButton = Button(label=f"Edit Facility", style=Self.ButtonStyle, row=0, custom_id="EditFacilityButton")
            Self.EditFacilityButton.callback = lambda Interaction: Self._Construct_Edit_Panel(Interaction)
            Self.BaseViewFrame.add_item(Self.EditFacilityButton)

        if SelectedPlot != None: Self.SelectedPlot = SelectedPlot

        if Self.Player.Data["Land Plots"] > 1 or Interaction is not None and Self.Player.Data["Land Plots"] > 1:
            Self.PlotSelectionChoices = [SelectOption(label=str(Index)) for Index in range(1, (Self.Player.Data["Land Plots"] + 1))]
            Self.PlotSelection = Select(placeholder=f"{Self.SelectedPlot}", options=Self.PlotSelectionChoices, row=2, custom_id=f"PlotSelection")
            Self.BaseViewFrame.add_item(Self.PlotSelection)
            Self.PlotSelection.callback = lambda SelectInteraction: Self._Construct_Panel(SelectInteraction, SelectedPlot=int(SelectInteraction.data["values"][0]))

        if len(Self.Player.ManufacturingFacilities) > 0 or Interaction is not None and len(Self.Player.ManufacturingFacilities) > 0:
            Self.ManufacturingFacilitiesByPlot = []
            Self.CopyOfManufacturingFacilities = [FacilityName for FacilityName in Self.Player.ManufacturingFacilities.keys()]
            Divider = len(Self.CopyOfManufacturingFacilities)/5
            if Divider < 1: Divider = 1
            if len(Self.CopyOfManufacturingFacilities) % Divider != 0: Divider = int(Divider) + 1
            else: Divider = int(Divider)
            for _ in range(1, (Divider + 1)):
                Self.ManufacturingFacilitiesByPlot.append([Facility for Facility in Self.CopyOfManufacturingFacilities[:5]])
                Self.CopyOfManufacturingFacilities = Self.CopyOfManufacturingFacilities[5:]

            Self.FacilitySelectionChoices = [SelectOption(label=FacilityName) for FacilityName in Self.ManufacturingFacilitiesByPlot[Self.SelectedPlot-1]]
            Self.FacilitySelection = Select(placeholder="Select a Facility", options=Self.FacilitySelectionChoices, row=3, custom_id=f"FacilitySelection")
            Self.BaseViewFrame.add_item(Self.FacilitySelection)
            Self.FacilitySelection.callback = lambda SelectInteraction: Self._Construct_Panel(SelectInteraction, FacilitySelected=SelectInteraction.data["values"][0])

        Self.HomepageButton = Button(label="Home", style=DiscordButtonStyle.grey, row=4, custom_id="HomePageButton")
        Self.HomepageButton.callback = lambda Interaction: Self.PlayPanel._Construct_Home(Self.Ether, Self.InitialContext, Interaction)
        Self.BaseViewFrame.add_item(Self.HomepageButton)

        Self.Ether.Logger.info(f"Sent Manufacturing Facilities panel to {Self.Player.Data['Name']}")
        await Self._Send_New_Panel(Self.Interaction)

    async def _Construct_Edit_Panel(Self, Interaction=None):
        if type(Interaction) == tuple:
            if len(Interaction) == 2:
                Data = Interaction
                Interaction = Data[0]

        if Self.Interaction.user.id in Self.Ether.Whitelist: pass
        elif Self.Interaction.user != Self.InitialContext.author: return

        if Interaction is not None:
            Self.BaseViewFrame = View(timeout=144000)
            Self.EmbedFrame = Embed(title=f"{Self.Player.Data['Name']}'s Manufacturing Facilities Panel")
            Self.Interaction = Interaction

        await Self._Generate_Info(Self.Ether, Self.InitialContext)
        Self.CollectButton = Button(label="Collect from Facilities", style=Self.ButtonStyle, row=0, custom_id="CollectButton")
        Self.CollectButton.callback = lambda Interaction: Self._Construct_Panel(Interaction)
        Self.BaseViewFrame.add_item(Self.CollectButton)

        Self.EmbedFrame.description += f"**{Self.Player.ManufacturingFacilities[Self.FacilitySelected].Data['Name']}**\n"
        Self.EmbedFrame.description += f"**Level:** {Self.Player.ManufacturingFacilities[Self.FacilitySelected].Data['Level']}\n"
        Self.EmbedFrame.description += f"**Recipe:** {Self.Player.ManufacturingFacilities[Self.FacilitySelected].Data['Recipe']}\n"
        
        Self.FacilityRecipeChoices = [SelectOption(label=Component) for Component in Components]
        Self.FacilityRecipeSelection = Select(placeholder="Select a Recipe", options=Self.FacilityRecipeChoices, row=1, custom_id=f"FacilityRecipeSelection")
        if Self.Player.ManufacturingFacilities[Self.FacilitySelected].Data["Recipe"] != None:
            Self.FacilityRecipeSelection.placeholder = Self.Player.ManufacturingFacilities[Self.FacilitySelected].Data["Recipe"]
        Self.FacilityRecipeSelection.callback = lambda SelectInteraction: Self._Change_Recipe(SelectInteraction, SelectInteraction.data["values"][0])
        Self.BaseViewFrame.add_item(Self.FacilityRecipeSelection)

        Self.FacilityPriorityLevels = [SelectOption(label=f"Priority {Level}") for Level in range(1, 21)]
        Self.FacilityPrioritySelection = Select(placeholder="Priority 1", options=Self.FacilityPriorityLevels, row=2, custom_id=f"FacilityPrioritySelection")
        Self.FacilityPrioritySelection.placeholder = f"Priority {Self.Player.ManufacturingFacilities[Self.FacilitySelected].Data['Priority']}"
        Self.FacilityPrioritySelection.callback = lambda SelectInteraction: Self._Change_Priority(SelectInteraction, int(SelectInteraction.data["values"][0].split(" ")[1]))
        Self.BaseViewFrame.add_item(Self.FacilityPrioritySelection)

        Self.ChangeFacilityNameButton = Button(label="Change Facility Name", style=Self.ButtonStyle, row=0, custom_id="ChangeFacilityNameButton")
        Self.ChangeFacilityNameButton.callback = lambda Interaction: Self._Send_Change_Name_Modal((Interaction, Self.FacilitySelected))
        Self.BaseViewFrame.add_item(Self.ChangeFacilityNameButton)

        Self.UpgradeFacilityButton = Button(label=f"Upgrade Facility for {Self.Player.ManufacturingFacilities[Self.FacilitySelected].Data['Upgrade Cost']:,}", style=Self.ButtonStyle, row=0, custom_id="UpgradeFacilityButton")
        Self.UpgradeFacilityButton.callback = lambda Interaction: Self._Construct_Panel(Interaction)
        Self.BaseViewFrame.add_item(Self.UpgradeFacilityButton)

        Self.ManufacturingFacilitiesButton = Button(label="Manufacturing Facilities", style=Self.ButtonStyle, row=4, custom_id="ManufacturingFacilitiesButton")
        Self.ManufacturingFacilitiesButton.callback = lambda Interaction: Self._Construct_Panel(Interaction, Self.FacilitySelected)
        Self.BaseViewFrame.add_item(Self.ManufacturingFacilitiesButton)

        Self.HomepageButton = Button(label="Home", style=DiscordButtonStyle.grey, row=4, custom_id="HomePageButton")
        Self.HomepageButton.callback = lambda Interaction: Self.PlayPanel._Construct_Home(Self.Ether, Self.InitialContext, Interaction)
        Self.BaseViewFrame.add_item(Self.HomepageButton)

        Self.Ether.Logger.info(f"Sent Manufacturing Facilities panel to {Self.Player.Data['Name']}")
        await Self._Send_New_Panel(Self.Interaction)

    async def _Send_Change_Name_Modal(Self, Data):
        Interaction = Data[0]
        if Interaction.user.id in Self.Ether.Whitelist: pass
        elif Interaction.user != Self.InitialContext.author: return
        Self.ChangeFacilityNameModal = Modal(title="Change Facility Name")
        Self.ChangeFacilityNameModal.on_submit = lambda ButtonInteraction: Self._Change_Facility_Name((ButtonInteraction,) + Data[1::])

        Self.FacilityName = TextInput(label="Enter new facility name:")
        Self.ChangeFacilityNameModal.add_item(Self.FacilityName)
        await Interaction.response.send_modal(Self.ChangeFacilityNameModal)

    
    async def _Change_Facility_Name(Self, Data, PlotSelected=None):
        Interaction, FacilitySelected = Data[0], Data[1]
        Self.Player.ManufacturingFacilities[Self.FacilityName.value] = Self.Player.ManufacturingFacilities[FacilitySelected]
        Self.Player.ManufacturingFacilities.pop(FacilitySelected)
        FacilitySelected = Self.FacilityName.value
        Self.Player.ManufacturingFacilities[FacilitySelected].Data["Name"] = FacilitySelected

        await Self._Construct_Panel(Interaction=Interaction, FacilitySelected=FacilitySelected)


    async def _Change_Recipe(Self, Interaction, ComponentSelected):
        Self.Player.ManufacturingFacilities[Self.FacilitySelected].Data["Recipe"] = ComponentSelected
        await Self._Construct_Edit_Panel(Interaction)


    async def _Change_Priority(Self, Interaction, PrioritySelected):
        Self.Player.ManufacturingFacilities[Self.FacilitySelected].Data["Priority"] = PrioritySelected
        await Self._Construct_Edit_Panel(Interaction)


    async def _Collect(Self, Interaction):
        if Interaction.user.id in Self.Ether.Whitelist: pass
        elif Interaction.user != Self.InitialContext.author: return

        # We're going to need to give each structure their own "Time of Last Production Collection" attribute that can be individually checked
        # This means that I'll have to use the same DataDict approach that I did with the manufacturing facilities
        # Production outputs will "trickle" down the priorities

        # the trickle down
        #
        # first we'll have to determine which production facilities need to be pulled from
        # Then we'll gather the production amounts from each of them, and make a dictionary of all the production amounts with their respective item, and amount
        # Then we'll iterate through each priority level, and within them each manufacturing facility, and determine if they can pull from production
        # If it's a component that is required for the recipe, 

        CollectionString = ""
        CollectionTime = int(Time())
        if Self.Player.Data["Time of Last Manufacturing Collection"] == "Never": Self.Player.Data["Time of Last Manufacturing Collection"] = CollectionTime

        # Pool facilities into their proper priorities
        PriorityLevels = {Level:[] for Level in range(1, 21)}
        for Facility in Self.Player.ManufacturingFacilities.values(): PriorityLevels[Facility.Data["Priority"]].append(Facility)

        # Get Production Requirements
        ProductionRequirements = []
        for Facility in Self.Player.ManufacturingFacilities.values():
            if Facility.Data["Recipe"] not in [None, "None"]:
                Recipe = Facility.Data["Recipe"]
                RecipeRequirements = Components[Recipe]
                for Item in RecipeRequirements.keys():
                    ProductionRequirements.append(Item)

        ProductionCollections = {}
        # Production Pool Gathering
        for Facility in Self.Player.ProductionFacilities.values():
            if Facility.Data["Output"] in ProductionRequirements:
                if Facility.Data["Time of Last Collect"] == "Never":
                    ProductionAmount = round((Facility.Data['Units Per Tick'] * (CollectionTime - Self.Player.Data["Join TimeStamp"])) , 2)
                else:
                    ProductionAmount = round(Facility.Data['Units Per Tick'] * (CollectionTime - Facility.Data["Time of Last Collect"]), 2)
                Facility.Data["Time of Last Collect"] = CollectionTime
                ProductionCollections.update({Facility.Data["Name"]:ProductionAmount})

        # Actual Collection
        for FacilityPool in PriorityLevels.values():
            for Facility in FacilityPool:
                OutputItem = Facility.Data["Recipe"]

                if Self.Player.Data["Time of Last Manufacturing Collection"] == "Never":
                    ManufacturingPotential = round((Facility.Data["Units Per Tick"] * (CollectionTime - Self.Player.Data["Join TimeStamp"])) , 2)
                else:
                    ManufacturingPotential = round(Facility.Data["Units Per Tick"] * (CollectionTime - Self.Player.Data["Time of Last Manufacturing Collection"]), 2)
                
                if Facility.Data["Recipe"] not in [None, "None"]:
                    RecipeRequirements = Components[OutputItem]
                    if len(RecipeRequirements) == 1:
                        RecipeRequirements = [(Item, Amount) for Item, Amount in Components[OutputItem].items()][0]
                        CraftingAmountRequirement = RecipeRequirements[1]
                        ActualPotential = ManufacturingPotential * CraftingAmountRequirement
                        if ManufacturingPotential < ActualPotential:
                            Self.Player.Inventory[OutputItem] = round(Self.Player.Inventory[OutputItem] + ActualPotential, 2)
                            CollectionString += f"{Facility.Data['Name']} output {ActualPotential} {OutputItem}"
                            ProductionCollections[FacilityMapping[OutputItem]] = round(ProductionCollections[FacilityMapping[OutputItem]] - ActualPotential, 2)
                        else:
                            Self.Player.Inventory[OutputItem] = round(Self.Player.Inventory[OutputItem] + ManufacturingPotential, 2)
                            CollectionString += f"{Facility.Data['Name']} output {ManufacturingPotential} {OutputItem}"
                            ProductionCollections[FacilityMapping[OutputItem]] = round(ProductionCollections[FacilityMapping[OutputItem]] - ManufacturingPotential, 2)

        # Give to player any production left over

        Self.Player.Data["Time of Last Manufacturing Collection"] = CollectionTime
        
        Self.EmbedFrame.clear_fields()

        await Self._Generate_Info(Self.Ether, Self.InitialContext, Exclusions=["Team", "Power"])

        Self.EmbedFrame.add_field(name="You've manufactured:", value=CollectionString)

        Self.Ether.Logger.info(f"{Self.Player} collected from manufacturing facilities")
        await Self._Send_New_Panel(Interaction)

        # Minus from production
        # Apply to Manufacturing
        # Get Manufacturing Output