from discord import VoiceChannel, VoiceClient, Member, VoiceState
from discord.ext import commands
from .songs_queue import SongsQueue
from .checks import is_connected_to_voice
import asyncio, random


class Voice(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.queue: SongsQueue = SongsQueue()
        self.voice_client: VoiceClient | None = None
        self.timeout: int = 60
        self.timeout_task: asyncio.Task | None = None

    async def timeout_voice_channel(self):
        await asyncio.sleep(self.timeout)
        await self.voice_client.disconnect()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):
        if self.voice_client:
            channel_members_count = len(self.voice_client.channel.members)

            if not self.timeout_task and channel_members_count == 1:
                self.timeout_task = self.bot.loop.create_task(self.timeout_voice_channel())
            elif self.timeout_task and channel_members_count > 1:
                self.timeout_task.cancel()
                self.timeout_task = None

    @commands.command()
    async def join(self, ctx: commands.Context):
        """
        Joins to your channel
        """
        if ctx.author.voice is None:
            return await ctx.send(f'{ctx.author.mention} You need to be connected to voice channel to use this command!')

        channel: VoiceChannel = ctx.author.voice.channel
        await channel.connect()
        self.voice_client = ctx.voice_client

    @commands.command()
    @is_connected_to_voice
    async def leave(self, ctx: commands.Context):
        """
        Disconnects from current channel
        """
        if self.voice_client is not None:
            await self.voice_client.disconnect()
            self.voice_client = None
            self.queue.clear()

    @commands.command()
    @is_connected_to_voice
    async def play(
        self,
        ctx: commands.Context,
        url: str = commands.parameter(description='Either direct url or name of the song to be played')
    ):
        """
        Adds song to queue and plays it
        """
        song: str | None = self.queue.add(url)

        if not song:
            return await ctx.send('Song couldn\'t be added.')

        await ctx.send(f'Added `{song}`.')

        if not self.voice_client.is_paused() and not self.voice_client.is_playing():
            self.queue.play(self.voice_client)

    @commands.command()
    @is_connected_to_voice
    async def pause(self, ctx: commands.Context):
        """
        Pauses current song
        """
        if self.voice_client.is_paused():
            return await ctx.send(f'{ctx.author.mention} Song is already paused.')

        self.voice_client.pause()

    @commands.command()
    @is_connected_to_voice
    async def resume(self, ctx: commands.Context):
        """
        Resumes current song
        """
        if self.voice_client.is_playing():
            return await ctx.send(f'{ctx.author.mention} Song is already resumed.')

        self.voice_client.resume()

    @commands.command()
    @is_connected_to_voice
    async def skip(self, ctx: commands.Context):
        """
        Skips current song
        """
        if not self.voice_client.is_paused() and not self.voice_client.is_playing():
            return await ctx.send(f'{ctx.author.mention} No song to skip.')

        self.voice_client.stop()

        await ctx.send('Current song has been skipped.')

    @commands.command()
    @is_connected_to_voice
    async def remove(
        self,
        ctx: commands.Context,
        title: str = commands.parameter(description='Must be exactly the same as the title displayed in $list command')
    ):
        """
        Removes song from queue
        """
        if not self.queue.remove(title):
            return await ctx.send(f'Song `{title}` not found in queue.')

        await ctx.send(f'Removed `{title}` from queue.')

    @commands.command()
    @is_connected_to_voice
    async def clear(self, ctx: commands.Context):
        """
        Clears song queue
        """
        self.voice_client.stop()
        self.queue.clear()

        await ctx.send('Song queue has been cleared.')

    @commands.command()
    @is_connected_to_voice
    async def insert(
        self,
        ctx: commands.Context,
        url: str = commands.parameter(description='Either direct url or name of the song to be played'),
        index: int = commands.parameter(description='Index before which song to insert this song')
    ):
        """
        Inserts song to queue at specified index
        """
        if index < 0 or index >= len(self.queue.get_queue()):
            return await ctx.send(f'{ctx.author.mention} Index is out of queue boundaries.')

        song: str | None = self.queue.insert(url, index)

        if not song:
            return await ctx.send('Song couldn\'t be inserted.')

        await ctx.send(f'Inserted `{song}` at position {index}.')

    @commands.command()
    @is_connected_to_voice
    async def move(
        self,
        ctx: commands.Context,
        from_index: int = commands.parameter(description='Index from which to move song'),
        to_index: int = commands.parameter(description='Index to which move song')
    ):
        """
        Move song from one position in queue to another
        """
        queue_length: int = len(self.queue.get_queue())

        if from_index < 0 or to_index < 0 or from_index >= queue_length or to_index >= queue_length:
            return await ctx.send(f'{ctx.author.mention} Positions are out of queue boundaries.')

        self.queue.move(from_index, to_index)

        await ctx.send(f'Moved song from position {from_index} to {to_index} position.')

    @commands.command()
    @is_connected_to_voice
    async def shuffle(self, ctx: commands.Context):
        """
        Shuffles randomly all songs from queue
        """
        random.shuffle(self.queue.get_queue())

        await ctx.send('Songs queue has been shuffled.')

    @commands.command()
    @is_connected_to_voice
    async def current(self, ctx: commands.Context):
        """
        Displays current song
        """
        current_song: dict[str, str] = self.queue.get_current_song()

        if not current_song:
            return await ctx.send(f'No song is currently playing.')

        await ctx.send(f'Currently playing `{current_song["title"]}`.')

    @commands.command()
    @is_connected_to_voice
    async def repeat(self, ctx: commands.Context):
        """
        Repeats current song in loop
        """
        is_repeat_enabled = self.queue.is_repeat_enabled()

        self.queue.set_repeat(not is_repeat_enabled)

        await ctx.send(f'Repeat has been `{"enabled" if not is_repeat_enabled else "disabled"}`.')

    @commands.command()
    @is_connected_to_voice
    async def list(self, ctx: commands.Context):
        """
        Lists all queued songs
        """
        songs_list: str = ''.join([f'\n- `{song["title"]}`' for song in self.queue.get_queue()])

        await ctx.send(f'Current songs list:' + songs_list)
