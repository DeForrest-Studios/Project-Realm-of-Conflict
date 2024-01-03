from asyncio import create_task
from os import remove
from os.path import join
from RealmOfConflict import RealmOfConflict
from discord.ext.commands import Context as DiscordContext
from discord import Interaction as DiscordInteraction
from discord import ButtonStyle as DiscordButtonStyle
from discord import SelectOption, Embed
from discord.ui import View, Select, Button, Modal, TextInput
from Panels.Panel import Panel
from Structures import ProductionFacility
from time import time as Time
from Player import Player

class DebugPanel(Panel):
    def __init__(Self, Ether:RealmOfConflict, InitialContext:DiscordContext, ButtonStyle, Interaction:DiscordInteraction, PlayPanel):
        super().__init__(Ether, InitialContext,
                         PlayPanel, "Debug",
                         Interaction=Interaction, ButtonStyle=ButtonStyle)

    async def _Construct_Panel(Self):
        if Self.Interaction.user != Self.InitialContext.author: return
        await Self._Generate_Info(Self.Ether, Self.InitialContext)

        Self.ResetPlayer = Button(label="Reset Player", style=Self.ButtonStyle, custom_id="ResetPlayerButton")
        Self.ResetPlayer.callback = lambda Interaction: Interaction.response.send_modal(Self.PlayerUUIDSubmission)
        Self.BaseViewFrame.add_item(Self.ResetPlayer)

        Self.EngageSimulationPlayer = Button(label="Engage Simulation", style=Self.ButtonStyle, custom_id="EngageSimulationPlayer")
        Self.EngageSimulationPlayer.callback = Self._Initialize_Simulation
        Self.BaseViewFrame.add_item(Self.EngageSimulationPlayer)

        Self.HomepageButton = Button(label="Home", style=DiscordButtonStyle.grey, row=3, custom_id="HomePageButton")
        Self.HomepageButton.callback = lambda Interaction: Self.PlayPanel._Construct_Home(Self.Ether, Self.InitialContext, Interaction)
        Self.BaseViewFrame.add_item(Self.HomepageButton)


        Self.PlayerUUIDSubmission = Modal(title="Submit Player UUID")
        Self.PlayerUUIDSubmission.on_submit = lambda Interaction: Self._Reset_Player(Interaction, int(Self.PlayerSubmittedUUID.value))
        Self.PlayerSubmittedUUID = TextInput(label="Player UUID") 
        Self.PlayerUUIDSubmission.add_item(Self.PlayerSubmittedUUID)

        Self.Ether.Logger.info(f"Sent Debug panel to {Self.Player.Data['Name']}")
        await Self._Send_New_Panel(Self.Interaction)


    async def _Initialize_Simulation(Self, Interaction:DiscordInteraction) -> None:
        if await Self.Ether.Engage_Simulation() == True:
            Self.EmbedFrame.clear_fields()
            await Self._Generate_Info(Self.Ether, Self.InitialContext)
            Self.EmbedFrame.description += "**You have started a simulation**"
        else:
            Self.EmbedFrame.description += "**Something went wrong went engaging simulation**"
        Self.Ether.Logger.info(f"{Self.Player.Data['Name']} started the simulation")
        await Self._Send_New_Panel(Interaction)


    async def _Reset_Player(Self, Interaction, SubmittedUUID):
        if Self.Interaction.user != Self.InitialContext.author:
            return
        if Self.Ether.Data["Players"][Self.InitialContext.author.id].Data["Team"] == "Analis":
            Choice = "Analis"
        if Self.Ether.Data["Players"][Self.InitialContext.author.id].Data["Team"] == "Titan":
            Choice = "Titan"
        Self.Ether.Data["Planets"][Choice].Data["Protector Count"] -= 1
        await Self.Ether.Data["Players"][SubmittedUUID].Data["Member Object"].remove_roles(Self.Ether.Roles[Choice])
        Self.Ether.Data["Players"][SubmittedUUID] = None
        Self.Ether.Data["Players"].pop(SubmittedUUID)
        remove(join("Data", "PlayerData", f"{SubmittedUUID}.data.roc"))
        remove(join("Data", "PlayerInventories", f"{SubmittedUUID}.inventory.roc"))
        remove(join("Data", "PlayerProductionFacilities", f"{SubmittedUUID}.production.roc"))
        remove(join("Data", "PlayerArmy", f"{SubmittedUUID}.army.roc"))

        Self.Ether.Logger.info(f"{Self.Player.Data['Name']} reset ID:{SubmittedUUID}")
        await Self._Send_New_Panel(Interaction)