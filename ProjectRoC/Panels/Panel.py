from discord import Interaction as DiscordInteraction

class Panel:
    async def _Send_New_Panel(Self, Interaction:DiscordInteraction):
        await Interaction.response.edit_message(embed=Self.EmbedFrame, view=Self.BaseViewFrame)

    async def _Generate_Info(Self, Ether, InitialContext, Exclusions:list=[], Inclusions:list=[]):
        Self.EmbedFrame.description = ""
        Fields = [Field for Field in ["Wallet", "Team", "Level", "Experience", "Power"] if Field not in Exclusions]
        Fields += Inclusions
        Info = ""

        if Ether.Data["Players"][InitialContext.author.id].Data["Skill Points"] > 0:
            Info +=f"**You have {format(int(Ether.Data['Players'][InitialContext.author.id].Data['Skill Points']), ',')} unspent skill point**\n"

        for Name, Value in Self.Player.Data.items():
            if Name in Fields:
                if Name == 'Wallet':
                    Info +=f"> **{Name}** ~ ${format(float(Value), ',')}\n"
                elif Name == 'Experience':
                    Info +=f"> **{Name}** ~ {format(float(Value), ',')} / {format(float(Ether.Data['Players'][InitialContext.author.id].ExperienceForNextLevel), ',')}\n"
                elif type(Value) == float:
                    Info +=f"> **{Name}** ~ {format(float(Value), ',')}\n"
                elif type(Value) == int:
                    Info +=f"> **{Name}** ~ {format(int(Value), ',')}\n"
                else:
                    Info +=f"> **{Name}** ~ {Value}\n"

        for Name, Value in Self.Player.Skills.items():
            if Name in Fields:
                Info += f"> **{Name}** ~ {format(int(Value), ',')}\n"

        Info += "\n\n"

        Self.EmbedFrame.description += Info