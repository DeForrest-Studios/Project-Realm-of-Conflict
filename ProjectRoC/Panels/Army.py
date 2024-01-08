from RealmOfConflict import RealmOfConflict
from discord.ext.commands import Context as DiscordContext
from discord import Interaction as DiscordInteraction
from discord import ButtonStyle as DiscordButtonStyle
from discord.ui import Button
from Panels.Panel import Panel

class ArmyPanel(Panel):
    def __init__(Self, Ether:RealmOfConflict, InitialContext:DiscordContext,
                 ButtonStyle:DiscordButtonStyle, Interaction:DiscordInteraction,
                 PlayPanel, SententsPanel):
        super().__init__(Ether, InitialContext,
                         PlayPanel, "Army",
                         Interaction=Interaction, ButtonStyle=ButtonStyle)
        Self.SententsPanel = SententsPanel

    async def _Construct_Panel(Self):
        if Self.Interaction.user != Self.InitialContext.author: return
        await Self._Generate_Info(Self.Ether, Self.InitialContext)

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

        Self.NextPageButton = Button(label="Next Page", style=Self.ButtonStyle,
                                     row=0, custom_id="NextPageButton")
        Self.NextPageButton.callback = lambda Interaction: ...
        Self.BaseViewFrame.add_item(Self.NextPageButton)

        Self.PreviousPageButton = Button(label="Previous Page", style=Self.ButtonStyle,
                                         row=0, custom_id="PreviousPageButton")
        Self.PreviousPageButton.callback = lambda Interaction: ...
        Self.BaseViewFrame.add_item(Self.PreviousPageButton)

        Self.SententsButton = Button(label="Return to Sentents", style=Self.ButtonStyle,
                                     row=2, custom_id="SententsButton")
        Self.SententsButton.callback = lambda Interaction: Self.SententsPanel.__ainit__(Self.Ether, Self.InitialContext, Self.ButtonStyle, Interaction, Self.PlayPanel)
        Self.BaseViewFrame.add_item(Self.SententsButton)

        Self.HomepageButton = Button(label="Home", style=DiscordButtonStyle.grey,
                                     row=3, custom_id="HomePageButton")
        # This is a bad callback. This is really bad, I'm well aware. But you know what, fuck it.
        Self.HomepageButton.callback = lambda Interaction: Self.PlayPanel._Construct_Home(Self.Ether, Self.InitialContext, Interaction)
        Self.BaseViewFrame.add_item(Self.HomepageButton)

        Self.Ether.Logger.info(f"Sent Army panel to {Self.Player.Data['Name']}")
        await Self._Send_New_Panel(Self.Interaction)