from asyncio import sleep, create_task
from discord import Embed, File
from random import randrange
from Tables import MaterialTable, RaidingTable
from os.path import join

class Simulation:
    def __init__(Self, Ether, Analis, Titan) -> None:
        print("Initializing Simulation Object")
        create_task(Self._Core_Simulation(Ether, Analis, Titan))

    async def _Generate_Simulation_Reports(Self, Analis, Titan) -> None:
        Self.AnalisEmbedReportString = "".join((f"Analis Population.: {format(Analis.Data['Population'], ',')}\n",
                                                f"Analis Attack: {format(Analis.Data['Offensive Power'], ',')}\n",
                                                f"Analis Defense: {format(Analis.Data['Defensive Power'], ',')}\n",
                                                f"Analis Energy Sapping: {format(Analis.Data['Energy Sapping'], ',')}\n",
                                                f"Total Analisian Protectors: {format(Analis.Data['Protector Count'], ',')}\n",
                                                f"Average Analisian Players Earned from Hacking: ${format(Analis.Data['Average Earnings'])}\n",
                                                f"Analisian Domination: {format(Analis.Data['Domination'], ',')}\n",
                                                f"Dominated: {format(Analis.Data['Population Dominated'], ',')} Pop.\n",
                                                f"Analisian Healing: {format(Analis.Data['Healing'], ',')}\n",
                                                f"Healed: {format(Analis.Data['Population Healed'], ',')} Pop.\n",))

        Self.TitanEmbedReportString = "".join((f"Titan Population.: {format(Titan.Data['Population'], ',')}\n",
                                               f"Titan Attack: {format(Titan.Data['Offensive Power'], ',')}\n",
                                               f"Titan Defense: {format(Titan.Data['Defensive Power'], ',')}\n",
                                               f"Titan Energy Sapping: {format(Titan.Data['Energy Sapping'], ',')}\n",
                                               f"Total Titan Protectors: {format(Titan.Data['Protector Count'], ',')}\n",
                                               f"Average Titan Players Earned from Hacking: ${format(Titan.Data['Average Earnings'])}\n",
                                               f"Titan Domination: {format(Titan.Data['Domination'], ',')}\n",
                                               f"Dominated: {format(Titan.Data['Population Dominated'], ',')} Pop.\n",
                                               f"Titan Healing: {format(Titan.Data['Healing'], ',')}\n",
                                               f"Healed: {format(Titan.Data['Population Healed'], ',')} Pop.\n\n"))

        if Self.VictoriousPlanet is not None:
            Self.EmbedReportString = f"**{Self.VictoriousPlanet} has claimed victory over {Self.DestroyedPlanet}.**\n\n", Self.EmbedReportString
            Self.FileReportString = f"**{Self.VictoriousPlanet} has claimed victory over {Self.DestroyedPlanet}.**\n\n", Self.FileReportString
            Self.ReportEmbed.add_field(name="\u200b", value=Self.EmbedReportString)

        if Self.AnalisDefended:
            Self.AnalisEmbedReportString += f"Analis defended Titan's Attack\n\n"
        else:
            Self.AnalisEmbedReportString += "".join((f"Analis lost {format(Analis.Data['Population Loss'], ',')} population\n",
                                             f"Analis's population is now {format(Analis.Data['Population'], ',')}\n\n"))

        if Self.TitanDefended:
            Self.TitanEmbedReportString += f"Titan defended Analis's Attack\n\n"
        else:
            Self.TitanEmbedReportString += "".join((f"Titan lost {format(Titan.Data['Population Loss'], ',')} population\n",
                                            f"Titan's population is now {format(Titan.Data['Population'], ',')}\n\n"))

        Self.ReportEmbed.add_field(name="\u200b", value=Self.AnalisEmbedReportString, inline=False)
        Self.ReportEmbed.add_field(name="\u200b", value=Self.TitanEmbedReportString, inline=False)

    async def _Core_Simulation(Self, Ether, Analis, Titan) -> None:
        Self.VictoriousPlanet = None
        Self.DestroyedPlanet = None

        while True:
            Ether.Logger.info("Starting core simulation loop")
            Self.AnalisDefended = False
            Self.TitanDefended = False
            Ether.Records['Skirmish Count'] += 1
            Self.ReportEmbed = Embed(title="Simulation Report")
            Self.ReportEmbed.add_field(name="Skirmish", value=Ether.Records['Skirmish Count'], inline=False)
            Self.VictoriousPlanet = None
            
            Analis.Data["Offensive Power"] = 0
            Analis.Data["Defensive Power"] = 0
            Analis.Data["Healing"] = 0
            Analis.Data["Hacking"] = 0
            Analis.Data["Energy Sapping"] = 0
            Analis.Data["Domination"] = 0
            Analis.Data["Population Loss"] = 0
            Analis.Data["Population Healed"] = 0
            Analis.Data["Population Dominated"] = 0
            Titan.Data["Offensive Power"] = 0
            Titan.Data["Defensive Power"] = 0
            Titan.Data["Healing"] = 0
            Titan.Data["Hacking"] = 0
            Titan.Data["Energy Sapping"] = 0
            Titan.Data["Domination"] = 0
            Titan.Data["Population Loss"] = 0
            Titan.Data["Population Healed"] = 0
            Titan.Data["Population Dominated"] = 0
            
            # Get stats
            for Player in Ether.Data["Players"].values():
                if Player.Data["Team"] == "Analis":
                    Analis.Data["Offensive Power"] += Player.Data["Offensive Power"]
                    Analis.Data["Defensive Power"] += Player.Data["Defensive Power"]
                    Analis.Data["Healing"] += Player.Skills["Healing"]
                    Analis.Data["Energy Sapping"] += Player.Data["Energy Sapping"]
                    Analis.Data["Domination"] += Player.Skills["Domination"]
                    Analis.Data["Hacking"] += Player.Skills["Hacking"]
                if Player.Data["Team"] == "Titan":
                    Titan.Data["Offensive Power"] += Player.Data["Offensive Power"]
                    Titan.Data["Defensive Power"] += Player.Data["Defensive Power"]
                    Titan.Data["Healing"] += Player.Skills["Healing"]
                    Titan.Data["Energy Sapping"] += Player.Data["Energy Sapping"]
                    Titan.Data["Domination"] += Player.Skills["Domination"]
                    Titan.Data["Hacking"] += Player.Skills["Hacking"]

            # Energy Sapping Phase
            if Analis.Data['Defensive Power'] - Titan.Data['Energy Sapping'] <= 0:
                Analis.Data['Defensive Power'] = 0
            else:
                Analis.Data['Defensive Power'] -= Titan.Data['Energy Sapping']

            if Titan.Data['Defensive Power'] - Analis.Data['Energy Sapping'] <= 0:
                Titan.Data['Defensive Power'] = 0
            else:
                Titan.Data['Defensive Power'] -= Analis.Data['Energy Sapping']

            # # Domination Damage Phase
            Titan.Data['Population Dominated'] = Titan.Data['Domination'] * 40000
            Analis.Data['Population'] -= Titan.Data['Population Dominated']

            Analis.Data['Population Dominated'] = Analis.Data['Domination'] * 40000
            Titan.Data['Population'] -= Analis.Data['Population Dominated']

            # # Healing Phase
            Titan.Data['Population Healed'] = Titan.Data['Healing'] * 80000
            Titan.Data['Population'] += Titan.Data['Population Healed']
            Analis.Data['Population Healed'] = Analis.Data['Healing'] * 80000
            Analis.Data['Population'] += Analis.Data['Population Healed']

            # # # Hacking Phase
            Analis.Data["Earned Pool"] = Analis.Data["Hacking"] * 8500
            Titan.Data["Earned Pool"] = Titan.Data["Hacking"] * 8500
            Self.EarnedPool = Analis.Data["Earned Pool"] + Titan.Data["Earned Pool"]

            Analis.Data['Population Loss'] += (Analis.Data['Population Healed'] - Titan.Data['Population Dominated'])
            Titan.Data['Population Loss'] += (Titan.Data['Population Healed'] - Analis.Data['Population Dominated'])

            while Self.EarnedPool > 0:
                for Player in Ether.Data["Players"].values():
                    if Player.Data["Team"] == "Analis":
                        if Analis.Data["Protector Count"] == 0:
                            Analis.Data["Average Earnings"] = round(Analis.Data["Earned Pool"] / (Analis.Data["Protector Count"] + 1), 2)
                        else:
                            Analis.Data["Average Earnings"] = round(Analis.Data["Earned Pool"] / (Analis.Data["Protector Count"]), 2)
                        Player.Data["Wallet"] = round(Player.Data["Wallet"] + Analis.Data["Average Earnings"], 2)
                        Self.EarnedPool = round(Self.EarnedPool - Analis.Data["Average Earnings"], 2)
                    if Player.Data["Team"] == "Titan":
                        if Titan.Data["Protector Count"] == 0:
                            Titan.Data["Average Earnings"] = round(Titan.Data["Earned Pool"] / (Titan.Data["Protector Count"] + 1), 2)
                        else:
                            Titan.Data["Average Earnings"] = round(Titan.Data["Earned Pool"] / (Titan.Data["Protector Count"]), 2)
                        Player.Data["Wallet"] = round(Player.Data["Wallet"] + Titan.Data["Average Earnings"], 2)
                        Self.EarnedPool = round(Self.EarnedPool - Titan.Data["Average Earnings"], 4)

            # Raiding Phase
            Self.Raids = ""
            for Player in Ether.Data['Players'].values():
                if Player.Skills["Raiding"] != 0:
                    PlayerRaidSuccesful = False
                    PlayerRaidString = ""
                    for RotationCount in range(Player.Skills["Raiding"]):
                        for Item in RaidingTable.items():
                            Roll = randrange(0, 100)
                            if Roll <= Item[1]:
                                PlayerRaidSuccesful = True
                                MaterialScavenged = list(MaterialTable.keys())[randrange(0, (len(MaterialTable.keys()) - 1))]
                                Start, End = MaterialTable[MaterialScavenged][0], MaterialTable[MaterialScavenged][1]
                                MaterialScavengedAmount = randrange(Start, End)
                                Player.Inventory[MaterialScavenged] = round(Player.Inventory[MaterialScavenged] + MaterialScavengedAmount, 2)
                                PlayerRaidString += f'\n{MaterialScavenged}: {MaterialScavengedAmount} \n'
                    if PlayerRaidSuccesful == True:
                        Self.Raids += f"{Player.Data['Name']} raided an obtained:\n"
                        Self.Raids += PlayerRaidString
                    PlayerRaidSuccesful = False
                        

            # Titan attacking Analis Phase
            if Titan.Data['Offensive Power'] >= Analis.Data['Defensive Power']:
                Ether.Logger.info("Titan attacked Analis")
                Titan.Data['Damage'] = (Titan.Data['Offensive Power'] - Analis.Data['Defensive Power'])
                if Analis.Data['Population'] - Titan.Data['Damage'] * 2 <= 0:
                    Analis.Data['Population'] = 0
                    Self.VictoriousPlanet = "Titan"
                    Self.DestroyedPlanet = "Analis"
                else:
                    Analis.Data['Population Loss'] = (Titan.Data['Damage'] * 2)
                    Analis.Data['Population'] -= (Titan.Data['Damage'] * 2)
            else:
                Ether.Logger.info("Analis defended against Titan")
                Self.AnalisDefended = True

            # Analis Attacking Titan Phase
            if Analis.Data['Offensive Power'] >= Titan.Data['Defensive Power']:
                Ether.Logger.info("Analis attacked Titan")
                Analis.Data['Damage'] = (Analis.Data['Offensive Power'] - Titan.Data['Defensive Power'])
                if Titan.Data['Population'] - Analis.Data['Damage'] * 2 <= 0:
                    Titan.Data['Population'] = 0
                    Self.VictoriousPlanet = "Analis"
                    Self.DestroyedPlanet = "Titan"
                else:
                    Titan.Data['Population Loss'] = (Analis.Data['Damage'] * 2)
                    Titan.Data['Population'] -= (Analis.Data['Damage'] * 2)
            else:
                Ether.Logger.info("Titan defended against Analis")
                Self.TitanDefended = True


            Ether.Logger.info("Sending Simulation Report")
            await create_task(Self._Generate_Simulation_Reports(Analis, Titan))

            if Self.VictoriousPlanet is None:
                await Ether.Data["Simulation Channel"].send(embed=Self.ReportEmbed)
                if Self.Raids != "":
                    with open(join('Data', f'Raid.txt'), "w+", encoding='utf-8') as RaidFile:
                        RaidFile.write(Self.Raids)
                    # RaidEmbed = Embed(title="Raiding Report")
                    # RaidEmbed.add_field(name="\u200b", value=Self.Raids, inline=False)
                    with open(join('Data', f'Raid.txt'), "rb") as RaidFile:
                        await Ether.Data["Simulation Channel"].send(file=File(RaidFile, filename=f'Raid.txt'))

            if Self.VictoriousPlanet is not None:
                Ether.Logger.info(f"{Self.VictoriousPlanet} won, and destroyed {Self.DestroyedPlanet}")
                for Player in Ether["Online Players"].values():
                    if Player.Data["Team"] == Self.VictoriousPlanet:
                        Player.victories += 1

                Ether.Data["Planets"][Self.VictoriousPlanet].Data["Wins"] += 1
                Ether.Data["Planets"][Self.DestroyedPlanet].Data["Losses"] += 1
                await Ether.Data["Simulation Channel"].send(embed=Self.ReportEmbed)
                if Self.Raids != "":
                    await Ether.Data["Simulation Channel"].send(embed=Self.Raids)
                break

            await sleep(300)
