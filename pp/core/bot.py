import pp.external.twitch.Utils as tUtils
import pp.external.discord.Utils as dUtils
import pp.external.python.Utils as pUtils

import pp.core.user_manager as ppUserManager
import pp.core.user as ppUser
import pp.core.settings as ppSettings

class Bot():
    def __init__(self):
        self.m_dBot = dUtils.CreateBot("!")
        self.m_userManager = ppUserManager.UserManager()
        self.m_settings = ppSettings.Settings()
        self.InitialiseCallbacks()
        self.InitialiseCommands()
        

    def InitialiseCallbacks(self):

        @self.m_dBot.event
        async def on_ready():
            print(f'{self.m_dBot.user.name} has connected to Discord!')
            self.m_dBot.loop.create_task(self.Start_Async())

    def InitialiseCommands(self):

        # Permission Roles
        roles = ['Moderator']

        @self.m_dBot.command()
        @dUtils.commands.has_any_role(*roles)
        async def version(ctx, *args):
            print("!version")
            await ctx.send("Poison Pod Bot v0.0.1")

        @self.m_dBot.command()
        @dUtils.commands.has_any_role(*roles)
        async def adduser(ctx, *args):
            print("!adduser")
            dID = args[0]
            tName = args[1]
            print(dID)
            print(tName)
            success = self.m_userManager.AddUser(dID, tName)
            if success:
                await ctx.send(f"User {dID} was succesfully added.")
            else:
                await ctx.send(f"User {dID} was not added, for some reason.")

        @self.m_dBot.command()
        @dUtils.commands.has_any_role(*roles)
        async def removeuser(ctx, *args):
            print("!removeuser")
            dID = args[0]
            success = self.m_userManager.RemoveUserByDiscordID(dID)
            if success:
                await ctx.send(f"User {dID} succesfully removed.")
            else:
                await ctx.send(f"User {dID} was not removed, for some reason.")

        @self.m_dBot.command()
        @dUtils.commands.has_any_role(*roles)
        async def users(ctx, *args):
            print("!users")
            usersStr = ""
            for user in self.m_userManager.GetUsers():
                isLiveStr = "Offline"
                if user.m_isLive:
                    isLiveStr = "Online"
                usersStr += f"{user.m_dID} ({user.m_tName}) is {isLiveStr}\n"
            dEmbed = dUtils.CreateEmbed("Registered Users", usersStr)
            await ctx.send(embed=dEmbed)

        @self.m_dBot.command()
        @dUtils.commands.has_any_role(*roles)
        async def channel(ctx, *args):
            print("!channel")
            await ctx.send(f"The output channel is set to <#{self.m_settings.GetChannelID()}>")

        @self.m_dBot.command()
        @dUtils.commands.has_any_role(*roles)
        async def setchannel(ctx, *args):
            print("!setchannel")

            channelID = args[0]

            try:
                channelID = dUtils.parse_channel(channelID)
            except:
                await ctx.send("Failed to parse channel.")
                return

            channel = self.m_dBot.get_channel(channelID)
            self.m_settings.m_dChannelID = channelID
            await ctx.send(f"Channel set to <#{channelID}>")

    def Run(self):
        print("Retrieving token!")
        token = pUtils.getEnvVar("DISCORD_TOKEN")
        print("Connecting bot to discord...")
        self.m_dBot.run(token)
        print("Finished running bot!")

    def SaveUserData(self):
        self.m_userManager.Save()

    async def Start_Async(self):
        channelId = self.m_settings.GetChannelID()
        interval = 60
        await self.m_dBot.wait_until_ready()
        while True:
            users = self.m_userManager.GetUsers()
            isDirty = False
            for user in users:
                dID = user.m_dID
                tName = user.m_tName
                wasLive = user.m_isLive
                isLive = tUtils.checkUser(tName)

                if isLive:
                    if not wasLive:
                        isDirty = True
                        if user.ShouldNotify():
                            await self.PostMessage_Async(channelId, f"{dID} went live! Check them out on https://www.twitch.tv/{tName}")
                else:
                    if wasLive:
                        isDirty = True

                user.SetIsLive(isLive)

            self.SaveUserData()

            await pUtils.sleep_async(interval)
        
    async def PostMessage_Async(self, channelID, message):
        channel = self.GetChannel(channelID)
        await channel.send(message)

    def GetChannel(self, channelID):
        return self.m_dBot.get_channel(channelID)