from os import mkdir, listdir
from os.path import join, exists
from discord import ButtonStyle, Embed, Intents, Member, Interaction
from discord.ui import Button, View
from discord.ext.commands import Bot, Context
from discord.utils import get
from logging import getLogger, Formatter,  DEBUG, INFO
from logging.handlers import RotatingFileHandler
from asyncio import create_task, sleep
from Planet import Planet
from Player import Player


class RealmOfConflict(Bot):
    def __init__(Self) -> None:
        super().__init__(command_prefix=['R', 'r'], intents=Intents.all())
        Self.remove_command('help')
        Self.Data = {
            "Players": {"42069": Player("Test")},
            "Planets": {
                "Analis": Planet("Analis"),
                "Titan": Planet("Titan"),
            },
            "Panels": {},
        }
        Self.Materials = [Facility.OutputItem for Facility in Self.Data["Players"]["42069"].ProductionFacilities.values()]
        Self.Initalize_Logger()


    def Get_Token(Self, Key: str) -> None:
        with open(join("Keys.txt")) as KeyFile:
            for line in KeyFile:
                line_data = line.split("~")
                if Key == line_data[0]:
                    return line_data[1].strip()


    def Initialize(Self) -> None:
        Self.run(Self.Get_Token("Cavan"))

    
    def Initalize_Logger(Self):
        Self.Logger = getLogger('discord')
        Self.Logger.setLevel(DEBUG)
        getLogger('discord.http').setLevel(INFO)

        Self.Handler = RotatingFileHandler(
            filename='RoC.log',
            encoding='utf-8',
            maxBytes=32 * 1024 * 1024,  # 32 MiB
            backupCount=5,  # Rotate through 5 files
        )
        DateTimeFormat = '%Y-%m-%d %H:%M:%S'
        Self.Formatter = Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', DateTimeFormat, style='{')
        Self.Handler.setFormatter(Self.Formatter)
        Self.Logger.addHandler(Self.Handler)


    def Load_Players(Self) -> None:
        print("Players have been loaded")
        if not exists("Data"):
            return
        Self.Load_Player_Data()
        Self.Load_Player_Inventories()
        # Self.Load_Player_Production_Facilities()


    def Load_Player_Data(Self) -> None:
        if not exists(join("Data", "PlayerData")):
            return
        Members = {M.id:M for M in Self.Guild.members}
        for PlayerDataFileName in listdir(join("Data", "PlayerData")):
            PlayerUUID = int(PlayerDataFileName.split(".")[0])
            with open(join("Data", "PlayerData", f"{PlayerUUID}.roc"), 'r') as PlayerDataFile:
                PlayerData = [Line.strip() for Line in PlayerDataFile.readlines()]
                if PlayerUUID == 42069: continue
                MemberObject = Members[PlayerUUID]
                LoadedPlayer = Player(MemberObject)
                for Field in PlayerData:
                    Contents = Field.split(":")
                    Name = Contents[0]
                    if Contents[1].replace(".", "").isdigit():
                        Value = float(Contents[1])
                        LoadedPlayer.Data[Name] = Value
                        continue
                    if Contents[1].isdigit():
                        Value = int(Contents[1])
                        LoadedPlayer.Data[Name] = Value
                        continue
                    if Contents[1] == "None":
                        Value = "None"
                        LoadedPlayer.Data[Name] = Value
                        continue
                    Value = Contents[1]
                    LoadedPlayer.Data[Name] = Value
                LoadedPlayer.Refresh_Stats()
                Self.Data["Players"].update({PlayerUUID:LoadedPlayer})


    def Load_Player_Inventories(Self) -> None:
        if not exists(join("Data", "PlayerInventories")):
            return
        for PlayerDataFileName in listdir(join("Data", "PlayerInventories")):
            PlayerUUID = int(PlayerDataFileName.split(".")[0])
            if PlayerUUID == 42069: continue
            with open(join("Data", "PlayerInventories", f"{PlayerUUID}.roc"), 'r') as PlayerDataFile:
                PlayerData = [Line.strip() for Line in PlayerDataFile.readlines()]
                for Field in PlayerData:
                    Contents = Field.split(":")
                    Name = Contents[0]
                    Value = float(Contents[1])
                    Self.Data["Players"][PlayerUUID].Inventory[Name] = Value


    def Load_Player_Production_Facilities(Self) -> None:
        if not exists(join("Data", "PlayerProductionFacilities")):
            return
        for PlayerDataFileName in listdir(join("Data", "PlayerProductionFacilities")):
            PlayerUUID = int(PlayerDataFileName.split(".")[0])
            if PlayerUUID == 42069: continue
            with open(join("Data", "PlayerProductionFacilities", f"{PlayerUUID}.roc"), 'r') as PlayerDataFile:
                PlayerData = [Line.strip() for Line in PlayerDataFile.readlines()]
                for Field in PlayerData:
                    Contents = Field.split(":")
                    Name = Contents[0]
                    Value = int(Contents[1])
                    Self.Data["Players"][PlayerUUID].Facilities[Name].Level = Value


    async def Autosave(Self) -> None:
        if not exists("Data"):
            mkdir("Data")
        if not exists(join("Data", "PlayerData")):
            mkdir(join("Data", "PlayerData"))
        if not exists(join("Data", "PlayerInventories")):
            mkdir(join("Data", "PlayerInventories"))
        if not exists(join("Data", "PlayerProductionFacilities")):
            mkdir(join("Data", "PlayerProductionFacilities"))
        if not exists(join("Data", "PlayerManufacturingFacilities")):
            mkdir(join("Data", "PlayerManufacturingFacilities"))
        while True:
            await sleep(5)
            print("Autosaving")
            await Self.Save_Player_Data()
            await Self.Save_Player_Inventories()
            await Self.Save_Player_ProductionFacilities()

    async def Save_Player_Data(Self) -> None:
        for UUID, Player in Self.Data["Players"].items():
            SaveData = ""
            with open(join("Data", "PlayerData", f"{UUID}.roc"), 'w+') as PlayerDataFile:
                for Name, Value in Player.Data.items():
                    SaveData += f"{Name}:{Value}\n"
                PlayerDataFile.write(SaveData)


    async def Save_Player_Inventories(Self) -> None:
        for UUID, Player in Self.Data["Players"].items():
            SaveData = ""
            with open(join("Data", "PlayerInventories", f"{UUID}.roc"), 'w+') as PlayerDataFile:
                for Name, Value in Player.Inventory.items():
                    SaveData += f"{Name}:{Value}\n"
                PlayerDataFile.write(SaveData)


    async def Save_Player_ProductionFacilities(Self) -> None:
        for UUID, Player in Self.Data["Players"].items():
            SaveData = ""
            with open(join("Data", "PlayerProductionFacilities", f"{UUID}.roc"), 'w+') as PlayerDataFile:
                for Facility in Player.ProductionFacilities.values():
                    SaveData += f"{Facility.Name}:{Facility.Level}\n"
                PlayerDataFile.write(SaveData)


    async def Choose_Team(Self, NewMember:Member, Choice:str, ButtonInteraction:Interaction) -> None:
        Self.Data["Players"].update({NewMember.id:Player(NewMember)})
        Self.Data["Players"][NewMember.id].Data["Team"] = Choice
        Self.Data["Planets"][Choice].Data["Protector Count"] += 1
        await NewMember.add_roles(get(Self.Guild.roles, name=Choice))

        MessageEmbed = Embed(title="Welcome")

        MessageEmbed.add_field(name="\u200b", value=f"Welcome to {Choice}")

        Self.Logger.info(f"{NewMember.author.name} joined {Choice}")

        await ButtonInteraction.response.edit_message(embed=MessageEmbed, view=None)


    async def Send_Welcome(Self, NewMember:Member) -> None:
        MessageEmbed = Embed(title="Welcome")
        MessageView = View()
        ChooseAnalisButton = Button(label="Choose Analis", style=ButtonStyle.blurple, custom_id=f"{NewMember.id} Analis Choice", row=1)
        ChooseTitanButton = Button(label="Choose Titan", style=ButtonStyle.red, custom_id=f"{NewMember.id} Titan Choice", row=1)

        ChooseAnalisButton.callback = lambda ButtonInteraction: create_task(Self.Choose_Team(NewMember, "Analis", ButtonInteraction))
        ChooseTitanButton.callback = lambda ButtonInteraction: create_task(Self.Choose_Team(NewMember, "Titan", ButtonInteraction))

        MessageView.add_item(ChooseAnalisButton)
        MessageView.add_item(ChooseTitanButton)

        await NewMember.send(embed=MessageEmbed, view=MessageView)


    async def Guild_Guard(Self, Context:Context):
        if Context.guild is None:
            return "Unprotected"
        if Context.guild.id in [1018734763378479164]: # DevServer
            return "Protected"
        return "Unprotected"


    # Override of existing on_ready from discord.py
    async def on_guild_available(Self, Guild):
        print(f"Guild available: {Guild.name}")
        # if Guild.name in ["Guild available: Project RoC - Dev Server"]:
        Self.Guild = Self.guilds[0]
        Self.Load_Players()
        await Self.Autosave()
        print("\nBot is alive.\n")


    # Override of existing on_member_join from discord.py
    # This sends a message to the player
    async def on_member_join(Self, NewMember:Member) -> None:
        await Self.Send_Welcome(NewMember)
