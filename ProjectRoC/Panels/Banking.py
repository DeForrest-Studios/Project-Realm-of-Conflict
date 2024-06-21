from RealmOfConflict import RealmOfConflict
from discord.ext.commands import Context as DiscordContext
from discord import Interaction as DiscordInteraction
from discord import ButtonStyle as DiscordButtonStyle
from discord import Embed
from discord.ui import Button, Modal, TextInput, View
from Panels.Panel import Panel

class BankingPanel(Panel):
    def __init__(Self, Ether:RealmOfConflict, InitialContext:DiscordContext, ButtonStyle, Interaction:DiscordInteraction, PlayPanel):
        super().__init__(Ether, InitialContext,
                         PlayPanel, "Banking",
                         Interaction=Interaction, ButtonStyle=ButtonStyle)

    async def _Construct_Panel(Self, Interaction=None, UserID=None, Value=None, Save=False, Pull=False, Send=False):
        if Self.Interaction.user != Self.InitialContext.author: return
        if Interaction != None: Self.Interaction = Interaction

        Self.BaseViewFrame = View(timeout=144000)
        Self.EmbedFrame = Embed(title=f"{Self.Player.Data['Name']}'s Banking Panel")

        BankingString = ""

        if Value != None:
            if Save == True:
                if Value <= Self.Player.Data["Wallet"]:
                    Self.Player.Data["Wallet"] = round(Self.Player.Data["Wallet"] - Value, 2)
                    Self.Player.Data["Savings"] = round(Self.Player.Data["Savings"] + Value, 2)
                else:
                    BankingString += "You did not have enough in your wallet\n"
            if Pull == True:
                if Value <= Self.Player.Data["Savings"]:
                    Self.Player.Data["Savings"] = round(Self.Player.Data["Savings"] - Value, 2)
                    Self.Player.Data["Wallet"] = round(Self.Player.Data["Wallet"] + Value, 2)
                else:
                    BankingString += "You did not have enough in savings\n"
            if Send == True:
                if Value <= Self.Player.Data["Wallet"]:
                    if UserID in Self.Ether.Data["Players"].keys():
                        Self.Ether.Data["Players"][UserID].Data["Wallet"] = round(Self.Ether.Data["Players"][UserID].Data["Wallet"] + Value, 2)
                    else:
                        BankingString += "Invalid Player ID\n"

        await Self._Generate_Info(Self.Ether, Self.InitialContext)

        BankingString += f"Current Interest Rate: {str(Self.Ether.InterestRate).replace('0.', '%')}\n"
        BankingString += f"In Savings Account: ${Self.Player.Data['Savings']}\n"

        Self.EmbedFrame.description += BankingString
 
        Self.InvestButton = Button(label="Save", style=Self.ButtonStyle, row=0, custom_id="SaveButton")
        Self.InvestButton.callback = lambda Interaction: Self._Send_Save_Modal(Interaction)
        Self.BaseViewFrame.add_item(Self.InvestButton)
 
        Self.PullButton = Button(label="Pull", style=Self.ButtonStyle, row=0, custom_id="PullButton")
        Self.PullButton.callback = lambda Interaction: Self._Send_Pull_Modal(Interaction)
        Self.BaseViewFrame.add_item(Self.PullButton)
 
 
        Self.SendButton = Button(label="Send", style=Self.ButtonStyle, row=0, custom_id="SendButton")
        Self.SendButton.callback = lambda Interaction: Self._Send_Money_Modal(Interaction)
        Self.BaseViewFrame.add_item(Self.SendButton)

 
        Self.HomepageButton = Button(label="Home", style=DiscordButtonStyle.grey, row=3, custom_id="HomePageButton")
        Self.HomepageButton.callback = lambda Interaction: Self.PlayPanel._Construct_Home(Self.Ether, Self.InitialContext, Interaction)
        Self.BaseViewFrame.add_item(Self.HomepageButton)

        Self.Ether.Logger.info(f"Sent Banking panel to {Self.Player.Data['Name']}")
        await Self._Send_New_Panel(Self.Interaction)


    async def _Send_Save_Modal(Self, Interaction):
        if Interaction.user != Self.InitialContext.author:return

        Self.SavingsQuantityModal = Modal(title="Enter Quantity to Save")
        Self.SavingsQuantityModal.on_submit = lambda ButtonInteraction: Self._Construct_Panel(ButtonInteraction, Value=int(Self.Quantity.value), Save=True)

        Self.Quantity = TextInput(label="Enter item quantity")
        Self.SavingsQuantityModal.add_item(Self.Quantity)
        await Interaction.response.send_modal(Self.SavingsQuantityModal)


    async def _Send_Pull_Modal(Self, Interaction):
        if Interaction.user != Self.InitialContext.author:return

        Self.PullQuantityModal = Modal(title="Enter Quantity to Pull")
        Self.PullQuantityModal.on_submit = lambda ButtonInteraction: Self._Construct_Panel(ButtonInteraction, Value=int(Self.Quantity.value), Pull=True)

        Self.Quantity = TextInput(label="Enter item quantity")
        Self.PullQuantityModal.add_item(Self.Quantity)
        await Interaction.response.send_modal(Self.PullQuantityModal)


    async def _Send_Money_Modal(Self, Interaction):
        if Interaction.user != Self.InitialContext.author:return

        Self.SendModal = Modal(title="Enter PlayerID, and Quantity to Send")
        Self.SendModal.on_submit = lambda ButtonInteraction: Self._Construct_Panel(ButtonInteraction, UserID=int(Self.UserID.value), Value=int(Self.Quantity.value), Send=True)

        Self.UserID = TextInput(label="Enter Player ID")
        Self.SendModal.add_item(Self.UserID)

        Self.Quantity = TextInput(label="Enter item quantity")
        Self.SendModal.add_item(Self.Quantity)
        await Interaction.response.send_modal(Self.SendModal)