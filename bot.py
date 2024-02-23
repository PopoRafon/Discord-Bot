import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

song_queue = []

@bot.event
async def on_ready():
    print('Bot is ready to use!')

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
async def join(ctx: commands.Context):
    """
    Joins to your channel
    """
    if ctx.author.voice is None:
        return await ctx.send(f'{ctx.author.mention} You need to be connected to voice channel to use this command!')

    channel = ctx.author.voice.channel
    await channel.connect()

@bot.command()
async def leave(ctx: commands.Context):
    """
    Disconnects from current channel
    """
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()

@bot.command()
async def play(ctx: commands.Context, song):
    """
    Adds song to queue
    """
    await ctx.send('Song has been added to queue.')

@bot.command()
async def pause(ctx: commands.Context):
    """
    Pauses current song
    """
    await ctx.send('Current song has been paused.')

@bot.command()
async def resume(ctx: commands.Context):
    """
    Resumes current song
    """
    await ctx.send('Current song has been resumed.')

@bot.command()
async def next(ctx: commands.Context):
    """
    Skips current song
    """
    await ctx.send('Current song has been skipped.')

@bot.command()
async def clear(ctx: commands.Context):
    """
    Clears song queue
    """
    await ctx.send('Song queue has been cleared.')

@bot.command()
async def list(ctx: commands.Context):
    """
    Lists all queued songs
    """
    await ctx.send(f'Current songs list: {song_queue}')
