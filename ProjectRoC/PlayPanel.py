from asyncio import create_task
from discord import ButtonStyle, Embed, SelectOption, Interaction, InteractionMessage
from discord.ext.commands import Context
from discord.ui import View, Button, Select
from RealmOfConflict import RealmOfConflict
from LootTables import ScavengeTable
from random import randrange
from Player import Player

class PlayPanel:
    def __init__(Self, Ether:RealmOfConflict, PlayerContext:Context):
        create_task(Self._Construct_Home(Ether, PlayerContext))


    async def _Send_New_Panel(Self, ButtonInteraction: Interaction):
        await ButtonInteraction.response.edit_message(embed=Self.EmbedFrame, view=Self.BaseViewFrame)


    async def _Determine_Team(Self):
        if "Titan" in str(Self.InitialContext.author.roles):
            Self.ButtonStyle = ButtonStyle.red
        elif "Analis" in str(Self.InitialContext.author.roles):
            Self.ButtonStyle = ButtonStyle.blurple
        else:
            Self.ButtonStyle = ButtonStyle.grey


    async def _Generate_Info(Self, Exclusions:list=[]):
        Fields = [Field for Field in ["Wallet", "Team", "Level", "Experience", "Power"] if Field not in Exclusions]
        Info = ""
        for Name, Value in Self.Player.Data.items():
            if Name in Fields:
                if Name == 'Wallet':
                    Info +=f"**{Name}** ~ ${format(float(Value), ',')}\n"
                elif type(Value) == float:
                    Info +=f"**{Name}** ~ {format(float(Value), ',')}\n"
                elif type(Value) == int:
                    Info +=f"**{Name}** ~ {format(int(Value), ',')}\n"
                else:
                    Info +=f"**{Name}** ~ {Value}\n"
        return Info


    async def _Determine_Whitelist(Self):
        if Self.InitialContext.author.id in Self.Whitelist:
            Self.EmbedFrame.title = Self.EmbedFrame.title + " (Developer)"


    async def _Construct_Home(Self, Ether:RealmOfConflict=None, InitialContext:Context=None, ButtonInteraction=None):
        Self.InitialContext = InitialContext
        Self.Ether = Ether
        Self.Whitelist = [897410636819083304, # Robert Reynolds, Cavan
                          ]
        Self.Player: Player = Ether.Data["Players"][InitialContext.author.id]
        await Self._Determine_Team()

        if Self.Player.Data["Experience"] >= Self.Player.ExperienceForNextLevel:
            Self.Player.Data["Level"] += 1
            Self.Player.Refresh_Stats()

        Self.BaseViewFrame = View(timeout=144000)
        Self.EmbedFrame = Embed(title=f"{Self.Player.Data['Name']}'s Home Panel")

        Self.EmbedFrame.insert_field_at(0, name="\u200b", value=await Self._Generate_Info(), inline=False)

        Self.FacilitiesButton = Button(label="Facilities", style=Self.ButtonStyle)
        Self.ScavengeButton = Button(label="Scavenge", style=Self.ButtonStyle)

        Self.FacilitiesButton.callback = Self._Construct_Facilities_Panel
        Self.ScavengeButton.callback = Self._Scavenge

        Self.BaseViewFrame.add_item(Self.FacilitiesButton)
        Self.BaseViewFrame.add_item(Self.ScavengeButton)

        if InitialContext.author.id in Self.Whitelist:
            Self.DebugButton = Button(label="Debug", style=ButtonStyle.grey, row=3)
            Self.BaseViewFrame.add_item(Self.DebugButton)

        await Self._Determine_Whitelist()
        if ButtonInteraction:
            await Self._Send_New_Panel(ButtonInteraction)
        else:
            Self.DashboardMessage = await Self.InitialContext.send(embed=Self.EmbedFrame, view=Self.BaseViewFrame)


    async def _Scavenge(Self, ButtonInteraction:Interaction):
        SuccessfulRolls = [Name for Name, Chance in ScavengeTable.items() if randrange(0 , 99) < Chance]
        Self.EmbedFrame.clear_fields()
        ScavengedString = ""
        ExperienceGained = round((0.65 * (0.35 * Self.Player.Data["Level"])) * len(SuccessfulRolls), 2)
        ScavengedString += f"Gained {ExperienceGained} experience\n"
        Self.Player.Data["Experience"] = round(Self.Player.Data["Experience"] + ExperienceGained, 2)

        for Roll in SuccessfulRolls:
            if Roll == "Wallet":
                MoneyScavenged = round(2.76 * (0.35 * Self.Player.Data["Level"]), 2)
                Self.Player.Data["Wallet"] = round(Self.Player.Data["Wallet"] + MoneyScavenged, 2)
                ScavengedString += f"Found ${MoneyScavenged}\n"

        if Self.Player.Data["Experience"] >= Self.Player.ExperienceForNextLevel:
            Self.Player.Data["Level"] += 1
            Self.Player.Refresh_Stats()
            
        Self.EmbedFrame.insert_field_at(0, name="\u200b", value=await Self._Generate_Info(), inline=False)
        Self.EmbedFrame.add_field(name=f"Scavenged", value=ScavengedString, inline=False)
        await Self._Send_New_Panel(ButtonInteraction)


    async def _Construct_Facilities_Panel(Self, ButtonInteraction:Interaction):
        Self.BaseViewFrame = View(timeout=144000)
        Self.EmbedFrame = Embed(title=f"{Self.InitialContext.author.name}'s Facilities Panel")

        Self.EmbedFrame.insert_field_at(0, name="\u200b", value=await Self._Generate_Info(Exclusions=["Team", "Power"]), inline=False)

        Self.CollectProductionButton = Button(label="Collect Production", style=Self.ButtonStyle)
        Self.CollectManufacturingButton = Button(label="Collect Manufacturing", style=Self.ButtonStyle)
        Self.Options = [SelectOption(label=Name) for Name, Building in Self.Player.ProductionFacilities.items() if Building != "None"]
        Self.HomepageButton = Button(label="Home", style=ButtonStyle.grey, row=3)

        Self.FacilitiesSelect = Select(placeholder="Select a Facility", options=Self.Options, custom_id=f"{Self.Player.Data['UUID']} ItemSelect")

        Self.HomepageButton.callback = lambda ButtonInteraction: Self._Construct_Home(ButtonInteraction)

        Self.BaseViewFrame.add_item(Self.CollectProductionButton)
        Self.BaseViewFrame.add_item(Self.CollectManufacturingButton)
        Self.BaseViewFrame.add_item(Self.FacilitiesSelect)
        Self.BaseViewFrame.add_item(Self.HomepageButton)

        Self.Ether.Logger.info(f"Sent Facilities panel to {Self.Player.Data['Name']}")
        await Self._Send_New_Panel(ButtonInteraction)