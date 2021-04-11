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
        roles = ['Moderators']

        @self.m_dBot.command()
        @dUtils.commands.has_any_role(*roles)
        async def version(ctx, *args):
            print("!version")
            await ctx.send("Poison Pod Bot v0.0.2\nhttps://github.com/JoelPage/PoisonPod")

        @self.m_dBot.command()
        @dUtils.commands.has_any_role(*roles)
        async def sethost(ctx, *args):
            print("!sethost")
            dID = args[0]
            tName = args[1]
            success = self.m_userManager.SetHost(dID, tName)
            if success:
                await ctx.send(f"Host {dID} was succesfully set.")
            else:
                await ctx.send(f"Host {dID} was not set, for some reason.")

        @self.m_dBot.command()
        @dUtils.commands.has_any_role(*roles)
        async def adduser(ctx, *args):
            print("!adduser")
            dID = args[0]
            tName = args[1]
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
        async def hostchannel(ctx, *args):
            print("!hostchannel")
            await ctx.send(f"The host output channel is set to <#{self.m_settings.GetHostChannelID()}>")

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
            if channel:
                self.m_settings.m_dChannelID = channelID
                self.m_settings.Save()
                await ctx.send(f"Channel set to <#{channelID}>")
            else:
                await ctx.send(f"Channel could not be found.")

        @self.m_dBot.command()
        @dUtils.commands.has_any_role(*roles)
        async def sethostchannel(ctx, *args):
            print("!sethostchannel")

            channelID = args[0]

            try:
                channelID = dUtils.parse_channel(channelID)
            except:
                await ctx.send("Failed to parse channel.")
                return

            channel = self.m_dBot.get_host_channel(channelID)
            if channel:
                self.m_settings.m_dHostChannelID = channelID
                self.m_settings.Save()
                await ctx.send(f"Host channel set to <#{channelID}>")
            else:
                await ctx.send(f"Channel could not be found.")

    def Run(self):
        print("Retrieving token!")
        token = pUtils.getEnvVar("DISCORD_TOKEN")
        print("Connecting bot to discord...")
        self.m_dBot.run(token)
        print("Finished running bot!")

    def SaveUserData(self):
        self.m_userManager.Save()

    async def Start_Async(self):
        interval = 30
        await self.m_dBot.wait_until_ready()
        while True:
            hostChannelID = self.m_settings.GetHostChannelID()
            channelID = self.m_settings.GetChannelID()
            host = self.m_userManager.GetHost()
            users = self.m_userManager.GetUsers()

            # looks like isDirty flag is vestigial 
            isDirty = False

            dHostID = host.m_dID
            tHostName = host.m_tName
            hostWasLive = host.m_isLive
            hostIsLive = tUtils.checkUser(tHostName)

            if hostIsLive:
                if not hostWasLive:
                    isDirty = True
                    if host.ShouldNotify():
                        await self.PostMessage_Async(hostChannelID, f"{dHostID} went live! Check them out on https://www.twitch.tv/{tHostName}")
            else:
                if hostWasLive:
                    isDirty = True

            for user in users:
                dID = user.m_dID
                tName = user.m_tName
                wasLive = user.m_isLive
                isLive = tUtils.checkUser(tName)

                if isLive:
                    if not wasLive:
                        isDirty = True
                        if user.ShouldNotify():
                            await self.PostMessage_Async(channelID, f"{dID} went live! Check them out on https://www.twitch.tv/{tName}")
                else:
                    if wasLive:
                        isDirty = True

                user.SetIsLive(isLive)

            self.SaveUserData()

            await pUtils.sleep_async(interval)
        
    async def PostMessage_Async(self, channelID, message):
        channel = self.m_dBot.get_channel(channelID)
        if channel:
            await channel.send(message)
        else:
            print(f"Failed to send message, channel with ID {channelID} could not be found.")
