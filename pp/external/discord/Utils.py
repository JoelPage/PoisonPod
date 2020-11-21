import discord
from discord.ext import commands as commands

def CreateBot(prefix):
    print("Creating bot")
    return commands.Bot(command_prefix=prefix)

def CreateEmbed(title, description):
    print("Creating Embed")
    return discord.Embed(title=title, description=description)

def parse_channel(string):
    try:
        if string.startswith('<#') and string.endswith('>'):
            print(string[2:len(string)-1])
            return int(string[2:len(string)-1])
        else:
            raise ValueError
    except ValueError: raise i_argparse.ArgumentTypeError(f"Failed to parse channel")  