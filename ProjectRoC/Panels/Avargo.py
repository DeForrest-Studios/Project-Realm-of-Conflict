from asyncio import create_task
from RealmOfConflict import RealmOfConflict
from discord.ext.commands import Context as DiscordContext
from discord import Interaction as DiscordInteraction
from discord import ButtonStyle as DiscordButtonStyle
from discord import SelectOption, Embed
from discord.ui import View, Select, Button, Modal, TextInput
from Panels.Panel import Panel
from Tables import MaterialWorthTable
from Player import Player

class AvargoPanel(Panel):
    def __init__(Self, Ether:RealmOfConflict, InitialContext:DiscordContext, ButtonStyle, Interaction:DiscordInteraction, PlayPanel):
        super().__init__()
        create_task(Self._Construct_Panel(Ether, InitialContext, ButtonStyle, Interaction, PlayPanel))
    
    async def _Construct_Panel(Self, Ether:RealmOfConflict, InitialContext:DiscordContext, ButtonStyle, Interaction:DiscordInteraction, PlayPanel):
        if Interaction.user != InitialContext.author:
            return
        
        Self.Ether:RealmOfConflict = Ether
        Self.InitialContext:DiscordContext = InitialContext
        Self.ButtonStyle:DiscordButtonStyle = ButtonStyle
        Self.PlayPanel:Panel = PlayPanel
        Self.Player:Player = Ether.Data['Players'][InitialContext.author.id]

        Self.BaseViewFrame = View(timeout=144000)
        Self.EmbedFrame = Embed(title=f"{Self.Player.Data['Name']}'s Avargo Panel")

        await Self._Generate_Info(Ether, InitialContext)

        Self.BuyButton = Button(label="Buy", style=ButtonStyle, custom_id="BuyButton")
        Self.BuyButton.callback = lambda ButtonInteraction : Self._Avargo_Sale(ButtonInteraction, "Buy")
        Self.BaseViewFrame.add_item(Self.BuyButton)

        Self.SellButton = Button(label="Sell", style=ButtonStyle, custom_id="SellButton")
        Self.SellButton.callback = lambda ButtonInteraction: Self._Avargo_Sale(ButtonInteraction, "Sell")
        Self.BaseViewFrame.add_item(Self.SellButton)

        Self.HomepageButton = Button(label="Home", style=DiscordButtonStyle.grey, row=3, custom_id="HomePageButton")
        # This is a bad callback. This is really bad, I'm well aware. But you know what, fuck it.
        Self.HomepageButton.callback = lambda ButtonInteraction: PlayPanel._Construct_Home(Ether, InitialContext, ButtonInteraction)
        Self.BaseViewFrame.add_item(Self.HomepageButton)

        await Self._Send_New_Panel(Interaction)


    async def _Construct_Quantity_Modal(Self, Interaction:DiscordInteraction):
        if Interaction.user != Self.InitialContext.author:
            return
        Self.AvargoItemQuantityModal = Modal(title="Enter Quantity")
        Self.AvargoItemQuantityModal.on_submit = lambda Interaction: Self._Avargo_Sale(Interaction, Self.SaleType, MaterialChosen=Self.MaterialChosen, ReceiptStarted=True, Quantity=float(Self.AvargoItemQuantity.value))

        Self.AvargoItemQuantity = TextInput(label="Enter item quantity")
        Self.AvargoItemQuantityModal.add_item(Self.AvargoItemQuantity)
        await Interaction.response.send_modal(Self.AvargoItemQuantityModal)
    

    async def _Avargo_Sale(Self, Interaction, SaleType, MaterialChosen=None, ReceiptStarted=False, Quantity=None, InsufficientFunds=False, InsufficientMaterials=False):
        if Interaction.user != Self.InitialContext.author:
            print(Interaction.user)
            print(Self.InitialContext.author)
            return
        Self.SaleType = SaleType
        if MaterialChosen is None or InsufficientFunds:
            Self.ReceiptString = ""
            Self.Receipt:{str:int} = {}
            Self.BaseViewFrame = View(timeout=144000)
            Self.EmbedFrame = Embed(title=f"{Self.Player.Data['Name']}'s Avargo Sale Panel")

            await Self._Generate_Info(Self.Ether, Self.InitialContext)

            Self.AddButton = Button(label="Add", style=Self.ButtonStyle, custom_id="AddButton")
            Self.AddButton.callback = lambda ButtonInteraction: Self._Construct_Quantity_Modal(ButtonInteraction)
            Self.BaseViewFrame.add_item(Self.AddButton)

            Self.CheckoutButton = Button(label="Checkout", style=Self.ButtonStyle, custom_id="CheckoutButton")
            Self.CheckoutButton.callback = lambda ButtonInteraction: Self._Avargo_Checkout(ButtonInteraction, SaleType)
            Self.BaseViewFrame.add_item(Self.CheckoutButton)

            Self.AvargoButton = Button(label="Avargo", style=Self.ButtonStyle, row=3, custom_id="AvargoButton")
            Self.AvargoButton.callback = lambda ButtonInteraction: Self._Construct_Panel(Self.Ether, Self.InitialContext, Self.ButtonStyle, ButtonInteraction, Self.PlayPanel)
            Self.BaseViewFrame.add_item(Self.AvargoButton)

            Self.HomepageButton = Button(label="Home", style=DiscordButtonStyle.grey, row=3, custom_id="HomePageButton")
            # This is a bad callback. This is really bad, I'm well aware. But you know what, fuck it.
            Self.HomepageButton.callback = lambda ButtonInteraction: Self.PlayPanel._Construct_Home(Self.Ether, Self.InitialContext, ButtonInteraction)
            Self.BaseViewFrame.add_item(Self.HomepageButton)
        
            if Self.SaleType == "Buy":
                Self.AvargoItemChoices = [SelectOption(label=f"{Material} at ${MaterialWorthTable[Material]} per unit") for Material in Self.Ether.Materials]
            if Self.SaleType == "Sell":
                Self.AvargoItemChoices = [SelectOption(label=f"{Material} at ${MaterialWorthTable[Material]/4} per unit") for Material in Self.Ether.Materials]

            Self.AvargoItemChoice = Select(placeholder="Select a material", options=Self.AvargoItemChoices, custom_id=f"ItemSelection", row=2)
            Self.BaseViewFrame.add_item(Self.AvargoItemChoice)
            Self.AvargoItemChoice.callback = lambda Interaction: Self._Avargo_Sale(Interaction, SaleType, ReceiptStarted=ReceiptStarted, MaterialChosen=Interaction.data["values"][0])
            

        if MaterialChosen:
            Self.AvargoItemChoice.placeholder = MaterialChosen
            Self.MaterialChosen:str = MaterialChosen
            Self.MaterialRaw:str = MaterialChosen.split(" at ")[0]
            Self.EmbedFrame.clear_fields()
            await Self._Generate_Info(Self.Ether, Self.InitialContext)
            Self.EmbedFrame.add_field(name=f"You have {Self.Ether.Data['Players'][Self.InitialContext.author.id].Inventory[Self.MaterialRaw]} {Self.MaterialRaw}", value="\u200b")
        if ReceiptStarted:
            if Quantity:
                Self.Receipt.update({Self.MaterialRaw:Quantity})
                if len(Self.ReceiptString) > 0:
                    Self.ReceiptString += "\n"
                if Self.SaleType == "Buy":
                    Self.ReceiptString += f"{Quantity} {Self.MaterialChosen} for ${format(round(MaterialWorthTable[Self.MaterialRaw] * int(Quantity), 2, ','))}"
                elif Self.SaleType == "Sell":
                    Self.ReceiptString += f"{Quantity} {Self.MaterialChosen} for ${format(round(MaterialWorthTable[Self.MaterialRaw] * int(Quantity)/4, 2), ',')}"
                Self.EmbedFrame.clear_fields()
                await Self._Generate_Info(Self.Ether, Self.InitialContext)
                Self.EmbedFrame.add_field(name="Receipt", value=Self.ReceiptString, inline=False)

        if InsufficientFunds:
            Self.EmbedFrame.add_field(name="Insufficient Funds", value="\u200b")

        if InsufficientMaterials:
            Self.EmbedFrame.add_field(name="Insufficient Materials", value=f"You only have {Self.Ether.Data['Players'][Self.InitialContext.author.id].Inventory[Self.InsufficientMaterial]} {Self.InsufficientMaterial}")

        await Self._Send_New_Panel(Interaction)


    async def _Avargo_Checkout(Self, Interaction:DiscordInteraction, SaleType):
        if Interaction.user != Self.InitialContext.author:
            return
        if len(Self.Receipt) == 0:
            return
        Total:int = 0
        EarnedExperience:float = 0.00
        for Material, Quantity in Self.Receipt.items():
            if SaleType == "Buy":
                Total += round(MaterialWorthTable[Material] * Quantity, 2) + (Self.Player.Data["Maiden's Grace"] * (0.02 * Self.Player.Data["Level"]))
                EarnedExperience = round(EarnedExperience + (MaterialWorthTable[Material]), 2) + (Self.Player.Data["Maiden's Grace"] * (0.08 * Self.Player.Data["Level"]))
            if SaleType == "Sell":
                if Quantity > Self.Ether.Data['Players'][Self.InitialContext.author.id].Inventory[Material]:
                    Self.InsufficientMaterial = Material
                    await Self._Avargo_Sale(Interaction, Self.SaleType, MaterialChosen=Self.MaterialChosen, ReceiptStarted=True, InsufficientMaterials=True)
                    return
                EarnedExperience = round((EarnedExperience + (MaterialWorthTable[Material]/2)) + (Self.Player.Data["Maiden's Grace"] * (0.08 * Self.Player.Data["Level"])), 2)
                Total = round(Total + (MaterialWorthTable[Material]/4) * Quantity, 2)
        
        Self.BaseViewFrame = View(timeout=144000)
        Self.EmbedFrame = Embed(title=f"{Self.Player.Data['Name']}'s Avargo Sale Panel")

        Self.EmbedFrame.add_field(name="Receipt", value=Self.ReceiptString, inline=False)
        Self.EmbedFrame.add_field(name="Total", value=f"${Total}", inline=False)
        Self.EmbedFrame.add_field(name="Experienced Earned", value=f"{EarnedExperience}", inline=False)

        Self.AvargoButton = Button(label="Avargo", style=Self.ButtonStyle, row=3, custom_id="AvargoButton")
        Self.AvargoButton.callback = lambda ButtonInteraction: Self._Construct_Panel(Self.Ether, Self.InitialContext, Self.ButtonStyle, ButtonInteraction, Self.PlayPanel)
        Self.BaseViewFrame.add_item(Self.AvargoButton)


        Self.HomepageButton = Button(label="Home", style=DiscordButtonStyle.grey, row=3, custom_id="HomePageButton")
        # This is a bad callback. This is really bad, I'm well aware. But you know what, fuck it.
        Self.HomepageButton.callback = lambda ButtonInteraction: Self.PlayPanel._Construct_Home(Self.Ether, Self.InitialContext, ButtonInteraction)
        Self.BaseViewFrame.add_item(Self.HomepageButton)

        if SaleType == "Buy":
            if Total <= Self.Ether.Data['Players'][Self.InitialContext.author.id].Data["Wallet"]:
                for Material, Quantity in Self.Receipt.items():
                    Self.Ether.Data['Players'][Self.InitialContext.author.id].Inventory[Material] = round(Self.Ether.Data['Players'][Self.InitialContext.author.id].Inventory[Material] + Quantity, 2)
                Self.Ether.Data['Players'][Self.InitialContext.author.id].Data["Wallet"] = round(Self.Ether.Data['Players'][Self.InitialContext.author.id].Data["Wallet"] - Total + (Self.Player.Data["Maiden's Grace"] * (0.07 * Self.Player.Data["Level"])), 2)
                Self.Ether.Data['Players'][Self.InitialContext.author.id].Data["Experience"] = round(Self.Ether.Data['Players'][Self.InitialContext.author.id].Data["Experience"] + EarnedExperience, 2)
                await Self._Generate_Info(Self.Ether, Self.InitialContext)
                await Self._Send_New_Panel(Interaction)
            else:
                await Self._Avargo_Sale(Interaction, Self.SaleType, MaterialChosen=Self.MaterialChosen, ReceiptStarted=True, InsufficientFunds=True)
        if SaleType == "Sell":
            for Material, Quantity in Self.Receipt.items():
                Self.Ether.Data['Players'][Self.InitialContext.author.id].Inventory[Material] = round(Self.Ether.Data['Players'][Self.InitialContext.author.id].Inventory[Material] - Quantity, 2)
                Self.Ether.Data['Players'][Self.InitialContext.author.id].Data["Wallet"] = round(Self.Ether.Data['Players'][Self.InitialContext.author.id].Data["Wallet"] + Total + (Self.Player.Data["Maiden's Grace"] * (0.03 * Self.Player.Data["Level"])), 2)
                Self.Ether.Data['Players'][Self.InitialContext.author.id].Data["Experience"] = round(Self.Ether.Data['Players'][Self.InitialContext.author.id].Data["Experience"] + EarnedExperience, 2)
                await Self._Generate_Info(Self.Ether, Self.InitialContext)
                await Self._Send_New_Panel(Interaction)