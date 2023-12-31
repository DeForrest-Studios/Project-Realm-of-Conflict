from asyncio import create_task
from RealmOfConflict import RealmOfConflict
from discord.ext.commands import Context as DiscordContext
from discord import Interaction as DiscordInteraction
from discord import ButtonStyle as DiscordButtonStyle
from discord import SelectOption, Embed
from discord.ui import View, Select, Button
from Panels.Panel import Panel
from Player import Player

class SkillsPanel(Panel):
    def __init__(Self, Ether:RealmOfConflict, InitialContext:DiscordContext, ButtonStyle, Interaction:DiscordInteraction, PlayPanel):
        super().__init__()
        create_task(Self._Construct_Panel(Ether, InitialContext, ButtonStyle, Interaction, PlayPanel))

    async def _Construct_Panel(Self, Ether, InitialContext, ButtonStyle, Interaction:DiscordInteraction, PlayPanel):
        if Interaction.user != InitialContext.author:
            return
        Self.Player:Player = Ether.Data['Players'][InitialContext.author.id]
        Self.BaseViewFrame = View(timeout=144000)
        Self.EmbedFrame = Embed(title=f"{Self.Player.Data['Name']}'s Skill Panel")
        await Self._Generate_Info(Ether, InitialContext, Inclusions=["Skill Points", "General Skill", "Offensive Skill",
                                                                     "Defensive Skill", "Counter Operations Skill"])

        Self.GeneralSkillsButton = Button(label="General Skills", style=ButtonStyle, custom_id="GeneralSkillsButton")
        Self.GeneralSkillsButton.callback = lambda Interaction: ...
        Self.BaseViewFrame.add_item(Self.GeneralSkillsButton)

        Self.OffensiveSkill = Button(label="Offensive Skill", style=ButtonStyle, custom_id="OffensiveSkill")
        Self.OffensiveSkill.callback = lambda Interaction: ...
        Self.BaseViewFrame.add_item(Self.OffensiveSkill)

        Self.DefensiveSkill = Button(label="Defensive Skill", style=ButtonStyle, custom_id="DefensiveSkill")
        Self.DefensiveSkill.callback = lambda Interaction: ...
        Self.BaseViewFrame.add_item(Self.DefensiveSkill)

        Self.CounterOperationsSkill = Button(label="Counter Operations Skill", style=ButtonStyle, custom_id="CounterOperationsSkill")
        Self.CounterOperationsSkill.callback = lambda Interaction: ...
        Self.BaseViewFrame.add_item(Self.CounterOperationsSkill)

        Self.HomepageButton = Button(label="Home", style=DiscordButtonStyle.grey, row=3, custom_id="HomePageButton")
        # This is a bad callback. This is really bad, I'm well aware. But you know what, fuck it.
        Self.HomepageButton.callback = lambda Interaction: PlayPanel._Construct_Home(Ether, InitialContext, Interaction)
        Self.BaseViewFrame.add_item(Self.HomepageButton)

        await Self._Send_New_Panel(Interaction)