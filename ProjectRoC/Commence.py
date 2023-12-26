from discord import Member
from discord.ext.commands import Context
from RealmOfConflict import RealmOfConflict
from PlayPanel import PlayPanel
from asyncio import create_task

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
        print(f"Guild available: {Guild.name}")
        # if Guild.name in ["Guild available: Project RoC - Dev Server"]:
        Ether.Guild = Ether.guilds[0]
        Ether.Load_Players()
        create_task(Ether.Autosave())
        if "Dev" in Ether.Guild.name:
            Ether.Roles = {
                "Titan":Ether.Guild.get_role(1018735284147466240),
                "Analis":Ether.Guild.get_role(1018735450053156894),
            }
        else:
            pass
        print("\nBot is alive.\n")


    # Override of existing on_member_join from discord.py
    # This sends a message to the player
    @Ether.event
    async def on_member_join(NewMember:Member) -> None:
        await Ether.Send_Welcome(NewMember)

    Ether.run(Ether.Get_Token("Cavan"))
