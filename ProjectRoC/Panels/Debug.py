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

        Self.HomepageButton = Button(label="Home", style=DiscordButtonStyle.grey, row=3, custom_id="HomePageButton")
        # This is a bad callback. This is really bad, I'm well aware. But you know what, fuck it.
        Self.HomepageButton.callback = lambda Interaction: Self.PlayPanel._Construct_Home(Self.Ether, Self.InitialContext, Interaction)
        Self.BaseViewFrame.add_item(Self.HomepageButton)


        Self.PlayerUUIDSubmission = Modal(title="Submit Player UUID")
        Self.PlayerUUIDSubmission.on_submit = lambda Interaction: Self._Reset_Player(Interaction, int(Self.PlayerSubmittedUUID.value))
        Self.PlayerSubmittedUUID = TextInput(label="Player UUID") 
        Self.PlayerUUIDSubmission.add_item(Self.PlayerSubmittedUUID)


        await Self._Send_New_Panel(Self.Interaction)


    async def _Reset_Player(Self, Interaction, SubmittedUUID):
        if Self.Interaction.user != Self.InitialContext.author:
            return
        if Self.Ether.Data["Players"][Self.InitialContext.author.id].Data["Team"] == "Analis":
            await Self.Ether.Data["Players"][SubmittedUUID].Data["Member Object"].remove_roles(Self.Ether.Roles["Analis"])
        if Self.Ether.Data["Players"][Self.InitialContext.author.id].Data["Team"] == "Titan":
            await Self.Ether.Data["Players"][SubmittedUUID].Data["Member Object"].remove_roles(Self.Ether.Roles["Titan"])
        Self.Ether.Data["Players"][SubmittedUUID] = None
        Self.Ether.Data["Players"].pop(SubmittedUUID)
        remove(join("Data", "PlayerData", f"{SubmittedUUID}.data.roc"))
        remove(join("Data", "PlayerInventories", f"{SubmittedUUID}.inventory.roc"))
        remove(join("Data", "PlayerProductionFacilities", f"{SubmittedUUID}.production.roc"))
        remove(join("Data", "PlayerArmy", f"{SubmittedUUID}.army.roc"))

        await Self._Send_New_Panel(Interaction)