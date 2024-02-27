import discord
from discord.ext import commands
from .chat_commands import Chat
from .voice_commands import Voice

intents: discord.Intents = discord.Intents.default()
intents.message_content = True
bot: commands.Bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    await bot.add_cog(Chat(bot))
    await bot.add_cog(Voice(bot))
    print('Bot is ready to use!')
