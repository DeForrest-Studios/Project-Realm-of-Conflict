class Planet():
    def __init__(Self, Name:str, ROC):
        Self.Data:{str:...} = {
            "Name": Name,
            "ROC": ROC,
            "Population": 92543784546,
            "Protector Count": 0,
            "Damage": 0,
            "Offensive Power": 0,
            "Defensive Power": 0,
            "Energy Sapping": 0,
            "Domination": 0,
            "Healing": 0,
            "Hacking": 0,
            "Raiding": 0,
            "Earned Pool": 0,
            "Average Earnings": 0,
            "Population Dominated": 0,
            "Population Healed": 0,
            "Population Loss": 0,
            "Offensive Leaderboard": {},
            "Defensive Leaderboard": {},
            "Energy Sapping Leaderboard": {},
            "Role": None,
        }

    def Refresh_Power(Self) -> None:
        for Player in Self.Data["Role"].members:
            Self.Data["Offensive Power"] += Self.Data["ROC"].Data["Players"][Player.id].Data["Offensive Power"]