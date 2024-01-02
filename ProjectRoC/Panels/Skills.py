from asyncio import create_task
from RealmOfConflict import RealmOfConflict
from discord.ext.commands import Context as DiscordContext
from discord import Interaction as DiscordInteraction
from discord import ButtonStyle as DiscordButtonStyle
from discord import SelectOption, Embed
from discord.ui import View, Select, Button
from Panels.Panel import Panel
from Player import Player

class SkillsPanel(Panel):
    def __init__(Self, Ether:RealmOfConflict, InitialContext:DiscordContext, ButtonStyle:DiscordButtonStyle,
                 Interaction:DiscordInteraction, PlayPanel:Panel):
        super().__init__()
        create_task(Self._Construct_Panel(Ether, InitialContext, ButtonStyle, Interaction, PlayPanel))

    async def _Construct_Panel(Self, Ether:RealmOfConflict, InitialContext:DiscordContext, ButtonStyle:DiscordButtonStyle,
                               Interaction:DiscordInteraction, PlayPanel:Panel):
        if Interaction.user != InitialContext.author:
            return
        Self.SelectedPanel = "None"
        Self.Ether = Ether
        Self.InitialContext = InitialContext
        Self.ButtonStyle = ButtonStyle
        Self.PlayPanel = PlayPanel
        Self.Player:Player = Ether.Data['Players'][InitialContext.author.id]
        Self.BaseViewFrame = View(timeout=144000)
        Self.EmbedFrame = Embed(title=f"{Self.Player.Data['Name']}'s Skill Panel")
        await Self._Generate_Info(Ether, InitialContext, Inclusions=["Skill Points", "General Skill", "Offensive Skill",
                                                                     "Defensive Skill", "Counter Operations Skill"])

        Self.GeneralSkillsButton = Button(label="General Skills", style=ButtonStyle, custom_id="GeneralSkillsButton")
        Self.GeneralSkillsButton.callback = Self._Construct_General_Skills
        Self.BaseViewFrame.add_item(Self.GeneralSkillsButton)

        Self.OffensiveSkillButton = Button(label="Offensive Skill", style=ButtonStyle, custom_id="OffensiveSkillButton")
        Self.OffensiveSkillButton.callback = Self._Construct_Offensive_Skills
        Self.BaseViewFrame.add_item(Self.OffensiveSkillButton)

        Self.DefensiveSkillButton = Button(label="Defensive Skill", style=ButtonStyle, custom_id="DefensiveSkillButton")
        Self.DefensiveSkillButton.callback = Self._Construct_Defensive_Skills
        Self.BaseViewFrame.add_item(Self.DefensiveSkillButton)

        Self.CounterOperationsSkillButton = Button(label="Counter Operations Skill", style=ButtonStyle, custom_id="CounterOperationsSkillButton")
        Self.CounterOperationsSkillButton.callback = Self._Construct_Counter_Operations_Skills
        Self.BaseViewFrame.add_item(Self.CounterOperationsSkillButton)

        Self.HomepageButton = Button(label="Home", style=DiscordButtonStyle.grey, row=3, custom_id="HomePageButton")
        # This is a bad callback. This is really bad, I'm well aware. But you know what, fuck it.
        Self.HomepageButton.callback = lambda Interaction: Self.PlayPanel._Construct_Home(Ether, InitialContext, Interaction)
        Self.BaseViewFrame.add_item(Self.HomepageButton)

        await Self._Send_New_Panel(Interaction)

    async def _Construct_General_Skills(Self, Interaction):
        Self.SelectedPanel = "General"
        Self.SelectedSkills = ["Production", "Manufacturing"]
        Self.BaseViewFrame = View(timeout=144000)
        Self.EmbedFrame = Embed(title=f"{Self.Player.Data['Name']}'s General Skills Panel")
        await Self._Generate_Info(Self.Ether, Self.InitialContext, Inclusions=["Skill Points", "General Skill"] + Self.SelectedSkills)

        Self.ProductionSkillButton = Button(label="Production", style=Self.ButtonStyle, custom_id="ProductionSkillButton")
        Self.ProductionSkillButton.callback = Self._Confirm_Skill_Point
        Self.BaseViewFrame.add_item(Self.ProductionSkillButton)
        
        Self.ManufacturingSkillButton = Button(label="Manufacturing", style=Self.ButtonStyle, custom_id="ManufacturingSkillButton")
        Self.ManufacturingSkillButton.callback = Self._Confirm_Skill_Point
        Self.BaseViewFrame.add_item(Self.ManufacturingSkillButton)

        Self.SkillsButton = Button(label="Skills", style=Self.ButtonStyle, row=2, custom_id="SkillsButton")
        Self.SkillsButton.callback = lambda ButtonInteraction: Self._Construct_Panel(Self.Ether, Self.InitialContext, Self.ButtonStyle, ButtonInteraction, Self.PlayPanel)
        Self.BaseViewFrame.add_item(Self.SkillsButton)

        Self.HomepageButton = Button(label="Home", style=DiscordButtonStyle.grey, row=3, custom_id="HomePageButton")
        Self.HomepageButton.callback = lambda ButtonInteraction: Self.PlayPanel._Construct_Home(Self.Ether, Self.InitialContext, ButtonInteraction)
        Self.BaseViewFrame.add_item(Self.HomepageButton)

        await Self._Send_New_Panel(Interaction)

    async def _Construct_Offensive_Skills(Self, Interaction):
        Self.SelectedPanel = "Offensive"
        Self.SelectedSkills = ["Offensive", "Domination"]
        Self.BaseViewFrame = View(timeout=144000)
        Self.EmbedFrame = Embed(title=f"{Self.Player.Data['Name']}'s Offensive Skills Panel")
        await Self._Generate_Info(Self.Ether, Self.InitialContext, Inclusions=["Skill Points", "Offensive Skill"] + Self.SelectedSkills)
        
        Self.OffensivePowerSkillButton = Button(label="Offensive Power", style=Self.ButtonStyle, custom_id="OffensivePowerSkillButton")
        Self.OffensivePowerSkillButton.callback = Self._Confirm_Skill_Point
        Self.BaseViewFrame.add_item(Self.OffensivePowerSkillButton)

        Self.DominationSkillButton = Button(label="Domination", style=Self.ButtonStyle, custom_id="DominationSkillButton")
        Self.DominationSkillButton.callback = Self._Confirm_Skill_Point
        Self.BaseViewFrame.add_item(Self.DominationSkillButton)

        Self.SkillsButton = Button(label="Skills", style=Self.ButtonStyle, row=2, custom_id="SkillsButton")
        Self.SkillsButton.callback = lambda ButtonInteraction: Self._Construct_Panel(Self.Ether, Self.InitialContext, Self.ButtonStyle, ButtonInteraction, Self.PlayPanel)
        Self.BaseViewFrame.add_item(Self.SkillsButton)

        Self.HomepageButton = Button(label="Home", style=DiscordButtonStyle.grey, row=3, custom_id="HomePageButton")
        Self.HomepageButton.callback = lambda ButtonInteraction: Self.PlayPanel._Construct_Home(Self.Ether, Self.InitialContext, ButtonInteraction)
        Self.BaseViewFrame.add_item(Self.HomepageButton)

        await Self._Send_New_Panel(Interaction)

    async def _Construct_Defensive_Skills(Self, Interaction):
        Self.SelectedPanel = "Defensive"
        Self.SelectedSkills = ["Defensive", "Healing"]
        Self.BaseViewFrame = View(timeout=144000)
        Self.EmbedFrame = Embed(title=f"{Self.Player.Data['Name']}'s Defensive Skills Panel")
        await Self._Generate_Info(Self.Ether, Self.InitialContext, Inclusions=["Skill Points", "Defensive Skill"] + Self.SelectedSkills)
        
        Self.DefensiveSkillButton = Button(label="Defensive Power", style=Self.ButtonStyle, custom_id="DefensiveSkillButton")
        Self.DefensiveSkillButton.callback = Self._Confirm_Skill_Point
        Self.BaseViewFrame.add_item(Self.DefensiveSkillButton)

        Self.HealingSkillButton = Button(label="Healing", style=Self.ButtonStyle, custom_id="HealingSkillButton")
        Self.HealingSkillButton.callback = Self._Confirm_Skill_Point
        Self.BaseViewFrame.add_item(Self.HealingSkillButton)

        Self.SkillsButton = Button(label="Skills", style=Self.ButtonStyle, row=2, custom_id="SkillsButton")
        Self.SkillsButton.callback = lambda ButtonInteraction: Self._Construct_Panel(Self.Ether, Self.InitialContext, Self.ButtonStyle, ButtonInteraction, Self.PlayPanel)
        Self.BaseViewFrame.add_item(Self.SkillsButton)

        Self.HomepageButton = Button(label="Home", style=DiscordButtonStyle.grey, row=3, custom_id="HomePageButton")
        Self.HomepageButton.callback = lambda ButtonInteraction: Self.PlayPanel._Construct_Home(Self.Ether, Self.InitialContext, ButtonInteraction)
        Self.BaseViewFrame.add_item(Self.HomepageButton)

        await Self._Send_New_Panel(Interaction)

    async def _Construct_Counter_Operations_Skills(Self, Interaction):
        Self.SelectedPanel = "Counter Operations"
        Self.SelectedSkills = ["Hacking", "Raiding"]
        Self.BaseViewFrame = View(timeout=144000)
        Self.EmbedFrame = Embed(title=f"{Self.Player.Data['Name']}'s Counter Operations Skills Panel")
        await Self._Generate_Info(Self.Ether, Self.InitialContext, Inclusions=["Skill Points", "Counter Operations Skill"] + Self.SelectedSkills)
        
        Self.HackingSkillButton = Button(label="Hacking", style=Self.ButtonStyle, custom_id="HackingSkillButton")
        Self.HackingSkillButton.callback = Self._Confirm_Skill_Point
        Self.BaseViewFrame.add_item(Self.HackingSkillButton)

        Self.RaidingSkillButton = Button(label="Raiding", style=Self.ButtonStyle, custom_id="RaidingSkillButton")
        Self.RaidingSkillButton.callback = Self._Confirm_Skill_Point
        Self.BaseViewFrame.add_item(Self.RaidingSkillButton)

        Self.SkillsButton = Button(label="Skills", style=Self.ButtonStyle, row=2, custom_id="SkillsButton")
        Self.SkillsButton.callback = lambda ButtonInteraction: Self._Construct_Panel(Self.Ether, Self.InitialContext, Self.ButtonStyle, ButtonInteraction, Self.PlayPanel)
        Self.BaseViewFrame.add_item(Self.SkillsButton)

        Self.HomepageButton = Button(label="Home", style=DiscordButtonStyle.grey, row=3, custom_id="HomePageButton")
        Self.HomepageButton.callback = lambda ButtonInteraction: Self.PlayPanel._Construct_Home(Self.Ether, Self.InitialContext, ButtonInteraction)
        Self.BaseViewFrame.add_item(Self.HomepageButton)

        await Self._Send_New_Panel(Interaction)


    async def _Confirm_Skill_Point(Self, Interaction):
        ChosenSkill = Interaction.data["custom_id"].split("Skill")[0]
        Self.EmbedFrame.clear_fields()
        if Self.Player.Add_Skill_Point(ChosenSkill):
            await Self._Generate_Info(Self.Ether, Self.InitialContext, Inclusions=["Skill Points", f"{Self.SelectedPanel} Skill"] + Self.SelectedSkills)
            Self.EmbedFrame.add_field(name=f"Your {ChosenSkill} skill is now {Self.Player.Skills[ChosenSkill]}", value="\u200b")
        else:
            await Self._Generate_Info(Self.Ether, Self.InitialContext, Inclusions=["Skill Points", f"{Self.SelectedPanel} Skill"] + Self.SelectedSkills)
            Self.EmbedFrame.add_field(name="You don't have any skill points.", value="\u200b")

        await Self._Send_New_Panel(Interaction)
