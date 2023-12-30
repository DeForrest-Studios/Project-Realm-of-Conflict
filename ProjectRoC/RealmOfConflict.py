from asyncio import create_task, sleep
from discord import ButtonStyle, Embed, Intents
from discord import Interaction as DiscordInteraction
from discord import Member as DiscordMember
from discord.ui import Button, View
from discord.ext.commands import Bot, Context
from logging import getLogger, Formatter,  DEBUG, INFO, Logger
from logging.handlers import RotatingFileHandler
from os import mkdir, listdir
from os.path import join, exists
from Planet import Planet
from Player import Player
from random import randrange
from Tables import InfantryToObject


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
            "Skirmish Count": 0,
        }
        Self.Guild = None
        Self.Roles = None
        Self.Members = None
        Self.Materials:[str] = [Facility.OutputItem for Facility in Self.Data["Players"]["42069"].ProductionFacilities.values()]
        Self.Initalize_Logger()


    def Get_Token(Self, Key:str) -> None:
        with open(join("Keys.txt")) as KeyFile:
            Line:str
            for Line in KeyFile:
                LineData:[str] = Line.split("~")
                if Key == LineData[0]:
                    return LineData[1].strip()


    def Initialize(Self) -> None:
        Self.run(Self.Get_Token("Cavan"))

    
    def Initalize_Logger(Self) -> None:
        Self.Logger:Logger = getLogger('discord')
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
        Self.Load_Player_Army()
        Self.Load_Planet_Data()
        # Self.Load_Player_Production_Facilities()


    def Load_Player_Data(Self) -> None:
        if not exists(join("Data", "PlayerData")):
            return
        Self.Members:{int:DiscordMember} = {M.id:M for M in Self.Guild.members}
        PlayerDataFileName:str
        for PlayerDataFileName in listdir(join("Data", "PlayerData")):
            PlayerUUID:int = int(PlayerDataFileName.split(".")[0])
            with open(join("Data", "PlayerData", f"{PlayerUUID}.roc"), 'r') as PlayerDataFile:
                PlayerData:[str] = [Line.strip() for Line in PlayerDataFile.readlines()]
                if PlayerUUID == 42069: continue
                MemberObject:DiscordMember = Self.Members[PlayerUUID]
                Self.Data["Players"].update({PlayerUUID:Player(MemberObject)})
                Field:str
                for Field in PlayerData:
                    Contents:str = Field.split(":")
                    Name:str = Contents[0]
                    if Name == "Member Object":
                        continue
                    if Contents[1].isdigit():
                        Value = int(Contents[1])
                        Self.Data["Players"][PlayerUUID].Data[Name] = Value
                        continue
                    if Contents[1].replace(".", "").isdigit():
                        Value = float(Contents[1])
                        Self.Data["Players"][PlayerUUID].Data[Name] = Value
                        continue
                    if Contents[1] == "None":
                        Value:str = "None"
                        Self.Data["Players"][PlayerUUID].Data[Name] = Value
                        continue
                    Value:str = Contents[1]
                    Self.Data["Players"][PlayerUUID].Data[Name] = Value
                Self.Data["Players"][PlayerUUID].Refresh_Stats()


    def Load_Planet_Data(Self) -> None:
        if not exists(join("Data", "PlanetData")):
            return
        PlayerDataFileName:str
        for PlanetDataFileName in listdir(join("Data", "PlanetData")):
            PlanetName:str = PlanetDataFileName.split(".")[0]
            with open(join("Data", "PlanetData", f"{PlanetName}.roc"), 'r') as PlanetDataFile:
                PlanetData:str = [Line.strip() for Line in PlanetDataFile.readlines()]
                Field:str
                for Field in PlanetData:
                    Contents:str = Field.split(":")
                    Name:str = Contents[0]
                    if Contents[1].isdigit():
                        Value = int(Contents[1])
                        Self.Data["Planets"][PlanetName].Data[Name] = Value
                        continue
                    if Contents[1].replace(".", "").isdigit():
                        Value = float(Contents[1])
                        Self.Data["Planets"][PlanetName].Data[Name] = Value
                        continue
                    if Contents[1] == "None":
                        Value = "None"
                        Self.Data["Planets"][PlanetName].Data[Name] = Value
                        continue
                    Value:str = Contents[1]
                    Self.Data["Planets"][PlanetName].Data[Name] = Value


    def Load_Player_Inventories(Self) -> None:
        if not exists(join("Data", "PlayerInventories")):
            return
        PlayerDataFileName:str
        for PlayerDataFileName in listdir(join("Data", "PlayerInventories")):
            PlayerUUID = int(PlayerDataFileName.split(".")[0])
            if PlayerUUID == 42069: continue
            with open(join("Data", "PlayerInventories", f"{PlayerUUID}.roc"), 'r') as PlayerDataFile:
                PlayerData = [Line.strip() for Line in PlayerDataFile.readlines()]
                Field:str
                for Field in PlayerData:
                    Contents:str = Field.split(":")
                    Name:str = Contents[0]
                    Value = float(Contents[1])
                    Self.Data["Players"][PlayerUUID].Inventory[Name] = Value


    def Load_Player_Production_Facilities(Self) -> None:
        if not exists(join("Data", "PlayerProductionFacilities")):
            return
        PlayerDataFileName:str
        for PlayerDataFileName in listdir(join("Data", "PlayerProductionFacilities")):
            PlayerUUID = int(PlayerDataFileName.split(".")[0])
            if PlayerUUID == 42069: continue
            with open(join("Data", "PlayerProductionFacilities", f"{PlayerUUID}.roc"), 'r') as PlayerDataFile:
                PlayerData = [Line.strip() for Line in PlayerDataFile.readlines()]
                Field:str
                for Field in PlayerData:
                    Contents:str = Field.split(":")
                    Name:str = Contents[0]
                    Value = int(Contents[1])
                    Self.Data["Players"][PlayerUUID].Facilities[Name].Level = Value


    def Load_Player_Army(Self) -> None:
        if not exists(join("Data", "PlayerArmy")):
            return
        PlayerDataFileName:str
        for PlayerDataFileName in listdir(join("Data", "PlayerArmy")):
            PlayerUUID = int(PlayerDataFileName.split(".")[0])
            if PlayerUUID == 42069: continue
            with open(join("Data", "PlayerArmy", f"{PlayerUUID}.roc"), 'r') as PlayerDataFile:
                PlayerData = [Line.strip() for Line in PlayerDataFile.readlines()]
                for Field in PlayerData:
                    Contents = Field.split(":")
                    Name:str = Contents[0]
                    Level = int(Contents[1])
                    Type:str = Contents[2]
                    Self.Data["Players"][PlayerUUID].Army.update({Name:InfantryToObject[Type](Level, Type, Self.Data["Players"][PlayerUUID], Name=Name)})
            Self.Data["Players"][PlayerUUID].Refresh_Power()
            

        

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
        if not exists(join("Data", "PlayerArmy")):
            mkdir(join("Data", "PlayerArmy"))
        if not exists(join("Data", "PlanetData")):
            mkdir(join("Data", "PlanetData"))
        while True:
            await sleep(5)
            print("Autosaving")
            await Self.Save_Player_Data()
            await Self.Save_Player_Inventories()
            await Self.Save_Player_ProductionFacilities()
            await Self.Save_Player_Army()
            await Self.Save_Planet_Data()

    async def Save_Planet_Data(Self) -> None:
        Name:str
        PlanetObject:Planet
        for Name, PlanetObject in Self.Data["Planets"].items():
            SaveData = ""
            with open(join("Data", "PlanetData", f"{Name}.roc"), 'w+') as PlayerDataFile:
                for Name, Value in PlanetObject.Data.items():
                    SaveData += f"{Name}:{Value}\n"
                PlayerDataFile.write(SaveData)

    async def Save_Player_Data(Self) -> None:
        UUID:int
        PlayerObject:Player
        for UUID, PlayerObject in Self.Data["Players"].items():
            SaveData = ""
            with open(join("Data", "PlayerData", f"{UUID}.roc"), 'w+') as PlayerDataFile:
                for Name, Value in PlayerObject.Data.items():
                    SaveData += f"{Name}:{Value}\n"
                PlayerDataFile.write(SaveData)


    async def Save_Player_Inventories(Self) -> None:
        UUID:int
        PlayerObject:Player
        for UUID, PlayerObject in Self.Data["Players"].items():
            SaveData = ""
            with open(join("Data", "PlayerInventories", f"{UUID}.roc"), 'w+') as PlayerDataFile:
                for Name, Value in PlayerObject.Inventory.items():
                    SaveData += f"{Name}:{Value}\n"
                PlayerDataFile.write(SaveData)


    async def Save_Player_ProductionFacilities(Self) -> None:
        UUID:int
        PlayerObject:Player
        for UUID, PlayerObject in Self.Data["Players"].items():
            SaveData = ""
            with open(join("Data", "PlayerProductionFacilities", f"{UUID}.roc"), 'w+') as PlayerDataFile:
                for Facility in PlayerObject.ProductionFacilities.values():
                    SaveData += f"{Facility.Name}:{Facility.Level}\n"
                PlayerDataFile.write(SaveData)


    async def Save_Player_Army(Self) -> None:
        UUID:int
        PlayerObject:Player
        for UUID, PlayerObject in Self.Data["Players"].items():
            SaveData = ""
            with open(join("Data", "PlayerArmy", f"{UUID}.roc"), 'w+') as PlayerDataFile:
                for InfantryID, Infantry in PlayerObject.Army.items():
                    SaveData += f"{InfantryID}:{Infantry.Level}:{Infantry.Type}\n"
                PlayerDataFile.write(SaveData)


    async def Choose_Team(Self, NewMember:DiscordMember, Choice:str, Interaction:DiscordInteraction) -> None:
        if Choice == "Maiden":
            if Self.Data["Planets"]["Analis"].Data["Protector Count"]-3 >= Self.Data["Planets"]["Titan"].Data["Protector Count"]:
                Choice:Planet = Self.Data["Planets"]["Titan"]
            elif Self.Data["Planets"]["Titan"].Data["Protector Count"]-3 >= Self.Data["Planets"]["Analis"].Data["Protector Count"]:
                Choice:Planet = Self.Data["Planets"]["Analis"]
            else:
                RandomNumber = randrange(0, 2)
                print(RandomNumber)
                Choice = list(Self.Data["Planets"].values())[RandomNumber]

        Self.Data["Players"].update({NewMember.id:Player(NewMember)})
        Self.Data["Players"][NewMember.id].Data["Team"] = Choice.Data["Name"]
        Choice.Data["Protector Count"] += 1
        await NewMember.add_roles(Self.Roles[Choice.Data["Name"]])

        MessageEmbed = Embed(title="Welcome")

        MessageEmbed.add_field(name="\u200b", value=f"Welcome to {Choice.Data['Name']}")

        Self.Logger.info(f"{NewMember.name} joined {Choice}")

        await Interaction.response.edit_message(embed=MessageEmbed, view=None)


    async def Send_Welcome(Self, NewMember:DiscordMember) -> None:
        MessageEmbed = Embed(title="Welcome")
        MessageView = View()
        ChooseAnalisButton = Button(label="Choose Analis", style=ButtonStyle.blurple, custom_id=f"{NewMember.id} Analis Choice", row=1)
        ChooseTitanButton = Button(label="Choose Titan", style=ButtonStyle.red, custom_id=f"{NewMember.id} Titan Choice", row=1)
        MaidensChoice = Button(label="Let the Maiden Choose", style=ButtonStyle.grey, custom_id=f"{NewMember.id} Maidens Choice", row=1)

        ChooseAnalisButton.callback = lambda ButtonInteraction: create_task(Self.Choose_Team(NewMember, "Analis", ButtonInteraction))
        ChooseTitanButton.callback = lambda ButtonInteraction: create_task(Self.Choose_Team(NewMember, "Titan", ButtonInteraction))
        MaidensChoice.callback = lambda ButtonInteraction: create_task(Self.Choose_Team(NewMember, "Maiden", ButtonInteraction))

        MessageView.add_item(ChooseAnalisButton)
        MessageView.add_item(ChooseTitanButton)
        MessageView.add_item(MaidensChoice)

        await NewMember.send(embed=MessageEmbed, view=MessageView)


    async def Guild_Guard(Self, Context:Context):
        if Context.guild is None:
            return "Unprotected"
        if Context.guild.id == Self.Guild.id: # DevServer
            return "Protected"
        return "Unprotected"