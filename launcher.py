from my_bot import MyBot

import os


bot = MyBot(command_prefix='n!', description="The cutest damn bot in the world.")

TOKEN = os.getenv('WAIFU_BOT_TOKEN')
bot.run(TOKEN)
