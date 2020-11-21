import pp.core.bot as ppBot

import pp.external.python.Utils as pUtils

def main():

    pUtils.MakeDir("data")

    bot = ppBot.Bot()
    bot.Run()

main()