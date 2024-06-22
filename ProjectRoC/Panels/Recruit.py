from RealmOfConflict import RealmOfConflict
from discord.ext.commands import Context as DiscordContext
from discord import Interaction as DiscordInteraction
from discord import ButtonStyle as DiscordButtonStyle
from discord import SelectOption, Embed
from discord.ui import View, Select, Button, Modal, TextInput
from Panels.Panel import Panel
from Tables import InfantryTable, InfantryToObject
from Player import Player

class RecruitPanel(Panel):
    def __init__(Self, Ether:RealmOfConflict, InitialContext:DiscordContext,
                 ButtonStyle:DiscordButtonStyle, Interaction:DiscordInteraction,
                 PlayPanel, SententsPanel, Emoji):
        super().__init__(Ether, InitialContext,
                         PlayPanel, "Recruit",
                         Interaction=Interaction, ButtonStyle=ButtonStyle, Emoji=Emoji)
        Self.SententsPanel = SententsPanel
        Self.InfantrySelected = None

    async def _Construct_Panel(Self, Interaction=None, InfantryRecruited=False):
        if Self.Interaction.user.id in Self.Ether.Whitelist: pass
        elif Self.Interaction.user != Self.InitialContext.author: return
        
        Self.BaseViewFrame = View(timeout=144000)
        Self.PanelTitle = f"{Self.Player.Data['Name']}'s Recruit Panel"
        Self.EmbedFrame = Embed(title=Self.Emoji*2 + Self.PanelTitle + Self.Emoji*2)

        if Interaction == None:
            await Self._Generate_Info(Self.Ether, Self.InitialContext)

            Self.RecruitButton = Button(label="Recruit Selection", style=Self.ButtonStyle,
                                        row=0, custom_id="RecruitButton")
            Self.RecruitButton.callback = lambda Interaction: Self._Construct_Panel(Interaction=Interaction, InfantryRecruited=True)
            Self.BaseViewFrame.add_item(Self.RecruitButton)

            Self.InfantyChoices = [SelectOption(label=f"{Infantry} for ${Worth}") for Infantry, Worth in InfantryTable.items()]
            Self.InfantryChoice = Select(placeholder="Select an Infantry", options=Self.InfantyChoices,
                                        row=1, custom_id=f"InfantrySelection")
            Self.InfantryChoice.callback = lambda Interaction: Self._Select_Item(Interaction=Interaction, InfantrySelected=Interaction.data["values"][0])
            Self.BaseViewFrame.add_item(Self.InfantryChoice)

            Self.SententsButton = Button(label="Return to Sentents", style=Self.ButtonStyle,
                                        row=2, custom_id="SententsButton")
            Self.SententsButton.callback = lambda Interaction: Self.SententsPanel.__ainit__(Self.Ether, Self.InitialContext, Self.ButtonStyle, Interaction, Self.PlayPanel)
            Self.BaseViewFrame.add_item(Self.SententsButton)

            Self.HomepageButton = Button(label="Home", style=DiscordButtonStyle.grey,
                                        row=3, custom_id="HomePageButton")
            Self.HomepageButton.callback = lambda Interaction: Self.PlayPanel._Construct_Home(Self.Ether, Self.InitialContext, Interaction)
            Self.BaseViewFrame.add_item(Self.HomepageButton)
        else:
            Self.Interaction = Interaction
        
        if Self.InfantrySelected:
            Self.InfantryChoice.placeholder = Self.InfantrySelected

        if InfantryRecruited == True:
            if Self.InfantrySelected == None:
                Self.EmbedFrame.description += f"\nYou have nothing selected"
                await Self._Send_New_Panel(Interaction)
                return
            InfantryKey = Self.InfantrySelected.split(" for ")[0]
            if Self.Player.Data["Wallet"] >= InfantryTable[InfantryKey]:
                Self.Player.Data["Wallet"] = round(Self.Player.Data["Wallet"] - InfantryTable[InfantryKey], 2)
                Self.EmbedFrame.add_field(name=f"Purchased {Self.InfantrySelected} for {InfantryTable[InfantryKey]}", value="\u200b")
                InfantryData = InfantryKey.split(" ~ ")
                InfantryLevel = int(InfantryData[0].split(" ")[1])
                InfantryType = InfantryData[1]
                NewInfantry = InfantryToObject[InfantryType](InfantryLevel, InfantryType, Self.Player)
                print(NewInfantry.Tier)
                Self.Player.Army.update({NewInfantry.Name:NewInfantry})
                Self.Player.Refresh_Power()
                Self.EmbedFrame.clear_fields()
                await Self._Generate_Info(Self.Ether, Self.InitialContext)
                Self.EmbedFrame.add_field(name=f"Recruited {NewInfantry.Name}", value="\u200b")
            else:
                Self.EmbedFrame.clear_fields()
                await Self._Generate_Info(Self.Ether, Self.InitialContext)
                Self.EmbedFrame.add_field(name=f"Insufficient Funds", value="\u200b")

        Self.Ether.Logger.info(f"Sent Recruit panel to {Self.Player.Data['Name']}")
        await Self._Send_New_Panel(Self.Interaction)

    async def _Select_Item(Self, Interaction:DiscordInteraction, InfantrySelected):
        Self.InfantrySelected:str = InfantrySelected
        await Self._Construct_Panel(Interaction)
