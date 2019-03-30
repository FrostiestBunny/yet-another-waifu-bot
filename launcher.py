from my_bot import MyBot

import os
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-m", "--maintenance", help="turn on maintenance mode",
                    action="store_true")
parser.add_argument("-n", "--newt", help="Turn on Newt mode", action="store_true")
COMMAND_ARGS = parser.parse_args()

if COMMAND_ARGS.newt:
    prefix = "n!"
else:
    prefix = "?"

bot = MyBot(command_prefix=prefix, description="The cutest damn bot in the world.")
bot.set_cmd_args(COMMAND_ARGS)

TOKEN = os.getenv('WAIFU_BOT_TOKEN')
bot.run(TOKEN)
