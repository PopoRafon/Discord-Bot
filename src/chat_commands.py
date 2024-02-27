from .bot import *

@bot.command()
async def prefix(ctx: commands.Context, prefix):
    """
    Changes used prefix
    """
    if len(prefix) > 2:
        return await ctx.send(f'{ctx.author.mention} Prefix cannot be longer than 2 characters!')

    bot.command_prefix = prefix
    await ctx.send(f'{ctx.author.mention} Prefix has been changed to `{prefix}`.')

@bot.command()
async def purge(ctx: commands.Context, count: str):
    """
    Deletes messages from chat
    """
    if not count.isnumeric():
        return await ctx.send(f'{ctx.author.mention} You need to provide valid number.')

    count = int(count)

    if count < 1 or count > 100:
        return await ctx.send(f'{ctx.author.mention} You need to provide number between 1 and 100.')

    await ctx.channel.purge(limit=count)
