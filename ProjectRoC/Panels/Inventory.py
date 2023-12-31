from asyncio import create_task
from RealmOfConflict import RealmOfConflict
from discord.ext.commands import Context as DiscordContext
from discord import Interaction as DiscordInteraction
from discord import ButtonStyle as DiscordButtonStyle
from discord import SelectOption, Embed
from discord.ui import View, Select, Button
from Panels.Panel import Panel
from time import time as Time

class InventoryPanel(Panel):
    def __init__(Self, Ether:RealmOfConflict, InitialContext:DiscordContext, ButtonStyle, Interaction:DiscordInteraction, PlayPanel):
        super().__init__()
        create_task(Self._Construct_Panel(Ether, InitialContext, ButtonStyle, Interaction, PlayPanel))

    async def _Construct_Panel(Self, Ether, InitialContext, ButtonStyle, Interaction:DiscordInteraction, PlayPanel):
        if Interaction.user != InitialContext.author:
            return
        Self.Player = Ether.Data['Players'][InitialContext.author.id]
        Self.BaseViewFrame = View(timeout=144000)
        Self.EmbedFrame = Embed(title=f"{InitialContext.author.name}'s Inventory Panel")

        InventoryString = ""

        PlayerInventoryLength = len(Self.Player.Inventory.items()) - 1
        Index:int
        Name:str
        Amount:float
        for Index, (Name, Amount) in enumerate(Self.Player.Inventory.items()):
            if Index == PlayerInventoryLength:
                InventoryString += f"{Amount} {Name}"
            else:
                InventoryString += f"{Amount} {Name}\n"

        await Self._Generate_Info(Ether, InitialContext, Exclusions=["Team", "Power"])

        Self.EmbedFrame.add_field(name="Inventory", value=InventoryString)

        Self.HomepageButton = Button(label="Home", style=DiscordButtonStyle.grey, row=3, custom_id="HomePageButton")
        # This is a bad callback. This is really bad, I'm well aware. But you know what, fuck it.
        Self.HomepageButton.callback = lambda Interaction: PlayPanel._Construct_Home(Ether, InitialContext, Interaction)
        Self.BaseViewFrame.add_item(Self.HomepageButton)

        Ether.Logger.info(f"Sent Inventory panel to {Self.Player.Data['Name']}")

        await Self._Send_New_Panel(Interaction)