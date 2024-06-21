from RealmOfConflict import RealmOfConflict
from discord.ext.commands import Context as DiscordContext
from discord import Interaction as DiscordInteraction
from discord import ButtonStyle as DiscordButtonStyle
from discord.ui import Button
from Panels.Panel import Panel

class BankingPanel(Panel):
    def __init__(Self, Ether:RealmOfConflict, InitialContext:DiscordContext, ButtonStyle, Interaction:DiscordInteraction, PlayPanel):
        super().__init__(Ether, InitialContext,
                         PlayPanel, "Banking",
                         Interaction=Interaction, ButtonStyle=ButtonStyle)

    async def _Construct_Panel(Self):
        if Self.Interaction.user != Self.InitialContext.author: return
        await Self._Generate_Info(Self.Ether, Self.InitialContext)

        BankingString = ""

        Self.EmbedFrame.description += BankingString
 
        Self.HomepageButton = Button(label="Home", style=DiscordButtonStyle.grey, row=3, custom_id="HomePageButton")
        Self.HomepageButton.callback = lambda Interaction: Self.PlayPanel._Construct_Home(Self.Ether, Self.InitialContext, Interaction)
        Self.BaseViewFrame.add_item(Self.HomepageButton)

        Self.Ether.Logger.info(f"Sent Banking panel to {Self.Player.Data['Name']}")
        await Self._Send_New_Panel(Self.Interaction)