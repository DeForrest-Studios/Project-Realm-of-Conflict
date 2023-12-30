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

class DebugPanel(Panel):
    def __init__(Self, Ether:RealmOfConflict, InitialContext:DiscordContext, ButtonStyle, Interaction:DiscordInteraction, PlayPanel):
        super().__init__()
        create_task(Self._Construct_Panel(Ether, InitialContext, ButtonStyle, Interaction, PlayPanel))

    async def _Construct_Panel(Self, Ether, InitialContext, ButtonStyle, Interaction:DiscordInteraction, PlayPanel):
        if Interaction.user != InitialContext.author:
            return
        Self.BaseViewFrame = View(timeout=144000)
        Self.EmbedFrame = Embed(title=f"{Ether.Data['Players'][InitialContext.author.id].Data['Name']}'s Debug Panel")

        await Self._Generate_Info(Ether, InitialContext)

        Self.ResetPlayer = Button(label="Reset Player", style=ButtonStyle, custom_id="ResetPlayerButton")
        Self.ResetPlayer.callback = lambda Interaction: Interaction.response.send_modal(Self.PlayerUUIDSubmission)
        Self.BaseViewFrame.add_item(Self.ResetPlayer)

        Self.HomepageButton = Button(label="Home", style=DiscordButtonStyle.grey, row=3, custom_id="HomePageButton")
        # This is a bad callback. This is really bad, I'm well aware. But you know what, fuck it.
        Self.HomepageButton.callback = lambda Interaction: PlayPanel._Construct_Home(Ether, InitialContext, Interaction)
        Self.BaseViewFrame.add_item(Self.HomepageButton)


        Self.PlayerUUIDSubmission = Modal(title="Submit Player UUID")
        Self.PlayerUUIDSubmission.on_submit = lambda Interaction: Self._Reset_Player(Interaction, int(Self.PlayerSubmittedUUID.value))
        Self.PlayerSubmittedUUID = TextInput(label="Player UUID") 
        Self.PlayerUUIDSubmission.add_item(Self.PlayerSubmittedUUID)


        await Self._Send_New_Panel(Interaction)


    async def _Reset_Player(Self, Ether, InitialContext, Interaction, SubmittedUUID):
        if Interaction.user != InitialContext.author:
            return
        if Ether.Data["Players"][InitialContext.author.id].Data["Team"] == "Analis":
            await Self.Ether.Data["Players"][SubmittedUUID].Data["Member Object"].remove_roles(Self.Ether.Roles["Analis"])
        if Ether.Data["Players"][InitialContext.author.id].Data["Team"] == "Titan":
            await Self.Ether.Data["Players"][SubmittedUUID].Data["Member Object"].remove_roles(Self.Ether.Roles["Titan"])
        Self.Ether.Data["Players"][SubmittedUUID] = None
        Self.Ether.Data["Players"].pop(SubmittedUUID)
        remove(join("Data", "PlayerData", f"{SubmittedUUID}.roc"))
        remove(join("Data", "PlayerInventories", f"{SubmittedUUID}.roc"))
        remove(join("Data", "PlayerProductionFacilities", f"{SubmittedUUID}.roc"))

        await Self._Send_New_Panel(Interaction)