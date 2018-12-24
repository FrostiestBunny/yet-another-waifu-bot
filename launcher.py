from bot import bot
import currency
import games
import image_fun
import os

TOKEN = os.getenv('WAIFU_BOT_TOKEN')

bot.run(TOKEN)
