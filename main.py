import os
from dotenv import load_dotenv
from bot import bot

load_dotenv()

TOKEN: str = os.getenv('AUTH_TOKEN')

if __name__ == '__main__':
    bot.run(TOKEN)
