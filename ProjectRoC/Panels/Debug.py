from os import remove
from os.path import join
from RealmOfConflict import RealmOfConflict
from discord.ext.commands import Context as DiscordContext
from discord import Interaction as DiscordInteraction
from discord import ButtonStyle as DiscordButtonStyle
from discord.ui import Button, Modal, TextInput, View
from Panels.Panel import Panel
from discord import Embed\

class DebugPanel(Panel):
    def __init__(Self, Ether:RealmOfConflict, InitialContext:DiscordContext, ButtonStyle, Interaction:DiscordInteraction, PlayPanel, Emoji):
        super().__init__(Ether, InitialContext,
                         PlayPanel, "Debug",
                         Interaction=Interaction, ButtonStyle=ButtonStyle, Emoji=Emoji)

    async def _Construct_Panel(Self):
        if Self.Interaction.user != Self.InitialContext.author: return
        
        Self.BaseViewFrame = View(timeout=144000)
        Self.PanelTitle = f"{Self.Player.Data['Name']}'s Debug Panel"
        Self.EmbedFrame = Embed(title=Self.Emoji*2 + Self.PanelTitle + Self.Emoji*2)

        await Self._Generate_Info(Self.Ether, Self.InitialContext)

        Self.ResetPlayerUUIDSubmission = Modal(title="Submit Player UUID")
        Self.ResetPlayerUUIDSubmission.on_submit = lambda Interaction: Self._Reset_Player(Interaction, int(Self.ResetPlayerSubmittedUUID.value))
        Self.ResetPlayerSubmittedUUID = TextInput(label="Player UUID")
        Self.ResetPlayerUUIDSubmission.add_item(Self.ResetPlayerSubmittedUUID)
        Self.ResetPlayer = Button(label="Reset Player", style=Self.ButtonStyle, custom_id="ResetPlayerButton")
        Self.ResetPlayer.callback = lambda Interaction: Interaction.response.send_modal(Self.ResetPlayerUUIDSubmission)
        Self.BaseViewFrame.add_item(Self.ResetPlayer)

        Self.SummonPanelUUIDSubmission = Modal(title="Submit Player UUID")
        Self.SummonPanelUUIDSubmission.on_submit = lambda Interaction: Self._Summon_Panel(Interaction, int(Self.SummonPanelSubmittedUUID.value))
        Self.SummonPanelSubmittedUUID = TextInput(label="Player UUID")
        Self.SummonPanelUUIDSubmission.add_item(Self.SummonPanelSubmittedUUID)
        Self.SummonPanel = Button(label="Summon Panel", style=Self.ButtonStyle, custom_id="SummonPanelButton")
        Self.SummonPanel.callback = lambda Interaction: Interaction.response.send_modal(Self.SummonPanelUUIDSubmission)
        Self.BaseViewFrame.add_item(Self.SummonPanel)

        Self.GiveMoneySubmission = Modal(title="Give Money to Player")
        Self.GiveMoneySubmission.on_submit = lambda Interaction: Self._Give_Money(Interaction, int(Self.GiveMoneyPlayerSubmittedUUID.value), int(Self.GiveMoneyAmount.value))
        Self.GiveMoneyPlayerSubmittedUUID = TextInput(label="Player UUID")
        Self.GiveMoneyAmount = TextInput(label="Amount")
        Self.GiveMoneySubmission.add_item(Self.GiveMoneyPlayerSubmittedUUID)
        Self.GiveMoneySubmission.add_item(Self.GiveMoneyAmount)
        Self.GiveMoney = Button(label="Give Player Money", style=Self.ButtonStyle, custom_id="GivePlayerMoneyButton")
        Self.GiveMoney.callback = lambda Interaction: Interaction.response.send_modal(Self.GiveMoneySubmission)
        Self.BaseViewFrame.add_item(Self.GiveMoney)

        Self.EngageSimulationPlayer = Button(label="Engage Simulation", style=Self.ButtonStyle, custom_id="EngageSimulationPlayer")
        Self.EngageSimulationPlayer.callback = Self._Initialize_Simulation
        Self.BaseViewFrame.add_item(Self.EngageSimulationPlayer)

        Self.HomepageButton = Button(label="Home", style=DiscordButtonStyle.grey, row=3, custom_id="HomePageButton")
        Self.HomepageButton.callback = lambda Interaction: Self.PlayPanel._Construct_Home(Self.Ether, Self.InitialContext, Interaction)
        Self.BaseViewFrame.add_item(Self.HomepageButton)

        Self.Ether.Logger.info(f"Sent Debug panel to {Self.Player.Data['Name']}")
        await Self._Send_New_Panel(Self.Interaction)


    async def _Initialize_Simulation(Self, Interaction:DiscordInteraction) -> None:
        if await Self.Ether.Engage_Simulation() == True:
            Self.EmbedFrame.clear_fields()
            await Self._Generate_Info(Self.Ether, Self.InitialContext)
            Self.EmbedFrame.description += "**You have started a simulation**"
        else:
            Self.EmbedFrame.description += "**Something went wrong went engaging simulation**"
        Self.Ether.Logger.info(f"{Self.Player.Data['Name']} started the simulation")
        await Self._Send_New_Panel(Interaction)

        with open("cheatlog.roc", 'a') as CheatLog:
            CheatLog.write(f"{Self.Ether.RunType}: {Self.Player.Data['Name']} {Self.Player.Data['UUID']} started sim\n")


    async def _Give_Money(Self, Interaction, SubmittedUUID, Amount):
        if Self.Interaction.user != Self.InitialContext.author:return
        Player = Self.Ether.Data['Players'][SubmittedUUID]
        Player.Data['Wallet'] = round(Player.Data['Wallet'] + Amount, 2)
        await Self._Send_New_Panel(Interaction)

        with open("cheatlog.roc", 'a') as CheatLog:
            CheatLog.write(f"{Self.Ether.RunType}: {Self.Player.Data['Name']} {Self.Player.Data['UUID']} gave {Self.Ether.Data['Players'][SubmittedUUID].Data['Name']} ${Amount}\n")


    async def _Reset_Player(Self, Interaction, SubmittedUUID):
        if Self.Interaction.user != Self.InitialContext.author:return
        with open("cheatlog.roc", 'a') as CheatLog:
            CheatLog.write(f"{Self.Ether.RunType}: {Self.Player.Data['Name']} {Self.Player.Data['UUID']} reset {Self.Ether.Data['Players'][SubmittedUUID].Data['Name']} {SubmittedUUID}\n")
        if Self.Ether.Data['Players'][SubmittedUUID].Data["Team"] == "Analis":
            Choice = "Analis"
        if Self.Ether.Data['Players'][SubmittedUUID].Data["Team"] == "Titan":
            Choice = "Titan"
        if Self.Ether.Data["Planets"][Choice].Data["Protector Count"] - 1 >= 0:
            Self.Ether.Data["Planets"][Choice].Data["Protector Count"] -= 1
        await Self.Ether.Data['Players'][SubmittedUUID].Data["Member Object"].remove_roles(Self.Ether.Roles[Choice])
        Self.Ether.Data['Players'][SubmittedUUID] = None
        Self.Ether.Data['Players'].pop(SubmittedUUID)
        remove(join(Self.Ether.DataDirectory, "PlayerData", f"{SubmittedUUID}.data.roc"))
        remove(join(Self.Ether.DataDirectory, "PlayerInventories", f"{SubmittedUUID}.inventory.roc"))
        remove(join(Self.Ether.DataDirectory, "PlayerProductionFacilities", f"{SubmittedUUID}.production.roc"))
        remove(join(Self.Ether.DataDirectory, "PlayerManufacturingFacilities", f"{SubmittedUUID}.manufacturing.roc"))
        remove(join(Self.Ether.DataDirectory, "PlayerArmy", f"{SubmittedUUID}.army.roc"))
        remove(join(Self.Ether.DataDirectory, "PlayerSkills", f"{SubmittedUUID}.skills.roc"))

        Self.Ether.Logger.info(f"{Self.Player.Data['Name']} reset ID:{SubmittedUUID}")
        await Self._Send_New_Panel(Interaction)



    async def _Summon_Panel(Self, Interaction, SubmittedUUID):
        # If the player already has a panel, delete the previous panel before sending them a new one
        if SubmittedUUID in Self.Ether.Data["Panels"].keys():
            await Self.Ether.Data["Panels"][SubmittedUUID].DashboardMessage.delete()
            Self.Ether.Data["Panels"].update({SubmittedUUID:Self.PlayPanel.PlayPanel(Self.Ether, Self.InitialContext, SummonedID=SubmittedUUID)})
            return
            
        # Default send message behavior
        Self.Ether.Data["Panels"].update({SubmittedUUID:Self.PlayPanel.PlayPanel(Self.Ether, Self.InitialContext, SummonedID=SubmittedUUID)})
        await Self._Send_New_Panel(Interaction)

        with open("cheatlog.roc", 'a') as CheatLog:
            CheatLog.write(f"{Self.Ether.RunType}: {Self.Player.Data['Name']} {Self.Player.Data['UUID']} summoned {Self.Ether.Data['Players'][SubmittedUUID].Data['Name']}'s ({SubmittedUUID}) panel\n")