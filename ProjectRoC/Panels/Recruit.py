from asyncio import create_task
from RealmOfConflict import RealmOfConflict
from discord.ext.commands import Context as DiscordContext
from discord import Interaction as DiscordInteraction
from discord import ButtonStyle as DiscordButtonStyle
from discord import SelectOption, Embed
from discord.ui import View, Select, Button, Modal, TextInput
from Panels.Panel import Panel
from Tables import InfantryTable, InfantryToObject

class RecruitPanel(Panel):
    def __init__(Self, Ether:RealmOfConflict, InitialContext:DiscordContext, ButtonStyle, Interaction:DiscordInteraction, PlayPanel):
        super().__init__()
        create_task(Self._Construct_Panel(Ether, InitialContext, ButtonStyle, Interaction, PlayPanel))


    async def _Construct_Panel(Self, Ether:RealmOfConflict, InitialContext:DiscordContext, ButtonStyle, Interaction:DiscordInteraction, PlayPanel, InfantrySelected=None, InfantryRecruited=None):
        if InfantrySelected == None:
            Self.BaseViewFrame = View(timeout=144000)
            Self.EmbedFrame = Embed(title=f"{Ether.Data['Players'][InitialContext.author.id].Data['Name']}'s Recruit Panel")
            await Self._Generate_Info(Ether, InitialContext)

            Self.RecruitButton = Button(label="Recruit", style=ButtonStyle, custom_id="RecruitButton")
            Self.RecruitButton.callback = lambda Interaction: Self._Construct_Panel(Ether, InitialContext, ButtonStyle, Interaction, PlayPanel, Self.InfantrySelected, Self.InfantrySelected)
            Self.BaseViewFrame.add_item(Self.RecruitButton)

            Self.InfantyChoices = [SelectOption(label=f"{Infantry} for ${Worth}") for Infantry, Worth in InfantryTable.items()]
            Self.InfantryChoice = Select(placeholder="Select an Infantry", options=Self.InfantyChoices, custom_id=f"InfantrySelection", row=2)
            Self.BaseViewFrame.add_item(Self.InfantryChoice)

            Self.HomepageButton = Button(label="Home", style=DiscordButtonStyle.grey, row=3, custom_id="HomePageButton")
            # This is a bad callback. This is really bad, I'm well aware. But you know what, fuck it.
            Self.HomepageButton.callback = lambda Interaction: PlayPanel._Construct_Home(Ether, InitialContext, Interaction)
            Self.BaseViewFrame.add_item(Self.HomepageButton)
        
        if InfantrySelected:
            Self.InfantrySelected = InfantrySelected
            Self.InfantryChoice.placeholder = InfantrySelected

        if InfantryRecruited:
            InfantryKey = Self.InfantrySelected.split(" for ")[0]
            if Ether.Data['Players'][InitialContext.author.id].Data["Wallet"] >= InfantryTable[InfantryKey]:
                Ether.Data['Players'][InitialContext.author.id].Data["Wallet"] = round(Ether.Data['Players'][InitialContext.author.id].Data["Wallet"] - InfantryTable[InfantryKey], 2)
                Self.EmbedFrame.add_field(name=f"Purchased {Self.InfantrySelected} for {InfantryTable[InfantryKey]}", value="\u200b")
                InfantryData = InfantryKey.split(" ~ ")
                InfantryLevel = int(InfantryData[0].split(" ")[1])
                InfantryType = InfantryData[1]
                NewInfantry = InfantryToObject[InfantryType](InfantryLevel, InfantryType, Ether.Data['Players'][InitialContext.author.id])
                Ether.Data['Players'][InitialContext.author.id].Army.update({NewInfantry.Name:NewInfantry})
                Ether.Data['Players'][InitialContext.author.id].Refresh_Power()
                Self.EmbedFrame.clear_fields()
                await Self._Generate_Info(Ether, InitialContext)
                Self.EmbedFrame.add_field(name=f"Recruited {NewInfantry.Name}", value="\u200b")
            else:
                Self.EmbedFrame.clear_fields()
                await Self._Generate_Info(Ether, InitialContext)
                Self.EmbedFrame.add_field(name=f"Insufficient Funds", value="\u200b")
        Self.InfantryChoice.callback = lambda Interaction: Self._Construct_Panel(Ether, InitialContext, ButtonStyle, Interaction, PlayPanel, Interaction.data["values"][0])
        await Self._Send_New_Panel(Interaction)