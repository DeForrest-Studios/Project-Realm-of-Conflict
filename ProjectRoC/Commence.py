from discord import Member
from discord import Guild as DiscordGuild
from discord import Role as DiscordRole
from discord.ext.commands import Context
from RealmOfConflict import RealmOfConflict
from Panels.PlayPanel import PlayPanel
from asyncio import create_task
from sys import exit

if __name__ == '__main__':
    Ether = RealmOfConflict()


    @Ether.command(aliases=["oc", "oC", "OC"])
    async def Play_Interaction(InitialContext: Context):
        if await Ether.Guild_Guard(InitialContext) == "Unprotected":
            return
        await InitialContext.message.delete()
        if InitialContext.author.id not in Ether.Data["Players"].keys() or Ether.Data["Players"][InitialContext.author.id].Data["Team"] is None:
            await Ether.Send_Welcome(InitialContext.author)
        elif InitialContext.author.id in Ether.Data["Panels"].keys():
            await Ether.Data["Panels"][InitialContext.author.id].DashboardMessage.delete()
            Ether.Data["Panels"].update({InitialContext.author.id:PlayPanel(Ether, InitialContext)})
        else:
            Ether.Data["Panels"].update({InitialContext.author.id:PlayPanel(Ether, InitialContext)})

    # Override of existing on_ready from discord.py
    @Ether.event
    async def on_guild_available(Guild):
        Ether.Logger.info(f"Guild available: {Guild.name}")
        if len(Ether.guilds) > 1:
            Ether.Logger.info("Your bot is in two places, whatever you're doing, just stop please.")
            Ether.Logger.info("Killing the bot.")
            exit()
        Ether.Guild:DiscordGuild = Ether.guilds[0]

        if Ether.Guild.id == 1190385562604015626:
            Ether.Logger.info("Running on Developer Server")
            Ether.Roles:{str:DiscordRole} = {
                "Titan":Ether.Guild.get_role(1190385562604015629),
                "Analis":Ether.Guild.get_role(1190385562604015628),
            }
            Ether.Data.update({"Simulation Channel": Ether.Guild.get_channel(1190385563505791017)})

        if Ether.Guild.id == 1135093444734361702:
            Ether.Logger.info("Running on Unstable Server")
            Ether.Roles:{str:DiscordRole} = {
                "Titan":Ether.Guild.get_role(1135093444734361705),
                "Analis":Ether.Guild.get_role(1135093444734361704),
            }
            Ether.Data.update({"Simulation Channel": Ether.Guild.get_channel(1135093445191532607)})

        if Ether.Guild.id == 1063056213589368953:
            Ether.Logger.info("Running on Official Server")
            Ether.Roles:{str:DiscordRole} = {
                "Titan":Ether.Guild.get_role(1190386754327412870),
                "Analis":Ether.Guild.get_role(1190386754327412869),
            }
            Ether.Data.update({"Simulation Channel": Ether.Guild.get_channel(1190386761831039096)})

        Ether.Load_Players()
        create_task(Ether.Autosave())
        Ether.Logger.info("Bot is alive")


    # Override of existing on_member_join from discord.py
    # This sends a message to the player
    @Ether.event
    async def on_member_join(NewMember:Member) -> None:
        await Ether.Send_Welcome(NewMember)

    Ether.run(Ether.Get_Token("Cavan"))
