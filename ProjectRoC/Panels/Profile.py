from asyncio import create_task
from RealmOfConflict import RealmOfConflict
from discord.ext.commands import Context as DiscordContext
from discord import Interaction as DiscordInteraction
from discord import ButtonStyle as DiscordButtonStyle
from discord import SelectOption, Embed
from discord.ui import View, Select, Button
from Panels.Panel import Panel

class ProfilePanel(Panel):
    def __init__(Self, Ether:RealmOfConflict, InitialContext:DiscordContext, ButtonStyle, Interaction:DiscordInteraction, PlayPanel):
        super().__init__()
        create_task(Self._Construct_Panel(Ether, InitialContext, ButtonStyle, Interaction, PlayPanel))

    async def _Construct_Panel(Self, Ether, InitialContext, ButtonStyle, Interaction:DiscordInteraction, PlayPanel):
        Self.Player = Ether.Data['Players'][InitialContext.author.id]
        Self.BaseViewFrame = View(timeout=144000)
        Self.EmbedFrame = Embed(title=f"{Self.Player.Data['Name']}'s Profile Panel")
        await Self._Generate_Info(Ether, InitialContext, Inclusions=["Offensive Power", "Defensive Power", "Healing Power",
                                              "Production Power", "Manufacturing Power", "Energy Sapping",])

        Self.ChangeNicknameButton = Button(label="Change Nickname", style=ButtonStyle, custom_id="ChangeNicknameButton")
        Self.ChangeNicknameButton.callback = lambda Interaction: Self._Construct_Army_Panel(Interaction=Interaction)
        Self.BaseViewFrame.add_item(Self.ChangeNicknameButton)

        Self.HomepageButton = Button(label="Home", style=DiscordButtonStyle.grey, row=3, custom_id="HomePageButton")
        # This is a bad callback. This is really bad, I'm well aware. But you know what, fuck it.
        Self.HomepageButton.callback = lambda Interaction: PlayPanel._Construct_Home(Ether, InitialContext, Interaction)
        Self.BaseViewFrame.add_item(Self.HomepageButton)

        await Self._Send_New_Panel(Interaction)