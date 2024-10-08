from RealmOfConflict import RealmOfConflict
from discord.ext.commands import Context as DiscordContext
from discord import Interaction as DiscordInteraction
from discord import ButtonStyle as DiscordButtonStyle
from discord import Embed
from discord.ui import Button, View
from Panels.Panel import Panel
from Panels.Recruit import RecruitPanel
from Panels.Army import ArmyPanel

class SententPanel(Panel):
    def __init__(Self, Ether:RealmOfConflict, InitialContext:DiscordContext,
                 ButtonStyle:DiscordButtonStyle, Interaction:DiscordInteraction,
                 PlayPanel, Emoji):
        super().__init__(Ether, InitialContext,
                         PlayPanel, "Sentents",
                         Interaction=Interaction, ButtonStyle=ButtonStyle, Emoji=Emoji)

    async def __ainit__(Self, Ether:RealmOfConflict, InitialContext:DiscordContext, # I'm sorry for this, but this is how the recruit panel,
                        ButtonStyle:DiscordButtonStyle, Interaction:DiscordInteraction, # and the army panel get back to the sentent panel
                        PlayPanel, Emoji):
        super().__init__(Ether, InitialContext,
                         PlayPanel, "Sentents",
                         Interaction=Interaction, ButtonStyle=ButtonStyle, Emoji=Emoji)

    async def _Construct_Panel(Self):
        if Self.Interaction.user.id in Self.Ether.Whitelist: pass
        elif Self.Interaction.user != Self.InitialContext.author: return

        Self.BaseViewFrame = View(timeout=144000)
        Self.PanelTitle = f"{Self.Player.Data['Name']}'s Sentent Panel"
        Self.EmbedFrame = Embed(title=Self.Emoji*2 + Self.PanelTitle + Self.Emoji*2)

        await Self._Generate_Info(Self.Ether, Self.InitialContext)

        Self.ArmyButton = Button(label="My Army", style=Self.ButtonStyle, custom_id="ArmyButton")
        Self.ArmyButton.callback = lambda Interaction: Self._Construct_New_Panel(Interaction)
        Self.BaseViewFrame.add_item(Self.ArmyButton)

        Self.RecruitButton = Button(label="Recruit", style=Self.ButtonStyle, custom_id="RecruitButton")
        Self.RecruitButton.callback = lambda Interaction: Self._Construct_New_Panel(Interaction)
        Self.BaseViewFrame.add_item(Self.RecruitButton)

        Self.HomepageButton = Button(label="Home", style=DiscordButtonStyle.grey, row=3, custom_id="HomePageButton")
        Self.HomepageButton.callback = lambda Interaction: Self.PlayPanel._Construct_Home(Self.Ether, Self.InitialContext, Interaction)
        Self.BaseViewFrame.add_item(Self.HomepageButton)

        Self.Ether.Logger.info(f"Sent Sentents panel to {Self.Player.Data['Name']}")
        await Self._Send_New_Panel(Self.Interaction)


    async def _Construct_New_Panel(Self, Interaction:DiscordInteraction):
        Mapping = {
            "ArmyButton":ArmyPanel,
            "RecruitButton":RecruitPanel,
        }
        Self.Ether.Data["Panels"][Self.InitialContext.author.id] = Mapping[Interaction.data["custom_id"]](Self.Ether, Self.InitialContext,
                                                                                                          Self.ButtonStyle, Interaction,
                                                                                                          Self.PlayPanel, Self, Self.Emoji)
