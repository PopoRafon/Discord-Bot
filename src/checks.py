from discord.ext import commands

async def _predicate_voice_connection(ctx: commands.Context):
    if ctx.voice_client is None:
        await ctx.send(f'{ctx.author.mention} Bot needs to be connected to voice channel.')
        return False

    return True

is_connected_to_voice = commands.check(_predicate_voice_connection)
