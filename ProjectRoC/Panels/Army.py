from RealmOfConflict import RealmOfConflict
from discord.ext.commands import Context as DiscordContext
from discord import Interaction as DiscordInteraction
from discord import ButtonStyle as DiscordButtonStyle
from discord.ui import Button
from Panels.Panel import Panel
from discord import Embed
from discord.ui import View
from asyncio import create_task

class ArmyPanel(Panel):
    def __init__(Self, Ether:RealmOfConflict, InitialContext:DiscordContext,
                 ButtonStyle:DiscordButtonStyle, Interaction:DiscordInteraction,
                 PlayPanel, SententsPanel):
        super().__init__(Ether, InitialContext,
                         PlayPanel, "Army",
                         Interaction=Interaction, ButtonStyle=ButtonStyle)
        Self.SententsPanel = SententsPanel
        Self.Index = 0
        Self.Pages = []

    async def Iterate_Index(Self, Interaction, Direction):
        if Direction == "Forward":
            if Self.Index+1 < (len(Self.Pages)):
                Self.Index += 1
        if Direction == "Backward":
            if Self.Index-1 >= 0:
                Self.Index -= 1
        await Self._Construct_Panel(Interaction)


    async def _Construct_Panel(Self, GivenInteraction=None):
        if Self.Interaction.user != Self.InitialContext.author: return
        
        Self.BaseViewFrame = View(timeout=144000)
        Self.EmbedFrame = Embed(title=f"{Self.Player.Data['Name']}'s Avargo Sale Panel")
        await Self._Generate_Info(Self.Ether, Self.InitialContext)

        if GivenInteraction != None: Self.Interaction = GivenInteraction

        ArmyString = ""
        if len(Self.Player.Army.values()) > 5:
            Divider = len(Self.Player.Army.values())//5
            if len(Self.Player.Army.values()) % Divider != 0:
                Divider += 1

        Self.Pages = []
        PlayerArmy = [Sentent for Sentent in Self.Player.Army.values()]
        while len(PlayerArmy) != 0:
            if len(PlayerArmy) >= 5:
                Self.Pages.append(PlayerArmy[0:5])
                PlayerArmy = PlayerArmy[5:]
            else:
                Self.Pages.append(PlayerArmy)
                PlayerArmy = []

        Name:str
        Sentent:object
        for Sentent in Self.Pages[Self.Index]:
            if len(ArmyString) + 36 >= 1024:
                print("Pagintion Required")
                break
            ArmyString += f"{Sentent.Name} ~ Tier {Sentent.Tier} ~ Level {Sentent.Level} ~ {Sentent.Type}\n"
            
            if hasattr(Sentent, "OffensivePower"):
                ArmyString += f"Offensive Power:{Sentent.OffensivePower}\n"
            if hasattr(Sentent, "DefensivePower"):
                ArmyString += f"Defensive Power:{Sentent.DefensivePower}\n"
            if hasattr(Sentent, "HealingPower"):
                ArmyString += f"Healing Power:{Sentent.HealingPower}\n"
            
            ArmyString += "\n"

        Self.EmbedFrame.add_field(name="\u200b", value=ArmyString, inline=False)

        Self.NextPageButton = Button(label="Next Page", style=Self.ButtonStyle,
                                     row=0, custom_id="NextPageButton")
        Self.NextPageButton.callback = lambda Interaction:Self.Iterate_Index(Interaction, "Forward")
        Self.BaseViewFrame.add_item(Self.NextPageButton)

        Self.PreviousPageButton = Button(label="Previous Page", style=Self.ButtonStyle,
                                         row=0, custom_id="PreviousPageButton")
        Self.PreviousPageButton.callback = lambda Interaction:Self.Iterate_Index(Interaction, "Backward")
        Self.BaseViewFrame.add_item(Self.PreviousPageButton)

        Self.SententsButton = Button(label="Return to Sentents", style=Self.ButtonStyle,
                                     row=2, custom_id="SententsButton")
        Self.SententsButton.callback = lambda Interaction: Self.SententsPanel.__ainit__(Self.Ether, Self.InitialContext, Self.ButtonStyle, Interaction, Self.PlayPanel)
        Self.BaseViewFrame.add_item(Self.SententsButton)

        Self.HomepageButton = Button(label="Home", style=DiscordButtonStyle.grey,
                                     row=3, custom_id="HomePageButton")
        Self.HomepageButton.callback = lambda Interaction: Self.PlayPanel._Construct_Home(Self.Ether, Self.InitialContext, Interaction)
        Self.BaseViewFrame.add_item(Self.HomepageButton)

        Self.Ether.Logger.info(f"Sent Army panel to {Self.Player.Data['Name']}")
        await Self._Send_New_Panel(Self.Interaction)