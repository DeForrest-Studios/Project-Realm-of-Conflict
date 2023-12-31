from asyncio import create_task
from RealmOfConflict import RealmOfConflict
from discord.ext.commands import Context as DiscordContext
from discord import Interaction as DiscordInteraction
from discord import ButtonStyle as DiscordButtonStyle
from discord import SelectOption, Embed
from discord.ui import View, Select, Button, Modal, TextInput
from Panels.Panel import Panel
from Panels.Recruit import RecruitPanel
from Panels.Army import ArmyPanel

class SententPanel(Panel):
    def __init__(Self, Ether:RealmOfConflict, InitialContext:DiscordContext, ButtonStyle, Interaction:DiscordInteraction, PlayPanel):
        super().__init__()
        create_task(Self._Construct_Panel(Ether, InitialContext, ButtonStyle, Interaction, PlayPanel))


    async def _Construct_Panel(Self, Ether:RealmOfConflict, InitialContext:DiscordContext, ButtonStyle, Interaction:DiscordInteraction, PlayPanel):
        if Interaction.user != InitialContext.author:
            return
        Self.PlayPanel = PlayPanel
        Self.Player = Ether.Data['Players'][InitialContext.author.id]
        Self.BaseViewFrame = View(timeout=144000)
        Self.EmbedFrame = Embed(title=f"{Self.Player.Data['Name']}'s Sentents Panel")
        await Self._Generate_Info(Ether, InitialContext)

        Self.ArmyButton = Button(label="My Army", style=ButtonStyle, custom_id="ArmyButton")
        Self.ArmyButton.callback = lambda Interaction: Self._Construct_New_Panel(Ether, InitialContext, ButtonStyle, Interaction, PlayPanel)
        Self.BaseViewFrame.add_item(Self.ArmyButton)

        Self.RecruitButton = Button(label="Recruit", style=ButtonStyle, custom_id="RecruitButton")
        Self.RecruitButton.callback = lambda Interaction: Self._Construct_New_Panel(Ether, InitialContext, ButtonStyle, Interaction, PlayPanel)
        Self.BaseViewFrame.add_item(Self.RecruitButton)

        Self.HomepageButton = Button(label="Home", style=DiscordButtonStyle.grey, row=3, custom_id="HomePageButton")
        # This is a bad callback. This is really bad, I'm well aware. But you know what, fuck it.
        Self.HomepageButton.callback = lambda Interaction: PlayPanel._Construct_Home(Ether, InitialContext, Interaction)
        Self.BaseViewFrame.add_item(Self.HomepageButton)

        await Self._Send_New_Panel(Interaction)


    async def _Construct_New_Panel(Self, Ether:RealmOfConflict, InitialContext:DiscordContext, ButtonStyle, Interaction:DiscordInteraction, PlayPanel):
        Mapping:{str:Panel} = {
            "ArmyButton":ArmyPanel,
            "RecruitButton":RecruitPanel,
        }
        Ether.Data["Panels"][InitialContext.author.id] = Mapping[Interaction.data["custom_id"]](Ether, InitialContext, ButtonStyle, Interaction, PlayPanel)
