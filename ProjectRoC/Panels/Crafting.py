from RealmOfConflict import RealmOfConflict
from discord.ext.commands import Context as DiscordContext
from discord import Interaction as DiscordInteraction
from discord import ButtonStyle as DiscordButtonStyle
from discord import SelectOption
from discord.ui import Button, Select
from Panels.Panel import Panel

# Values that are a tuple are: ({RecipeItem:Quantity,
#                                RecipeItem:Quantity}:
#                                OutputAmount)
# As the default output amount is 1, this allows the ability for some outputs to be multiple, like logs, or paper

Components = {"Copper":     {"Copper Ore":4},
              "Iron":       {"Iron Ore":4},
              "Aluminum":   {"Aluminum Ore":5},
              "Lithium":    {"Lithium Ore":2},
              "Bread":      {"Wheat":12},
              "Lumber":     ({"Log":1},
                              4),
              "Paper":      ({"Log":1},
                              36),
              "Fabric":     {"Cotton":8},
              "Clothes":    {"Fabric":4},
              "Concrete":   {"Water":12,
                             "Limestone":4,
                             "Gravel":4},
              "Steel":      {"Coal":4,
                             "Iron":4},
              "Plastic":    {"Oil":6},
              "Fuel":       {"Oil":9},
              "Silicone":   {"Coal":2,
                             "Sand":6},
              "Wire":       ({"Copper":1},
                              8),
              "Batteries":  {"Copper":2,
                             "Aluminum":4,
                             "Lithium":3},
              "Bullets":    {"Copper":1,
                             "Iron":2,
                             "Steel":1},
              "Firearms":   {"Iron":10,
                             "Aluminum":5,
                             "Steel":4,
                             "Plastic":4},
              "Med-kits":   {"Fabric":10,
                             "Paper":12,
                             "Steel":12,
                             "Plastic":8},}

Weapons = {"Tier 1 Missile":{"Copper":500,
                             "Iron":500,
                             "Aluminum":360,
                             "Steel":280,
                             "Fuel":205},
           "Tier 2 Missile":{"Copper":1250,
                             "Iron":1250,
                             "Aluminum":920,
                             "Steel":685,
                             "Fuel":465},
           "Tier 3 Missile":{"Copper":2900,
                             "Iron":2900,
                             "Aluminum":2360,
                             "Steel":1545,
                             "Fuel":720},
           "Tier 4 Missile":{"Copper":6400,
                             "Iron":6400,
                             "Aluminum":5450,
                             "Steel":3740,
                             "Fuel":1310},
           "Tier 5 Missile":{"Copper":144000,
                             "Iron":144000,
                             "Aluminum":133000,
                             "Steel":7980,
                             "Fuel":3610},
           "Tier 1 Shield":{"Copper":500,
                             "Iron":500,
                             "Aluminum":360,
                             "Steel":280,
                             "Batteries":180},
           "Tier 2 Shield":{"Copper":1250,
                             "Iron":1250,
                             "Aluminum":920,
                             "Steel":685,
                             "Batteries":420},
           "Tier 3 Shield":{"Copper":2900,
                             "Iron":2900,
                             "Aluminum":2360,
                             "Steel":1545,
                             "Batteries":860},
           "Tier 4 Shield":{"Copper":6400,
                             "Iron":6400,
                             "Aluminum":5450,
                             "Steel":3740,
                             "Batteries":1920},
           "Tier 5 Shield":{"Copper":144000,
                             "Iron":144000,
                             "Aluminum":133000,
                             "Steel":7980,
                             "Batteries":4250},
           "Tier 1 EMP":{"Iron": 600,
                         "Copper": 900,
                         "Aluminum":450,
                         "Batteries":400},
           "Tier 2 EMP":{"Iron": 1450,
                         "Copper": 1980,
                         "Aluminum":1000,
                         "Batteries":960},
           "Tier 3 EMP":{"Iron": 3400,
                         "Copper": 3900,
                         "Aluminum":1550,
                         "Batteries":2000},}

TypeMapping = {"Components":Components,
           "Weapons":Weapons}

class CraftingPanel(Panel):
    def __init__(Self, Ether:RealmOfConflict, InitialContext:DiscordContext,
                 ButtonStyle:DiscordButtonStyle, Interaction:DiscordInteraction,
                 PlayPanel):
        super().__init__(Ether, InitialContext,
                         PlayPanel, "Crafting",
                         Interaction=Interaction, ButtonStyle=ButtonStyle)

    async def _Construct_Panel(Self, Interaction=None, CraftingTypeSelected=None, CraftingItemSelection=None):
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
            
            try:
                Self.CraftingItemChoice
            except AttributeError:
                Self.CraftingItemChoice = Select(placeholder="Select an Item", options=[SelectOption(label=Key) for Key in TypeMapping[Self.CraftingTypeSelected].keys()],
                                            row=2, custom_id=f"CraftingItemChoice")
                Self.CraftingItemChoice.callback = lambda Interaction: Self._Construct_Panel(Interaction=Interaction, CraftingTypeSelected=Self.CraftingTypeSelected,
                                                                                            CraftingItemSelection=Interaction.data["values"][0])
                Self.BaseViewFrame.add_item(Self.CraftingItemChoice)

        if CraftingItemSelection is not None:
            Self.CraftingItemSelection = CraftingItemSelection
            Recipe = TypeMapping[Self.CraftingTypeSelected][Self.CraftingItemSelection]
            Self.EmbedFrame.description += f"### Recipe\n"
            if type(Recipe) == tuple:
                Recipe = Recipe[0]
                OutputQuantity = Recipe[1]
                Self.EmbedFrame.description += f"**Outputs** - {OutputQuantity}\n"
                for Name, Quantity in Recipe.items():
                    Self.EmbedFrame.description += f"**{Name}** - {Quantity}\{Self.Player.Inventory[Name]}\n"
            if type(Recipe) == dict:
                for Name, Quantity in Recipe.items():
                    Self.EmbedFrame.description += f"**{Name}** - {Quantity}\{Self.Player.Inventory[Name]}\n"


        Self.Ether.Logger.info(f"Sent Crafting panel to {Self.Player.Data['Name']}")
        await Self._Send_New_Panel(Self.Interaction)