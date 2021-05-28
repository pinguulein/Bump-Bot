import discord

from humanfriendly import format_timespan as ftime
from humanfriendly import round_number
from core import embeds

commands = discord.ext.commands

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(embed=embeds.Embeds(f"Es fehlt `{error.param}` als Argument.").error())
        elif isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.CheckFailure):
            return await ctx.send(embed=embeds.Embeds("Du hast keine Rechte dazu.").error())
        elif isinstance(error, commands.CommandOnCooldown):
            seconds = error.retry_after
            return await ctx.send(embed=embeds.Embeds(f"**Du bist im Cooldown versuche erneut in: **{ftime(seconds)}**.").error())
        else:
            await ctx.send(embed=embeds.Embeds("Ein Error ist aufgetreten.").error(Error=error))
            raise error

def setup(bot):
    bot.add_cog(ErrorHandler(bot))