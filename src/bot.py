import discord
from discord.ext import commands
from .chat_commands import Chat
from .voice_commands import Voice
import os

intents: discord.Intents = discord.Intents.default()
intents.message_content = True
bot: commands.Bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    BLUE: str = '\033[94m'
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'{BLUE}Connected to the server as {bot.user}!')

@bot.event
async def setup_hook():
    bot.dispatch('voice_client_pause')
    await bot.add_cog(Chat(bot))
    await bot.add_cog(Voice(bot))
