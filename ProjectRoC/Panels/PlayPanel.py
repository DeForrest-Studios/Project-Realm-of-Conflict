from asyncio import create_task
from discord import ButtonStyle, Embed, SelectOption
from discord import Interaction as DiscordInteraction
from discord import Message as DiscordMessage
from discord.ext.commands import Context as DiscordContext
from discord.ui import View, Button, Select, Modal, TextInput
from Structures import ProductionFacility
from os import remove
from os.path import join
from Player import Player
from random import randrange
from RealmOfConflict import RealmOfConflict
from Tables import ScavengeTable, MaterialTable, InfantryTable, InfantryToObject
from time import time
from Panels.Panel import Panel
from Panels.Facilities import FacilitiesPanel
from Panels.Avargo import AvargoPanel


class PlayPanel(Panel):
    def __init__(Self, Ether:RealmOfConflict, PlayerContext:DiscordContext):
        super().__init__()
        create_task(Self._Construct_Home(Ether, PlayerContext))


    async def _Determine_Team(Self, InitialContext):
        if "Titan" in str(InitialContext.author.roles):
            Self.ButtonStyle = ButtonStyle.red
        elif "Analis" in str(InitialContext.author.roles):
            Self.ButtonStyle = ButtonStyle.blurple
        else:
            Self.ButtonStyle = ButtonStyle.grey


    async def _Construct_Home(Self, Ether:RealmOfConflict, InitialContext:DiscordContext, Interaction:DiscordInteraction=None):
        Ether:RealmOfConflict = Ether
        Whitelist:[int] = [897410636819083304, # Robert Reynolds, Cavan
                          ]
        Self.Player:Player = Ether.Data["Players"][InitialContext.author.id]
        Self.MaterialChosen = None
        Self.InfantrySelected = None
        Self.ReceiptString = ""
        Self.Receipt:{str:int} = {}
        await Self._Determine_Team(InitialContext)

        if Self.Player.Data["Experience"] >= Self.Player.ExperienceForNextLevel:
            Self.Player.Data["Level"] += 1
            Self.Player.Refresh_Stats()

        Self.BaseViewFrame = View(timeout=144000)
        Self.EmbedFrame = Embed(title=f"{Self.Player.Data['Name']}'s Home Panel")

        await Self._Generate_Info(Ether, InitialContext, )

        Self.ScavengeButton = Button(label="Scavenge", style=Self.ButtonStyle, custom_id="ScavengeButton")
        Self.ScavengeButton.callback = Self._Scavenge
        Self.BaseViewFrame.add_item(Self.ScavengeButton)

        Self.FacilitiesButton = Button(label="Facilities", style=Self.ButtonStyle, custom_id="FacilitiesButton")
        Self.FacilitiesButton.callback = lambda Interaction: Self._Construct_New_Panel(Ether, InitialContext, Self.ButtonStyle, Interaction)
        Self.BaseViewFrame.add_item(Self.FacilitiesButton)

        Self.AvargoButton = Button(label="Avargo", style=Self.ButtonStyle, custom_id="AvargoButton")
        Self.AvargoButton.callback = lambda Interaction: Self._Construct_New_Panel(Ether, InitialContext, Self.ButtonStyle, Interaction)
        Self.BaseViewFrame.add_item(Self.AvargoButton)

        Self.SententsButton = Button(label="Sentents", style=Self.ButtonStyle, custom_id="SententsButton")
        Self.SententsButton.callback = lambda Interaction: Self._Construct_New_Panel(Ether, InitialContext, Self.ButtonStyle, Interaction)
        Self.BaseViewFrame.add_item(Self.SententsButton)

        Self.InventoryButton = Button(label="Inventory", style=Self.ButtonStyle, custom_id="InventoryButton")
        Self.InventoryButton.callback = lambda Interaction: Self._Construct_New_Panel(Ether, InitialContext, Self.ButtonStyle, Interaction)
        Self.BaseViewFrame.add_item(Self.InventoryButton)

        Self.ProfileButton = Button(label="Profile", style=Self.ButtonStyle, custom_id="ProfileButton")
        Self.ProfileButton.callback = lambda Interaction: Self._Construct_New_Panel(Ether, InitialContext, Self.ButtonStyle, Interaction)
        Self.BaseViewFrame.add_item(Self.ProfileButton)

        if InitialContext.author.id in Whitelist:
            Self.DebugButton = Button(label="Debug", style=ButtonStyle.grey, row=3)
            Self.DebugButton.callback = Self._Construct_Debug_Panel
            Self.BaseViewFrame.add_item(Self.DebugButton)


        if Interaction:
            if Interaction.user != InitialContext.author:
                return
            await Self._Send_New_Panel(Interaction)
        else:
            Self.DashboardMessage:DiscordMessage = await InitialContext.send(embed=Self.EmbedFrame, view=Self.BaseViewFrame)

        
    async def _Construct_New_Panel(Self, Ether:RealmOfConflict, InitialContext:DiscordContext, ButtonStyle, Interaction:DiscordInteraction):
        Mapping:{str:Panel} = {
            "FacilitiesButton":FacilitiesPanel,
            "AvargoButton":AvargoPanel,
        }
        Ether.Data["Panels"][InitialContext.author.id] = Mapping[Interaction.data["custom_id"]](Ether, InitialContext, ButtonStyle, Interaction, Self)


    async def _Construct_Sentents_Panel(Self, Interaction:DiscordInteraction):
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


    async def _Construct_Recruit_Panel(Self, Interaction:DiscordInteraction, InfantrySelected=None, InfantryRecruited=None):
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


    async def _Construct_Army_Panel(Self, Interaction:DiscordInteraction):
        Self.BaseViewFrame = View(timeout=144000)
        Self.EmbedFrame = Embed(title=f"{Self.Player.Data['Name']}'s Army Panel")
        await Self._Generate_Info()

        ArmyString = ""

        Index:int
        Name:str
        Infantry:object
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


    async def _Reset_Player(Self, Interaction:DiscordInteraction, SubmittedUUID):
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
        SuccessfulRolls:[str] = [Name for Name, Chance in ScavengeTable.items() if randrange(0 , 99) < Chance]
        Self.EmbedFrame.clear_fields()
        ScavengedString = ""
        ExperienceGained:float = round((0.65 * (0.35 * Self.Player.Data["Level"])) * len(SuccessfulRolls), 2)
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


    async def _Construct_Inventory_Panel(Self, Interaction:DiscordInteraction):
        if Interaction.user != Self.InitialContext.author:
            return
        Self.BaseViewFrame = View(timeout=144000)
        Self.EmbedFrame = Embed(title=f"{Self.InitialContext.author.name}'s Inventory Panel")
        Self.HomepageButton = Button(label="Home", style=ButtonStyle.grey, row=3, custom_id="HomePageButton")

        InventoryString = ""

        PlayerInventoryLength = len(Self.Player.Inventory.items()) - 1
        Index:int
        Name:str
        Amount:float
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
    

    async def _Construct_Profile_Panel(Self, Interaction:DiscordInteraction):
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