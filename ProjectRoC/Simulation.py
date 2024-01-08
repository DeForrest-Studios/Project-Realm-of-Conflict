from asyncio import sleep, create_task
from discord import Embed


class Simulation:
    def __init__(Self, Ether, Analis, Titan) -> None:
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
        
        # if Analis.Data["Protector Count"] >= 3 and Titan.Data["Protector Count"] >= 3:
        #     Self.AnalisLeaderboardReportString = "".join((f"Top Analis Offensive Power Players:\n",
        #         f"\t1: {Analis.OffensiveLeaderboard[0][0].Data['Name']} with {format(Analis.OffensiveLeaderboard[0][1], ',')} Offensive Power\n",
        #         f"\t2: {Analis.OffensiveLeaderboard[1][0].Data['Name']} with {format(Analis.OffensiveLeaderboard[1][1], ',')} Offensive Power\n",
        #         f"\t3: {Analis.OffensiveLeaderboard[2][0].Data['Name']} with {format(Analis.OffensiveLeaderboard[2][1], ',')} Offensive Power\n\n",

        #         f"Top Analis Defensive Power Players:\n",
        #         f"\t1: {Analis.DefensiveLeaderboard[0][0].Data['Name']} with {format(Analis.DefensiveLeaderboard[0][1], ',')} Defensive Power\n",
        #         f"\t2: {Analis.DefensiveLeaderboard[1][0].Data['Name']} with {format(Analis.DefensiveLeaderboard[1][1], ',')} Defensive Power\n",
        #         f"\t3: {Analis.DefensiveLeaderboard[2][0].Data['Name']} with {format(Analis.DefensiveLeaderboard[2][1], ',')} Defensive Power\n\n",

        #         f"Top Analis Energy Sapping Players:\n",
        #         f"\t1: {Analis.EnergySappingLeaderboard[0][0].Data['Name']} with {format(Analis.EnergySappingLeaderboard[0][1], ',')} Energy Sapping\n",
        #         f"\t2: {Analis.EnergySappingLeaderboard[1][0].Data['Name']} with {format(Analis.EnergySappingLeaderboard[1][1], ',')} Energy Sapping\n",
        #         f"\t3: {Analis.EnergySappingLeaderboard[2][0].Data['Name']} with {format(Analis.EnergySappingLeaderboard[2][1], ',')} Energy Sapping\n\n\n"))
            
        #     Self.TitanLeaderboardReportString = "".join((f"Top Titan Offensive Power Players:\n",
        #         f"\t1: {Titan.OffensiveLeaderboard[0][0].Data['Name']} with {format(Titan.OffensiveLeaderboard[0][1], ',')} Offensive Power\n",
        #         f"\t2: {Titan.OffensiveLeaderboard[1][0].Data['Name']} with {format(Titan.OffensiveLeaderboard[1][1], ',')} Offensive Power\n",
        #         f"\t3: {Titan.OffensiveLeaderboard[2][0].Data['Name']} with {format(Titan.OffensiveLeaderboard[2][1], ',')} Offensive Power\n\n",

        #         f"Top Titan Defensive Power Players:\n",
        #         f"\t1: {Titan.DefensiveLeaderboard[0][0].Data['Name']} with {format(Titan.DefensiveLeaderboard[0][1], ',')} Defensive Power\n",
        #         f"\t2: {Titan.DefensiveLeaderboard[1][0].Data['Name']} with {format(Titan.DefensiveLeaderboard[1][1], ',')} Defensive Power\n",
        #         f"\t3: {Titan.DefensiveLeaderboard[2][0].Data['Name']} with {format(Titan.DefensiveLeaderboard[2][1], ',')} Defensive Power\n\n",

        #         f"Top Titan Energy Sapping Players:\n",
        #         f"\t1: {Titan.EnergySappingLeaderboard[0][0].Data['Name']} with {format(Titan.EnergySappingLeaderboard[0][1], ',')} Energy Sapping\n",
        #         f"\t2: {Titan.EnergySappingLeaderboard[1][0].Data['Name']} with {format(Titan.EnergySappingLeaderboard[1][1], ',')} Energy Sapping\n",
        #         f"\t3: {Titan.EnergySappingLeaderboard[2][0].Data['Name']} with {format(Titan.EnergySappingLeaderboard[2][1], ',')} Energy Sapping\n\n"))
        #     Self.ReportEmbed.add_field(name="\u200b", value=Self.AnalisLeaderboardReportString, inline=False)
        #     Self.ReportEmbed.add_field(name="\u200b", value=Self.TitanLeaderboardReportString, inline=False)

    async def _Core_Simulation(Self, Ether, Analis, Titan) -> None:
        Self.VictoriousPlanet = None
        Self.DestroyedPlanet = None

        while True:
            Ether.Logger.info("Starting core simulation loop")
            Self.AnalisDefended = False
            Self.TitanDefended = False
            Ether.Data['Skirmish Count'] += 1
            Self.ReportEmbed = Embed(title="Simulation Report")
            Self.ReportEmbed.add_field(name="Skirmish", value=Ether.Data['Skirmish Count'], inline=False)
            Self.VictoriousPlanet = None
            Analis.OffensiveLeaderboard = {Player: Player.Data["Offensive Power"] for Player in Ether.Data["Players"].values() if Player.Data["Team"] == "Analis"}
            Analis.DefensiveLeaderboard = {Player: Player.Data["Defensive Power"] for Player in Ether.Data["Players"].values() if Player.Data["Team"] == "Analis"}
            # Analis.EnergySappingLeaderboard = {Player: Player.Data["Energy Sapping"] for Player in Ether.Data["Players"].values() if Player.Data["Team"] == "Analis"}

            Titan.OffensiveLeaderboard = {Player: Player.Data["Offensive Power"] for Player in Ether.Data["Players"].values() if Player.Data["Team"] == "Titan"}
            Titan.DefensiveLeaderboard = {Player: Player.Data["Defensive Power"] for Player in Ether.Data["Players"].values() if Player.Data["Team"] == "Titan"}
            # Titan.EnergySappingLeaderboard = {Player: Player.Data["Energy Sapping"] for Player in Ether.Data["Players"].values() if Player.Data["Team"] == "Titan"}

            Analis.OffensiveLeaderboard = sorted(Analis.OffensiveLeaderboard.items(), key=lambda x: x[1], reverse=True)
            Analis.DefensiveLeaderboard = sorted(Analis.DefensiveLeaderboard.items(), key=lambda x: x[1], reverse=True)
            # Analis.EnergySappingLeaderboard = sorted(Analis.EnergySappingLeaderboard.items(), key=lambda x: x[1], reverse=True)

            Titan.OffensiveLeaderboard = sorted(Titan.OffensiveLeaderboard.items(), key=lambda x: x[1], reverse=True)
            Titan.DefensiveLeaderboard = sorted(Titan.DefensiveLeaderboard.items(), key=lambda x: x[1], reverse=True)
            # Titan.EnergySappingLeaderboard = sorted(Titan.EnergySappingLeaderboard.items(), key=lambda x: x[1], reverse=True)
            Analis.Data["Offensive Power"] = 0
            Analis.Data["Defensive Power"] = 0
            Titan.Data["Offensive Power"] = 0
            Titan.Data["Defensive Power"] = 0
            # Get stats
            for Player in Ether.Data["Players"].values():
                if Player.Data["Team"] == "Analis":
                    Analis.Data["Offensive Power"] += Player.Data["Offensive Power"]
                    Analis.Data["Defensive Power"] += Player.Data["Defensive Power"]
                    # Analis.Data["Energy Sapping"] += Player.Data["Energy Sapping"]
                    # Analis.Data["Domination"] += Player.skills["Domination"]
                    # Analis.Data["Healing"] += Player.skills["Healing"]
                    # Analis.Data["Hacking"] += Player.skills["Hacking"]
                if Player.Data["Team"] == "Titan":
                    Titan.Data["Offensive Power"] += Player.Data["Offensive Power"]
                    Titan.Data["Defensive Power"] += Player.Data["Defensive Power"]
                    # Titan.Data["Energy Sapping"] += Player.Data["Energy Sapping"]
                    # Titan.Data["Domination"] += Player.skills["Domination"]
                    # Titan.Data["Healing"] += Player.skills["Healing"]
                    # Titan.Data["Hacking"] += Player.skills["Hacking"]

            # Energy Sapping Phase
            # if Analis.Data['Defensive Power'] - Titan.Data['Energy Sapping'] <= 0:
            #     Analis.Data['Defensive Power'] = 0
            # else:
            #     Analis.Data['Defensive Power'] -= Titan.Data['Energy Sapping']

            # if Titan.Data['Defensive Power'] - Analis.Data['Energy Sapping'] <= 0:
            #     Titan.Data['Defensive Power'] = 0
            # else:
            #     Titan.Data['Defensive Power'] -= Analis.Data['Energy Sapping']

            # Titan attacking Analis Phase
            if Titan.Data['Offensive Power'] >= Analis.Data['Defensive Power']:
                Ether.Logger.info("Titan attacked Analis")
                Titan.Data['Damage'] = (Titan.Data['Offensive Power'] - Analis.Data['Defensive Power'])
                if Analis.Data['Population'] - Titan.Data['Damage'] * 2 <= 0:
                    Analis.Data['Population'] = 0
                    Self.VictoriousPlanet = "Titan"
                    Self.DestroyedPlanet = "Analis"
                else:
                    Analis.Data['Population Loss'] += (Titan.Data['Damage'] * 2)
                    Analis.Data['Population'] -= (Titan.Data['Damage'] * 2)
            else:
                Ether.Logger.info("Analis defended against Titan")
                Self.AnalisDefended = True

            # Analis Attacking Titan Phase
            if Analis.Data['Offensive Power'] >= Titan.Data['Defensive Power']:
                Ether.Logger.info("Analis attacked Titan")
                Analis.Data['Damage'] += (Analis.Data['Offensive Power'] - Titan.Data['Defensive Power'])
                if Titan.Data['Population'] - Analis.Data['Damage'] * 2 <= 0:
                    Titan.Data['Population'] = 0
                    Self.VictoriousPlanet = "Analis"
                    Self.DestroyedPlanet = "Titan"
                else:
                    Titan.Data['Population Loss'] += (Analis.Data['Damage'] * 2)
                    Titan.Data['Population'] -= Analis.Data['Damage']
            else:
                Ether.Logger.info("Titan defended against Analis")
                Self.TitanDefended = True

            # # Domination Damage Phase
            # Titan.Data['Population Dominated'] = Analis.Data['Domination'] * 40000
            # Titan.Data['Population'] -= Titan.Data['Population Dominated']
            # Analis.Data['Population Dominated'] = Titan.Data['Domination'] * 40000
            # Analis.Data['Population'] -= Analis.Data['Population Dominated']

            # # Healing Phase
            # Titan.Data['Population Healed'] = Titan.Data['Healing'] * 80000
            # Titan.Data['Population'] += Titan.Data['Population Healed']
            # Analis.Data['Population Healed'] = Analis.Data['Healing'] * 80000
            # Analis.Data['Population'] += Analis.Data['Population Healed']

            # # Hacking Phase
            # Analis.Data["Earned Pool"] = Analis.Data["Hacking"] * 25000
            # Titan.Data["Earned Pool"] = Titan.Data["Hacking"] * 25000
            # Self.EarnedPool = Analis.Data["Earned Pool"] + Titan.Data["Earned Pool"]

            # Analis.Data['Population Loss'] += Analis.Data['Population Healed'] - Titan.Data['Population Dominated']
            # Titan.Data['Population Loss'] += Titan.Data['Population'] + Titan.Data['Population Healed'] - Analis.Data['Population Dominated']

            # while Self.EarnedPool > 0:
            #     for Player in Ether["Online Players"].values():
            #         if Player.team == "Analis":
            #             Analis.Data["Average Earnings"] = round(Analis.Data["Earned Pool"] / (Analis.Data["Protector Count"] + 1), 2)
            #             Player.wallet = round(Player.wallet + Analis.Data["Average Earnings"], 2)
            #             Self.EarnedPool = round(Self.EarnedPool - Analis.Data["Average Earnings"], 2)
            #         if Player.team == "Titan":
            #             Titan.Data["Average Earnings"] = round(Titan.Data["Earned Pool"] / (Titan.Data["Protector Count"] + 1), 2)
            #             Player.wallet = round(Player.wallet + Titan.Data["Average Earnings"], 2)
            #             Self.EarnedPool = round(Self.EarnedPool - Titan.Data["Average Earnings"], 4)

            # # Raiding Phase
            # Self.Raids = ""
            # for Player in Ether['Online Players'].values():
            #     if Player.skills["Raiding"] != 0:
            #         for rotation_count in range(Player.skills["Raiding"]):
            #             Self.player_items = []
            #             Self.player_materials = {}
            #             Self.experience_earned = randrange((Player.skills["Raiding"]+1)//8, 5 + Player.skills["Raiding"])
            #             Player.experience = round(Player.experience + Self.experience_earned, 2)
            #             for item in raiding_references["Items"].items():
            #                 roll = randrange(0, 100)
            #                 Self.item_tier = int(item[0].split(" ~ ")[0].split("r ")[1])
            #                 Self.item_name = item[0].split(" ~ ")[1]
            #                 if roll <= item[1]:
            #                     Self.generated_item = object_references[Self.item_name](Self.item_tier)
            #                     Player.items.append(Self.generated_item)
            #                     Self.player_items.append(Self.generated_item)
            #                     if await Is_Int(Self.generated_item.attack_power) is not False:
            #                         Player.Data["Offensive Power"] += Self.generated_item.attack_power
            #                     if await Is_Int(Self.generated_item.defensive_power) is not False:
            #                         Player.Data["Defensive Power"] += Self.generated_item.defensive_power
            #                     if await Is_Int(Self.generated_item.energy_sapping) is not False:
            #                         Player.Data["Energy Sapping"] += Self.generated_item.energy_sapping

            #             for material in raiding_references["Materials"].items():
            #                 roll = randrange(0, 100)
            #                 if roll <= material[1]:
            #                     quantity = randrange(1, Player.skills["Raiding"] * 4)
            #                     Player.inventory[material[0]] += quantity
            #                     Self.player_materials.update({material[0]: quantity})
            #         Self.Raids += f"\n{Player.Data['Name']} raided and got:\n"
            #         Self.Raids += '\n'.join([f'{item.id}\n' for item in Self.player_items])
            #         Self.Raids += '\n'.join([f'{item[1]} {item[0]}' for item in Self.player_materials.items()])
            #         Self.Raids += '\n\n'

            Ether.Logger.info("Sending Simulation Report")
            await create_task(Self._Generate_Simulation_Reports(Analis, Titan))

            if Self.VictoriousPlanet is None:
                await Ether.Data["Simulation Channel"].send(embed=Self.ReportEmbed)

            if Self.VictoriousPlanet is not None:
                Ether.Logger.info(f"{Self.VictoriousPlanet} won, and destroyed {Self.DestroyedPlanet}")
                for Player in Ether["Online Players"].values():
                    if Player.Data["Team"] == Self.VictoriousPlanet:
                        Player.victories += 1

                Ether.Data["Planets"][Self.VictoriousPlanet].Data["Wins"] += 1
                Ether.Data["Planets"][Self.DestroyedPlanet].Data["Losses"] += 1
                await Ether["Simulation Channel"].send(embed=Self.ReportEmbed)
                break

            await sleep(120)
