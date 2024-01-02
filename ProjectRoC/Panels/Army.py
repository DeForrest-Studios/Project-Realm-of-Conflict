from asyncio import create_task
from RealmOfConflict import RealmOfConflict
from discord.ext.commands import Context as DiscordContext
from discord import Interaction as DiscordInteraction
from discord import ButtonStyle as DiscordButtonStyle
from discord import Embed
from discord.ui import View, Button
from Panels.Panel import Panel
from time import time as Time

class ArmyPanel(Panel):
    def __init__(Self, Ether:RealmOfConflict, InitialContext:DiscordContext, ButtonStyle, Interaction:DiscordInteraction, PlayPanel):
        super().__init__()
        create_task(Self._Construct_Panel(Ether, InitialContext, ButtonStyle, Interaction, PlayPanel))

    async def _Construct_Panel(Self, Ether, InitialContext, ButtonStyle, Interaction:DiscordInteraction, PlayPanel):
        if Interaction.user != InitialContext.author:
            return
        Self.PlayPanel = PlayPanel
        Self.Player = Ether.Data['Players'][InitialContext.author.id]
        Self.BaseViewFrame = View(timeout=144000)
        Self.EmbedFrame = Embed(title=f"{Self.Player.Data['Name']}'s Army Panel")
        await Self._Generate_Info(Ether, InitialContext)

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

        Self.NextPageButton = Button(label="Next Page", style=ButtonStyle, custom_id="NextPageButton")
        Self.NextPageButton.callback = lambda Interaction: ...
        Self.BaseViewFrame.add_item(Self.NextPageButton)

        Self.PreviousPageButton = Button(label="Previous Page", style=ButtonStyle, custom_id="PreviousPageButton")
        Self.PreviousPageButton.callback = lambda Interaction: ...
        Self.BaseViewFrame.add_item(Self.PreviousPageButton)

        Self.HomepageButton = Button(label="Home", style=DiscordButtonStyle.grey, row=3, custom_id="HomePageButton")
        # This is a bad callback. This is really bad, I'm well aware. But you know what, fuck it.
        Self.HomepageButton.callback = lambda Interaction: PlayPanel._Construct_Home(Ether, InitialContext, Interaction)
        Self.BaseViewFrame.add_item(Self.HomepageButton)

        await Self._Send_New_Panel(Interaction)