from asyncio import create_task
from discord import ButtonStyle, Embed, SelectOption, InteractionMessage
from discord import Interaction as DiscordInteraction
from discord.ext.commands import Context
from discord.ui import View, Button, Select, Modal, TextInput
from RealmOfConflict import RealmOfConflict
from Tables import ScavengeTable, MaterialTable, MaterialWorthTable, InfantryTable, InfantryToObject
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


    async def _Send_New_Panel(Self, Interaction:DiscordInteraction):
        await Interaction.response.edit_message(embed=Self.EmbedFrame, view=Self.BaseViewFrame)


    async def _Determine_Team(Self):
        if "Titan" in str(Self.InitialContext.author.roles):
            Self.ButtonStyle = ButtonStyle.red
        elif "Analis" in str(Self.InitialContext.author.roles):
            Self.ButtonStyle = ButtonStyle.blurple
        else:
            Self.ButtonStyle = ButtonStyle.grey


    async def _Generate_Info(Self, Exclusions:list=[], Inclusions=[]):
        Fields = [Field for Field in ["Wallet", "Team", "Level", "Experience", "Power"] if Field not in Exclusions]
        Fields += Inclusions
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
        Self.MaterialChosen = None
        Self.InfantrySelected = None
        Self.ReceiptString = ""
        Self.Receipt = {}
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

        Self.SententsButton = Button(label="Sentents", style=Self.ButtonStyle, custom_id="SententsButton")
        Self.SententsButton.callback = Self._Construct_Sentents_Panel
        Self.BaseViewFrame.add_item(Self.SententsButton)

        Self.InventoryButton = Button(label="Inventory", style=Self.ButtonStyle, custom_id="InventoryButton")
        Self.InventoryButton.callback = Self._Construct_Inventory_Panel
        Self.BaseViewFrame.add_item(Self.InventoryButton)

        Self.ProfileButton = Button(label="Profile", style=Self.ButtonStyle, custom_id="ProfileButton")
        Self.ProfileButton.callback = Self._Construct_Profile_Panel
        Self.BaseViewFrame.add_item(Self.ProfileButton)

        if InitialContext.author.id in Self.Whitelist:
            Self.DebugButton = Button(label="Debug", style=ButtonStyle.grey, row=3)
            Self.DebugButton.callback = Self._Construct_Debug_Panel
            Self.BaseViewFrame.add_item(Self.DebugButton)

        if Interaction:
            if Interaction.user != Self.InitialContext.author:
                return
            await Self._Send_New_Panel(Interaction)
        else:
            Self.DashboardMessage = await Self.InitialContext.send(embed=Self.EmbedFrame, view=Self.BaseViewFrame)


    async def _Construct_Avargo_Panel(Self, Interaction:DiscordInteraction):
        if Interaction.user != Self.InitialContext.author:
            return
        Self.BaseViewFrame = View(timeout=144000)
        Self.EmbedFrame = Embed(title=f"{Self.Player.Data['Name']}'s Avargo Panel")

        await Self._Generate_Info()

        Self.BuyButton = Button(label="Buy", style=Self.ButtonStyle, custom_id="BuyButton")
        Self.BuyButton.callback = lambda Interaction: Self._Avargo_Sale(Interaction, "Buy")
        Self.BaseViewFrame.add_item(Self.BuyButton)

        Self.SellButton = Button(label="Sell", style=Self.ButtonStyle, custom_id="SellButton")
        Self.SellButton.callback = lambda Interaction: Self._Avargo_Sale(Interaction, "Sell")
        Self.BaseViewFrame.add_item(Self.SellButton)

        Self.HomepageButton = Button(label="Home", style=ButtonStyle.grey, row=3, custom_id="HomePageButton")
        Self.HomepageButton.callback = lambda Interaction: Self._Construct_Home(Interaction=Interaction)
        Self.BaseViewFrame.add_item(Self.HomepageButton)

        await Self._Send_New_Panel(Interaction)


    async def _Construct_Quantity_Modal(Self, Interaction):
        if Interaction.user != Self.InitialContext.author:
            return
        Self.AvargoItemQuantityModal = Modal(title="Enter Quantity")
        Self.AvargoItemQuantityModal.on_submit = lambda Interaction: Self._Avargo_Sale(Interaction, Self.SaleType, MaterialChosen=Self.MaterialChosen, ReceiptStarted=True, Quantity=int(Self.AvargoItemQuantity.value))

        Self.AvargoItemQuantity = TextInput(label="Enter item quantity")
        Self.AvargoItemQuantityModal.add_item(Self.AvargoItemQuantity)
        await Interaction.response.send_modal(Self.AvargoItemQuantityModal)
    

    async def _Avargo_Sale(Self, Interaction:DiscordInteraction, SaleType, MaterialChosen=None, ReceiptStarted=False, Quantity=None, InsufficientFunds=False, InsufficientMaterials=False):
        if Interaction.user != Self.InitialContext.author:
            return
        Self.SaleType = SaleType
        if MaterialChosen is None:
            Self.ReceiptString = ""
            Self.Receipt = {}
            Self.BaseViewFrame = View(timeout=144000)
            Self.EmbedFrame = Embed(title=f"{Self.Player.Data['Name']}'s Avargo Sale Panel")

            await Self._Generate_Info()

            Self.AddButton = Button(label="Add", style=Self.ButtonStyle, custom_id="AddButton")
            Self.AddButton.callback = Self._Construct_Quantity_Modal
            Self.BaseViewFrame.add_item(Self.AddButton)

            Self.CheckoutButton = Button(label="Checkout", style=Self.ButtonStyle, custom_id="CheckoutButton")
            Self.CheckoutButton.callback = lambda Interaction: Self._Avargo_Checkout(Interaction, SaleType)
            Self.BaseViewFrame.add_item(Self.CheckoutButton)

            Self.AvargoButton = Button(label="Avargo", style=Self.ButtonStyle, row=3, custom_id="AvargoButton")
            Self.AvargoButton.callback = Self._Construct_Avargo_Panel
            Self.BaseViewFrame.add_item(Self.AvargoButton)

            Self.HomepageButton = Button(label="Home", style=ButtonStyle.grey, row=3, custom_id="HomePageButton")
            Self.HomepageButton.callback = lambda Interaction: Self._Construct_Home(Interaction=Interaction)
            Self.BaseViewFrame.add_item(Self.HomepageButton)
        
            if Self.SaleType == "Buy":
                Self.AvargoItemChoices = [SelectOption(label=f"{Material} at ${MaterialWorthTable[Material]} per unit") for Material in Self.Ether.Materials]
            if Self.SaleType == "Sell":
                Self.AvargoItemChoices = [SelectOption(label=f"{Material} at ${MaterialWorthTable[Material]/4} per unit") for Material in Self.Ether.Materials]

            Self.AvargoItemChoice = Select(placeholder="Select a material", options=Self.AvargoItemChoices, custom_id=f"ItemSelection", row=2)
            Self.BaseViewFrame.add_item(Self.AvargoItemChoice)
            Self.AvargoItemChoice.callback = lambda Interaction: Self._Avargo_Sale(Interaction, SaleType, ReceiptStarted=ReceiptStarted, MaterialChosen=Interaction.data["values"][0])
            

        if MaterialChosen:
            Self.AvargoItemChoice.placeholder = MaterialChosen
            Self.MaterialChosen = MaterialChosen
            Self.MaterialRaw = MaterialChosen.split(" at ")[0]
            Self.EmbedFrame.add_field(name=f"You have {Self.Player.Inventory[Self.MaterialRaw]} {Self.MaterialRaw}", value="\u200b")
        if ReceiptStarted:
            if Quantity:
                Self.Receipt.update({Self.MaterialRaw:Quantity})
                if Self.SaleType == "Buy":
                    if len(Self.ReceiptString) > 0:
                        Self.ReceiptString += f"\n{Quantity} {Self.MaterialChosen} for ${MaterialWorthTable[Self.MaterialRaw] * int(Quantity)}"
                    else:
                        Self.ReceiptString += f"{Quantity} {Self.MaterialChosen} for ${MaterialWorthTable[Self.MaterialRaw] * int(Quantity)}"
                elif Self.SaleType == "Sell":
                    if len(Self.ReceiptString) > 0:
                        Self.ReceiptString += f"\n{Quantity} {Self.MaterialChosen} for ${MaterialWorthTable[Self.MaterialRaw] * int(Quantity)/4}"
                    else:
                        Self.ReceiptString += f"{Quantity} {Self.MaterialChosen} for ${MaterialWorthTable[Self.MaterialRaw] * int(Quantity)/4}"
                Self.EmbedFrame.clear_fields()
                await Self._Generate_Info()
                Self.EmbedFrame.add_field(name="Receipt", value=Self.ReceiptString, inline=False)

        if InsufficientFunds:
            Self.EmbedFrame.add_field(name="Insufficient Funds", value="\u200b")

        if InsufficientMaterials:
            Self.EmbedFrame.add_field(name="Insufficient Materials", value=f"You only have {Self.Player.Inventory[Self.InsufficientMaterial]} {Self.InsufficientMaterial}")

        await Self._Send_New_Panel(Interaction)


    async def _Avargo_Checkout(Self, Interaction, SaleType):
        if Interaction.user != Self.InitialContext.author:
            return
        if len(Self.Receipt) == 0:
            return
        Total = 0
        EarnedExperience = 0
        for Material, Quantity in Self.Receipt.items():
            if SaleType == "Buy":
                Total += round(MaterialWorthTable[Material] * Quantity, 2)
                EarnedExperience = round(EarnedExperience + (MaterialWorthTable[Material]/4), 2)
            if SaleType == "Sell":
                if Quantity > Self.Player.Inventory[Material]:
                    Self.InsufficientMaterial = Material
                    await Self._Avargo_Sale(Interaction, Self.SaleType, MaterialChosen=Self.MaterialChosen, ReceiptStarted=True, InsufficientMaterials=True)
                    return
                EarnedExperience = round(EarnedExperience + (MaterialWorthTable[Material]/8), 2)
                Total = round(Total + (MaterialWorthTable[Material]/4) * Quantity, 2)
        
        Self.BaseViewFrame = View(timeout=144000)
        Self.EmbedFrame = Embed(title=f"{Self.Player.Data['Name']}'s Avargo Sale Panel")

        Self.EmbedFrame.add_field(name="Receipt", value=Self.ReceiptString, inline=False)
        Self.EmbedFrame.add_field(name="Total", value=f"${Total}", inline=False)
        Self.EmbedFrame.add_field(name="Experienced Earned", value=f"{EarnedExperience}", inline=False)

        Self.AvargoButton = Button(label="Avargo", style=Self.ButtonStyle, row=3, custom_id="AvargoButton")
        Self.AvargoButton.callback = Self._Construct_Avargo_Panel
        Self.BaseViewFrame.add_item(Self.AvargoButton)

        Self.HomepageButton = Button(label="Home", style=ButtonStyle.grey, row=3, custom_id="HomePageButton")
        Self.HomepageButton.callback = lambda Interaction: Self._Construct_Home(Interaction=Interaction)

        Self.BaseViewFrame.add_item(Self.HomepageButton)
        if SaleType == "Buy":
            if Total <= Self.Player.Data["Wallet"]:
                for Material, Quantity in Self.Receipt.items():
                    Self.Player.Inventory[Material] = round(Self.Player.Inventory[Material] + Quantity, 2)
                Self.Player.Data["Wallet"] = round(Self.Player.Data["Wallet"] - Total, 2)
                Self.Player.Data["Experience"] = round(Self.Player.Data["Experience"] + EarnedExperience, 2)
                await Self._Generate_Info()
                await Self._Send_New_Panel(Interaction)
            else:
                await Self._Avargo_Sale(Interaction, Self.SaleType, MaterialChosen=Self.MaterialChosen, ReceiptStarted=True, InsufficientFunds=True)
        if SaleType == "Sell":
            for Material, Quantity in Self.Receipt.items():
                Self.Player.Inventory[Material] = round(Self.Player.Inventory[Material] - Quantity, 2)
                Self.Player.Data["Wallet"] = round(Self.Player.Data["Wallet"] + Total, 2)
                Self.Player.Data["Experience"] = round(Self.Player.Data["Experience"] + EarnedExperience, 2)
                await Self._Generate_Info()
                await Self._Send_New_Panel(Interaction)


    async def _Construct_Sentents_Panel(Self, Interaction):
        Self.BaseViewFrame = View(timeout=144000)
        Self.EmbedFrame = Embed(title=f"{Self.Player.Data['Name']}'s Sentents Panel")
        await Self._Generate_Info()

        Self.ArmyButton = Button(label="My Army", style=Self.ButtonStyle, custom_id="ArmyButton")
        Self.ArmyButton.callback = lambda Interaction: Self._Construct_Army_Panel(Interaction=Interaction)
        Self.BaseViewFrame.add_item(Self.ArmyButton)

        Self.RecruitButton = Button(label="Recruit", style=Self.ButtonStyle, custom_id="RecruitButton")
        Self.RecruitButton.callback = lambda Interaction: Self._Construct_Recruit_Panel(Interaction=Interaction)
        Self.BaseViewFrame.add_item(Self.RecruitButton)

        Self.HomepageButton = Button(label="Home", style=ButtonStyle.grey, row=3, custom_id="HomePageButton")
        Self.HomepageButton.callback = lambda Interaction: Self._Construct_Home(Interaction=Interaction)
        Self.BaseViewFrame.add_item(Self.HomepageButton)

        await Self._Send_New_Panel(Interaction)


    async def _Construct_Recruit_Panel(Self, Interaction, InfantrySelected=None, InfantryRecruited=None):
        if InfantrySelected == None:
            Self.BaseViewFrame = View(timeout=144000)
            Self.EmbedFrame = Embed(title=f"{Self.Player.Data['Name']}'s Recruit Panel")
            await Self._Generate_Info()

            Self.RecruitButton = Button(label="Recruit", style=Self.ButtonStyle, custom_id="RecruitButton")
            Self.RecruitButton.callback = lambda Interaction: Self._Construct_Recruit_Panel(Interaction, Self.InfantrySelected, Self.InfantrySelected)
            Self.BaseViewFrame.add_item(Self.RecruitButton)

            Self.InfantyChoices = [SelectOption(label=f"{Infantry} for ${Worth}") for Infantry, Worth in InfantryTable.items()]
            Self.InfantryChoice = Select(placeholder="Select an Infantry", options=Self.InfantyChoices, custom_id=f"InfantrySelection", row=2)
            Self.BaseViewFrame.add_item(Self.InfantryChoice)

            Self.HomepageButton = Button(label="Home", style=ButtonStyle.grey, row=3, custom_id="HomePageButton")
            Self.HomepageButton.callback = lambda Interaction: Self._Construct_Home(Interaction=Interaction)
            Self.BaseViewFrame.add_item(Self.HomepageButton)
        
        if InfantrySelected:
            Self.InfantrySelected = InfantrySelected
            Self.InfantryChoice.placeholder = InfantrySelected

        if InfantryRecruited:
            InfantryKey = Self.InfantrySelected.split(" for ")[0]
            if Self.Player.Data["Wallet"] >= InfantryTable[InfantryKey]:
                Self.Player.Data["Wallet"] = round(Self.Player.Data["Wallet"] - InfantryTable[InfantryKey], 2)
                Self.EmbedFrame.add_field(name=f"Purchased {Self.InfantrySelected} for {InfantryTable[InfantryKey]}", value="\u200b")
                InfantryData = InfantryKey.split(" ~ ")
                InfantryLevel = int(InfantryData[0].split(" ")[1])
                InfantryType = InfantryData[1]
                NewInfantry = InfantryToObject[InfantryType](InfantryLevel, InfantryType, Self.Player)
                Self.Player.Army.update({NewInfantry.Name:NewInfantry})
                Self.Player.Refresh_Power()
                Self.EmbedFrame.clear_fields()
                await Self._Generate_Info()
                Self.EmbedFrame.add_field(name=f"Recruited {NewInfantry.Name}", value="\u200b")
            else:
                Self.EmbedFrame.clear_fields()
                await Self._Generate_Info()
                Self.EmbedFrame.add_field(name=f"Insufficient Funds", value="\u200b")
        Self.InfantryChoice.callback = lambda Interaction: Self._Construct_Recruit_Panel(Interaction, Interaction.data["values"][0])
        await Self._Send_New_Panel(Interaction)


    async def _Construct_Army_Panel(Self, Interaction):
        Self.BaseViewFrame = View(timeout=144000)
        Self.EmbedFrame = Embed(title=f"{Self.Player.Data['Name']}'s Army Panel")
        await Self._Generate_Info()

        ArmyString = ""

        for Index, (Name, Infantry) in enumerate(Self.Player.Army.items()):
            if len(ArmyString) + 36 >= 1024:
                print("Pagintion Required")
                Self.ArmyPaginationRequired = True
                Self.ArmyIndex = Index
                break
            ArmyString += f"{Name} ~ Level {Infantry.Level} ~ {Infantry.Type}\n"

        Self.EmbedFrame.add_field(name="\u200b", value=ArmyString, inline=False)

        Self.NextPageButton = Button(label="Next Page", style=Self.ButtonStyle, custom_id="NextPageButton")
        Self.NextPageButton.callback = lambda Interaction: ...
        Self.BaseViewFrame.add_item(Self.NextPageButton)

        Self.PreviousPageButton = Button(label="Previous Page", style=Self.ButtonStyle, custom_id="PreviousPageButton")
        Self.PreviousPageButton.callback = lambda Interaction: ...
        Self.BaseViewFrame.add_item(Self.PreviousPageButton)

        Self.HomepageButton = Button(label="Home", style=ButtonStyle.grey, row=3, custom_id="HomePageButton")
        Self.HomepageButton.callback = lambda Interaction: Self._Construct_Home(Interaction=Interaction)
        Self.BaseViewFrame.add_item(Self.HomepageButton)

        await Self._Send_New_Panel(Interaction)


    async def _Construct_Debug_Panel(Self, Interaction):
        if Interaction.user != Self.InitialContext.author:
            return
        Self.BaseViewFrame = View(timeout=144000)
        Self.EmbedFrame = Embed(title=f"{Self.Player.Data['Name']}'s Home Panel")

        await Self._Generate_Info()

        Self.ResetPlayer = Button(label="Reset Player", style=Self.ButtonStyle, custom_id="ResetPlayerButton")
        Self.ResetPlayer.callback = lambda Interaction: Interaction.response.send_modal(Self.PlayerUUIDSubmission)
        Self.BaseViewFrame.add_item(Self.ResetPlayer)

        Self.HomepageButton = Button(label="Home", style=ButtonStyle.grey, row=3, custom_id="HomePageButton")
        Self.HomepageButton.callback = lambda Interaction: Self._Construct_Home(Interaction=Interaction)
        Self.BaseViewFrame.add_item(Self.HomepageButton)


        Self.PlayerUUIDSubmission = Modal(title="Submit Player UUID")
        Self.PlayerUUIDSubmission.on_submit = lambda Interaction: Self._Reset_Player(Interaction, int(SubmittedUUID.value))
        SubmittedUUID = TextInput(label="Player UUID") 
        Self.PlayerUUIDSubmission.add_item(SubmittedUUID)


        await Self._Send_New_Panel(Interaction)


    async def _Reset_Player(Self, Interaction, SubmittedUUID):
        if Interaction.user != Self.InitialContext.author:
            return
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
        

    async def _Scavenge(Self, Interaction:DiscordInteraction):
        if Interaction.user != Self.InitialContext.author:
            return
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


    async def _Construct_Facilities_Panel(Self, Interaction:DiscordInteraction):
        if Interaction.user != Self.InitialContext.author:
            return
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
            Self.HomepageButton.callback = lambda Interaction: Self._Construct_Home(Interaction=Interaction)
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

        Self.Ether.Logger.info(f"Sent Facilities panel to {Self.Player.Data['Name']}")
        await Self._Send_New_Panel(Interaction)


    async def _Collect_Production_Facilities(Self, Interaction):
        if Interaction.user != Self.InitialContext.author:
            return
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

            Self.Player.Inventory[Facility.OutputItem] = round(Self.Player.Inventory[Facility.OutputItem] + EarnedAmount, 2)
        
        Self.Player.Data["Time of Last Production Collection"] = CollectionTime

        Self.EmbedFrame.clear_fields()

        await Self._Generate_Info(Exclusions=["Team", "Power"])

        Self.EmbedFrame.add_field(name="Collected:", value=CollectionString)

        await Self._Send_New_Panel(Interaction)


    async def _Construct_Inventory_Panel(Self, Interaction:DiscordInteraction):
        if Interaction.user != Self.InitialContext.author:
            return
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
    
    
    async def _Construct_Profile_Panel(Self, Interaction):
        Self.BaseViewFrame = View(timeout=144000)
        Self.EmbedFrame = Embed(title=f"{Self.Player.Data['Name']}'s Profile Panel")
        await Self._Generate_Info(Inclusions=["Offensive Power", "Defensive Power", "Healing Power",
                                              "Production Power", "Manufacturing Power", "Energy Sapping",])

        Self.ChangeNicknameButton = Button(label="Change Nickname", style=Self.ButtonStyle, custom_id="ChangeNicknameButton")
        Self.ChangeNicknameButton.callback = lambda Interaction: Self._Construct_Army_Panel(Interaction=Interaction)
        Self.BaseViewFrame.add_item(Self.ChangeNicknameButton)

        Self.HomepageButton = Button(label="Home", style=ButtonStyle.grey, row=3, custom_id="HomePageButton")
        Self.HomepageButton.callback = lambda Interaction: Self._Construct_Home(Interaction=Interaction)
        Self.BaseViewFrame.add_item(Self.HomepageButton)

        await Self._Send_New_Panel(Interaction)