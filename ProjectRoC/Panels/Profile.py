from RealmOfConflict import RealmOfConflict
from discord.ext.commands import Context as DiscordContext
from discord import Interaction as DiscordInteraction
from discord import ButtonStyle as DiscordButtonStyle
from discord import SelectOption, Embed
from discord.ui import View, Select, Button
from Panels.Panel import Panel
from Player import Player

class ProfilePanel(Panel):
    def __init__(Self, Ether:RealmOfConflict, InitialContext:DiscordContext, ButtonStyle, Interaction:DiscordInteraction, PlayPanel):
        super().__init__(Ether, InitialContext,
                         PlayPanel, "Profile",
                         Interaction=Interaction, ButtonStyle=ButtonStyle)

    async def _Construct_Panel(Self):
        if Self.Interaction.user != Self.InitialContext.author: return

        await Self._Generate_Info(Self.Ether, Self.InitialContext, Inclusions=["Skill Points", "Offensive Power", "Defensive Power", "Healing Power",
                                              "Production Power", "Manufacturing Power", "Energy Sapping",])

        Self.ChangeNicknameButton = Button(label="Change Nickname (WIP)", style=Self.ButtonStyle, custom_id="ChangeNicknameButton")
        Self.ChangeNicknameButton.callback = lambda Interaction: Self._Construct_Army_Panel(Interaction=Interaction)
        Self.BaseViewFrame.add_item(Self.ChangeNicknameButton)

        Self.HomepageButton = Button(label="Home", style=DiscordButtonStyle.grey, row=3, custom_id="HomePageButton")
        # This is a bad callback. This is really bad, I'm well aware. But you know what, fuck it.
        Self.HomepageButton.callback = lambda Interaction: Self.PlayPanel._Construct_Home(Self.Ether, Self.InitialContext, Interaction)
        Self.BaseViewFrame.add_item(Self.HomepageButton)

        Self.Ether.Logger.info(f"Sent Profile panel to {Self.Player.Data['Name']}")
        await Self._Send_New_Panel(Self.Interaction)