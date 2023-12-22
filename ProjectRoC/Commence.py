from discord.ext.commands import Context
from RealmOfConflict import RealmOfConflict
from PlayPanel import PlayPanel

if __name__ == '__main__':
    Ether = RealmOfConflict()


    @Ether.command(aliases=["oc", "oC", "OC"])
    async def Play_Interaction(InitialContext: Context):
        if await Ether.Guild_Guard(InitialContext) == "Unprotected":
            return
        await InitialContext.message.delete()
        if InitialContext.author.id not in Ether.Data["Players"].keys() or Ether.Data["Players"][InitialContext.author.id].Data["Team"] is None:
            await Ether.Send_Welcome(InitialContext, InitialContext.author)
        elif InitialContext.author.id in Ether.Data["Panels"].keys():
            await Ether.Data["Panels"][InitialContext.author.id].DashboardMessage.delete()
            Ether.Data["Panels"].update({InitialContext.author.id:PlayPanel(Ether, InitialContext)})
        else:
            Ether.Data["Panels"].update({InitialContext.author.id:PlayPanel(Ether, InitialContext)})


    @Ether.event
    async def on_ready() -> None:
        Guild = Ether.guilds[0]
        await Ether.Autosave()
        print("\nBot is alive.\n")

    Ether.run(Ether.Get_Token("Cavan"))
