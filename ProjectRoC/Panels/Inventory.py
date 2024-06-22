from RealmOfConflict import RealmOfConflict
from discord.ext.commands import Context as DiscordContext
from discord import Interaction as DiscordInteraction
from discord import ButtonStyle as DiscordButtonStyle
from discord import Embed
from discord.ui import Button, View
from Panels.Panel import Panel

class InventoryPanel(Panel):
    def __init__(Self, Ether:RealmOfConflict, InitialContext:DiscordContext, ButtonStyle, Interaction:DiscordInteraction, PlayPanel, Emoji):
        super().__init__(Ether, InitialContext,
                         PlayPanel, "Inventory",
                         Interaction=Interaction, ButtonStyle=ButtonStyle, Emoji=Emoji)

    async def _Construct_Panel(Self):
        if Self.Interaction.user.id in Self.Ether.Whitelist: pass
        elif Self.Interaction.user != Self.InitialContext.author: return
        
        Self.BaseViewFrame = View(timeout=144000)
        Self.PanelTitle = f"{Self.Player.Data['Name']}'s Inventory Panel"
        Self.EmbedFrame = Embed(title=Self.Emoji*2 + Self.PanelTitle + Self.Emoji*2)

        await Self._Generate_Info(Self.Ether, Self.InitialContext)

        InventoryString = ""

        PlayerInventoryLength = len(Self.Player.Inventory.items()) - 1

        Index:int
        Name:str
        Amount:float
        for Index, (Name, Amount) in enumerate(Self.Player.Inventory.items()):
            FormattedAmount = str(Amount).split('.')
            InventoryString += f"**__{Name}__** ~ **{format(int(FormattedAmount[0]), ',')}**.{FormattedAmount[1]}"
            if Index != PlayerInventoryLength:
                InventoryString += "\n"


        # Self.EmbedFrame.add_field(name="Inventory", value=InventoryString)
        Self.EmbedFrame.description += InventoryString

        Self.HomepageButton = Button(label="Home", style=DiscordButtonStyle.grey, row=3, custom_id="HomePageButton")
        Self.HomepageButton.callback = lambda Interaction: Self.PlayPanel._Construct_Home(Self.Ether, Self.InitialContext, Interaction)
        Self.BaseViewFrame.add_item(Self.HomepageButton)

        Self.Ether.Logger.info(f"Sent Inventory panel to {Self.Player.Data['Name']}")
        await Self._Send_New_Panel(Self.Interaction)