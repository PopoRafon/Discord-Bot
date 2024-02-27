from .songs_queue import SongsQueue
from .bot import *

queue = SongsQueue()

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
async def play(ctx: commands.Context, url: str):
    """
    Adds song to queue and plays it
    """
    song = queue.add(url)

    await ctx.send(f'Added `{song}`')

    voice_client: None | discord.VoiceClient = ctx.voice_client

    if voice_client is None:
        channel = ctx.author.voice.channel
        voice_client = await channel.connect()

    if not voice_client.is_paused() and not voice_client.is_playing():
        queue.play(voice_client)

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
async def skip(ctx: commands.Context):
    """
    Skips current song
    """
    voice_client: None | discord.VoiceClient = ctx.voice_client

    if voice_client is None:
        return await ctx.send(f'{ctx.author.mention} Bot needs to be connected to voice channel to skip song!')

    if not voice_client.is_paused() and not voice_client.is_playing():
        return await ctx.send(f'{ctx.author.mention} No song to skip.')

    voice_client.stop()
    await ctx.send('Current song has been skipped.')

    if len(queue.get()) >= 1:
        queue.play(voice_client)

@bot.command()
async def remove(ctx: commands.Context, title: str):
    """
    Removes song from queue
    """
    for song in queue.get():
        if song['title'] == title:
            queue.remove(song)
            return await ctx.send(f'Removed `{title}` from queue.')

    await ctx.send(f'Song `{title}` not found in queue.')

@bot.command()
async def clear(ctx: commands.Context):
    """
    Clears song queue
    """
    voice_client: None | discord.VoiceClient = ctx.voice_client

    if voice_client is None:
        return await ctx.send(f'{ctx.author.mention} Bot needs to be connected to voice channel to clear queue!')

    voice_client.stop()
    queue.clear()

    await ctx.send('Song queue has been cleared.')

@bot.command()
async def list(ctx: commands.Context):
    """
    Lists all queued songs
    """
    songs_list: str = ''.join([f'\n- `{song["title"]}`' for song in queue.get()])
    await ctx.send(f'Current songs list:' + songs_list)
