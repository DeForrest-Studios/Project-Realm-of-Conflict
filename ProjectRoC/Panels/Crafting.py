from RealmOfConflict import RealmOfConflict
from discord.ext.commands import Context as DiscordContext
from discord import Interaction as DiscordInteraction
from discord import ButtonStyle as DiscordButtonStyle
from discord import SelectOption
from discord.ui import Button, Select, Modal, TextInput
from Panels.Panel import Panel
from Tables import TypeMapping

class CraftingPanel(Panel):
    def __init__(Self, Ether:RealmOfConflict, InitialContext:DiscordContext,
                 ButtonStyle:DiscordButtonStyle, Interaction:DiscordInteraction,
                 PlayPanel):
        super().__init__(Ether, InitialContext,
                         PlayPanel, "Crafting",
                         Interaction=Interaction, ButtonStyle=ButtonStyle)

    async def _Construct_Panel(Self, Interaction:DiscordInteraction=None, CraftingTypeSelected:str=None,
                               CraftingItemSelection:str=None, CraftedAmount:int=None):
        if Self.Interaction.user != Self.InitialContext.author: return

        await Self._Generate_Info(Self.Ether, Self.InitialContext)
        if Interaction == None:
            Self.CraftingTypeChoices = [SelectOption(label="Components"), SelectOption(label="Weapons")]
            Self.CraftingTypes = Select(placeholder="Select a Crafting Type", options=Self.CraftingTypeChoices,
                                        row=1, custom_id=f"InfantrySelection")
            Self.CraftingTypes.callback = lambda Interaction: Self._Construct_Panel(Interaction=Interaction, CraftingTypeSelected=Interaction.data["values"][0])
            Self.BaseViewFrame.add_item(Self.CraftingTypes)

            Self.HomepageButton = Button(label="Home", style=DiscordButtonStyle.grey,
                                        row=3, custom_id="HomePageButton")
            Self.HomepageButton.callback = lambda Interaction: Self.PlayPanel._Construct_Home(Self.Ether, Self.InitialContext, Interaction)
            Self.BaseViewFrame.add_item(Self.HomepageButton)
        else:
            Self.Interaction = Interaction

        if CraftingTypeSelected is not None:
            Self.CraftingTypeSelected = CraftingTypeSelected
            Self.CraftingTypes.placeholder = Self.CraftingTypeSelected
            
            if hasattr(Self, "CraftingItemChoice"):
                Self.BaseViewFrame.remove_item(Self.CraftingItemChoice)
            
            Self.CraftingItemChoice = Select(placeholder="Select an Item", options=[SelectOption(label=Key) for Key in TypeMapping[Self.CraftingTypeSelected].keys()],
                                        row=2, custom_id=f"CraftingItemChoice")
            Self.CraftingItemChoice.callback = lambda Interaction: Self._Construct_Panel(Interaction=Interaction, CraftingTypeSelected=Self.CraftingTypeSelected,
                                                                                        CraftingItemSelection=Interaction.data["values"][0])
            Self.BaseViewFrame.add_item(Self.CraftingItemChoice)

        if CraftedAmount is not None:
            ItemRecipe = TypeMapping[Self.CraftingTypeSelected][Self.CraftingItemSelection]
            if type(ItemRecipe) == tuple:
                Quantity = ItemRecipe[1]
                ItemRecipe = ItemRecipe[0]
                for Item, AmountRequired in ItemRecipe.items():
                    if Self.Player.Inventory[Item] <= (AmountRequired * CraftedAmount) * Quantity:
                        Self.EmbedFrame.description += f"**Insufficient Resources** {Item}\n"
                        Self.Ether.Logger.info(f"Sent Crafting panel to {Self.Player.Data['Name']}")
                        await Self._Send_New_Panel(Self.Interaction)
                        return
                    
                for Item, AmountRequired in ItemRecipe.items():
                    Self.Player.Inventory[Item] = round(Self.Player.Inventory[Item] - (AmountRequired * CraftedAmount) * Quantity, 2)
            if type(ItemRecipe) == dict:
                for Item, AmountRequired in ItemRecipe.items():
                    if Self.Player.Inventory[Item] <= AmountRequired * CraftedAmount:
                        Self.EmbedFrame.description += f"**Insufficient Resources** {Item}\n"
                        Self.Ether.Logger.info(f"Sent Crafting panel to {Self.Player.Data['Name']}")
                        await Self._Send_New_Panel(Self.Interaction)
                        return

                for Item, AmountRequired in ItemRecipe.items():
                    Self.Player.Inventory[Item] = round(Self.Player.Inventory[Item] - AmountRequired * CraftedAmount, 2)
            
            PreviousAmount = Self.Player.Inventory[CraftingItemSelection]
            Self.Player.Inventory[CraftingItemSelection] = round(Self.Player.Inventory[CraftingItemSelection] + CraftedAmount, 2)
            Self.EmbedFrame.description += f"**You crafted:** {CraftedAmount} {CraftingItemSelection}, you had {PreviousAmount} and now have {Self.Player.Inventory[CraftingItemSelection]}\n"

        if CraftingItemSelection is not None:
            try:
                Self.CraftItem
            except AttributeError:
                Self.CraftItem = Button(label="Craft", style=Self.ButtonStyle, row=0, custom_id="CraftItem")
                Self.CraftItem.callback = lambda ButtonInteraction: Self._Send_Quantity_Modal(ButtonInteraction)
                Self.BaseViewFrame.add_item(Self.CraftItem)
            Self.CraftingItemSelection = CraftingItemSelection
            Self.CraftingItemChoice.placeholder = Self.CraftingItemSelection
            ItemRecipe = TypeMapping[Self.CraftingTypeSelected][Self.CraftingItemSelection]
            Self.EmbedFrame.description += f"### Recipe\n"
            if type(ItemRecipe) == tuple:
                Recipe = ItemRecipe[0]
                OutputQuantity = ItemRecipe[1]
                Self.EmbedFrame.description += f"**Outputs** - {OutputQuantity}\n"
                for Name, Quantity in Recipe.items():
                    Self.EmbedFrame.description += f"**{Name}** - {Quantity}\{Self.Player.Inventory[Name]}\n"
            if type(ItemRecipe) == dict:
                for Name, Quantity in ItemRecipe.items():
                    Self.EmbedFrame.description += f"**{Name}** - {Quantity}\{Self.Player.Inventory[Name]}\n"

        Self.Ether.Logger.info(f"Sent Crafting panel to {Self.Player.Data['Name']}")
        await Self._Send_New_Panel(Self.Interaction)


    async def _Send_Quantity_Modal(Self, Interaction):
        if Interaction.user != Self.InitialContext.author:return

        Self.ItemQuantityModal = Modal(title="Enter Quantity")
        Self.ItemQuantityModal.on_submit = lambda ButtonInteraction: Self._Construct_Panel(ButtonInteraction, CraftingTypeSelected=Self.CraftingTypeSelected,
                                                                                           CraftingItemSelection=Self.CraftingItemSelection, CraftedAmount=int(Self.ItemQuantity.value))

        Self.ItemQuantity = TextInput(label="Enter item quantity")
        Self.ItemQuantityModal.add_item(Self.ItemQuantity)
        await Interaction.response.send_modal(Self.ItemQuantityModal)