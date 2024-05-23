from RealmOfConflict import RealmOfConflict
from discord.ext.commands import Context as DiscordContext
from discord import Interaction as DiscordInteraction
from discord import ButtonStyle as DiscordButtonStyle
from discord import SelectOption, Embed
from discord.ui import View, Select, Button, Modal, TextInput
from Panels.Panel import Panel
from Tables import MaterialWorthTable

class AvargoPanel(Panel):
    def __init__(Self, Ether:RealmOfConflict, InitialContext:DiscordContext,
                 ButtonStyle:DiscordButtonStyle, Interaction:DiscordInteraction,
                 PlayPanel):
        super().__init__(Ether, InitialContext,
                         PlayPanel, "Avargo",
                         Interaction=Interaction, ButtonStyle=ButtonStyle)


    async def _Construct_Panel(Self, Interaction:DiscordInteraction=None):
        Self.MaterialChosen = None
        Self.MaterialRaw = None
        Self.ReceiptStarted = False
        Self.Quantity = None
        Self.ReceiptString = ""
        Self.Receipt = {}
        if Self.Interaction.user != Self.InitialContext.author: return
        
        Self.BaseViewFrame = View(timeout=144000)
        Self.EmbedFrame = Embed(title=f"{Self.Player.Data['Name']}'s Avargo Sale Panel")
        await Self._Generate_Info(Self.Ether, Self.InitialContext)
        Self.Ether.Logger.info(f"Sent Avargo panel to {Self.Player.Data['Name']}")

        Self.BuyButton = Button(label="Buy", style=Self.ButtonStyle, custom_id="BuyButton")
        Self.BuyButton.callback = lambda ButtonInteraction : Self._Construct_Buy_Panel(ButtonInteraction)
        Self.BaseViewFrame.add_item(Self.BuyButton)

        Self.SellButton = Button(label="Sell", style=Self.ButtonStyle, custom_id="SellButton")
        Self.SellButton.callback = lambda ButtonInteraction: Self._Construct_Sell_Panel(ButtonInteraction)
        Self.BaseViewFrame.add_item(Self.SellButton)

        Self.HomepageButton = Button(label="Home", style=DiscordButtonStyle.grey, row=3, custom_id="HomePageButton")
        Self.HomepageButton.callback = lambda ButtonInteraction: Self.PlayPanel._Construct_Home(Self.Ether, Self.InitialContext, ButtonInteraction)
        Self.BaseViewFrame.add_item(Self.HomepageButton)

        Self.Ether.Logger.info(f"Sent Avargo panel to {Self.Player.Data['Name']}")
        if Interaction is not None:
            await Self._Send_New_Panel(Interaction)
        else:
            await Self._Send_New_Panel(Self.Interaction)


    async def _Construct_Buy_Panel(Self, Interaction:DiscordInteraction) -> None:
        if Interaction.user != Self.InitialContext.author:return
        Self.SaleType = "Buy"
        Self.BaseViewFrame = View(timeout=144000)
        Self.EmbedFrame = Embed(title=f"{Self.Player.Data['Name']}'s Avargo Buy Panel")

        await Self._Generate_Info(Self.Ether, Self.InitialContext)

        Self.AddButton = Button(label="Add", style=Self.ButtonStyle, custom_id="AddButton")
        Self.AddButton.callback = lambda ButtonInteraction: Self._Construct_Quantity_Modal(ButtonInteraction)
        Self.BaseViewFrame.add_item(Self.AddButton)

        Self.CheckoutButton = Button(label="Checkout", style=Self.ButtonStyle, custom_id="CheckoutButton")
        Self.CheckoutButton.callback = lambda ButtonInteraction: Self._Avargo_Checkout(ButtonInteraction)
        Self.BaseViewFrame.add_item(Self.CheckoutButton)

        Self.AvargoItemChoices = [SelectOption(label=f"{Material} at ${MaterialWorthTable[Material]} per unit") for Material in Self.Ether.Materials]
        Self.AvargoItemChoice = Select(placeholder="Select a material", options=Self.AvargoItemChoices, custom_id=f"ItemSelection", row=2)
        Self.BaseViewFrame.add_item(Self.AvargoItemChoice)
        Self.AvargoItemChoice.callback = lambda SelectInteraction: Self._Select_Item(SelectInteraction, SelectInteraction.data["values"][0])
        
        if Self.MaterialChosen is not None:
            Self.AvargoItemChoice.placeholder = Self.MaterialChosen
        
        if Self.MaterialRaw is not None:
            Self.EmbedFrame.description += f"You have {Self.Player.Inventory[Self.MaterialRaw]} {Self.MaterialRaw}"

        if Self.ReceiptStarted and Self.Quantity:
            Self.EmbedFrame.add_field(name="Receipt", value=Self.ReceiptString, inline=False)

        Self.AvargoButton = Button(label="Avargo", style=Self.ButtonStyle, row=3, custom_id="AvargoButton")
        Self.AvargoButton.callback = lambda ButtonInteraction: Self._Construct_Panel(ButtonInteraction)
        Self.BaseViewFrame.add_item(Self.AvargoButton)

        Self.HomepageButton = Button(label="Home", style=DiscordButtonStyle.grey, row=3, custom_id="HomePageButton")
        Self.HomepageButton.callback = lambda ButtonInteraction: Self.PlayPanel._Construct_Home(Self.Ether, Self.InitialContext, ButtonInteraction)
        Self.BaseViewFrame.add_item(Self.HomepageButton)
        
        await Self._Send_New_Panel(Interaction)


    async def _Construct_Sell_Panel(Self, Interaction:DiscordInteraction) -> None:
        if Interaction.user != Self.InitialContext.author:return
        Self.SaleType = "Sell"
        Self.BaseViewFrame = View(timeout=144000)
        Self.EmbedFrame = Embed(title=f"{Self.Player.Data['Name']}'s Avargo Sell Panel")
        
        await Self._Generate_Info(Self.Ether, Self.InitialContext)

        Self.AddButton = Button(label="Add", style=Self.ButtonStyle, custom_id="AddButton")
        Self.AddButton.callback = lambda ButtonInteraction: Self._Construct_Quantity_Modal(ButtonInteraction)
        Self.BaseViewFrame.add_item(Self.AddButton)

        Self.CheckoutButton = Button(label="Checkout", style=Self.ButtonStyle, custom_id="CheckoutButton")
        Self.CheckoutButton.callback = lambda ButtonInteraction: Self._Avargo_Checkout(ButtonInteraction)
        Self.BaseViewFrame.add_item(Self.CheckoutButton)

        Self.SellHundredButton = Button(label=f"Sell 100", style=Self.ButtonStyle, custom_id="SellHundredButton")
        Self.SellHundredButton.callback = Self._Sell_Hundred
        Self.BaseViewFrame.add_item(Self.SellHundredButton)

        Self.SellThousandButton = Button(label=f"Sell 1,000", style=Self.ButtonStyle, custom_id="SellThousandButton")
        Self.SellThousandButton.callback = Self._Sell_Thousand
        Self.BaseViewFrame.add_item(Self.SellThousandButton)

        Self.SellTenThousandButton = Button(label=f"Sell 10,000", style=Self.ButtonStyle, custom_id="SellTenThousandButton")
        Self.SellTenThousandButton.callback = Self._Sell_TenThousand
        Self.BaseViewFrame.add_item(Self.SellTenThousandButton)

        Self.SellAllButton = Button(label=f"Sell All", style=Self.ButtonStyle, custom_id="SellAllButton")
        Self.SellAllButton.callback = Self._Sell_All
        Self.BaseViewFrame.add_item(Self.SellAllButton)

        Self.AvargoItemChoices = [SelectOption(label=f"{Material} at ${MaterialWorthTable[Material]/4} per unit") for Material in Self.Ether.Materials]
        Self.AvargoItemChoice = Select(placeholder="Select a material", options=Self.AvargoItemChoices, custom_id=f"ItemSelection", row=2)
        Self.BaseViewFrame.add_item(Self.AvargoItemChoice)
        Self.AvargoItemChoice.callback = lambda SelectInteraction: Self._Select_Item(SelectInteraction, SelectInteraction.data["values"][0])
        
        if Self.MaterialChosen is not None:
            Self.AvargoItemChoice.placeholder = Self.MaterialChosen
        
        if Self.MaterialRaw is not None:
            Self.EmbedFrame.description += f"You have {Self.Player.Inventory[Self.MaterialRaw]} {Self.MaterialRaw}"

        if Self.ReceiptStarted and Self.Quantity:
            Self.EmbedFrame.add_field(name="Receipt", value=Self.ReceiptString, inline=False)

        Self.AvargoButton = Button(label="Avargo", style=Self.ButtonStyle, row=3, custom_id="AvargoButton")
        Self.AvargoButton.callback = lambda ButtonInteraction: Self._Construct_Panel(ButtonInteraction)
        Self.BaseViewFrame.add_item(Self.AvargoButton)

        Self.HomepageButton = Button(label="Home", style=DiscordButtonStyle.grey, row=3, custom_id="HomePageButton")
        Self.HomepageButton.callback = lambda ButtonInteraction: Self.PlayPanel._Construct_Home(Self.Ether, Self.InitialContext, ButtonInteraction)
        Self.BaseViewFrame.add_item(Self.HomepageButton)
        
        await Self._Send_New_Panel(Interaction)


    async def _Add_To_Cart(Self, Interaction, Quantity):
        if Self.SaleType == "Buy":
            if (MaterialWorthTable[Self.MaterialRaw] * Quantity) > Self.Player.Data["Wallet"]:
                Self.EmbedFrame.description += f"\nYou do not have enough money"
                await Self._Send_New_Panel(Interaction)
                return
        if Self.SaleType == "Sell":
            if Quantity > Self.Player.Inventory[Self.MaterialRaw]:
                Self.EmbedFrame.description += f"\nYou do not have enough {Self.MaterialRaw}"
                await Self._Send_New_Panel(Interaction)
                return
        else:
            Self.Quantity = Quantity
            Self.ReceiptStarted = True
            Self.EmbedFrame.description += f"You have {Self.Player.Inventory[Self.MaterialRaw]} {Self.MaterialRaw}"
            Self.Receipt.update({Self.MaterialRaw:Self.Quantity})
            Self.ReceiptString += f"{Self.Quantity} {Self.MaterialChosen} for ${format(round(MaterialWorthTable[Self.MaterialRaw] * int(Self.Quantity)/4, 2), ',')}"
        if Self.SaleType == "Buy":
            await Self._Construct_Buy_Panel(Interaction)
        if Self.SaleType == "Sell":
            await Self._Construct_Sell_Panel(Interaction)


    async def _Select_Item(Self, Interaction:DiscordInteraction, MaterialChosen):
        Self.MaterialChosen:str = MaterialChosen
        Self.MaterialRaw:str = MaterialChosen.split(" at ")[0]
        if Self.SaleType == "Buy":
            await Self._Construct_Buy_Panel(Interaction)
        if Self.SaleType == "Sell":
            await Self._Construct_Sell_Panel(Interaction)

    async def _Sell_Hundred(Self, Interaction:DiscordInteraction):
        if Self.MaterialRaw == None:
            Self.EmbedFrame.description += f"\nYou have nothing selected"
            await Self._Send_New_Panel(Interaction)
            return
        if Self.Player.Inventory[Self.MaterialRaw] >= 100:
            Self.Player.Inventory[Self.MaterialRaw] -= 100
            EarnedExperience:float = 0.00
            Total = round(Total + (MaterialWorthTable[Self.MaterialRaw]/4) * 100, 2)
            Total = round(Total + (Self.Player.Data["Maiden's Grace"] * (0.03 * Self.Player.Data["Level"])), 2)
            EarnedExperience = round((EarnedExperience + (MaterialWorthTable[Self.MaterialRaw]/2)) + (Self.Player.Data["Maiden's Grace"] * (0.08 * Self.Player.Data["Level"])), 2)
            Self.Player.Data["Wallet"] = round(Self.Player.Data["Wallet"] + Total, 2)
            Self.Player.Data["Experience"] = round(Self.Player.Data["Experience"] + EarnedExperience, 2)
            Self.ReceiptString += f"10 {Self.MaterialChosen} for ${format(Total, ',')}"
            await Self._Generate_Info(Self.Ether, Self.InitialContext)
            Self.EmbedFrame.description += f"### Receipt\n{Self.ReceiptString}"
            await Self._Send_New_Panel(Interaction)
            Self.MaterialChosen = None
            Self.MaterialRaw = None
            Self.ReceiptStarted = False
            Self.Quantity = None
            Self.ReceiptString = ""
            Self.Receipt = {}
        else:
            Self.EmbedFrame.description += f"\nYou do not have enough {Self.MaterialRaw}"
            await Self._Send_New_Panel(Interaction)
            return

    async def _Sell_Thousand(Self, Interaction:DiscordInteraction):
        if Self.MaterialRaw == None:
            Self.EmbedFrame.description += f"\nYou have nothing selected"
            await Self._Send_New_Panel(Interaction)
            return
        if Self.Player.Inventory[Self.MaterialRaw] >= 1000:
            Self.Player.Inventory[Self.MaterialRaw] -= 1000
            EarnedExperience:float = 0.00
            Total = round(Total + (MaterialWorthTable[Self.MaterialRaw]/4) * 1000, 2)
            Total = round(Total + (Self.Player.Data["Maiden's Grace"] * (0.03 * Self.Player.Data["Level"])), 2)
            EarnedExperience = round((EarnedExperience + (MaterialWorthTable[Self.MaterialRaw]/2)) + (Self.Player.Data["Maiden's Grace"] * (0.08 * Self.Player.Data["Level"])), 2)
            Self.Player.Data["Wallet"] = round(Self.Player.Data["Wallet"] + Total, 2)
            Self.Player.Data["Experience"] = round(Self.Player.Data["Experience"] + EarnedExperience, 2)
            Self.ReceiptString += f"10 {Self.MaterialChosen} for ${format(Total, ',')}"
            await Self._Generate_Info(Self.Ether, Self.InitialContext)
            Self.EmbedFrame.description += f"### Receipt\n{Self.ReceiptString}"
            await Self._Send_New_Panel(Interaction)
            Self.MaterialChosen = None
            Self.MaterialRaw = None
            Self.ReceiptStarted = False
            Self.Quantity = None
            Self.ReceiptString = ""
            Self.Receipt = {}
        else:
            Self.EmbedFrame.description += f"\nYou do not have enough {Self.MaterialRaw}"
            await Self._Send_New_Panel(Interaction)
            return

    async def _Sell_TenThousand(Self, Interaction:DiscordInteraction):
        if Self.MaterialRaw == None:
            Self.EmbedFrame.description += f"\nYou have nothing selected"
            await Self._Send_New_Panel(Interaction)
            return
        if Self.Player.Inventory[Self.MaterialRaw] >= 10000:
            Self.Player.Inventory[Self.MaterialRaw] -= 10000
            EarnedExperience:float = 0.00
            Total = round(Total + (MaterialWorthTable[Self.MaterialRaw]/4) * 10000, 2)
            Total = round(Total + (Self.Player.Data["Maiden's Grace"] * (0.03 * Self.Player.Data["Level"])), 2)
            EarnedExperience = round((EarnedExperience + (MaterialWorthTable[Self.MaterialRaw]/2)) + (Self.Player.Data["Maiden's Grace"] * (0.08 * Self.Player.Data["Level"])), 2)
            Self.Player.Data["Wallet"] = round(Self.Player.Data["Wallet"] + Total, 2)
            Self.Player.Data["Experience"] = round(Self.Player.Data["Experience"] + EarnedExperience, 2)
            Self.ReceiptString += f"10 {Self.MaterialChosen} for ${format(Total, ',')}"
            await Self._Generate_Info(Self.Ether, Self.InitialContext)
            Self.EmbedFrame.description += f"### Receipt\n{Self.ReceiptString}"
            await Self._Send_New_Panel(Interaction)
            Self.MaterialChosen = None
            Self.MaterialRaw = None
            Self.ReceiptStarted = False
            Self.Quantity = None
            Self.ReceiptString = ""
            Self.Receipt = {}
        else:
            Self.EmbedFrame.description += f"\nYou do not have enough {Self.MaterialRaw}"
            await Self._Send_New_Panel(Interaction)
            return

    async def _Sell_All(Self, Interaction:DiscordInteraction):
        EarnedExperience:float = 0.00
        Total:int = 0
        EarnedExperience = round((EarnedExperience + (MaterialWorthTable[Self.MaterialRaw]/2)) + (Self.Player.Data["Maiden's Grace"] * (0.08 * Self.Player.Data["Level"])), 2)
        Total = round(Total + (MaterialWorthTable[Self.MaterialRaw]/4) * Self.Player.Inventory[Self.MaterialRaw], 2)
        Total = round(Total + (Self.Player.Data["Maiden's Grace"] * (0.03 * Self.Player.Data["Level"])), 2)
        Self.ReceiptString += f"{Self.Player.Inventory[Self.MaterialRaw]} {Self.MaterialChosen} for ${format(Total, ',')}"
        Self.Player.Inventory[Self.MaterialRaw] = 0
        Self.Player.Data["Wallet"] = round(Self.Player.Data["Wallet"] + Total, 2)
        Self.Player.Data["Experience"] = round(Self.Player.Data["Experience"] + EarnedExperience, 2)
        await Self._Generate_Info(Self.Ether, Self.InitialContext)
        Self.EmbedFrame.description += f"### Receipt\n{Self.ReceiptString}"
        await Self._Send_New_Panel(Interaction)
        Self.MaterialChosen = None
        Self.MaterialRaw = None
        Self.ReceiptStarted = False
        Self.Quantity = None
        Self.ReceiptString = ""
        Self.Receipt = {}


    async def _Construct_Quantity_Modal(Self, Interaction:DiscordInteraction):
        if Interaction.user != Self.InitialContext.author:
            return
        Self.AvargoItemQuantityModal = Modal(title="Enter Quantity")
        if Self.SaleType == "Buy":
            Self.AvargoItemQuantityModal.on_submit = lambda ButtonInteraction: Self._Add_To_Cart(ButtonInteraction, Quantity=float(Self.AvargoItemQuantity.value))
        if Self.SaleType == "Sell":
            Self.AvargoItemQuantityModal.on_submit = lambda ButtonInteraction: Self._Add_To_Cart(ButtonInteraction, Quantity=float(Self.AvargoItemQuantity.value))

        Self.AvargoItemQuantity = TextInput(label="Enter item quantity")
        Self.AvargoItemQuantityModal.add_item(Self.AvargoItemQuantity)
        await Interaction.response.send_modal(Self.AvargoItemQuantityModal)


    async def _Avargo_Checkout(Self, Interaction:DiscordInteraction):
        if Interaction.user != Self.InitialContext.author:
            return
        if len(Self.Receipt) == 0:
            return
        
        Self.BaseViewFrame = View(timeout=144000)
        Self.EmbedFrame = Embed(title=f"{Self.Player.Data['Name']}'s Avargo Sale Panel")

        Self.AvargoButton = Button(label="Avargo", style=Self.ButtonStyle, row=3, custom_id="AvargoButton")
        Self.AvargoButton.callback = lambda ButtonInteraction: Self._Construct_Panel(ButtonInteraction)
        Self.BaseViewFrame.add_item(Self.AvargoButton)


        Self.HomepageButton = Button(label="Home", style=DiscordButtonStyle.grey, row=3, custom_id="HomePageButton")
        Self.HomepageButton.callback = lambda ButtonInteraction: Self.PlayPanel._Construct_Home(Self.Ether, Self.InitialContext, ButtonInteraction)
        Self.BaseViewFrame.add_item(Self.HomepageButton)

        Total:int = 0
        EarnedExperience:float = 0.00
        for Material, Quantity in Self.Receipt.items():
            if Self.SaleType == "Buy":
                Total += round(MaterialWorthTable[Material] * Quantity, 2) + (Self.Player.Data["Maiden's Grace"] * (0.02 * Self.Player.Data["Level"]))
                EarnedExperience = round(EarnedExperience + (MaterialWorthTable[Material]), 2) + (Self.Player.Data["Maiden's Grace"] * (0.08 * Self.Player.Data["Level"]))
            if Self.SaleType == "Sell":
                if Quantity > Self.Player.Inventory[Material]:
                    Self.InsufficientMaterial = Material
                    await Self._Construct_Sell_Panel(Interaction)
                    return
                EarnedExperience = round((EarnedExperience + (MaterialWorthTable[Material]/2)) + (Self.Player.Data["Maiden's Grace"] * (0.08 * Self.Player.Data["Level"])), 2)
                Total = round(Total + (MaterialWorthTable[Material]/4) * Quantity, 2)


        if Self.SaleType == "Buy":
            if Total <= Self.Player.Data["Wallet"]:
                for Material, Quantity in Self.Receipt.items():
                    Self.Player.Inventory[Material] = round(Self.Player.Inventory[Material] + Quantity, 2)
                Self.Player.Data["Wallet"] = round(Self.Player.Data["Wallet"] - Total + (Self.Player.Data["Maiden's Grace"] * (0.07 * Self.Player.Data["Level"])), 2)
                Self.Player.Data["Experience"] = round(Self.Player.Data["Experience"] + EarnedExperience, 2)
                await Self._Generate_Info(Self.Ether, Self.InitialContext)
                Self.EmbedFrame.description += f"You have {Self.Player.Inventory[Self.MaterialRaw]} {Self.MaterialRaw}"
                Self.EmbedFrame.add_field(name="Receipt", value=Self.ReceiptString, inline=False)
                Self.EmbedFrame.add_field(name="Total", value=f"${Total}", inline=False)
                Self.EmbedFrame.add_field(name="Experienced Earned", value=f"{EarnedExperience}", inline=False)
                await Self._Send_New_Panel(Interaction)
            else:
                await Self._Avargo_Sale(Interaction, Self.SaleType, MaterialChosen=Self.MaterialChosen, ReceiptStarted=True, InsufficientFunds=True)
        if Self.SaleType == "Sell":
            for Material, Quantity in Self.Receipt.items():
                Self.Player.Inventory[Material] = round(Self.Player.Inventory[Material] - Quantity, 2)
                Self.Player.Data["Wallet"] = round(Self.Player.Data["Wallet"] + Total + (Self.Player.Data["Maiden's Grace"] * (0.03 * Self.Player.Data["Level"])), 2)
                Self.Player.Data["Experience"] = round(Self.Player.Data["Experience"] + EarnedExperience, 2)
                await Self._Generate_Info(Self.Ether, Self.InitialContext)
                Self.EmbedFrame.description += f"You have {Self.Player.Inventory[Self.MaterialRaw]} {Self.MaterialRaw}"
                Self.EmbedFrame.add_field(name="Receipt", value=Self.ReceiptString, inline=False)
                Self.EmbedFrame.add_field(name="Total", value=f"${Total}", inline=False)
                Self.EmbedFrame.add_field(name="Experienced Earned", value=f"{EarnedExperience}", inline=False)
                await Self._Send_New_Panel(Interaction)

        Self.MaterialChosen = None
        Self.MaterialRaw = None
        Self.ReceiptStarted = False
        Self.Quantity = None
        Self.ReceiptString = ""
        Self.Receipt = {}
