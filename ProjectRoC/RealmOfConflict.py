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
from typing import Union, Dict
from Planet import Planet
from Player import Player
from random import randrange
from Tables import InfantryToObject
from Simulation import Simulation
from Structures import ManufacturingFacility

class RealmOfConflict(Bot):
    def __init__(Self) -> None:
        super().__init__(command_prefix=['R', 'r'], intents=Intents.all())
        Self.remove_command('help')
        Self.Data = {
            "Players": {"42069": Player("Test")},
            "Planets": {
                "Analis": Planet("Analis", Self),
                "Titan": Planet("Titan", Self),
            },
            "Panels": {},
        }
        Self.Records = {
            "Skirmish Count": 0,
            "PlayerInteractions":0,
        }
        Self.DataDirectory = "Data"
        Self.Guild = None
        Self.Roles = None
        Self.Members = None
        Self.CoreSimulation = None
        Self.Materials:Union[str] = [Facility.OutputItem for Facility in Self.Data["Players"]["42069"].ProductionFacilities.values()]
        Self.Initalize_Logger()

    
    def Dev_Mode(Self):
        Self.DataDirectory = "DevData"


    def Get_Token(Self, Key:str) -> None:
        Self.Logger.info("Getting token")
        with open(join("Keys.txt")) as KeyFile:
            Line:str
            for Line in KeyFile:
                LineData:Union[str] = Line.split("~")
                if Key == LineData[0]:
                    return LineData[1].strip()
        Self.Logger.info("Got dat token")


    def Initialize(Self) -> None:
        Self.Logger.info("Running on the bot")
        Self.run(Self.Get_Token("Cavan"))
        Self.Logger.info("The bot should be running now")

    
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
        Self.Logger.info("Logger is setup")


    def Load_Records(Self):
        if exists(join(Self.DataDirectory, f"record.roc")) == False: return
        Self.Logger.info("Loading Records")
        with open(join(Self.DataDirectory, f"record.roc"), 'r') as RecordsFile:
            RecordData = RecordsFile.readlines()
            for Line in RecordData:
                if Line != "":
                    Data:Union[str:str] = Line.split(":")
                    RecordName:str = Data[0]
                    RecordValue:str = Data[1]
                    if RecordValue[0].isdigit():
                        RecordValue = int(RecordValue)
                    elif type(RecordValue.split(".")) != list:
                        RecordValue = float(RecordValue)
                    Self.Records[RecordName] = RecordValue

    async def Save_Record(Self) -> None:
        Self.Logger.info("Saving Records")
        SaveData = ""
        Counter = 0
        for RecordName, RecordValue in Self.Records.items():
            SaveData += f"{RecordName}:{RecordValue}"
            if Counter != len(Self.Records.keys()) - 1:
                SaveData += "\n"
            Counter += 1

        with open(join(Self.DataDirectory, f"record.roc"), 'w+') as RecordsFile:
            RecordsFile.write(SaveData)


    def Load_Players(Self) -> None:
        Self.Logger.info("Loading Players")
        if not exists(Self.DataDirectory):
            return
        Self.Load_Player_Data()
        Self.Load_Player_Inventories()
        Self.Load_Player_Army()
        Self.Load_Planet_Data()
        Self.Load_Player_Production_Facilities()
        Self.Load_Player_Manufacturing_Facilities()
        Self.Load_Player_Skills()
        Self.Logger.info("Players have been loaded")


    def Load_Player_Data(Self) -> None:
        Self.Logger.info("Loading Player Data")
        Self.Members:Dict[int:DiscordMember] = {M.id:M for M in Self.Guild.members}
        if not exists(join(Self.DataDirectory, "PlayerData")):
            return
        PlayerDataFileName:str
        for PlayerDataFileName in listdir(join(Self.DataDirectory, "PlayerData")):
            PlayerUUID:int = int(PlayerDataFileName.split(".")[0])
            if PlayerUUID not in Self.Members:continue
            with open(join(Self.DataDirectory, "PlayerData", f"{PlayerUUID}.data.roc"), 'r') as PlayerDataFile:
                PlayerData:Union[str] = [Line.strip() for Line in PlayerDataFile.readlines()]
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
        if not exists(join(Self.DataDirectory, "PlanetData")):
            return
        Self.Logger.info("Loading Planet Data")
        PlayerDataFileName:str
        for PlanetDataFileName in listdir(join(Self.DataDirectory, "PlanetData")):
            PlanetName:str = PlanetDataFileName.split(".")[0]
            with open(join(Self.DataDirectory, "PlanetData", f"{PlanetName}.data.roc"), 'r') as PlanetDataFile:
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
        if not exists(join(Self.DataDirectory, "PlayerInventories")):
            return
        Self.Logger.info("Loading Player Inventories")
        PlayerDataFileName:str
        for PlayerDataFileName in listdir(join(Self.DataDirectory, "PlayerInventories")):
            PlayerUUID = int(PlayerDataFileName.split(".")[0])
            if PlayerUUID not in Self.Members:continue
            if PlayerUUID == 42069: continue
            with open(join(Self.DataDirectory, "PlayerInventories", f"{PlayerUUID}.inventory.roc"), 'r') as PlayerDataFile:
                PlayerData = [Line.strip() for Line in PlayerDataFile.readlines()]
                Field:str
                for Field in PlayerData:
                    Contents:str = Field.split(":")
                    Name:str = Contents[0]
                    Value = float(Contents[1])
                    Self.Data["Players"][PlayerUUID].Inventory[Name] = Value


    def Load_Player_Production_Facilities(Self) -> None:
        if not exists(join(Self.DataDirectory, "PlayerProductionFacilities")):
            return
        Self.Logger.info("Loading Player Production Facilities")
        PlayerDataFileName:str
        for PlayerDataFileName in listdir(join(Self.DataDirectory, "PlayerProductionFacilities")):
            PlayerUUID = int(PlayerDataFileName.split(".")[0])
            if PlayerUUID not in Self.Members:continue
            if PlayerUUID == 42069: continue
            with open(join(Self.DataDirectory, "PlayerProductionFacilities", f"{PlayerUUID}.production.roc"), 'r') as PlayerDataFile:
                PlayerData = [Line.strip() for Line in PlayerDataFile.readlines()]
                Field:str
                for Field in PlayerData:
                    Contents:str = Field.split(":")
                    Name:str = Contents[0]
                    Value = int(Contents[1])
                    Self.Data["Players"][PlayerUUID].ProductionFacilities[Name].Level = Value
                    Self.Data["Players"][PlayerUUID].ProductionFacilities[Name].Refresh_Stats()


    def Load_Player_Manufacturing_Facilities(Self) -> None:
        if not exists(join(Self.DataDirectory, "PlayerManufacturingFacilities")):
            return
        Self.Logger.info("Loading Player Manufacturing Facilities")
        PlayerDataFileName:str
        for PlayerDataFileName in listdir(join(Self.DataDirectory, "PlayerManufacturingFacilities")):
            PlayerUUID = int(PlayerDataFileName.split(".")[0])
            if PlayerUUID not in Self.Members:continue
            if PlayerUUID == 42069: continue
            with open(join(Self.DataDirectory, "PlayerManufacturingFacilities", f"{PlayerUUID}.manufacturing.roc"), 'r') as PlayerDataFile:
                PlayerData = [Line.strip() for Line in PlayerDataFile.readlines()]
                Field:str
                for Field in PlayerData:
                    Contents:str = Field.split(":")
                    Name:str = Contents[0]
                    Level = int(Contents[1])
                    Recipe = Contents[2]
                    Self.Data["Players"][PlayerUUID].ManufacturingFacilities.update({Name:ManufacturingFacility(Name)})
                    Self.Data["Players"][PlayerUUID].ManufacturingFacilities[Name].Data["Level"] = Level
                    Self.Data["Players"][PlayerUUID].ManufacturingFacilities[Name].Data["Recipe"] = Recipe
                    Self.Data["Players"][PlayerUUID].ManufacturingFacilities[Name].Refresh_Stats()


    def Load_Player_Army(Self) -> None:
        if not exists(join(Self.DataDirectory, "PlayerArmy")):
            return
        Self.Logger.info("Loading Player Armies")
        PlayerDataFileName:str
        for PlayerDataFileName in listdir(join(Self.DataDirectory, "PlayerArmy")):
            PlayerUUID = int(PlayerDataFileName.split(".")[0])
            if PlayerUUID not in Self.Members:continue
            if PlayerUUID == 42069: continue
            with open(join(Self.DataDirectory, "PlayerArmy", f"{PlayerUUID}.army.roc"), 'r') as PlayerDataFile:
                PlayerData = [Line.strip() for Line in PlayerDataFile.readlines()]
                for Field in PlayerData:
                    Contents = Field.split(":")
                    Name:str = Contents[0]
                    Level = int(Contents[1])
                    Type:str = Contents[2]
                    Self.Data["Players"][PlayerUUID].Army.update({Name:InfantryToObject[Type](Level, Type, Self.Data["Players"][PlayerUUID], Name=Name)})
            [Self.Data["Planets"][_].Refresh_Power() for _ in Self.Data["Planets"]]
            Self.Data["Players"][PlayerUUID].Refresh_Power()
            

    def Load_Player_Skills(Self):
        if not exists(join(Self.DataDirectory, "PlayerSkills")):
            return
        Self.Logger.info("Loading Player Skills")
        PlayerDataFileName:str
        for PlayerDataFileName in listdir(join(Self.DataDirectory, "PlayerSkills")):
            PlayerUUID = int(PlayerDataFileName.split(".")[0])
            if PlayerUUID not in Self.Members:continue
            if PlayerUUID == 42069: continue
            with open(join(Self.DataDirectory, "PlayerSkills", f"{PlayerUUID}.skills.roc"), 'r') as PlayerDataFile:
                PlayerData = [Line.strip() for Line in PlayerDataFile.readlines()]
                Field:str
                for Field in PlayerData:
                    Contents:str = Field.split(":")
                    Name:str = Contents[0]
                    Value = int(Contents[1])
                    Self.Data["Players"][PlayerUUID].Skills[Name] = Value
            Self.Data["Players"][PlayerUUID].Refresh_All_Skills()

    
    async def Engage_Simulation(Self) -> bool:
        print("Attempting to engage simulation")
        if Self.CoreSimulation is None:
            Self.Logger.info("Engaging Simulation")
            Self.CoreSimulation = Simulation(Self, Self.Data["Planets"]["Analis"], Self.Data["Planets"]["Titan"])
            return True
        else:
            Self.Logger.info("Failed to engage simulation")
            return False


    async def Autosave(Self) -> None:
        if not exists(Self.DataDirectory):
            mkdir(Self.DataDirectory)
        if not exists(join(Self.DataDirectory, "PlayerData")):
            mkdir(join(Self.DataDirectory, "PlayerData"))
        if not exists(join(Self.DataDirectory, "PlayerInventories")):
            mkdir(join(Self.DataDirectory, "PlayerInventories"))
        if not exists(join(Self.DataDirectory, "PlayerProductionFacilities")):
            mkdir(join(Self.DataDirectory, "PlayerProductionFacilities"))
        if not exists(join(Self.DataDirectory, "PlayerManufacturingFacilities")):
            mkdir(join(Self.DataDirectory, "PlayerManufacturingFacilities"))
        if not exists(join(Self.DataDirectory, "PlayerArmy")):
            mkdir(join(Self.DataDirectory, "PlayerArmy"))
        if not exists(join(Self.DataDirectory, "PlayerSkills")):
            mkdir(join(Self.DataDirectory, "PlayerSkills"))
        if not exists(join(Self.DataDirectory, "PlanetData")):
            mkdir(join(Self.DataDirectory, "PlanetData"))
        while True:
            await sleep(5)
            Self.Logger.info("Autosaving")
            await Self.Save_Player_Data()
            await Self.Save_Player_Inventories()
            await Self.Save_Player_ProductionFacilities()
            await Self.Save_Player_ManufacturingFacilities()
            await Self.Save_Player_Army()
            await Self.Save_Planet_Data()
            await Self.Save_Player_Skills()
            await Self.Save_Record()

    async def Save_Planet_Data(Self) -> None:
        Self.Logger.info("Saving Planet Data")
        Name:str
        PlanetObject:Planet
        for Name, PlanetObject in Self.Data["Planets"].items():
            SaveData = ""
            with open(join(Self.DataDirectory, "PlanetData", f"{Name}.data.roc"), 'w+') as PlayerDataFile:
                for Name, Value in PlanetObject.Data.items():
                    SaveData += f"{Name}:{Value}\n"
                PlayerDataFile.write(SaveData)

    async def Save_Player_Data(Self) -> None:
        Self.Logger.info("Saving Player Data")
        UUID:int
        PlayerObject:Player
        for UUID, PlayerObject in Self.Data["Players"].items():
            SaveData = ""
            with open(join(Self.DataDirectory, "PlayerData", f"{UUID}.data.roc"), 'w+') as PlayerDataFile:
                for Name, Value in PlayerObject.Data.items():
                    SaveData += f"{Name}:{Value}\n"
                PlayerDataFile.write(SaveData)


    async def Save_Player_Inventories(Self) -> None:
        Self.Logger.info("Saving Player Inventories")
        UUID:int
        PlayerObject:Player
        for UUID, PlayerObject in Self.Data["Players"].items():
            SaveData = ""
            with open(join(Self.DataDirectory, "PlayerInventories", f"{UUID}.inventory.roc"), 'w+') as PlayerDataFile:
                for Name, Value in PlayerObject.Inventory.items():
                    SaveData += f"{Name}:{Value}\n"
                PlayerDataFile.write(SaveData)


    async def Save_Player_ProductionFacilities(Self) -> None:
        Self.Logger.info("Saving Player Production Facilities")
        UUID:int
        PlayerObject:Player
        for UUID, PlayerObject in Self.Data["Players"].items():
            SaveData = ""
            with open(join(Self.DataDirectory, "PlayerProductionFacilities", f"{UUID}.production.roc"), 'w+') as PlayerDataFile:
                for Facility in PlayerObject.ProductionFacilities.values():
                    SaveData += f"{Facility.Name}:{Facility.Level}\n"
                PlayerDataFile.write(SaveData)


    async def Save_Player_ManufacturingFacilities(Self) -> None:
        Self.Logger.info("Saving Player Manufacturing Facilities")
        UUID:int
        PlayerObject:Player
        for UUID, PlayerObject in Self.Data["Players"].items():
            SaveData = ""
            with open(join(Self.DataDirectory, "PlayerManufacturingFacilities", f"{UUID}.manufacturing.roc"), 'w+') as PlayerDataFile:
                for Facility in PlayerObject.ManufacturingFacilities.values():
                    SaveData += f"{Facility.Data['Name']}:{Facility.Data['Level']}:{Facility.Data['Recipe']}\n"
                PlayerDataFile.write(SaveData)


    async def Save_Player_Army(Self) -> None:
        Self.Logger.info("Saving Player Armies")
        UUID:int
        PlayerObject:Player
        for UUID, PlayerObject in Self.Data["Players"].items():
            SaveData = ""
            with open(join(Self.DataDirectory, "PlayerArmy", f"{UUID}.army.roc"), 'w+') as PlayerDataFile:
                for InfantryID, Infantry in PlayerObject.Army.items():
                    SaveData += f"{InfantryID}:{Infantry.Tier}:{Infantry.Type}\n"
                PlayerDataFile.write(SaveData)


    async def Save_Player_Skills(Self) -> None:
        Self.Logger.info("Saving Player Skills")
        UUID:int
        PlayerObject:Player
        for UUID, PlayerObject in Self.Data["Players"].items():
            SaveData = ""
            with open(join(Self.DataDirectory, "PlayerSkills", f"{UUID}.skills.roc"), 'w+') as PlayerDataFile:
                for Name, Level in PlayerObject.Skills.items():
                    SaveData += f"{Name}:{Level}\n"
                PlayerDataFile.write(SaveData)


    async def Choose_Team(Self, NewMember:DiscordMember, Choice:str, Interaction:DiscordInteraction) -> None:
        if Choice == "Maiden":
            if Self.Data["Planets"]["Analis"].Data["Protector Count"]-3 >= Self.Data["Planets"]["Titan"].Data["Protector Count"]:
                Choice:Planet = Self.Data["Planets"]["Titan"]
            elif Self.Data["Planets"]["Titan"].Data["Protector Count"]-3 >= Self.Data["Planets"]["Analis"].Data["Protector Count"]:
                Choice:Planet = Self.Data["Planets"]["Analis"]
            else:
                RandomNumber = randrange(0, 2)
                Choice = list(Self.Data["Planets"].values())[RandomNumber]
        else:
            Choice:Planet = Self.Data["Planets"][Choice]

        Self.Data["Players"].update({NewMember.id:Player(NewMember)})
        Self.Data["Players"][NewMember.id].Data["Team"] = Choice.Data["Name"]
        Self.Data["Players"][NewMember.id].Data["Maiden's Grace"] = 1
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

        Self.Logger.info(f"Sending welcome to {NewMember.name}")
        await NewMember.send(embed=MessageEmbed, view=MessageView)


    async def Guild_Guard(Self, Context:Context):
        if Context.guild is None:
            return "Unprotected"
        if Context.guild.id == Self.Guild.id: # DevServer
            return "Protected"
        return "Unprotected"