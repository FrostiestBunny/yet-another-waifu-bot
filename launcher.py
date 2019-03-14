from my_bot import MyBot

import os


bot = MyBot(command_prefix='?', description="Best bot.")

TOKEN = os.getenv('WAIFU_BOT_TOKEN')
bot.run(TOKEN)
