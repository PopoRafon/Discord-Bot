from discord import VoiceChannel, VoiceClient
from discord.ext import commands
from .songs_queue import SongsQueue


class Voice(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.queue: SongsQueue = SongsQueue()

    @commands.command()
    async def join(self, ctx: commands.Context):
        """
        Joins to your channel
        """
        if ctx.author.voice is None:
            return await ctx.send(f'{ctx.author.mention} You need to be connected to voice channel to use this command!')

        channel: VoiceChannel = ctx.author.voice.channel
        await channel.connect()

    @commands.command()
    async def leave(self, ctx: commands.Context):
        """
        Disconnects from current channel
        """
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()

    @commands.command()
    async def play(
        self,
        ctx: commands.Context,
        url: str = commands.parameter(description='Either direct url or name of the song to be played')
    ):
        """
        Adds song to queue and plays it
        """
        song: str = self.queue.add(url)

        await ctx.send(f'Added `{song}`')

        voice_client: None | VoiceClient = ctx.voice_client

        if voice_client is None:
            channel: VoiceChannel = ctx.author.voice.channel
            voice_client: VoiceClient = await channel.connect()

        if not voice_client.is_paused() and not voice_client.is_playing():
            self.queue.play(voice_client)

    @commands.command()
    async def pause(self, ctx: commands.Context):
        """
        Pauses current song
        """
        voice_client: None | VoiceClient = ctx.voice_client

        if voice_client is None:
            return await ctx.send(f'{ctx.author.mention} Bot needs to be connected to voice channel to pause song!')

        if voice_client.is_paused():
            return await ctx.send(f'{ctx.author.mention} Song is already paused.')

        voice_client.pause()

    @commands.command()
    async def resume(self, ctx: commands.Context):
        """
        Resumes current song
        """
        voice_client: None | VoiceClient = ctx.voice_client

        if voice_client is None:
            return await ctx.send(f'{ctx.author.mention} Bot needs to be connected to voice channel to resume song!')

        if voice_client.is_playing():
            return await ctx.send(f'{ctx.author.mention} Song is already resumed.')

        voice_client.resume()

    @commands.command()
    async def skip(self, ctx: commands.Context):
        """
        Skips current song
        """
        voice_client: None | VoiceClient = ctx.voice_client

        if voice_client is None:
            return await ctx.send(f'{ctx.author.mention} Bot needs to be connected to voice channel to skip song!')

        if not voice_client.is_paused() and not voice_client.is_playing():
            return await ctx.send(f'{ctx.author.mention} No song to skip.')

        voice_client.stop()
        await ctx.send('Current song has been skipped.')

        if len(self.queue.get()) >= 1:
            self.queue.play(voice_client)

    @commands.command()
    async def remove(
        self,
        ctx: commands.Context,
        title: str = commands.parameter(description='Must be exactly the same as the title displayed in $list command')
    ):
        """
        Removes song from queue
        """
        for song in self.queue.get():
            if song['title'] == title:
                self.queue.remove(song)
                return await ctx.send(f'Removed `{title}` from queue.')

        await ctx.send(f'Song `{title}` not found in queue.')

    @commands.command()
    async def clear(self, ctx: commands.Context):
        """
        Clears song queue
        """
        voice_client: None | VoiceClient = ctx.voice_client

        if voice_client is None:
            return await ctx.send(f'{ctx.author.mention} Bot needs to be connected to voice channel to clear queue!')

        voice_client.stop()
        self.queue.clear()

        await ctx.send('Song queue has been cleared.')

    @commands.command()
    async def list(self, ctx: commands.Context):
        """
        Lists all queued songs
        """
        songs_list: str = ''.join([f'\n- `{song["title"]}`' for song in self.queue.get()])
        await ctx.send(f'Current songs list:' + songs_list)
