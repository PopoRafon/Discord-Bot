from discord.ext import commands


class Chat(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.command()
    async def prefix(
        self,
        ctx: commands.Context,
        prefix: str = commands.parameter(description='Prefix you want to use (cannot be longer than 2 characters)')
    ):
        """
        Changes used prefix
        """
        if len(prefix) > 2:
            return await ctx.send(f'{ctx.author.mention} Prefix cannot be longer than 2 characters!')

        self.bot.command_prefix = prefix
        await ctx.send(f'{ctx.author.mention} Prefix has been changed to `{prefix}`.')

    @commands.command()
    async def purge(
        self,
        ctx: commands.Context,
        count: int = commands.parameter(description='Must be valid number between 1 and 100')
    ):
        """
        Deletes messages from chat
        """
        if count < 1 or count > 100:
            return await ctx.send(f'{ctx.author.mention} You need to provide number between 1 and 100.')

        await ctx.channel.purge(limit=count)
