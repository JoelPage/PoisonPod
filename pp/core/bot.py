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
        async def addhost(ctx, *args):
            print("!addhost")
            dID = args[0]
            tName = args[1]
            success = self.m_userManager.AddHost(dID, tName)
            if success:
                await ctx.send(f"Host {dID} was succesfully set.")
            else:
                await ctx.send(f"Host {dID} was not set, for some reason.")

        @self.m_dBot.command()
        @dUtils.commands.has_any_role(*roles)
        async def removehost(ctx, *args):
            print("!removehost")
            dID = args[0]
            success = self.m_userManager.RemoveHostByDiscordID(dID)
            if success:
                await ctx.send(f"Host {dID} succesfully removed.")
            else:
                await ctx.send(f"Host {dID} was not removed, for some reason.")

        @self.m_dBot.command()
        @dUtils.commands.has_any_role(*roles)
        async def adduser(ctx, *args):
            print("!adduser")
            try:
                dID = args[0]
                tName = args[1]
                success = self.m_userManager.AddUser(dID, tName)
                if success:
                    await ctx.send(f"User {dID} was succesfully added.")
                else:
                    await ctx.send(f"User {dID} was not added, for some reason.")
            except:
                await ctx.send(f"You dun goofed.")

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
        async def hosts(ctx, *args):
            print("!hosts")
            hostsStr = ""
            for host in self.m_userManager.GetHosts():
                isLiveStr = "Offline"
                if host.m_isLive:
                    isLiveStr = "Online"
                hostsStr += f"{host.m_dID} ({host.m_tName}) is {isLiveStr}\n"
            dEmbed = dUtils.CreateEmbed("Registered Users", hostsStr)
            await ctx.send(embed=dEmbed)

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

            channel = self.m_dBot.get_channel(channelID)
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
            userChannelID = self.m_settings.GetChannelID()
            hosts = self.m_userManager.GetHosts()
            users = self.m_userManager.GetUsers()

            for host in hosts:
                await self.PostGoLiveEmbed_Async(host, hostChannelID, True)

            for user in users:
                await self.PostGoLiveEmbed_Async(user, userChannelID, False)

            self.SaveUserData()

            await pUtils.sleep_async(interval)
        
    async def PostMessage_Async(self, channelID, message):
        channel = self.m_dBot.get_channel(channelID)
        if channel:
            await channel.send(message)
        else:
            print(f"Failed to send message, channel with ID {channelID} could not be found.")

    async def PostEmbed_Async(self, channelID, embed, message):
        channel = self.m_dBot.get_channel(channelID)
        if channel:
            await channel.send(message, embed=embed)
        else:
            print(f"Failed to send embed, channel with ID {channelID} could not be found.")

    async def PostGoLiveEmbed_Async(self, user, channelID, shouldTag):
        print("PostGoLiveEmbed_Async")
        dID = user.m_dID
        name = user.m_tName
        wasLive = user.m_isLive
        isLive = False

        print(f"name : {name}")
        data = tUtils.getUserData(name)
        game = "placeholdergame"
        status = "placeholderstatus"
        logo = "placeholderlogo"
        description = "placeholderdesc"

        if data is None:
            print("data is none")
            return

        if not 'stream' in data:
            print("not stream in data")
            return

        streamData = data['stream']

        if streamData is None:
            print("streamData is none")
            return

        isLive = True
        if not wasLive:
            print("wasNotLive")
            if user.ShouldNotify():
                print("should notify")
                game = streamData['game'] #could crash if no exist.
                channelData = streamData['channel'] #could crash if no exist.
                status = channelData['status'] #could crash if no exist.
                logo = channelData['logo'] #could crash if no exist.
                description = channelData['description'] #could crash if no exist.

                tUrl = f"https://www.twitch.tv/{name}"
                # Get title of stream
                dEmbed = dUtils.CreateEmbed(status, description)
                dEmbed.url = tUrl
                dEmbed.set_thumbnail(url=logo)
                dEmbed.set_image(url=f"https://static-cdn.jtvnw.net/previews-ttv/live_user_{name}-1920x1080.jpg?width=1606&height=904")
                dEmbed.timestamp = pUtils.utcnow()
                dEmbed.set_footer(text="ppbot")
                dEmbed.set_author(name=f"{name}", icon_url=logo)

                message = f"{dID} went live! Check them out at {tUrl}"

                if shouldTag:
                    message = f"Hey @everyone {message}"

                await self.PostEmbed_Async(channelID, embed=dEmbed, message=message)

        user.SetIsLive(isLive)