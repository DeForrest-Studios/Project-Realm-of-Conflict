from discord import Interaction as DiscordInteraction
from discord import Message as DiscordMessage
from discord.ext.commands import Context as DiscordContext
from discord import ButtonStyle as DiscordButtonStyle
from discord import Embed
from discord.ui import View
from RealmOfConflict import RealmOfConflict
from Player import Player
from asyncio import create_task

class Panel:
    def __init__(Self, Ether:RealmOfConflict, InitialContext:DiscordContext,
                       PlayPanel, PanelType:str,
                       Interaction:DiscordInteraction=None, ButtonStyle:DiscordButtonStyle=None) -> None:
        
        Self.Ether:RealmOfConflict = Ether
        Self.InitialContext:DiscordContext = InitialContext
        Self.PlayPanel:Panel = PlayPanel
        Self.ButtonStyle:DiscordButtonStyle = ButtonStyle
        Self.Player:Player = Ether.Data['Players'][InitialContext.author.id]

        Self.BaseViewFrame = View(timeout=144000)
        Self.EmbedFrame = Embed(title=f"{Self.Player.Data['Name']}'s {PanelType} Panel")
        Ether.Data["Panels"].update({InitialContext.author.id:Self})
        if Interaction is not None:
            Self.Interaction:DiscordInteraction = Interaction
            create_task(Self._Construct_Panel())


    async def _Send_New_Panel(Self, Interaction:DiscordInteraction) -> None:
        Self.Ether.Records["PlayerInteractions"] += 1
        await Interaction.response.edit_message(embed=Self.EmbedFrame, view=Self.BaseViewFrame)
        Self.DashboardMessage:DiscordMessage = Interaction.message


    async def _Generate_Info(Self, Ether, InitialContext, Exclusions:list=[], Inclusions:list=[]):
        Self.Player.Refresh_Stats()
        Self.EmbedFrame.description = ""
        Fields = [Field for Field in ["Wallet", "Team", "Level", "Experience", "Power"] if Field not in Exclusions]
        Fields += Inclusions
        Info = ""

        if Ether.Data["Players"][InitialContext.author.id].Data["Skill Points"] > 0:
            Info +=f"**You have {format(int(Ether.Data['Players'][InitialContext.author.id].Data['Skill Points']), ',')} unspent skill point**\n"

        for Name, Value in Self.Player.Data.items():
            if Name in Fields:
                if Name == 'Wallet':
                    Info +=f"> **{Name}** ~ ${format(float(Value), ',')}\n"
                elif Name == 'Experience':
                    Info +=f"> **{Name}** ~ {format(float(Value), ',')} / {format(float(Ether.Data['Players'][InitialContext.author.id].ExperienceForNextLevel), ',')}\n"
                elif type(Value) == float:
                    Info +=f"> **{Name}** ~ {format(float(Value), ',')}\n"
                elif type(Value) == int:
                    Info +=f"> **{Name}** ~ {format(int(Value), ',')}\n"
                else:
                    Info +=f"> **{Name}** ~ {Value}\n"

        for Name, Value in Self.Player.Skills.items():
            if Name in Fields:
                Info += f"> **{Name}** ~ {format(int(Value), ',')}\n"

        Info += "\n\n"

        Self.EmbedFrame.description += Info