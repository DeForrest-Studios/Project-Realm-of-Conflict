from asyncio import create_task
from discord import ButtonStyle, Embed
from discord import Interaction as DiscordInteraction
from discord import Message as DiscordMessage
from discord import ButtonStyle as DiscordButtonStyle
from discord.ext.commands import Context as DiscordContext
from discord.ui import View, Button
from random import randrange
from RealmOfConflict import RealmOfConflict
from Tables import ScavengeTable, MaterialTable
from Panels.Panel import Panel
from Panels.ProductionFacilities import ProductionFacilitiesPanel
from Panels.Avargo import AvargoPanel
from Panels.Sentents import SententPanel
from Panels.Inventory import InventoryPanel
from Panels.Profile import ProfilePanel
from Panels.Debug import DebugPanel
from Panels.Skills import SkillsPanel
from Player import Player


class PlayPanel:
    def __init__(Self, Ether:RealmOfConflict, InitialContext:DiscordContext) -> None:
        create_task(Self._Construct_Home(Ether, InitialContext))


    async def _Generate_Info(Self, Ether, InitialContext, Exclusions:list=[], Inclusions:list=[]):
        return await Panel._Generate_Info(Self, Ether, InitialContext, Exclusions, Inclusions)
    

    async def _Send_New_Panel(Self, Interaction):
        return await Panel._Send_New_Panel(Self, Interaction)


    async def _Determine_Team(Self, InitialContext):
        if "Titan" in str(InitialContext.author.roles):
            Self.ButtonStyle = ButtonStyle.red
        elif "Analis" in str(InitialContext.author.roles):
            Self.ButtonStyle = ButtonStyle.blurple
        else:
            Self.ButtonStyle = ButtonStyle.grey


    async def _Construct_Home(Self, Ether:RealmOfConflict, InitialContext:DiscordContext, Interaction:DiscordInteraction=None):
        Self.Ether:RealmOfConflict = Ether
        Self.InitialContext:DiscordContext = InitialContext
        Self.PlayPanel:Panel = PlayPanel
        Self.ButtonStyle:DiscordButtonStyle = ButtonStyle
        Self.Player:Player = Ether.Data['Players'][InitialContext.author.id]

        Self.BaseViewFrame = View(timeout=144000)
        Self.EmbedFrame = Embed(title=f"{Self.Player.Data['Name']}'s Home Panel")

        Whitelist:[int] = [897410636819083304, # Robert Reynolds, Cavan
        ]
        Self.Mapping = {}
        Self.ReceiptString = ""
        Self.Receipt:{str:int} = {}
        await Self._Determine_Team(InitialContext)

        await Self._Generate_Info(Ether, InitialContext)

        Self.ScavengeButton = Button(label="Scavenge", style=Self.ButtonStyle, custom_id="ScavengeButton")
        Self.ScavengeButton.callback = lambda Interaction: Self._Scavenge(Ether, InitialContext, Interaction)
        Self.BaseViewFrame.add_item(Self.ScavengeButton)

        Self.ProductionFacilitiesButton = Button(label="Production Facilities", style=Self.ButtonStyle, custom_id="ProductionFacilitiesButton")
        Self.ProductionFacilitiesButton.callback = lambda Interaction: Self._Construct_New_Panel(Ether, InitialContext, Self.ButtonStyle, Interaction)
        Self.BaseViewFrame.add_item(Self.ProductionFacilitiesButton)

        Self.ManufacturingFacilitiesButton = Button(label="Manufacturing Facilities (WIP)", style=Self.ButtonStyle, custom_id="ManufacturingFacilitiesButton")
        Self.ManufacturingFacilitiesButton.callback = lambda Interaction: Self._Construct_New_Panel(Ether, InitialContext, Self.ButtonStyle, Interaction)
        Self.BaseViewFrame.add_item(Self.ManufacturingFacilitiesButton)

        Self.CraftingButton = Button(label="Crafting (WIP)", style=Self.ButtonStyle, custom_id="CraftingButton")
        Self.CraftingButton.callback = lambda Interaction: Self._Construct_New_Panel(Ether, InitialContext, Self.ButtonStyle, Interaction)
        Self.BaseViewFrame.add_item(Self.CraftingButton)

        Self.AvargoButton = Button(label="Avargo", style=Self.ButtonStyle, custom_id="AvargoButton")
        Self.AvargoButton.callback = lambda Interaction: Self._Construct_New_Panel(Ether, InitialContext, Self.ButtonStyle, Interaction)
        Self.BaseViewFrame.add_item(Self.AvargoButton)

        Self.SententsButton = Button(label="Sentents", style=Self.ButtonStyle, custom_id="SententsButton")
        Self.SententsButton.callback = lambda Interaction: Self._Construct_New_Panel(Ether, InitialContext, Self.ButtonStyle, Interaction)
        Self.BaseViewFrame.add_item(Self.SententsButton)

        Self.InventoryButton = Button(label="Inventory", style=Self.ButtonStyle, custom_id="InventoryButton")
        Self.InventoryButton.callback = lambda Interaction: Self._Construct_New_Panel(Ether, InitialContext, Self.ButtonStyle, Interaction)
        Self.BaseViewFrame.add_item(Self.InventoryButton)

        Self.PlanetButton = Button(label="Planet (WIP)", style=Self.ButtonStyle, custom_id="PlanetButton")
        Self.PlanetButton.callback = lambda Interaction: Self._Construct_New_Panel(Ether, InitialContext, Self.ButtonStyle, Interaction)
        Self.BaseViewFrame.add_item(Self.PlanetButton)

        Self.ProfileButton = Button(label="Profile", style=Self.ButtonStyle, custom_id="ProfileButton")
        Self.ProfileButton.callback = lambda Interaction: Self._Construct_New_Panel(Ether, InitialContext, Self.ButtonStyle, Interaction)
        Self.BaseViewFrame.add_item(Self.ProfileButton)

        Self.SkillsButton = Button(label="Skills", style=Self.ButtonStyle, custom_id="SkillsButton")
        Self.SkillsButton.callback = lambda Interaction: Self._Construct_New_Panel(Ether, InitialContext, Self.ButtonStyle, Interaction)
        Self.BaseViewFrame.add_item(Self.SkillsButton)

        Self.P2PMarketButton = Button(label="P2P Market (WIP)", style=Self.ButtonStyle, custom_id="P2PMarketButton")
        Self.P2PMarketButton.callback = lambda Interaction: Self._Construct_New_Panel(Ether, InitialContext, Self.ButtonStyle, Interaction)
        Self.BaseViewFrame.add_item(Self.P2PMarketButton)

        Self.InfoButton = Button(label="Info (WIP)", style=Self.ButtonStyle, custom_id="InfoButton")
        Self.InfoButton.callback = lambda Interaction: Self._Construct_New_Panel(Ether, InitialContext, Self.ButtonStyle, Interaction)
        Self.BaseViewFrame.add_item(Self.InfoButton)

        Self.CreaturesButton = Button(label="Creatures (WIP)", style=Self.ButtonStyle, custom_id="CreaturesButton")
        Self.CreaturesButton.callback = lambda Interaction: Self._Construct_New_Panel(Ether, InitialContext, Self.ButtonStyle, Interaction)
        Self.BaseViewFrame.add_item(Self.CreaturesButton)

        Self.TerrariumButton = Button(label="Terrarium (WIP)", style=Self.ButtonStyle, custom_id="TerrariumButton")
        Self.TerrariumButton.callback = lambda Interaction: Self._Construct_New_Panel(Ether, InitialContext, Self.ButtonStyle, Interaction)
        Self.BaseViewFrame.add_item(Self.TerrariumButton)

        if InitialContext.author.id in Whitelist:
            Self.Mapping.update({"DebugButton":DebugPanel})
            Self.DebugButton = Button(label="Debug", style=ButtonStyle.grey, row=3, custom_id="DebugButton")
            Self.DebugButton.callback = lambda Interaction: Self._Construct_New_Panel(Ether, InitialContext, Self.ButtonStyle, Interaction)
            Self.BaseViewFrame.add_item(Self.DebugButton)


        if Interaction:
            if Interaction.user != InitialContext.author:
                return
            Self.Ether.Logger.info(f"Sent Home panel to {Self.Player.Data['Name']}")
            await Self._Send_New_Panel(Interaction)
        else:
            Self.Ether.Logger.info(f"Sent Home panel to {Self.Player.Data['Name']}")
            Self.DashboardMessage:DiscordMessage = await InitialContext.send(embed=Self.EmbedFrame, view=Self.BaseViewFrame)

        
    async def _Construct_New_Panel(Self, Ether:RealmOfConflict, InitialContext:DiscordContext, ButtonStyle, Interaction:DiscordInteraction):
        Self.Mapping.update({
            "ProductionFacilitiesButton":ProductionFacilitiesPanel,
            "AvargoButton":AvargoPanel,
            "SententsButton":SententPanel,
            "InventoryButton":InventoryPanel,
            "ProfileButton":ProfilePanel,
            "SkillsButton":SkillsPanel
        })
        # Ether.Data["Panels"][InitialContext.author.id] = Self.Mapping[Interaction.data["custom_id"]](Ether, InitialContext, ButtonStyle, Interaction, Self)
        Self.Mapping[Interaction.data["custom_id"]](Ether, InitialContext, ButtonStyle, Interaction, Self)
        

    async def _Scavenge(Self, Ether, InitialContext, Interaction:DiscordInteraction):
        if Interaction.user != InitialContext.author:
            return
        SuccessfulRolls:[str] = [Name for Name, Chance in ScavengeTable.items() if randrange(0 , 99) < Chance]
        Self.EmbedFrame.clear_fields()
        ScavengedString = ""
        ExperienceGained:float = round(((0.65 * (0.35 * Self.Player.Data["Level"])) * len(SuccessfulRolls)) + (Self.Player.Data["Maiden's Grace"] * (0.11 * Self.Player.Data["Level"])), 2)
        ScavengedString += f"Gained {ExperienceGained} experience\n"
        Self.Player.Data["Experience"] = round(Self.Player.Data["Experience"] + ExperienceGained, 2)

        for Roll in SuccessfulRolls:
            if Roll == "Wallet":
                MoneyScavenged = round(2.76 * (0.35 * Self.Player.Data["Level"]) + (Self.Player.Data["Maiden's Grace"] * (0.4 * Self.Player.Data["Level"])), 2)
                Self.Player.Data["Wallet"] = round(Self.Player.Data["Wallet"] + MoneyScavenged, 2)
                ScavengedString += f"Found ${MoneyScavenged}\n"
            if Roll == "Material" or Roll == "Bonus Material":
                MaterialScavenged = list(MaterialTable.keys())[randrange(0, (len(MaterialTable.keys()) - 1))]
                Start, End = MaterialTable[MaterialScavenged][0], MaterialTable[MaterialScavenged][1]
                MaterialScavengedAmount = randrange(Start, End)
                Self.Player.Inventory[MaterialScavenged] = round(Self.Player.Inventory[MaterialScavenged] + MaterialScavengedAmount + (Self.Player.Data["Maiden's Grace"] * (0.08 * Self.Player.Data["Level"])), 2)
                ScavengedString += f"Found {MaterialScavengedAmount} {MaterialScavenged}\n"

        if Self.Player.Refresh_Stats() == "Level Up":
            Self.EmbedFrame.insert_field_at(0, name=f"You leveled up!", value="\u200b", inline=False)
            
        await Self._Generate_Info(Ether, InitialContext)
        Self.EmbedFrame.add_field(name=f"Scavenged", value=ScavengedString, inline=False)
        await Self._Send_New_Panel(Interaction)