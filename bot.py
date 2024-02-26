import discord, yt_dlp
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
async def play(ctx: commands.Context, url):
    """
    Adds song to queue
    """
    voice_client: None | discord.VoiceClient = ctx.voice_client

    if voice_client is None:
        channel = ctx.author.voice.channel
        voice_client = await channel.connect()

    ydl_opts = {'format': 'bestaudio/best'}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        await ctx.send(f'Playing {url}')
        voice_client.play(discord.FFmpegPCMAudio(info['url']))

@bot.command()
async def pause(ctx: commands.Context):
    """
    Pauses current song
    """
    voice_client: None | discord.VoiceClient = ctx.voice_client

    if voice_client is None:
        return await ctx.send(f'{ctx.author.mention} Bot needs to be connected to voice channel to pause song!')

    if voice_client.is_paused():
        return await ctx.send(f'{ctx.author.mention} Song is already paused.')

    voice_client.pause()

@bot.command()
async def resume(ctx: commands.Context):
    """
    Resumes current song
    """
    voice_client: None | discord.VoiceClient = ctx.voice_client

    if voice_client is None:
        return await ctx.send(f'{ctx.author.mention} Bot needs to be connected to voice channel to resume song!')

    if voice_client.is_playing():
        return await ctx.send(f'{ctx.author.mention} Song is already resumed.')

    voice_client.resume()

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
    song_queue.clear()
    await ctx.send('Song queue has been cleared.')

@bot.command()
async def list(ctx: commands.Context):
    """
    Lists all queued songs
    """
    await ctx.send(f'Current songs list: {song_queue}')

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
