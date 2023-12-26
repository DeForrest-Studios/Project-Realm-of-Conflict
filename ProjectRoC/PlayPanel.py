from asyncio import create_task
from discord import ButtonStyle, Embed, SelectOption, Interaction, InteractionMessage
from discord.ext.commands import Context
from discord.ui import View, Button, Select, Modal, TextInput
from RealmOfConflict import RealmOfConflict
from LootTables import ScavengeTable, MaterialTable
from random import randrange
from time import time
from Player import Player
from os import remove
from os.path import join
from Facilities import ProductionFacility

class PlayPanel:
    def __init__(Self, Ether:RealmOfConflict, PlayerContext:Context):
        Self.Ether = None
        Self.InitialContext = None
        create_task(Self._Construct_Home(Ether, PlayerContext))


    async def _Send_New_Panel(Self, Interaction: Interaction):
        await Interaction.response.edit_message(embed=Self.EmbedFrame, view=Self.BaseViewFrame)


    async def _Determine_Team(Self):
        if "Titan" in str(Self.InitialContext.author.roles):
            Self.ButtonStyle = ButtonStyle.red
        elif "Analis" in str(Self.InitialContext.author.roles):
            Self.ButtonStyle = ButtonStyle.blurple
        else:
            Self.ButtonStyle = ButtonStyle.grey


    async def _Generate_Info(Self, Exclusions:list=[]):
        Fields = [Field for Field in ["Wallet", "Team", "Level", "Experience", "Power"] if Field not in Exclusions]

        Info = ""

        for Name, Value in Self.Player.Data.items():
            if Name in Fields:
                if Name == 'Wallet':
                    Info +=f"**{Name}** ~ ${format(float(Value), ',')}\n"
                elif type(Value) == float:
                    Info +=f"**{Name}** ~ {format(float(Value), ',')}\n"
                elif type(Value) == int:
                    Info +=f"**{Name}** ~ {format(int(Value), ',')}\n"
                else:
                    Info +=f"**{Name}** ~ {Value}\n"

        Self.EmbedFrame.insert_field_at(0, name="\u200b", value=Info, inline=False)


    async def _Determine_Whitelist(Self):
        if Self.InitialContext.author.id in Self.Whitelist:
            Self.EmbedFrame.title = Self.EmbedFrame.title + " (Developer)"


    async def _Construct_Home(Self, Ether:RealmOfConflict=None, InitialContext:Context=None, Interaction=None):
        if Self.Ether:
            Ether = Self.Ether
        if Self.InitialContext:
            InitialContext = Self.InitialContext

        Self.InitialContext:Context = InitialContext
        Self.Ether:RealmOfConflict = Ether
        Self.Whitelist = [897410636819083304, # Robert Reynolds, Cavan
                          ]
        Self.Player: Player = Ether.Data["Players"][InitialContext.author.id]
        Self.FacilitySelected = None
        await Self._Determine_Team()

        if Self.Player.Data["Experience"] >= Self.Player.ExperienceForNextLevel:
            Self.Player.Data["Level"] += 1
            Self.Player.Refresh_Stats()

        Self.BaseViewFrame = View(timeout=144000)
        Self.EmbedFrame = Embed(title=f"{Self.Player.Data['Name']}'s Home Panel")

        await Self._Generate_Info()

        Self.ScavengeButton = Button(label="Scavenge", style=Self.ButtonStyle, custom_id="ScavengeButton")
        Self.ScavengeButton.callback = Self._Scavenge
        Self.BaseViewFrame.add_item(Self.ScavengeButton)

        Self.FacilitiesButton = Button(label="Facilities", style=Self.ButtonStyle, custom_id="FacilitiesButton")
        Self.FacilitiesButton.callback = Self._Construct_Facilities_Panel
        Self.BaseViewFrame.add_item(Self.FacilitiesButton)

        Self.AvargoButton = Button(label="Avargo", style=Self.ButtonStyle, custom_id="AvargoButton")
        Self.AvargoButton.callback = Self._Construct_Avargo_Panel
        Self.BaseViewFrame.add_item(Self.AvargoButton)

        Self.InventoryButton = Button(label="Inventory", style=Self.ButtonStyle, custom_id="InventoryButton")
        Self.InventoryButton.callback = Self._Construct_Inventory_Panel
        Self.BaseViewFrame.add_item(Self.InventoryButton)

        if InitialContext.author.id in Self.Whitelist:
            Self.DebugButton = Button(label="Debug", style=ButtonStyle.grey, row=3)
            Self.DebugButton.callback = Self._Construct_Debug_Panel
            Self.BaseViewFrame.add_item(Self.DebugButton)

        await Self._Determine_Whitelist()
        if Interaction:
            await Self._Send_New_Panel(Interaction)
        else:
            Self.DashboardMessage = await Self.InitialContext.send(embed=Self.EmbedFrame, view=Self.BaseViewFrame)


    async def _Construct_Avargo_Panel(Self, Interaction:Interaction):
        Self.BaseViewFrame = View(timeout=144000)
        Self.EmbedFrame = Embed(title=f"{Self.Player.Data['Name']}'s Avargo Panel")

        await Self._Generate_Info()

        Self.BuyButton = Button(label="Buy", style=Self.ButtonStyle, custom_id="BuyButton")
        Self.BuyButton.callback = Self._Avargo_Sale
        Self.BaseViewFrame.add_item(Self.BuyButton)

        Self.SellButton = Button(label="Sell", style=Self.ButtonStyle, custom_id="SellButton")
        Self.SellButton.callback = Self._Avargo_Sale
        Self.BaseViewFrame.add_item(Self.SellButton)

        Self.HomepageButton = Button(label="Home", style=ButtonStyle.grey, row=3, custom_id="HomePageButton")
        Self.HomepageButton.callback = lambda Interaction: Self._Construct_Home(Interaction)
        Self.BaseViewFrame.add_item(Self.HomepageButton)

        await Self._Send_New_Panel(Interaction)



    async def _Avargo_Sale(Self, Interaction:Interaction):
        async def _Select_Material(Interaction, MaterialChosen):
            Self.AvargoItemChoice.placeholder = MaterialChosen
            await Interaction.response.edit_message(view=Self.BaseViewFrame)

        Self.BaseViewFrame = View(timeout=144000)
        Self.EmbedFrame = Embed(title=f"{Self.Player.Data['Name']}'s Avargo Buy Panel")

        await Self._Generate_Info()

        Self.BuyButton = Button(label="Buy", style=Self.ButtonStyle, custom_id="BuyButton")
        Self.BuyButton.callback = lambda Interaction: Interaction.response.send_modal(Self.AvargoForm)
        Self.BaseViewFrame.add_item(Self.BuyButton)

        Self.AvargoButton = Button(label="Avargo", style=Self.ButtonStyle, row=3, custom_id="AvargoButton")
        Self.AvargoButton.callback = Self._Construct_Avargo_Panel
        Self.BaseViewFrame.add_item(Self.AvargoButton)

        Self.HomepageButton = Button(label="Home", style=ButtonStyle.grey, row=3, custom_id="HomePageButton")
        Self.HomepageButton.callback = lambda Interaction: Self._Construct_Home(Interaction)
        Self.BaseViewFrame.add_item(Self.HomepageButton)

        # Format a string that has the material cost next to it
        Self.AvargoItemChoices = [SelectOption(label=Material) for Material in Self.Ether.Materials]
        Self.AvargoItemChoice = Select(placeholder="Select a material", options=Self.AvargoItemChoices, custom_id=f"ItemSelection", row=2)
        Self.AvargoItemChoice.callback = lambda Interaction: _Select_Material(Interaction, Interaction.data["values"][0])
        Self.BaseViewFrame.add_item(Self.AvargoItemChoice)

        await Self._Send_New_Panel(Interaction)


    async def _Construct_Debug_Panel(Self, Interaction):
        Self.BaseViewFrame = View(timeout=144000)
        Self.EmbedFrame = Embed(title=f"{Self.Player.Data['Name']}'s Home Panel")

        await Self._Generate_Info()

        Self.ResetPlayer = Button(label="Reset Player", style=Self.ButtonStyle, custom_id="ResetPlayerButton")
        Self.ResetPlayer.callback = lambda Interaction: Interaction.response.send_modal(Self.PlayerUUIDSubmission)
        Self.BaseViewFrame.add_item(Self.ResetPlayer)

        Self.PlayerUUIDSubmission = Modal(title="Submit Player UUID")
        Self.PlayerUUIDSubmission.on_submit = lambda Interaction: Self._Reset_Player(Interaction, int(SubmittedUUID.value))
        Self.PlayerUUIDSubmission.add_item(SubmittedUUID)

        SubmittedUUID = TextInput(label="Player UUID") 

        await Self._Send_New_Panel(Interaction)


    async def _Reset_Player(Self, Interaction, SubmittedUUID):
        if Self.Player.Data["Team"] == "Analis":
            await Self.Ether.Data["Players"][SubmittedUUID].Data["Member Object"].remove_roles(Self.Ether.Roles["Analis"])
        if Self.Player.Data["Team"] == "Titan":
            await Self.Ether.Data["Players"][SubmittedUUID].Data["Member Object"].remove_roles(Self.Ether.Roles["Titan"])
        Self.Ether.Data["Players"][SubmittedUUID] = None
        Self.Ether.Data["Players"].pop(SubmittedUUID)
        remove(join("Data", "PlayerData", f"{SubmittedUUID}.roc"))
        remove(join("Data", "PlayerInventories", f"{SubmittedUUID}.roc"))
        remove(join("Data", "PlayerProductionFacilities", f"{SubmittedUUID}.roc"))

        await Self._Send_New_Panel(Interaction)
        

    async def _Scavenge(Self, Interaction:Interaction):
        SuccessfulRolls = [Name for Name, Chance in ScavengeTable.items() if randrange(0 , 99) < Chance]
        Self.EmbedFrame.clear_fields()
        ScavengedString = ""
        ExperienceGained = round((0.65 * (0.35 * Self.Player.Data["Level"])) * len(SuccessfulRolls), 2)
        ScavengedString += f"Gained {ExperienceGained} experience\n"
        Self.Player.Data["Experience"] = round(Self.Player.Data["Experience"] + ExperienceGained, 2)

        for Roll in SuccessfulRolls:
            if Roll == "Wallet":
                MoneyScavenged = round(2.76 * (0.35 * Self.Player.Data["Level"]), 2)
                Self.Player.Data["Wallet"] = round(Self.Player.Data["Wallet"] + MoneyScavenged, 2)
                ScavengedString += f"Found ${MoneyScavenged}\n"
            if Roll == "Material" or Roll == "Bonus Material":
                MaterialScavenged = list(MaterialTable.keys())[randrange(0, (len(MaterialTable.keys()) - 1))]
                Start, End = MaterialTable[MaterialScavenged][0], MaterialTable[MaterialScavenged][1]
                MaterialScavengedAmount = randrange(Start, End)
                Self.Player.Inventory[MaterialScavenged] = round(Self.Player.Inventory[MaterialScavenged] + MaterialScavengedAmount, 2)
                ScavengedString += f"Found {MaterialScavengedAmount} {MaterialScavenged}\n"

        if Self.Player.Data["Experience"] >= Self.Player.ExperienceForNextLevel:
            Self.Player.Data["Level"] += 1
            Self.Player.Refresh_Stats()
            Self.EmbedFrame.insert_field_at(0, name=f"You leveled up!", value="\u200b", inline=False)
            
        await Self._Generate_Info()
        Self.EmbedFrame.add_field(name=f"Scavenged", value=ScavengedString, inline=False)
        await Self._Send_New_Panel(Interaction)


    async def _Construct_Facilities_Panel(Self, Interaction:Interaction):
        if Interaction.data["custom_id"] == "ItemSelection":
            Self.FacilitySelected: ProductionFacility = Self.Player.ProductionFacilities[Interaction.data["values"][0]]
            Self.FacilitiesSelect.placeholder = Interaction.data["values"][0]

        if Interaction.data["custom_id"] == "FacilityUpgradeButton":
            Self.FacilitySelected.Upgrade()
            # Do not refresh BaseViewFrame, and EmbedFrame
        else:
            Self.BaseViewFrame = View(timeout=144000)
            Self.EmbedFrame = Embed(title=f"{Self.InitialContext.author.name}'s Facilities Panel")

            Self.CollectProductionButton = Button(label="Collect Production", style=Self.ButtonStyle, custom_id="CollectProductionButton")
            Self.CollectProductionButton.callback = lambda Interaction: Self._Collect_Production_Facilities(Interaction)
            Self.BaseViewFrame.add_item(Self.CollectProductionButton)

            Self.HomepageButton = Button(label="Home", style=ButtonStyle.grey, row=3, custom_id="HomePageButton")
            Self.HomepageButton.callback = lambda Interaction: Self._Construct_Home(Interaction)
            Self.BaseViewFrame.add_item(Self.HomepageButton)

            Self.Options = [SelectOption(label=Name) for Name, Building in Self.Player.ProductionFacilities.items() if Building != "None"]
            Self.FacilitiesSelect = Select(options=Self.Options, custom_id=f"ItemSelection", row=2)
            Self.FacilitiesSelect.callback = lambda Interaction: Self._Construct_Facilities_Panel(Interaction)
            Self.BaseViewFrame.add_item(Self.FacilitiesSelect)

            await Self._Generate_Info(Exclusions=["Team", "Power"])
        
        if Self.FacilitySelected:
            Self.EmbedFrame.clear_fields()
            Self.FacilityUpgradeButton = Button(label="Upgrade", style=Self.ButtonStyle, custom_id="FacilityUpgradeButton", row=1)
            Self.BaseViewFrame.add_item(Self.FacilityUpgradeButton)
            Self.FacilityUpgradeButton.callback = lambda SelectInteraction: Self._Construct_Facilities_Panel(SelectInteraction)
            FacilityInfoString = (f"Level: {Self.FacilitySelected.Level}\n"+
                                    f"Capacity: {Self.FacilitySelected.Capacity}\n"+
                                    f"Units Per Second: {Self.FacilitySelected.UnitsPerTick}\n"+
                                    f"Upgrade Cost: {Self.FacilitySelected.UpgradeCost}")
            Self.EmbedFrame.add_field(name=f"{Self.FacilitySelected.Name} Info", value=FacilityInfoString)
        
        await Self._Generate_Info(Exclusions=["Team", "Power"])
        Self.Ether.Logger.info(f"Sent Facilities panel to {Self.Player.Data['Name']}")
        await Self._Send_New_Panel(Interaction)


    async def _Collect_Production_Facilities(Self, Interaction):
        CollectionString = ""
        ProductionFacilityLength = len(Self.Player.ProductionFacilities.values()) - 1
        CollectionTime = int(time())
        for Index, Facility in enumerate(Self.Player.ProductionFacilities.values()):
            if Self.Player.Data["Time of Last Production Collection"] == "Never":
                EarnedAmount = round(Facility.UnitsPerTick * (CollectionTime - Self.Player.Data["Join TimeStamp"]), 2)
            else:
                EarnedAmount = round(Facility.UnitsPerTick * (CollectionTime - Self.Player.Data["Time of Last Production Collection"]), 2)

            if Index == ProductionFacilityLength:
                CollectionString += f"{EarnedAmount} {Facility.OutputItem}"
            else:
                CollectionString += f"{EarnedAmount} {Facility.OutputItem}\n"

            Self.Player.Inventory[Facility.OutputItem] = EarnedAmount
        
        Self.Player.Data["Time of Last Production Collection"] = CollectionTime

        Self.EmbedFrame.clear_fields()

        await Self._Generate_Info(Exclusions=["Team", "Power"])

        Self.EmbedFrame.add_field(name="Collected:", value=CollectionString)

        await Self._Send_New_Panel(Interaction)


    async def _Construct_Inventory_Panel(Self, Interaction:Interaction):
        Self.BaseViewFrame = View(timeout=144000)
        Self.EmbedFrame = Embed(title=f"{Self.InitialContext.author.name}'s Inventory Panel")
        Self.HomepageButton = Button(label="Home", style=ButtonStyle.grey, row=3, custom_id="HomePageButton")

        InventoryString = ""

        PlayerInventoryLength = len(Self.Player.Inventory.items()) - 1
        for Index, (Name, Amount) in enumerate(Self.Player.Inventory.items()):
            if Index == PlayerInventoryLength:
                InventoryString += f"{Amount} {Name}"
            else:
                InventoryString += f"{Amount} {Name}\n"

        await Self._Generate_Info(Exclusions=["Team", "Power"])

        Self.EmbedFrame.add_field(name="Inventory", value=InventoryString)

        Self.HomepageButton.callback = lambda Interaction: Self._Construct_Home(Interaction=Interaction)

        Self.BaseViewFrame.add_item(Self.HomepageButton)

        Self.Ether.Logger.info(f"Sent Inventory panel to {Self.Player.Data['Name']}")

        await Self._Send_New_Panel(Interaction)